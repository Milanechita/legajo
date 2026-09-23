"""Corrida del circuito, separada de como se presenta.

Existe por una razon concreta: hay dos salidas del mismo calculo, la planilla
y el visor web, y una segunda copia del encadenado de etapas garantiza que en
la proxima correccion las dos empiecen a dar resultados distintos. Es la
misma regla por la que la interfaz de escritorio llama a `cli.main` en vez de
rearmar los comandos.

Aca no se decide nada nuevo. Se encadenan las cuatro etapas en orden y se
devuelve todo lo que produjeron, sin formato. Quien quiera una planilla, un
JSON o una linea de texto lo arma desde `Corrida`.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .alertas import Alerta, monitorear, reglas_inactivas
from .beneficiario import Resolucion, resolver
from .capacidad import Capacidad, calcular as calcular_capacidad
from .config import POLITICA_POR_DEFECTO, Politica, parametros_con_listas
from .congelamiento import Congelamiento, obligaciones
from .fuentes.base import Padron
from .io_planilla import (
    leer_arca, leer_estructura, leer_operaciones, leer_padron, leer_peps,
    leer_perfiles,
    leer_respaldos,
)
from .matriz import MATRIZ_POR_DEFECTO
from .modelo import Caso, Cliente, Estado
from .operaciones import Operatoria, Perfil, agrupar
from .pep import RegistroPEP
from .riesgo import Evaluacion, evaluar_casos
from .sanciones import Exposicion, estimar
from .screening import Coincidencia, ResultadoScreening, screenear
from .societaria import Estructura


@dataclass
class Corrida:
    """Todo lo que produjo el circuito, sin decidir como se muestra."""

    politica: Politica
    padron: Padron
    clientes: list[Cliente]
    casos: list[Caso]
    screening: ResultadoScreening
    coincidencias: dict[str, list[Coincidencia]]
    estructura: Estructura | None = None
    resoluciones: dict[str, Resolucion] = field(default_factory=dict)
    registro_pep: RegistroPEP | None = None
    evaluaciones: dict[str, Evaluacion] = field(default_factory=dict)
    operatorias: dict[str, Operatoria] = field(default_factory=dict)
    perfiles: dict[str, Perfil] = field(default_factory=dict)
    alertas: dict[str, list[Alerta]] = field(default_factory=dict)
    capacidades: dict[str, Capacidad] = field(default_factory=dict)
    congelamientos: list[Congelamiento] = field(default_factory=list)
    exposicion: Exposicion | None = None
    umbral_reporte: float = 0.0

    @property
    def nombres(self) -> dict[str, str]:
        return {c.cliente.cliente_id: c.cliente.nombre for c in self.casos}

    @property
    def por_cliente(self) -> dict[str, Caso]:
        return {c.cliente.cliente_id: c for c in self.casos}

    def caso(self, cliente_id: str) -> Caso | None:
        return self.por_cliente.get(cliente_id)


def correr(
    padron: Padron,
    clientes: list[Cliente],
    *,
    politica: Politica = POLITICA_POR_DEFECTO,
    societaria: str | Path | None = None,
    peps: str | Path | None = None,
    operaciones: str | Path | None = None,
    perfiles: str | Path | None = None,
    respaldos: str | Path | None = None,
    arca: str | Path | None = None,
    umbral_reporte: float | None = None,
    actor: str = "sistema/legajo",
    avisar: Any = None,
) -> Corrida:
    """Encadena las cuatro etapas y devuelve el resultado completo.

    `avisar` recibe las lineas de progreso. Se pasa como parametro en vez de
    imprimir directo porque el mismo calculo lo consume la planilla, el visor
    y las pruebas, y una funcion que escribe en stdout sin que se lo pidan no
    se puede probar sin capturar la salida.
    """
    decir = avisar or (lambda *_: None)

    casos = [Caso(caso_id=f"C{i:05d}", cliente=c) for i, c in enumerate(clientes, 1)]

    # --- Etapa 1: screening ---
    decir(f"\n[1/4] Screening: {len(clientes)} cliente(s) contra {len(padron)} designado(s)")
    resultado = screenear(casos, padron, politica, actor=actor)
    decir(f"      {len(resultado.coincidencias)} coincidencia(s), "
          f"{sum(1 for c in casos if c.estado is Estado.ESCALADO)} escalado(s)")

    por_cliente: dict[str, list[Coincidencia]] = {}
    for c in resultado.coincidencias:
        por_cliente.setdefault(c.cliente_id, []).append(c)

    # --- Etapa 2: beneficiario final y scoring ---
    decir("\n[2/4] Beneficiario final y scoring EBR")

    estructura = leer_estructura(societaria, clientes) if societaria else None
    resoluciones: dict[str, Resolucion] = {}
    if estructura is not None:
        for cliente in clientes:
            if cliente.tipo == "PERSONA":
                continue
            resoluciones[cliente.cliente_id] = resolver(estructura, cliente.cliente_id)
        decir(f"      {len(resoluciones)} estructura(s) analizada(s)")

    registro_pep = leer_peps(peps) if peps else None
    if registro_pep is not None:
        vencidas = registro_pep.vencidas()
        cola = (f", {len(vencidas)} vencida(s) por el plazo de 2 anios"
                if vencidas else "")
        decir(f"      {len(registro_pep)} declaracion(es) de PEP{cola}")

    evaluaciones = evaluar_casos(
        casos, resoluciones, por_cliente,
        registro_pep=registro_pep,
        umbral_probable=politica.umbral_probable,
        matriz=MATRIZ_POR_DEFECTO,
        actor=actor,
    )

    # --- Capacidad economica documentada ---
    # Va antes del monitoreo porque una de sus reglas la consume, y se calcula
    # una vez por cliente en vez de una vez por regla.
    registro_legajos = leer_respaldos(respaldos) if respaldos else None
    if arca:
        # Las constancias van al mismo legajo que los respaldos: dos
        # registros paralelos por cliente se despegan solos.
        registro_legajos = leer_arca(arca, registro_legajos)
    capacidades: dict[str, Capacidad] = {}
    if registro_legajos is not None:
        for cliente in clientes:
            capacidades[cliente.cliente_id] = calcular_capacidad(
                cliente, registro_legajos.de(cliente.cliente_id))
        documentados = sum(1 for c in capacidades.values() if c.documentada)
        decir(f"      {documentados} cliente(s) con capacidad documentada")

    # --- Cotejo contra las fuentes externas, item 3.4 ---
    # El expediente recibe las dos clases por separado. Un hallazgo es algo que
    # el programa puede afirmar, como un codigo de actividad que cambio. Una
    # lectura es un par de valores que difieren en texto libre y que decide una
    # persona. Mezclarlas ahoga a las primeras: medido contra ARCA, comparar la
    # actividad por texto da 30% de precision y por codigo da 100%.
    if registro_legajos is not None:
        indice_casos = {c.cliente.cliente_id: c for c in casos}
        total_hallazgos = total_lecturas = 0
        for cliente in clientes:
            legajo = registro_legajos.de(cliente.cliente_id)
            caso = indice_casos.get(cliente.cliente_id)
            if caso is None or not len(legajo):
                continue

            for cotejo in legajo.hallazgos(cliente):
                total_hallazgos += 1
                caso.registrar(
                    actor, "DISCREPANCIA_CONSTATADA",
                    campo=cotejo.campo.value,
                    declarado=cotejo.declarado,
                    constatado=cotejo.hallado,
                    origen=cotejo.constatacion.origen.value,
                    consultado=cotejo.constatacion.fecha_consulta.isoformat(),
                    referencia=cotejo.constatacion.referencia,
                )
            for cotejo in legajo.para_revisar(cliente):
                total_lecturas += 1
                caso.registrar(
                    actor, "DIFERENCIA_PARA_LEER",
                    campo=cotejo.campo.value,
                    declarado=cotejo.declarado,
                    constatado=cotejo.hallado,
                    origen=cotejo.constatacion.origen.value,
                    nota=("texto libre: puede ser la misma cosa escrita de otra "
                          "forma. Lo decide el analista"),
                )
            for cotejo in legajo.completados(cliente):
                caso.registrar(
                    actor, "DATO_COMPLETADO",
                    campo=cotejo.campo.value,
                    constatado=cotejo.hallado,
                    origen=cotejo.constatacion.origen.value,
                )

        if total_hallazgos or total_lecturas:
            decir(f"      {total_hallazgos} discrepancia(s) constatada(s), "
                  f"{total_lecturas} diferencia(s) de texto para leer")

    # --- Etapa 3: monitoreo transaccional ---
    alertas: dict[str, list[Alerta]] = {}
    operatorias: dict[str, Operatoria] = {}
    tabla_perfiles: dict[str, Perfil] = {}
    umbral_usado = 0.0

    if operaciones:
        decir("\n[3/4] Monitoreo transaccional")
        operatorias = agrupar(leer_operaciones(operaciones))
        tabla_perfiles = leer_perfiles(perfiles) if perfiles else {}

        parametros = parametros_con_listas(umbral_reporte=umbral_reporte)
        umbral_usado = parametros.umbral_reporte
        if parametros.umbral_reporte <= 0:
            decir("      aviso: sin umbral de reporte, la regla de fraccionamiento no corre",
                  True)
        else:
            origen = "parametro" if umbral_reporte else "40 SMVM, Res. 78/2025"
            decir(f"      umbral de reporte: ${parametros.umbral_reporte:,.0f} ({origen})")

        # Los clientes van al monitoreo porque hay reglas que comparan la
        # operatoria contra lo que el cliente declaro en el alta, y las
        # capacidades porque hay una que la compara contra lo que documento.
        # La capacidad se calcula una vez por cliente y no una vez por regla.
        alertas = monitorear(operatorias, tabla_perfiles, parametros,
                             clientes={c.cliente_id: c for c in clientes},
                             capacidades=capacidades)
        total_ops = sum(o.cantidad for o in operatorias.values())
        decir(f"      {total_ops} operacion(es) de {len(operatorias)} cliente(s), "
              f"{len(tabla_perfiles)} perfil(es) declarado(s)")

        for r in reglas_inactivas():
            decir(f"      regla apagada: {r.codigo}", True)

        indice = {c.cliente.cliente_id: c for c in casos}
        for cliente_id, lista in alertas.items():
            caso = indice.get(cliente_id)
            if caso is None:
                continue
            for a in lista:
                caso.registrar(
                    actor, "ALERTA_MONITOREO",
                    tipo=a.codigo, severidad=a.severidad,
                    descripcion=a.descripcion, metodologia=a.metodologia,
                    monto=round(a.monto_involucrado, 2),
                    vence=a.vence.isoformat(),
                )
            # Una alerta reabre el legajo cerrado: la debida diligencia
            # continuada alcanza a todos los clientes, no solo a los de
            # riesgo alto.
            if caso.estado in (Estado.CERRADO, Estado.SCORING):
                origen = caso.estado.value
                caso.transicionar(
                    Estado.ANALISIS, actor,
                    f"{len(lista)} alerta(s) de monitoreo"
                    + (" (reapertura del legajo)" if origen == "CERRADO" else ""),
                )

    # --- Etapa 4: congelamiento y exposicion ---
    nombres = {c.cliente.cliente_id: c.cliente.nombre for c in casos}
    congelamientos = obligaciones(
        resultado.coincidencias, nombres, politica.umbral_probable
    )

    if congelamientos:
        decir("\n[4/4] Congelamiento administrativo")
        decir(f"      {len(congelamientos)} obligacion(es), reporte dentro de 24hs")
        for c in congelamientos:
            decir(f"      {c.cliente_id}  {c.resumen()}")

    indice = {c.cliente.cliente_id: c for c in casos}
    for c in congelamientos:
        caso = indice.get(c.cliente_id)
        if caso is None:
            continue
        caso.registrar(
            actor, "CONGELAMIENTO_REQUERIDO",
            regimen=c.regimen.value, lista=c.lista, designado=c.designado,
            norma=c.norma, plazo="24 horas",
            reserva="prohibido informar al cliente",
        )

    sin_perfil = [cid for cid, lista in alertas.items()
                  if any(a.codigo == "SIN_PERFIL" for a in lista)]
    sin_bf = [cid for cid, r in resoluciones.items() if not r.identificado]
    exposicion = estimar(alertas, congelamientos, nombres, sin_perfil, sin_bf)

    return Corrida(
        politica=politica,
        padron=padron,
        clientes=clientes,
        casos=casos,
        screening=resultado,
        coincidencias=por_cliente,
        estructura=estructura,
        resoluciones=resoluciones,
        registro_pep=registro_pep,
        evaluaciones=evaluaciones,
        operatorias=operatorias,
        perfiles=tabla_perfiles,
        alertas=alertas,
        capacidades=capacidades,
        congelamientos=congelamientos,
        exposicion=exposicion,
        umbral_reporte=umbral_usado,
    )


def a_consola(linea: str, es_error: bool = False) -> None:
    """Emisor de progreso que escribe en la terminal."""
    print(linea, file=sys.stderr if es_error else sys.stdout)
