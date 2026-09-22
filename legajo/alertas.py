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

import hashlib
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Callable

from . import monotributo
from .config import ParametrosMonitoreo, PARAMETROS_POR_DEFECTO
from .modelo import Cliente
from .operaciones import Operacion, Operatoria, Perfil
from .paises import iso, nombre as nombre_pais
from .regimen import Regimen, regimen_de_alerta, vencimiento

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

    @property
    def identificador(self) -> str:
        """Identidad estable de la alerta, derivada de su contenido.

        Tiene que ser deterministica: el circuito se vuelve a correr entre que
        se exporta el informe y que se leen las decisiones del analista. Un id
        aleatorio romperia el ida y vuelta en silencio, porque las decisiones
        no matchearian y las alertas volverian a figurar como pendientes sin
        que nadie se entere.

        La clave (cliente, codigo) no alcanza: la misma tipologia puede
        disparar varias veces sobre un cliente, con dos jurisdicciones
        distintas o dos grupos de fraccionamiento separados.
        """
        crudo = (f"{self.cliente_id}|{self.codigo}|{self.fecha_operacion.isoformat()}"
                 f"|{self.monto_involucrado:.2f}")
        return hashlib.sha256(crudo.encode("utf-8")).hexdigest()[:12]

    @property
    def regimen(self) -> Regimen:
        """El regimen no se declara, se deriva del tipo de inusualidad.

        Un campo cargado a mano es un campo que alguien carga mal, y el error
        recien aparece cuando la UIF pregunta por que un reporte de
        terrorismo salio a los tres meses.
        """
        return regimen_de_alerta(self.codigo)

    @property
    def fecha_operacion(self) -> date:
        """La mas antigua de las operaciones involucradas.

        El tope de 90 dias corre desde que la operacion fue realizada, no
        desde que se detecto. Tomar la mas reciente daria mas plazo del que
        hay.
        """
        if not self.operaciones:
            return self.generada
        return min(o.fecha for o in self.operaciones)

    @property
    def vencimiento(self):
        return vencimiento(self.regimen, self.fecha_operacion, self.generada)

    @property
    def vence(self) -> date:
        return self.vencimiento.vence

    @property
    def dias_restantes(self) -> int:
        return (self.vence - self.generada).days

    @property
    def vencida(self) -> bool:
        return self.vence < self.generada

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
            "alerta_id": self.identificador,
            "cliente_id": self.cliente_id,
            "nivel_riesgo": nivel_riesgo,
            "perfil": perfil,
            "operaciones": self.detalle_operaciones,
            "metodologia": self.metodologia,
            "generada": self.generada.isoformat(),
            "tipo_inusualidad": self.codigo,
            "regimen": self.regimen.value,
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
    evaluar: Callable[..., list[Alerta]]
    # Las reglas reciben (operatoria, perfil, parametros, cliente). El cliente
    # entro despues, cuando aparecieron las reglas que comparan la operatoria
    # contra lo que el cliente declaro en el alta: categoria de monotributo,
    # actividad, provincia. Va al final y con valor por defecto para que una
    # regla que no lo necesita no tenga que nombrarlo.
    activa: bool = True
    motivo_inactiva: str = ""


# ---------------------------------------------------------------------------
# Reglas
# ---------------------------------------------------------------------------

def _sin_perfil(op: Operatoria, perfil: Perfil | None, p: ParametrosMonitoreo,
         cliente: Cliente | None = None):
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


def _desvio_perfil(op: Operatoria, perfil: Perfil | None, p: ParametrosMonitoreo,
         cliente: Cliente | None = None):
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


def _fraccionamiento(op: Operatoria, perfil: Perfil | None, p: ParametrosMonitoreo,
         cliente: Cliente | None = None):
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


def _efectivo_desproporcionado(op: Operatoria, perfil: Perfil | None, p: ParametrosMonitoreo,
         cliente: Cliente | None = None):
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


def _jurisdiccion_no_declarada(op: Operatoria, perfil: Perfil | None, p: ParametrosMonitoreo,
         cliente: Cliente | None = None):
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


def _aceleracion(op: Operatoria, perfil: Perfil | None, p: ParametrosMonitoreo,
         cliente: Cliente | None = None):
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


def _montos_redondos(op: Operatoria, perfil: Perfil | None, p: ParametrosMonitoreo,
         cliente: Cliente | None = None):
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


def _monotributo_excedido(op: Operatoria, perfil: Perfil | None,
                          p: ParametrosMonitoreo,
                          cliente: Cliente | None = None):
    """Volumen operado anualizado por encima del tope de la categoria declarada.

    Es la pregunta central del proyecto puesta sobre el caso mas simple que
    hay: un monotributista declara una categoria, y esa categoria tiene un
    tope de ingresos brutos anuales que fija ARCA.

    Lo que se compara NO es ingreso contra tope. El volumen que ve el banco
    incluye transferencias entre cuentas propias, prestamos, devoluciones y
    plata que no es facturacion. Por eso la alerta describe una inconsistencia
    entre lo declarado y lo operado, y no afirma que el cliente evadio: eso lo
    resuelve el analista pidiendo la documentacion.

    No dispara si faltan meses de operatoria. Anualizar una ventana corta
    produce un numero que no significa nada, y una alerta que no significa
    nada entrena al analista a ignorar las alertas.
    """
    if cliente is None:
        return []
    if (cliente.condicion_iva or "").strip().upper() != "MONOTRIBUTO":
        return []

    categoria = (cliente.categoria_monotributo or "").strip().upper()
    tope = monotributo.tope_anual(categoria)
    if tope is None:
        # Categoria vacia o fuera de la tabla cargada. No se puede evaluar, y
        # no evaluarla es distinto de darla por buena.
        return []

    if op.meses < p.meses_minimos_para_anualizar:
        return []

    anualizado = op.total / op.meses * 12
    if anualizado <= tope:
        return []

    veces = anualizado / tope
    # SIN CALIBRAR: revisar antes de usar en produccion. El corte entre
    # MEDIA y ALTA sale de razonar, no de medir. Ver config.py.
    grave = veces >= p.factor_monotributo_grave

    return [Alerta(
        cliente_id=op.cliente_id,
        codigo="MONOTRIBUTO_EXCEDIDO",
        severidad=ALTA if grave else MEDIA,
        descripcion=(
            f"categoria {categoria} declarada, tope ${tope:,.0f} anuales. "
            f"Opero ${op.total:,.0f} en {op.meses:.1f} mes(es), que anualizado "
            f"da ${anualizado:,.0f}, {veces:.1f} veces el tope"
        ),
        metodologia=(
            f"volumen operado anualizado contra el tope de la categoria "
            f"declarada, escala {monotributo.FUENTE} vigente desde "
            f"{monotributo.VIGENCIA_DESDE.isoformat()}"
        ),
        operaciones=tuple(op.operaciones[:8]),
        monto_involucrado=op.total,
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
    Regla("MONOTRIBUTO_EXCEDIDO",
          "volumen anualizado por encima del tope de la categoria declarada",
          MEDIA, _monotributo_excedido),
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
    clientes: dict[str, Cliente] | None = None,
) -> dict[str, list[Alerta]]:
    """Corre el catalogo sobre cada operatoria.

    El motor no sabe que hace ninguna regla. Solo las recorre.

    `clientes` es opcional. Sin el, las reglas que comparan contra lo declarado
    en el alta no disparan, que es lo correcto: no tener el dato no es lo mismo
    que tenerlo y que no cierre.
    """
    resultado: dict[str, list[Alerta]] = {}

    for cliente_id, operatoria in operatorias.items():
        perfil = perfiles.get(cliente_id)
        cliente = (clientes or {}).get(cliente_id)
        alertas: list[Alerta] = []
        for regla in catalogo:
            if not regla.activa:
                continue
            alertas.extend(regla.evaluar(operatoria, perfil, parametros, cliente))
        if alertas:
            alertas.sort(key=lambda a: (_ORDEN_SEVERIDAD[a.severidad], -a.monto_involucrado))
            resultado[cliente_id] = alertas

    return resultado


def reglas_inactivas(catalogo: tuple[Regla, ...] = CATALOGO) -> list[Regla]:
    """Reglas apagadas y por que. Hay que poder mostrarlo en una supervision."""
    return [r for r in catalogo if not r.activa]
