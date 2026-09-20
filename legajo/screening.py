"""Orquestador de screening.

Recorre el padron de designados por cada cliente, aplica el matcher, ajusta
por atenuantes y registra todo en el expediente del caso.

Regla que gobierna este archivo: nada se decide en silencio. Cada ajuste de
puntaje queda escrito en la evidencia con su motivo. Un analista tiene que
poder reconstruir por que una coincidencia quedo en 84 y no en 96.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .config import POLITICA_POR_DEFECTO, Politica
from .fuentes.base import Designado, Padron
from .indice import Indice
from .matcher import mejor_alias
from .modelo import Caso, Cliente, Estado


@dataclass(frozen=True)
class Coincidencia:
    """Una posible correspondencia entre un cliente y un designado."""

    cliente_id: str
    lista: str
    id_origen: str
    nombre_designado: str
    nombre_matcheado: str      # contra que alias especifico coincidio
    score: float
    criterio: str              # DOCUMENTO | NOMBRE
    atenuantes: tuple[str, ...] = ()
    programas: tuple[str, ...] = ()

    @property
    def probable(self) -> bool:
        return self.score >= POLITICA_POR_DEFECTO.umbral_probable


@dataclass
class ResultadoScreening:
    coincidencias: list[Coincidencia] = field(default_factory=list)
    clientes_evaluados: int = 0
    designados_evaluados: int = 0

    @property
    def clientes_con_coincidencia(self) -> int:
        return len({c.cliente_id for c in self.coincidencias})


def _claves_documento(cliente: Cliente) -> set[str]:
    return {d.clave() for d in cliente.documentos}


def _atenuantes(cliente: Cliente, designado: Designado, politica: Politica) -> tuple[float, tuple[str, ...]]:
    """Calcula el descuento por datos secundarios discordantes.

    Solo se penaliza cuando ambos lados tienen el dato y difieren. Un dato
    ausente no penaliza: las listas son notoriamente incompletas en campos
    secundarios y castigar la ausencia generaria falsos negativos.
    """
    descuento = 0.0
    motivos: list[str] = []

    if cliente.fecha_nacimiento and designado.fechas_nacimiento:
        anio_cliente = cliente.fecha_nacimiento[:4]
        anios_lista = {f[-4:] for f in designado.fechas_nacimiento}
        if anio_cliente and anios_lista and anio_cliente not in anios_lista:
            descuento += politica.penalidad_fecha_distinta
            motivos.append(
                f"anio de nacimiento discordante ({anio_cliente} vs {'/'.join(sorted(anios_lista))})"
            )

    if cliente.nacionalidad and designado.nacionalidades:
        nac = cliente.nacionalidad.upper()
        lista_nac = {n.upper() for n in designado.nacionalidades}
        if nac not in lista_nac:
            descuento += politica.penalidad_nacionalidad_distinta
            motivos.append(f"nacionalidad discordante ({nac} vs {'/'.join(sorted(lista_nac))})")

    return descuento, tuple(motivos)


def cotejar_cliente(
    cliente: Cliente,
    padron: Padron,
    politica: Politica = POLITICA_POR_DEFECTO,
    indice: Indice | None = None,
) -> list[Coincidencia]:
    """Coteja un cliente contra el padron.

    Con indice se compara solo contra los candidatos; sin indice, contra todo.
    El resultado tiene que ser el mismo: el indice descarta trabajo, no
    coincidencias. Que sea opcional permite verificar esa equivalencia
    corriendo las dos formas sobre el mismo padron.
    """
    docs_cliente = _claves_documento(cliente)
    es_entidad = cliente.tipo != "PERSONA"
    encontradas: list[Coincidencia] = []

    designados = indice.candidatos(cliente) if indice is not None else padron.designados

    for designado in designados:
        # Coincidencia determinista: un documento identico no se discute.
        # Devuelve el mismo tipo de objeto que la via difusa, asi que aguas
        # abajo no hay que distinguir un caso del otro.
        comunes = docs_cliente & set(designado.documentos)
        if comunes:
            encontradas.append(
                Coincidencia(
                    cliente_id=cliente.cliente_id,
                    lista=designado.lista,
                    id_origen=designado.id_origen,
                    nombre_designado=designado.nombre,
                    nombre_matcheado=sorted(comunes)[0],
                    score=politica.score_documento,
                    criterio="DOCUMENTO",
                    programas=designado.programas,
                )
            )
            continue

        score, alias = mejor_alias(
            cliente.nombre, designado.todos_los_nombres, es_entidad=es_entidad
        )
        if score < politica.umbral_revision:
            continue

        descuento, motivos = _atenuantes(cliente, designado, politica)
        final = round(max(score - descuento, 0.0), 1)
        if final < politica.umbral_revision:
            continue

        encontradas.append(
            Coincidencia(
                cliente_id=cliente.cliente_id,
                lista=designado.lista,
                id_origen=designado.id_origen,
                nombre_designado=designado.nombre,
                nombre_matcheado=alias,
                score=final,
                criterio="NOMBRE",
                atenuantes=motivos,
                programas=designado.programas,
            )
        )

    encontradas.sort(key=lambda c: c.score, reverse=True)
    return encontradas


def screenear(
    casos: list[Caso],
    padron: Padron,
    politica: Politica = POLITICA_POR_DEFECTO,
    actor: str = "sistema/screening",
    usar_indice: bool = True,
) -> ResultadoScreening:
    """Ejecuta el screening sobre un lote de casos y avanza sus estados.

    Cada caso recibe en su expediente la procedencia completa de las listas
    usadas. Sin eso, el registro de screening no es oponible a un supervisor.
    """
    resultado = ResultadoScreening(
        clientes_evaluados=len(casos),
        designados_evaluados=len(padron),
    )

    # El indice se construye una vez para todo el lote. Con un solo cliente
    # no se amortiza, asi que ahi conviene la busqueda directa.
    indice = Indice(padron) if usar_indice and len(casos) > 1 else None

    for caso in casos:
        caso.transicionar(Estado.SCREENING, actor, "inicio de cotejo contra listas")
        caso.registrar(
            actor,
            "SCREENING_EJECUTADO",
            listas=padron.procedencia,
            umbral_revision=politica.umbral_revision,
            umbral_probable=politica.umbral_probable,
            designados_evaluados=len(padron),
        )

        coincidencias = cotejar_cliente(caso.cliente, padron, politica, indice)
        resultado.coincidencias.extend(coincidencias)

        if not coincidencias:
            caso.registrar(actor, "SIN_COINCIDENCIAS")
            caso.transicionar(Estado.SCORING, actor, "sin coincidencias en listas")
            continue

        for c in coincidencias:
            caso.registrar(
                actor,
                "COINCIDENCIA",
                lista=c.lista,
                id_origen=c.id_origen,
                designado=c.nombre_designado,
                matcheo_contra=c.nombre_matcheado,
                score=c.score,
                criterio=c.criterio,
                atenuantes=list(c.atenuantes),
                programas=list(c.programas),
            )

        criticas = [c for c in coincidencias if c.lista in politica.listas_criticas]
        if criticas:
            caso.transicionar(
                Estado.ESCALADO,
                actor,
                f"coincidencia en lista critica ({criticas[0].lista}, score {criticas[0].score})",
            )
        else:
            caso.transicionar(
                Estado.SCORING, actor, f"{len(coincidencias)} coincidencia(s) para revision"
            )

    return resultado
