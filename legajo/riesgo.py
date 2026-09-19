"""Evaluador de riesgo con enfoque basado en riesgo.

No contiene ningun umbral ni ninguna lista: todo viene de matriz.py. Este
archivo solo decide que factores aplican y los suma.

Dos reglas gobiernan el diseno:

1. Todo punto asignado queda desglosado. Un nivel de riesgo que no se puede
   explicar factor por factor no sirve: hay que poder justificar por que un
   cliente quedo en reforzada.

2. Los elevadores fijan un piso, no suman puntos. Sin ese mecanismo, "pero si
   es PEP entonces siempre alto" termina como un if disperso en cinco lugares
   distintos del codigo. Con el, es una linea de configuracion.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from .beneficiario import Resolucion
from .matriz import (
    MATRIZ_POR_DEFECTO, MESES_HASTA_REVISION, NIVELES, REGIMEN, Factor, MatrizRiesgo,
)
from .modelo import Caso, Cliente, Estado
from .pep import PEP, RegistroPEP
from .screening import Coincidencia


@dataclass
class Evaluacion:
    """Resultado del scoring de un cliente."""

    cliente_id: str
    puntaje: float = 0.0
    nivel: str = "BAJO"
    regimen: str = "DD_SIMPLIFICADA"
    factores: list[Factor] = field(default_factory=list)
    elevadores: list[str] = field(default_factory=list)

    @property
    def desglose(self) -> str:
        return " | ".join(f"{f.codigo}+{f.puntos:g}" for f in self.factores)

    @property
    def meses_hasta_revision(self) -> int:
        return MESES_HASTA_REVISION[self.nivel]

    def proxima_revision(self, desde: date | None = None) -> date:
        """Fecha tope para volver a mirar el legajo.

        La periodicidad sale del nivel de riesgo, no de una agenda aparte.
        Calcularla aca evita que el plazo y el nivel se desincronicen.
        """
        base = desde or date.today()
        meses = self.meses_hasta_revision
        anio = base.year + (base.month - 1 + meses) // 12
        mes = (base.month - 1 + meses) % 12 + 1
        dia = min(base.day, 28)
        return date(anio, mes, dia)


def _nivel_por_puntaje(puntaje: float, matriz: MatrizRiesgo) -> str:
    if puntaje >= matriz.umbral_alto:
        return "ALTO"
    if puntaje >= matriz.umbral_medio:
        return "MEDIO"
    return "BAJO"


def _normalizar(valor: str | None) -> str:
    return (valor or "").strip().upper()


def _factores_cliente(
    cliente: Cliente, resolucion: Resolucion | None, matriz: MatrizRiesgo
) -> tuple[list[Factor], list[str]]:
    factores: list[Factor] = []
    elevadores: list[str] = []

    if cliente.tipo != "PERSONA":
        factores.append(Factor(
            "PERSONA_JURIDICA", "CLIENTE",
            "cliente es persona juridica o estructura",
            matriz.puntos_persona_juridica,
        ))

    if resolucion is None:
        return factores, elevadores

    if not resolucion.identificado:
        factores.append(Factor(
            "BENEFICIARIO_NO_IDENTIFICADO", "CLIENTE",
            "no se identifico beneficiario final",
            matriz.puntos_beneficiario_no_identificado,
        ))
        elevadores.append("BENEFICIARIO_NO_IDENTIFICADO")

    if any(b.via == "SUPLETORIO" for b in resolucion.beneficiarios):
        factores.append(Factor(
            "BENEFICIARIO_SUPLETORIO", "CLIENTE",
            "beneficiario final determinado por via supletoria (administrador)",
            matriz.puntos_beneficiario_no_identificado * 0.6,
        ))

    capas = max(resolucion.profundidad_maxima - 1, 0)
    if capas > 0:
        factores.append(Factor(
            "ESTRUCTURA_MULTICAPA", "CLIENTE",
            f"cadena de titularidad de {capas + 1} nivel(es)",
            matriz.puntos_estructura_multicapa * capas,
        ))

    if resolucion.titularidad_opaca > 1e-9:
        factores.append(Factor(
            "TITULARIDAD_OPACA", "CLIENTE",
            f"titularidad no identificada: {resolucion.titularidad_opaca:.1%}",
            round(matriz.puntos_titularidad_opaca * resolucion.titularidad_opaca, 1),
        ))

    if resolucion.ciclos:
        factores.append(Factor(
            "PARTICIPACION_CIRCULAR", "CLIENTE",
            f"{len(resolucion.ciclos)} participacion(es) circular(es)",
            matriz.puntos_participacion_circular,
        ))

    return factores, elevadores


def _factores_geograficos(cliente: Cliente, matriz: MatrizRiesgo) -> tuple[list[Factor], list[str]]:
    factores: list[Factor] = []
    elevadores: list[str] = []

    paises = {_normalizar(cliente.pais_residencia), _normalizar(cliente.nacionalidad)}
    paises.discard("")

    alto = paises & matriz.jurisdicciones_alto_riesgo
    if alto:
        factores.append(Factor(
            "JURISDICCION_ALTO_RIESGO", "GEOGRAFICO",
            f"vinculacion con jurisdiccion de alto riesgo: {', '.join(sorted(alto))}",
            matriz.puntos_jurisdiccion_alto_riesgo,
        ))
        elevadores.append("JURISDICCION_ALTO_RIESGO")

    monitoreo = paises & matriz.jurisdicciones_monitoreo
    if monitoreo:
        factores.append(Factor(
            "JURISDICCION_MONITOREO", "GEOGRAFICO",
            f"jurisdiccion bajo monitoreo intensificado: {', '.join(sorted(monitoreo))}",
            matriz.puntos_jurisdiccion_monitoreo,
        ))

    nac = _normalizar(cliente.nacionalidad)
    res = _normalizar(cliente.pais_residencia)
    if nac and res and nac != res:
        factores.append(Factor(
            "RESIDENCIA_DISTINTA", "GEOGRAFICO",
            f"reside en {res} con nacionalidad {nac}",
            matriz.puntos_residencia_distinta_nacionalidad,
        ))

    return factores, elevadores


def _factores_actividad(cliente: Cliente, matriz: MatrizRiesgo) -> list[Factor]:
    actividad = _normalizar(cliente.actividad)

    if not actividad:
        return [Factor(
            "ACTIVIDAD_NO_DECLARADA", "ACTIVIDAD",
            "el cliente no declaro actividad",
            matriz.puntos_actividad_no_declarada,
        )]

    coincidentes = [s for s in matriz.actividades_sensibles if s in actividad]
    if coincidentes:
        return [Factor(
            "ACTIVIDAD_SENSIBLE", "ACTIVIDAD",
            f"actividad de exposicion elevada: {actividad}",
            matriz.puntos_actividad_sensible,
        )]

    return []


def _factores_control(
    coincidencias: list[Coincidencia], umbral_probable: float, matriz: MatrizRiesgo
) -> tuple[list[Factor], list[str]]:
    if not coincidencias:
        return [], []

    probables = [c for c in coincidencias if c.score >= umbral_probable]
    if probables:
        peor = max(probables, key=lambda c: c.score)
        return (
            [Factor(
                "COINCIDENCIA_PROBABLE", "CONTROL",
                f"coincidencia probable en {peor.lista} ({peor.score}) con {peor.nombre_designado}",
                matriz.puntos_coincidencia_probable,
            )],
            ["COINCIDENCIA_PROBABLE"],
        )

    peor = max(coincidencias, key=lambda c: c.score)
    return (
        [Factor(
            "COINCIDENCIA_REVISION", "CONTROL",
            f"{len(coincidencias)} coincidencia(s) pendiente(s) de revision (max {peor.score})",
            matriz.puntos_coincidencia_revision,
        )],
        [],
    )


def evaluar(
    cliente: Cliente,
    *,
    resolucion: Resolucion | None = None,
    coincidencias: list[Coincidencia] | None = None,
    pep: PEP | None = None,
    canal_no_presencial: bool = False,
    umbral_probable: float = 92.0,
    matriz: MatrizRiesgo = MATRIZ_POR_DEFECTO,
) -> Evaluacion:
    """Calcula el nivel de riesgo y el regimen de diligencia correspondiente."""
    factores: list[Factor] = []
    elevadores: list[str] = []

    f, e = _factores_cliente(cliente, resolucion, matriz)
    factores += f
    elevadores += e

    if pep is not None:
        codigo = "PEP_EXTRANJERA" if pep.extranjera else "PEP_NACIONAL"
        puntos = (
            matriz.puntos_pep_extranjera if pep.extranjera
            else matriz.puntos_pep_nacional
        )
        if pep.por_parentesco:
            puntos += matriz.puntos_pep_parentesco
        factores.append(Factor(codigo, "CLIENTE", pep.descripcion(), puntos))
        elevadores.append(codigo)

    f, e = _factores_geograficos(cliente, matriz)
    factores += f
    elevadores += e

    factores += _factores_actividad(cliente, matriz)

    if canal_no_presencial:
        factores.append(Factor(
            "CANAL_NO_PRESENCIAL", "CANAL",
            "vinculacion no presencial",
            matriz.puntos_canal_no_presencial,
        ))

    f, e = _factores_control(coincidencias or [], umbral_probable, matriz)
    factores += f
    elevadores += e

    puntaje = round(sum(x.puntos for x in factores), 1)
    nivel = _nivel_por_puntaje(puntaje, matriz)

    # Los elevadores fijan un piso. Nunca bajan el nivel.
    aplicados = [x for x in dict.fromkeys(elevadores) if x in matriz.eleva_a_alto]
    if aplicados and NIVELES.index(nivel) < NIVELES.index("ALTO"):
        nivel = "ALTO"

    return Evaluacion(
        cliente_id=cliente.cliente_id,
        puntaje=puntaje,
        nivel=nivel,
        regimen=REGIMEN[nivel],
        factores=factores,
        elevadores=aplicados,
    )


def evaluar_casos(
    casos: list[Caso],
    resoluciones: dict[str, Resolucion],
    coincidencias_por_cliente: dict[str, list[Coincidencia]],
    *,
    registro_pep: RegistroPEP | None = None,
    umbral_probable: float = 92.0,
    matriz: MatrizRiesgo = MATRIZ_POR_DEFECTO,
    actor: str = "sistema/scoring",
) -> dict[str, Evaluacion]:
    """Evalua un lote de casos y registra todo en cada expediente."""
    registro_pep = registro_pep or RegistroPEP()
    resultados: dict[str, Evaluacion] = {}

    for caso in casos:
        if caso.estado is not Estado.SCORING:
            # Un caso escalado en screening no se scorea: ya esta en otra via.
            continue

        cliente_id = caso.cliente.cliente_id
        resolucion = resoluciones.get(cliente_id)

        if resolucion is not None:
            caso.registrar(
                actor, "BENEFICIARIO_FINAL",
                identificados=[
                    f"{b.nombre} {b.porcentaje_rector:.2%} ({b.via})"
                    for b in resolucion.beneficiarios
                ],
                titularidad_opaca=f"{resolucion.titularidad_opaca:.2%}",
                niveles=resolucion.profundidad_maxima,
                observaciones=resolucion.observaciones,
            )

        evaluacion = evaluar(
            caso.cliente,
            resolucion=resolucion,
            coincidencias=coincidencias_por_cliente.get(cliente_id, []),
            pep=registro_pep.consultar(cliente_id),
            umbral_probable=umbral_probable,
            matriz=matriz,
        )
        resultados[cliente_id] = evaluacion

        caso.registrar(
            actor, "SCORING_EBR",
            puntaje=evaluacion.puntaje,
            nivel=evaluacion.nivel,
            regimen=evaluacion.regimen,
            factores=[f"{f.codigo}(+{f.puntos:g}): {f.descripcion}" for f in evaluacion.factores],
            elevadores=evaluacion.elevadores,
            proxima_revision=evaluacion.proxima_revision().isoformat(),
        )

        if evaluacion.nivel == "ALTO":
            caso.transicionar(
                Estado.ANALISIS, actor,
                f"riesgo alto ({evaluacion.puntaje} pts) requiere diligencia reforzada",
            )
        else:
            caso.transicionar(
                Estado.CERRADO, actor,
                f"riesgo {evaluacion.nivel.lower()} ({evaluacion.puntaje} pts), {evaluacion.regimen}",
            )

    return resultados
