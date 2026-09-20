"""Pruebas del monitoreo transaccional.

El riesgo de un motor de reglas no es que falle, es que haga ruido. Una regla
que dispara sobre operatoria normal entrena al analista a cerrar alertas sin
leerlas, y a partir de ahi el sistema entero deja de servir. Varias de estas
pruebas verifican justamente que las reglas NO disparen.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from legajo.alertas import CATALOGO, monitorear, reglas_inactivas
from legajo.config import ParametrosMonitoreo, parametros_con_listas
from legajo.modelo import Caso, Cliente, Estado
from legajo.operaciones import (
    Operacion, Operatoria, Perfil, agrupar, recalibracion_sugerida,
)

INICIO = date(2026, 3, 2)
UMBRAL = 30_000_000.0


def params(**kw) -> ParametrosMonitoreo:
    base = dict(umbral_reporte=UMBRAL)
    base.update(kw)
    return ParametrosMonitoreo(**base)


def op(dia: int, monto: float, *, cid="X1", instrumento="TRANSFERENCIA", pais="Argentina"):
    return Operacion(
        cliente_id=cid, fecha=INICIO + timedelta(days=dia), monto=monto,
        instrumento=instrumento, pais_contraparte=pais,
    )


def correr(operaciones, perfil=None, p=None):
    operatoria = Operatoria(cliente_id="X1", operaciones=list(operaciones))
    perfiles = {"X1": perfil} if perfil else {}
    return monitorear({"X1": operatoria}, perfiles, p or params()).get("X1", [])


def codigos(alertas):
    return {a.codigo for a in alertas}


# --- ventanas deslizantes --------------------------------------------------

def test_las_ventanas_se_calculan_una_sola_vez_y_son_lineales():
    """Cada regla que necesita ventanas consume las mismas, no arma las suyas."""
    operatoria = Operatoria("X1", [op(i, 1000) for i in range(50)])
    ventanas = list(operatoria.ventanas(7))
    assert len(ventanas) == 50
    assert all(v.cantidad <= 7 for v in ventanas)


def test_la_ventana_respeta_los_dias_corridos():
    operatoria = Operatoria("X1", [op(0, 100), op(3, 100), op(9, 100)])
    primera = next(iter(operatoria.ventanas(7)))
    assert primera.cantidad == 2  # la del dia 9 queda afuera


def test_las_operaciones_se_ordenan_por_fecha():
    operatoria = Operatoria("X1", [op(9, 100), op(0, 100), op(3, 100)])
    assert [o.fecha for o in operatoria.operaciones] == sorted(
        o.fecha for o in operatoria.operaciones
    )


# --- fraccionamiento -------------------------------------------------------

def test_detecta_fraccionamiento_clasico():
    """Cinco depositos apenas por debajo del umbral, en una semana."""
    ops = [op(i, 28_000_000, instrumento="EFECTIVO") for i in range(5)]
    alertas = [a for a in correr(ops) if a.codigo == "FRACCIONAMIENTO"]
    assert len(alertas) == 1
    assert alertas[0].severidad == "ALTA"
    assert len(alertas[0].operaciones) == 5


def test_una_sola_operacion_grande_no_es_fraccionamiento():
    """Si supera el umbral se reporta igual: no hubo evasion del control."""
    ops = [op(0, 140_000_000), op(1, 500_000), op(2, 500_000)]
    assert "FRACCIONAMIENTO" not in codigos(correr(ops))


def test_operaciones_chicas_no_forman_parte_del_reparto():
    """Nadie fracciona 30 millones con depositos de cien mil."""
    ops = [op(i, 100_000) for i in range(400)]
    assert "FRACCIONAMIENTO" not in codigos(correr(ops))


def test_el_pago_chico_que_cae_en_la_ventana_no_ensucia_la_alerta():
    ops = [op(i, 28_000_000, instrumento="EFECTIVO") for i in range(5)]
    ops.append(op(2, 90_000))  # haberes, en el medio de la ventana
    alerta = [a for a in correr(ops) if a.codigo == "FRACCIONAMIENTO"][0]
    assert len(alerta.operaciones) == 5
    assert all(o.monto > 1_000_000 for o in alerta.operaciones)


def test_la_ventana_corrida_un_dia_no_genera_una_alerta_nueva():
    """Es la misma agrupacion vista de nuevo, no un patron distinto."""
    ops = [op(i, 28_000_000) for i in range(7)]
    alertas = [a for a in correr(ops) if a.codigo == "FRACCIONAMIENTO"]
    assert len(alertas) == 1


def test_dos_grupos_separados_generan_dos_alertas():
    ops = [op(i, 28_000_000) for i in range(4)]
    ops += [op(60 + i, 28_000_000) for i in range(4)]
    alertas = [a for a in correr(ops) if a.codigo == "FRACCIONAMIENTO"]
    assert len(alertas) == 2


def test_sin_umbral_declarado_la_regla_no_corre():
    """Detectar evasion de un umbral desconocido seria inventar el resultado."""
    ops = [op(i, 28_000_000) for i in range(5)]
    alertas = correr(ops, p=params(umbral_reporte=0.0))
    assert "FRACCIONAMIENTO" not in codigos(alertas)


# --- desvio del perfil -----------------------------------------------------

def test_detecta_desvio_sobre_lo_declarado():
    perfil = Perfil("X1", monto_mensual=1_000_000, operaciones_mensuales=4)
    ops = [op(i * 3, 8_000_000) for i in range(6)]
    alertas = [a for a in correr(ops, perfil) if a.codigo == "DESVIO_PERFIL"]
    assert alertas and alertas[0].severidad == "ALTA"


def test_operar_dentro_del_perfil_no_genera_alerta():
    perfil = Perfil("X1", monto_mensual=5_000_000, operaciones_mensuales=10)
    ops = [op(i * 6, 900_000) for i in range(10)]
    assert "DESVIO_PERFIL" not in codigos(correr(ops, perfil))


def test_la_tolerancia_absorbe_el_desvio_menor():
    perfil = Perfil("X1", monto_mensual=1_000_000, operaciones_mensuales=4)
    ops = [op(i, 550_000) for i in range(2)]  # 1.1M contra 1M, dentro del 25%
    assert "DESVIO_PERFIL" not in codigos(correr(ops, perfil))


def test_el_desvio_reporta_el_peor_mes_no_el_promedio():
    """Promediar todo el periodo diluye justo el mes que hay que mirar."""
    perfil = Perfil("X1", monto_mensual=1_000_000, operaciones_mensuales=4)
    ops = [op(i * 10, 200_000) for i in range(12)]          # meses tranquilos
    ops += [op(200 + i, 9_000_000) for i in range(5)]       # un mes disparado
    alerta = [a for a in correr(ops, perfil) if a.codigo == "DESVIO_PERFIL"][0]
    assert alerta.monto_involucrado >= 40_000_000


# --- efectivo --------------------------------------------------------------

def test_detecta_efectivo_desproporcionado():
    perfil = Perfil("X1", monto_mensual=10_000_000, operaciones_mensuales=10,
                    proporcion_efectivo=0.05)
    ops = [op(i * 3, 1_000_000, instrumento="EFECTIVO") for i in range(9)]
    assert "EFECTIVO_DESPROPORCIONADO" in codigos(correr(ops, perfil))


def test_efectivo_dentro_de_lo_declarado_no_alerta():
    perfil = Perfil("X1", monto_mensual=10_000_000, operaciones_mensuales=10,
                    proporcion_efectivo=0.50)
    ops = [op(i * 3, 1_000_000, instrumento="EFECTIVO") for i in range(3)]
    ops += [op(i * 3 + 1, 1_000_000) for i in range(7)]
    assert "EFECTIVO_DESPROPORCIONADO" not in codigos(correr(ops, perfil))


# --- jurisdicciones --------------------------------------------------------

def test_contraparte_en_pais_no_declarado():
    perfil = Perfil("X1", monto_mensual=50_000_000, operaciones_mensuales=20,
                    paises=("AR",))
    ops = [op(i * 5, 1_000_000, pais="Uruguay") for i in range(4)]
    alertas = [a for a in correr(ops, perfil) if a.codigo == "JURISDICCION_NO_DECLARADA"]
    assert alertas


def test_pais_de_riesgo_eleva_la_severidad():
    perfil = Perfil("X1", monto_mensual=50_000_000, operaciones_mensuales=20,
                    paises=("AR",))
    p = parametros_con_listas(umbral_reporte=UMBRAL)
    comun = correr([op(i, 1_000_000, pais="Uruguay") for i in range(3)], perfil, p)
    riesgo = correr([op(i, 1_000_000, pais="Islas Vírgenes Británicas") for i in range(3)], perfil, p)

    sev = {a.codigo: a.severidad for a in comun}
    sev_riesgo = {a.codigo: a.severidad for a in riesgo}
    assert sev["JURISDICCION_NO_DECLARADA"] == "MEDIA"
    assert sev_riesgo["JURISDICCION_NO_DECLARADA"] == "ALTA"


def test_el_pais_declarado_en_el_perfil_no_alerta():
    perfil = Perfil("X1", monto_mensual=50_000_000, operaciones_mensuales=20,
                    paises=("AR", "UY"))
    ops = [op(i * 5, 1_000_000, pais="Uruguay") for i in range(4)]
    assert "JURISDICCION_NO_DECLARADA" not in codigos(correr(ops, perfil))


def test_el_pais_local_no_alerta():
    perfil = Perfil("X1", monto_mensual=50_000_000, operaciones_mensuales=20, paises=())
    ops = [op(i * 5, 1_000_000, pais="Argentina") for i in range(4)]
    assert "JURISDICCION_NO_DECLARADA" not in codigos(correr(ops, perfil))


# --- perfil ausente y recalibracion ----------------------------------------

def test_operar_sin_perfil_declarado_es_una_alerta():
    ops = [op(i * 10, 3_000_000) for i in range(5)]
    assert "SIN_PERFIL" in codigos(correr(ops))


def test_una_operacion_aislada_no_exige_perfil():
    assert "SIN_PERFIL" not in codigos(correr([op(0, 500_000)]))


def test_la_recalibracion_se_sugiere_y_no_se_aplica():
    """Ajustar el perfil solo haria desaparecer el desvio justo cuando importa."""
    perfil = Perfil("X1", monto_mensual=1_000_000, operaciones_mensuales=4)
    operatoria = Operatoria("X1", [op(i * 3, 8_000_000) for i in range(6)])

    sugerido = recalibracion_sugerida(operatoria, perfil)
    assert sugerido is not None
    assert sugerido.monto_mensual > perfil.monto_mensual
    assert perfil.monto_mensual == 1_000_000  # el original no se toco


def test_sin_desvio_no_hay_recalibracion_que_sugerir():
    perfil = Perfil("X1", monto_mensual=50_000_000, operaciones_mensuales=20)
    operatoria = Operatoria("X1", [op(i * 6, 500_000) for i in range(6)])
    assert recalibracion_sugerida(operatoria, perfil) is None


# --- catalogo --------------------------------------------------------------

def test_las_reglas_son_datos_no_ramas_del_motor():
    """Agregar una tipologia es agregar una entrada, no tocar el motor."""
    assert len(CATALOGO) >= 7
    assert all(callable(r.evaluar) for r in CATALOGO)
    assert len({r.codigo for r in CATALOGO}) == len(CATALOGO)


def test_una_regla_apagada_no_corre_pero_explica_por_que():
    apagadas = reglas_inactivas()
    assert apagadas
    assert all(r.motivo_inactiva for r in apagadas)
    assert "MONTOS_REDONDOS" in {r.codigo for r in apagadas}


def test_los_montos_redondos_no_disparan_estando_apagada():
    ops = [op(i * 4, 500_000) for i in range(12)]
    assert "MONTOS_REDONDOS" not in codigos(correr(ops))


def test_la_alerta_trae_el_contenido_minimo_del_registro():
    """Los manuales fijan que debe contener el registro de inusuales."""
    perfil = Perfil("X1", monto_mensual=1_000_000, operaciones_mensuales=4)
    alerta = [a for a in correr([op(i * 3, 8_000_000) for i in range(6)], perfil)][0]
    fila = alerta.como_fila(nivel_riesgo="ALTO", perfil="$1.000.000/mes")

    for campo in ("nivel_riesgo", "perfil", "operaciones", "metodologia",
                  "generada", "tipo_inusualidad", "vence"):
        assert fila[campo] != "", campo
    # Las dos que resuelve el analista salen vacias a proposito.
    assert fila["medidas_adoptadas"] == ""
    assert fila["decision_final"] == ""


def test_el_plazo_corre_desde_la_operacion_y_no_desde_la_deteccion():
    """Detectar tarde no regala plazo.

    El tope de 90 dias corre desde que la operacion fue realizada. Si se
    detecta pasado ese plazo, la ventana de reporte ya esta cerrada y el
    sistema tiene que decirlo en vez de mostrar noventa dias por delante.
    """
    alerta = correr([op(i, 28_000_000) for i in range(5)])[0]
    assert alerta.fecha_operacion == INICIO
    assert alerta.vence <= INICIO + timedelta(days=90)


def test_una_alerta_detectada_tarde_figura_como_vencida():
    alerta = correr([op(i, 28_000_000) for i in range(5)])[0]
    # Los fixtures son de marzo y la corrida es posterior a junio.
    assert alerta.vencida
    assert alerta.dias_restantes < 0


# --- circuito --------------------------------------------------------------

def test_una_alerta_reabre_un_legajo_cerrado():
    """La debida diligencia continuada alcanza a todos, no solo al riesgo alto."""
    caso = Caso(caso_id="C1", cliente=Cliente(cliente_id="X1", nombre="Test"))
    for destino in (Estado.SCREENING, Estado.SCORING, Estado.CERRADO):
        caso.transicionar(destino, "test", "avance")
    assert caso.estado is Estado.CERRADO

    caso.transicionar(Estado.ANALISIS, "monitoreo", "alerta (reapertura del legajo)")
    assert caso.estado is Estado.ANALISIS


def test_agrupar_reparte_las_operaciones_por_cliente():
    ops = [op(0, 100, cid="A"), op(1, 200, cid="B"), op(2, 300, cid="A")]
    agrupadas = agrupar(ops)
    assert set(agrupadas) == {"A", "B"}
    assert agrupadas["A"].cantidad == 2
    assert agrupadas["A"].total == 400
