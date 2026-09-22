"""Pruebas de la regla de personas juridicas sin respaldo documental.

Cubre el hueco que CAPACIDAD_EXCEDIDA deja a proposito: esa no dispara sin
documentacion, porque un legajo a medio cargar no es un cliente que no puede
justificar. Para una sociedad que mueve plata por encima del umbral de
reporte, la ausencia total de respaldo si es un hallazgo.
"""

from __future__ import annotations

from datetime import date, timedelta

from legajo.alertas import monitorear
from legajo.capacidad import calcular
from legajo.config import ParametrosMonitoreo, parametros_con_listas
from legajo.modelo import Cliente
from legajo.operaciones import Operacion, Operatoria
from legajo.procedencia import LegajoCliente, Periodicidad, Respaldo

INICIO = date(2026, 1, 15)
PARAMETROS = parametros_con_listas()
UMBRAL = PARAMETROS.umbral_reporte


def sociedad(constitucion="2015-04-10") -> Cliente:
    return Cliente(cliente_id="CL900", nombre="Nodo Sur S.A.S.", tipo="ENTIDAD",
                   fecha_constitucion=constitucion)


def humana() -> Cliente:
    return Cliente(cliente_id="CL900", nombre="Juan Perez", tipo="PERSONA")


def operatoria(total: float, meses: float = 6, cantidad: int = 12) -> Operatoria:
    paso = timedelta(days=meses * 30.44 / max(cantidad - 1, 1))
    return Operatoria(cliente_id="CL900", operaciones=[
        Operacion(cliente_id="CL900", fecha=INICIO + paso * i, monto=total / cantidad)
        for i in range(cantidad)
    ])


def correr(cli, op, respaldos=(), parametros=PARAMETROS):
    legajo = LegajoCliente("CL900")
    for r in respaldos:
        legajo.agregar_respaldo(r)
    alertas = monitorear({"CL900": op}, {}, parametros,
                         clientes={"CL900": cli},
                         capacidades={"CL900": calcular(cli, legajo)})
    return [a for a in alertas.get("CL900", []) if a.codigo == "SOCIEDAD_SIN_RESPALDO"]


def balance(monto=200_000_000.0) -> Respaldo:
    return Respaldo("CL900", "BALANCE", emitido=date(2026, 3, 1), monto=monto,
                    periodicidad=Periodicidad.ANUAL,
                    periodo_hasta=date(2025, 12, 31))


# --- dispara cuando corresponde -------------------------------------------

def test_una_sociedad_vieja_que_mueve_fuerte_sin_un_solo_balance_alerta():
    [a] = correr(sociedad("2015-04-10"), operatoria(UMBRAL * 8))
    assert a.severidad == "ALTA"
    assert "sin ningun documento" in a.descripcion
    assert "constituida hace 11 anio(s)" in a.descripcion


def test_una_sociedad_recien_constituida_alerta_pero_con_menos_severidad():
    # Todavia no pudo cerrar su primer ejercicio, asi que la falta de balance
    # se explica sola. Lo que importa ahi es el volumen, no el papel faltante.
    [a] = correr(sociedad("2025-11-01"), operatoria(UMBRAL * 8))
    assert a.severidad == "MEDIA"
    assert "sin cerrar su primer ejercicio" in a.descripcion


def test_sin_fecha_de_constitucion_alerta_igual_y_lo_dice():
    # Falta el dato, no la operatoria. El analista tiene que ver las dos cosas.
    [a] = correr(sociedad(None), operatoria(UMBRAL * 8))
    assert "sin fecha de constitucion" in a.descripcion
    assert a.severidad == "ALTA"


# --- no dispara cuando no corresponde -------------------------------------

def test_una_persona_humana_nunca_dispara_esta_regla():
    # Una persona no cierra balances. Aplicarle la regla seria pedirle un
    # documento que no existe para ella.
    assert correr(humana(), operatoria(UMBRAL * 8)) == []


def test_una_sociedad_con_balance_no_dispara():
    # Con respaldo cargado, la comparacion la hace CAPACIDAD_EXCEDIDA. Que las
    # dos disparen sobre el mismo cliente seria contarlo dos veces.
    assert correr(sociedad(), operatoria(UMBRAL * 8), respaldos=[balance()]) == []


def test_una_sociedad_que_opera_por_debajo_del_umbral_no_dispara():
    # El corte es el umbral de reporte, que es normativo. Una sociedad chica
    # sin balance es un legajo incompleto, que le toca al item 5.1.
    assert correr(sociedad(), operatoria(UMBRAL * 0.5)) == []


def test_sin_umbral_de_reporte_la_regla_no_corre():
    # Sin umbral no hay corte de volumen, y disparar sobre toda sociedad sin
    # balance llenaria el informe de ruido.
    sin_umbral = ParametrosMonitoreo(umbral_reporte=0.0)
    assert correr(sociedad(), operatoria(UMBRAL * 8), parametros=sin_umbral) == []


# --- la frontera con las otras reglas -------------------------------------

def test_no_duplica_la_comparacion_que_ya_hace_capacidad_excedida():
    # El roadmap pedia "ventas del balance contra operado". Eso ya lo hace
    # CAPACIDAD_EXCEDIDA: para una entidad, el balance alimenta la capacidad
    # anual. Esta regla cubre el caso contrario, el de no tener balance.
    con_balance = monitorear(
        {"CL900": operatoria(UMBRAL * 30)}, {}, PARAMETROS,
        clientes={"CL900": sociedad()},
        capacidades={"CL900": calcular(sociedad(), _legajo_con_balance())},
    )["CL900"]
    codigos = {a.codigo for a in con_balance}
    assert "CAPACIDAD_EXCEDIDA" in codigos
    assert "SOCIEDAD_SIN_RESPALDO" not in codigos


def _legajo_con_balance() -> LegajoCliente:
    l = LegajoCliente("CL900")
    l.agregar_respaldo(balance())
    return l


def test_los_dos_cortes_salen_de_afuera_y_no_de_una_eleccion():
    # El volumen sale del umbral de reporte (40 SMVM, Res. 78/2025) y la
    # antiguedad de si cerro o no su primer ejercicio, que es anual por
    # definicion. Ninguno es un parametro elegido a ojo.
    assert UMBRAL > 0
    justo_debajo = correr(sociedad(), operatoria(UMBRAL * 0.99))
    justo_encima = correr(sociedad(), operatoria(UMBRAL * 1.01))
    assert justo_debajo == []
    assert justo_encima != []


def test_la_alerta_no_acusa_de_nada():
    [a] = correr(sociedad(), operatoria(UMBRAL * 8))
    texto = (a.descripcion + " " + a.metodologia).lower()
    for palabra in ("evad", "fraude", "delito", "ilicit", "pantalla", "sospech"):
        assert palabra not in texto, f"la alerta dice {palabra!r}"
