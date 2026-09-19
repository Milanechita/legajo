"""Motor de alertas de monitoreo transaccional.

Una regla es una entrada del catalogo, no una rama del motor. El motor
recorre el catalogo y no sabe que hace cada regla; agregar una tipologia es
agregar una linea al final de CATALOGO.

Esa forma importa mas de lo que parece. Un motor escrito como cadena de if
crece hasta que nadie puede decir que dispara que, y entonces el equipo deja
de tocarlo y las tipologias nuevas nunca se incorporan.

El contenido de la alerta no es arbitrario. Los manuales del sector fijan el
minimo que debe tener un registro de operaciones inusuales: nivel de riesgo
del cliente, perfil, identificacion de la operacion, metodologia de deteccion,
procedencia y fecha de la alerta, tipo de inusualidad, medidas adoptadas y
decision final motivada. Las seis primeras las completa el sistema. Las dos
ultimas son del analista y salen en blanco a proposito, porque son
justamente la parte que una maquina no puede resolver.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Callable

from .config import ParametrosMonitoreo, PARAMETROS_POR_DEFECTO
from .operaciones import Operacion, Operatoria, Perfil
from .paises import iso, nombre as nombre_pais

ALTA = "ALTA"
MEDIA = "MEDIA"
BAJA = "BAJA"

_ORDEN_SEVERIDAD = {ALTA: 0, MEDIA: 1, BAJA: 2}


@dataclass(frozen=True)
class Alerta:
    """Una inusualidad detectada, con el contenido minimo que exige la norma."""

    cliente_id: str
    codigo: str                     # tipo de inusualidad
    severidad: str
    descripcion: str
    metodologia: str                # como se detecto
    operaciones: tuple[Operacion, ...] = ()
    monto_involucrado: float = 0.0
    generada: date = field(default_factory=date.today)
    plazo_dias: int = 90            # plazo de analisis

    @property
    def vence(self) -> date:
        return self.generada + timedelta(days=self.plazo_dias)

    @property
    def detalle_operaciones(self) -> str:
        return " | ".join(o.resumen() for o in self.operaciones[:8])

    def como_fila(self, nivel_riesgo: str = "", perfil: str = "") -> dict:
        """Fila del registro de operaciones inusuales.

        Las dos ultimas columnas van vacias: las completa el analista cuando
        resuelve la alerta. Dejarlas pre-llenadas seria fingir un analisis
        que no ocurrio.
        """
        return {
            "cliente_id": self.cliente_id,
            "nivel_riesgo": nivel_riesgo,
            "perfil": perfil,
            "operaciones": self.detalle_operaciones,
            "metodologia": self.metodologia,
            "generada": self.generada.isoformat(),
            "tipo_inusualidad": self.codigo,
            "severidad": self.severidad,
            "descripcion": self.descripcion,
            "monto_involucrado": self.monto_involucrado,
            "vence": self.vence.isoformat(),
            "medidas_adoptadas": "",
            "decision_final": "",
        }


@dataclass(frozen=True)
class Regla:
    """Una tipologia del catalogo.

    `activa` existe porque no toda tipologia aplica a toda jurisdiccion ni a
    todo sujeto obligado. Una regla que genera ruido entrena al analista a
    ignorar las alertas, y eso es peor que no tener la regla.
    """

    codigo: str
    descripcion: str
    severidad: str
    evaluar: Callable[[Operatoria, Perfil | None, ParametrosMonitoreo], list[Alerta]]
    activa: bool = True
    motivo_inactiva: str = ""


# ---------------------------------------------------------------------------
# Reglas
# ---------------------------------------------------------------------------

def _sin_perfil(op: Operatoria, perfil: Perfil | None, p: ParametrosMonitoreo):
    """Cliente que opera sin perfil transaccional declarado.

    No es una conducta del cliente sino una falta de control, y es de las
    primeras cosas que encuentra una inspeccion.
    """
    if perfil is not None and perfil.declarado:
        return []
    if op.cantidad < p.minimo_operaciones_para_exigir_perfil:
        return []
    return [Alerta(
        cliente_id=op.cliente_id,
        codigo="SIN_PERFIL",
        severidad=MEDIA,
        descripcion=(f"opero {op.cantidad} vez/veces por ${op.total:,.0f} sin perfil "
                     f"transaccional declarado"),
        metodologia="ausencia de perfil declarado con operatoria registrada",
        monto_involucrado=op.total,
    )]


def _desvio_perfil(op: Operatoria, perfil: Perfil | None, p: ParametrosMonitoreo):
    """Operatoria mensual por encima de lo declarado.

    Se evalua mes calendario por mes calendario y se reporta el peor. Un
    promedio sobre todo el periodo diluye justo el mes que hay que mirar.
    """
    if perfil is None or not perfil.declarado or perfil.monto_mensual <= 0:
        return []

    tope = perfil.monto_mensual * (1 + p.tolerancia_desvio)
    peor, peor_total = None, 0.0
    for clave, ops in op.por_mes().items():
        total = sum(o.monto for o in ops)
        if total > tope and total > peor_total:
            peor, peor_total = (clave, ops), total

    if peor is None:
        return []

    (anio, mes), ops = peor
    veces = peor_total / perfil.monto_mensual
    return [Alerta(
        cliente_id=op.cliente_id,
        codigo="DESVIO_PERFIL",
        severidad=ALTA if veces >= p.desvio_severo else MEDIA,
        descripcion=(f"{mes:02d}/{anio}: opero ${peor_total:,.0f} contra "
                     f"${perfil.monto_mensual:,.0f} declarados ({veces:.1f}x)"),
        metodologia=f"comparacion mensual contra perfil, tolerancia {p.tolerancia_desvio:.0%}",
        operaciones=tuple(sorted(ops, key=lambda o: -o.monto)),
        monto_involucrado=peor_total,
    )]


def _fraccionamiento(op: Operatoria, perfil: Perfil | None, p: ParametrosMonitoreo):
    """Operaciones sucesivas bajo el umbral de reporte que en conjunto lo superan.

    Dos condiciones hacen que esto sea fraccionamiento y no volumen alto.

    Cada operacion tiene que estar individualmente por debajo del umbral: si
    una sola lo supera, esa operacion se reporta igual y no hubo evasion del
    control.

    Y cada operacion tiene que ser materialmente parte del reparto. Nadie
    fracciona una suma grande en depositos diminutos, porque necesitaria
    cientos. Incluir los movimientos chicos que caen en la ventana ensucia la
    alerta con operatoria cotidiana y le hace perder tiempo al analista.
    """
    if p.umbral_reporte <= 0:
        return []

    piso = p.umbral_reporte * p.piso_fraccionamiento
    alertas: list[Alerta] = []
    cubiertas: set[int] = set()

    for v in op.ventanas(p.ventana_fraccionamiento):
        candidatas = [o for o in v.operaciones if piso <= o.monto < p.umbral_reporte]
        if len(candidatas) < p.minimo_operaciones_fraccionadas:
            continue
        total = sum(o.monto for o in candidatas)
        if total < p.umbral_reporte:
            continue

        # Una ventana que se corrio un dia es la misma agrupacion vista de
        # nuevo, no un patron distinto. Solo se emite alerta si aporta al
        # menos el minimo de operaciones que todavia no estaban cubiertas.
        nuevas = [o for o in candidatas if id(o) not in cubiertas]
        if len(nuevas) < p.minimo_operaciones_fraccionadas:
            continue
        cubiertas.update(id(o) for o in candidatas)

        # Que tan cerca del umbral estuvo la mayor. Cuanto mas cerca, mas
        # dificil es que sea casualidad.
        cercania = max(o.monto for o in candidatas) / p.umbral_reporte
        alertas.append(Alerta(
            cliente_id=op.cliente_id,
            codigo="FRACCIONAMIENTO",
            severidad=ALTA if cercania >= p.cercania_umbral_severa else MEDIA,
            descripcion=(f"{len(candidatas)} operaciones en {p.ventana_fraccionamiento} "
                         f"dias por ${total:,.0f}, todas bajo el umbral de reporte "
                         f"(${p.umbral_reporte:,.0f}); la mayor llego al {cercania:.0%}"),
            metodologia=(f"ventana deslizante de {p.ventana_fraccionamiento} dias, "
                         f"minimo {p.minimo_operaciones_fraccionadas} operaciones, "
                         f"piso {p.piso_fraccionamiento:.0%} del umbral"),
            operaciones=tuple(candidatas),
            monto_involucrado=total,
        ))
    return alertas


def _efectivo_desproporcionado(op: Operatoria, perfil: Perfil | None, p: ParametrosMonitoreo):
    """Uso de efectivo por encima de lo esperado para la actividad."""
    if not op.total:
        return []

    real = op.proporcion_efectivo
    esperado = perfil.proporcion_efectivo if perfil and perfil.declarado else None
    tope = (esperado + p.tolerancia_efectivo) if esperado is not None else p.efectivo_sin_perfil

    if real <= tope:
        return []

    referencia = (f"{esperado:.0%} declarado" if esperado is not None
                  else f"{p.efectivo_sin_perfil:.0%} de referencia, sin perfil")
    return [Alerta(
        cliente_id=op.cliente_id,
        codigo="EFECTIVO_DESPROPORCIONADO",
        severidad=ALTA if real >= p.efectivo_severo else MEDIA,
        descripcion=(f"{real:.0%} de la operatoria en efectivo "
                     f"(${op.total_efectivo:,.0f}) contra {referencia}"),
        metodologia="proporcion de efectivo sobre el total operado",
        operaciones=tuple(o for o in op.operaciones if o.es_efectivo)[:10],
        monto_involucrado=op.total_efectivo,
    )]


def _jurisdiccion_no_declarada(op: Operatoria, perfil: Perfil | None, p: ParametrosMonitoreo):
    """Contrapartes en paises que el cliente no declaro operar.

    Reusa la normalizacion y las listas de la etapa 2: si el pais ademas esta
    en una lista de riesgo, la alerta sube de severidad.
    """
    esperados = set(perfil.paises) if perfil else set()
    hallazgos: dict[str, list[Operacion]] = {}

    for o in op.operaciones:
        codigo = iso(o.pais_contraparte)
        if codigo is None or codigo == p.pais_local or codigo in esperados:
            continue
        hallazgos.setdefault(codigo, []).append(o)

    alertas = []
    for codigo, ops in sorted(hallazgos.items()):
        riesgosa = codigo in p.jurisdicciones_de_riesgo
        total = sum(o.monto for o in ops)
        alertas.append(Alerta(
            cliente_id=op.cliente_id,
            codigo="JURISDICCION_NO_DECLARADA",
            severidad=ALTA if riesgosa else MEDIA,
            descripcion=(f"{len(ops)} operacion(es) por ${total:,.0f} con contraparte en "
                         f"{nombre_pais(codigo)}"
                         + (", jurisdiccion en lista de riesgo" if riesgosa else
                            ", pais no declarado en el perfil")),
            metodologia="paises de contraparte normalizados a ISO, contra el perfil y las listas",
            operaciones=tuple(ops)[:10],
            monto_involucrado=total,
        ))
    return alertas


def _aceleracion(op: Operatoria, perfil: Perfil | None, p: ParametrosMonitoreo):
    """Salto de volumen respecto del propio historial del cliente.

    Es independiente del perfil declarado: un cliente puede estar dentro de
    lo declarado y aun asi cambiar de comportamiento de golpe.
    """
    if op.cantidad < p.minimo_operaciones_para_linea_base:
        return []

    recientes = op.ultimos(p.ventana_aceleracion)
    if not recientes:
        return []

    historicas = [o for o in op.operaciones if o not in recientes]
    if not historicas:
        return []

    dias_hist = max((op.hasta - op.desde).days - p.ventana_aceleracion, 1)
    diario_hist = sum(o.monto for o in historicas) / dias_hist
    diario_rec = sum(o.monto for o in recientes) / p.ventana_aceleracion

    if diario_hist <= 0 or diario_rec / diario_hist < p.factor_aceleracion:
        return []

    veces = diario_rec / diario_hist
    return [Alerta(
        cliente_id=op.cliente_id,
        codigo="ACELERACION",
        severidad=MEDIA,
        descripcion=(f"los ultimos {p.ventana_aceleracion} dias promedian "
                     f"${diario_rec:,.0f} diarios contra ${diario_hist:,.0f} "
                     f"historicos ({veces:.1f}x)"),
        metodologia=f"promedio diario de los ultimos {p.ventana_aceleracion} dias contra el resto",
        operaciones=tuple(recientes)[:10],
        monto_involucrado=sum(o.monto for o in recientes),
    )]


def _montos_redondos(op: Operatoria, perfil: Perfil | None, p: ParametrosMonitoreo):
    """Proporcion alta de importes exactos.

    Tipologia clasica: la operatoria genuina deja decimales, la armada usa
    cifras redondas.
    """
    if op.cantidad < p.minimo_operaciones_para_linea_base:
        return []

    redondas = [o for o in op.operaciones
                if o.monto > 0 and o.monto % p.multiplo_redondo == 0]
    proporcion = len(redondas) / op.cantidad
    if proporcion < p.proporcion_redondos:
        return []

    return [Alerta(
        cliente_id=op.cliente_id,
        codigo="MONTOS_REDONDOS",
        severidad=BAJA,
        descripcion=(f"{proporcion:.0%} de las operaciones son multiplos exactos de "
                     f"${p.multiplo_redondo:,.0f}"),
        metodologia=f"importes multiplos de {p.multiplo_redondo:,.0f} sobre el total",
        operaciones=tuple(redondas)[:10],
        monto_involucrado=sum(o.monto for o in redondas),
    )]


# ---------------------------------------------------------------------------
# Catalogo
# ---------------------------------------------------------------------------

CATALOGO: tuple[Regla, ...] = (
    Regla("SIN_PERFIL", "opera sin perfil transaccional declarado", MEDIA, _sin_perfil),
    Regla("DESVIO_PERFIL", "operatoria mensual por encima de lo declarado", ALTA, _desvio_perfil),
    Regla("FRACCIONAMIENTO", "operaciones sucesivas bajo el umbral de reporte", ALTA, _fraccionamiento),
    Regla("EFECTIVO_DESPROPORCIONADO", "uso de efectivo mayor al esperado", ALTA, _efectivo_desproporcionado),
    Regla("JURISDICCION_NO_DECLARADA", "contraparte en pais no declarado", MEDIA, _jurisdiccion_no_declarada),
    Regla("ACELERACION", "salto de volumen contra el propio historial", MEDIA, _aceleracion),
    Regla(
        "MONTOS_REDONDOS", "proporcion alta de importes exactos", BAJA, _montos_redondos,
        activa=False,
        motivo_inactiva=(
            "En Argentina los importes redondos son culturalmente comunes por el "
            "orden de magnitud nominal, asi que esta regla dispara sobre operatoria "
            "normal. Queda disponible pero apagada: una regla ruidosa entrena al "
            "analista a ignorar las alertas. Activarla despues de calibrar el "
            "multiplo contra la operatoria propia."
        ),
    ),
)


def monitorear(
    operatorias: dict[str, Operatoria],
    perfiles: dict[str, Perfil],
    parametros: ParametrosMonitoreo = PARAMETROS_POR_DEFECTO,
    catalogo: tuple[Regla, ...] = CATALOGO,
) -> dict[str, list[Alerta]]:
    """Corre el catalogo sobre cada operatoria.

    El motor no sabe que hace ninguna regla. Solo las recorre.
    """
    resultado: dict[str, list[Alerta]] = {}

    for cliente_id, operatoria in operatorias.items():
        perfil = perfiles.get(cliente_id)
        alertas: list[Alerta] = []
        for regla in catalogo:
            if not regla.activa:
                continue
            alertas.extend(regla.evaluar(operatoria, perfil, parametros))
        if alertas:
            alertas.sort(key=lambda a: (_ORDEN_SEVERIDAD[a.severidad], -a.monto_involucrado))
            resultado[cliente_id] = alertas

    return resultado


def reglas_inactivas(catalogo: tuple[Regla, ...] = CATALOGO) -> list[Regla]:
    """Reglas apagadas y por que. Hay que poder mostrarlo en una supervision."""
    return [r for r in catalogo if not r.activa]
