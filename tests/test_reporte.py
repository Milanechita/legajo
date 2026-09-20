"""Pruebas de regimen de reporte, congelamiento y exposicion sancionatoria.

Lo que se verifica aca son plazos con sancion. Un error en esta parte no
produce ruido ni falsos positivos: produce un reporte fuera de termino, que
segun la Res. UIF 129/2024 se liquida por una vez el valor total de la
operacion.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from legajo.alertas import Alerta
from legajo.config import UMBRALES, umbral_reporte_vigente, SMVM
from legajo.congelamiento import PASOS, obligaciones
from legajo.operaciones import Operacion
from legajo.regimen import (
    PLAZOS, Regimen, regimen_de_alerta, regimen_de_coincidencia, vencimiento,
)
from legajo.sanciones import (
    MODULO, Exposicion, cargo_por_incumplimiento, cargo_por_no_reportar,
    estimar, pesos,
)
from legajo.screening import Coincidencia


def coincidencia(**kw) -> Coincidencia:
    base = dict(cliente_id="X1", lista="OFAC_SDN", id_origen="1",
                nombre_designado="Designado", nombre_matcheado="Designado",
                score=100.0, criterio="NOMBRE", programas=())
    base.update(kw)
    return Coincidencia(**base)


# --- umbral de reporte ----------------------------------------------------

def test_el_umbral_de_reporte_sale_de_la_norma_no_de_un_numero_inventado():
    """40 SMVM, Res. UIF 78/2025 art. 7, que lo subio desde 20."""
    assert UMBRALES.reporte_efectivo == 40.0
    assert umbral_reporte_vigente() == 40.0 * SMVM


def test_los_umbrales_se_recalculan_al_cambiar_el_salario():
    antes = UMBRALES.en_pesos("reporte_efectivo")
    assert antes == pytest.approx(40.0 * SMVM)


# --- regimen ---------------------------------------------------------------

def test_los_tres_regimenes_tienen_plazos_distintos():
    assert PLAZOS[Regimen.LA].dias_tope_desde_operacion == 90
    assert PLAZOS[Regimen.FT].dias_tope_desde_operacion is None
    assert PLAZOS[Regimen.FPADM].dias_tope_desde_operacion is None


def test_terrorismo_y_proliferacion_son_urgentes_y_lavado_no():
    assert PLAZOS[Regimen.FT].urgente
    assert PLAZOS[Regimen.FPADM].urgente
    assert not PLAZOS[Regimen.LA].urgente


def test_el_regimen_sale_del_comite_no_de_la_lista():
    """La Consolidada de la ONU mezcla terrorismo y proliferacion."""
    assert regimen_de_coincidencia("ONU_CONSOLIDADA", ("Al-Qaida",)) is Regimen.FT
    assert regimen_de_coincidencia("ONU_CONSOLIDADA", ("DPRK", "RES1718")) is Regimen.FPADM


def test_repet_es_terrorismo_por_el_decreto_que_lo_creo():
    assert regimen_de_coincidencia("REPET", ()) is Regimen.FT


def test_una_coincidencia_sin_designacion_especifica_es_lavado():
    assert regimen_de_coincidencia("OFAC_SDN", ("SDNTK",)) is Regimen.LA


def test_ninguna_tipologia_de_monitoreo_es_terrorismo_por_si_sola():
    """El regimen surge de las listas, no del comportamiento transaccional."""
    for codigo in ("FRACCIONAMIENTO", "DESVIO_PERFIL", "ACELERACION",
                   "EFECTIVO_DESPROPORCIONADO", "SIN_PERFIL"):
        assert regimen_de_alerta(codigo) is Regimen.LA


# --- plazos ----------------------------------------------------------------

def test_en_lavado_el_tope_corre_desde_la_operacion():
    operacion = date(2026, 3, 2)
    v = vencimiento(Regimen.LA, operacion, fecha_deteccion=date(2026, 3, 3))
    assert v.vence == date(2026, 3, 4)  # un dia desde la deteccion


def test_detectar_tarde_no_regala_plazo():
    """Un analisis que empieza el dia 89 tiene un dia, no noventa."""
    operacion = date(2026, 3, 2)
    v = vencimiento(Regimen.LA, operacion, fecha_deteccion=date(2026, 5, 29))
    assert v.vence == date(2026, 5, 30)


def test_el_tope_de_noventa_dias_es_absoluto():
    operacion = date(2026, 3, 2)
    v = vencimiento(Regimen.LA, operacion, fecha_deteccion=date(2026, 9, 19))
    assert v.vence == operacion + timedelta(days=90)
    assert v.vence < v.fecha_deteccion  # ya vencido


def test_terrorismo_vence_en_veinticuatro_horas_sin_tope():
    operacion = date(2026, 3, 2)
    v = vencimiento(Regimen.FT, operacion, fecha_deteccion=date(2026, 9, 19))
    assert v.vence == date(2026, 9, 20)
    assert v.urgente


def test_la_alerta_deriva_el_plazo_de_sus_operaciones():
    ops = (
        Operacion("X1", date(2026, 3, 10), 1000),
        Operacion("X1", date(2026, 3, 2), 1000),
    )
    a = Alerta("X1", "FRACCIONAMIENTO", "ALTA", "x", "y",
               operaciones=ops, generada=date(2026, 3, 15))
    # Se toma la mas antigua: tomar la reciente daria mas plazo del que hay.
    assert a.fecha_operacion == date(2026, 3, 2)
    assert a.regimen is Regimen.LA


def test_una_alerta_con_el_plazo_pasado_figura_vencida():
    ops = (Operacion("X1", date(2026, 1, 1), 1000),)
    a = Alerta("X1", "DESVIO_PERFIL", "ALTA", "x", "y",
               operaciones=ops, generada=date(2026, 9, 19))
    assert a.vencida
    assert a.dias_restantes < 0


# --- congelamiento ---------------------------------------------------------

def test_una_coincidencia_de_terrorismo_genera_congelamiento():
    c = coincidencia(programas=("Al-Qaida",))
    obs = obligaciones([c], {"X1": "Cliente"}, umbral_confirmacion=92.0)
    assert len(obs) == 1
    assert obs[0].regimen is Regimen.FT


def test_una_coincidencia_de_lavado_no_genera_congelamiento():
    """El congelamiento administrativo es para terrorismo y proliferacion."""
    c = coincidencia(programas=("SDNTK",))
    assert obligaciones([c], {"X1": "Cliente"}, umbral_confirmacion=92.0) == []


def test_una_coincidencia_debil_no_congela_los_bienes_de_nadie():
    """Inmovilizar inaudita parte a un homonimo es un dano que hay que explicar."""
    c = coincidencia(score=80.0, programas=("Al-Qaida",))
    assert obligaciones([c], {"X1": "Cliente"}, umbral_confirmacion=92.0) == []


def test_varias_coincidencias_del_mismo_regimen_son_una_sola_obligacion():
    """Se inmoviliza una vez y se reporta una vez."""
    cs = [
        coincidencia(lista="OFAC_SDN", id_origen="1", score=95.0, programas=("Al-Qaida",)),
        coincidencia(lista="REPET", id_origen="2", score=100.0, programas=("Al-Qaida",)),
        coincidencia(lista="ONU_CONSOLIDADA", id_origen="3", score=98.0, programas=("Al-Qaida",)),
    ]
    obs = obligaciones(cs, {"X1": "Cliente"}, umbral_confirmacion=92.0)
    assert len(obs) == 1
    assert obs[0].score == 100.0  # se queda con la mas firme


def test_dos_regimenes_distintos_son_dos_obligaciones():
    """El tipo de reporte cambia: no es lo mismo un ROS de FT que uno de FPADM."""
    cs = [
        coincidencia(lista="OFAC_SDN", programas=("Al-Qaida",)),
        coincidencia(lista="ONU_CONSOLIDADA", id_origen="2", programas=("RES1718",)),
    ]
    obs = obligaciones(cs, {"X1": "Cliente"}, umbral_confirmacion=92.0)
    assert {o.regimen for o in obs} == {Regimen.FT, Regimen.FPADM}


def test_los_pasos_salen_sin_cumplir():
    """Marcarlos de oficio seria documentar un cumplimiento que no ocurrio."""
    c = coincidencia(programas=("Al-Qaida",))
    obs = obligaciones([c], {"X1": "Cliente"}, umbral_confirmacion=92.0)[0]
    assert len(obs.pasos) == len(PASOS)
    assert not any(p.cumplido for p in obs.pasos)


def test_la_obligacion_de_reserva_esta_entre_los_pasos():
    """Informarle al cliente convierte el cumplimiento en un aviso."""
    codigos = {c for c, _ in PASOS}
    assert "RESERVA" in codigos
    c = coincidencia(programas=("Al-Qaida",))
    assert obligaciones([c], {"X1": "C"}, umbral_confirmacion=92.0)[0].confidencial


# --- exposicion ------------------------------------------------------------

def test_el_modulo_es_el_de_la_resolucion_vigente():
    assert MODULO == 54_140.0
    assert pesos(30) == 30 * 54_140.0


def test_no_reportar_cuesta_el_valor_entero_de_la_operacion():
    """Res. UIF 129/2024 art. 35 inc. 1. No es un porcentaje ni una multa fija."""
    cargo = cargo_por_no_reportar("Cliente", 137_000_000)
    assert cargo.monto == 137_000_000
    assert cargo.modulos is None


def test_incumplimiento_total_y_parcial_tienen_cargos_distintos():
    total = cargo_por_incumplimiento("Monitoreo", total=True)
    parcial = cargo_por_incumplimiento("Monitoreo", total=False)
    assert total.modulos == 30 and parcial.modulos == 25
    assert total.monto > parcial.monto


def test_la_exposicion_toma_el_mayor_monto_por_cliente_no_la_suma():
    """Las tipologias se superponen sobre las mismas operaciones."""
    ops = (Operacion("X1", date(2026, 3, 2), 1000),)
    alertas = {"X1": [
        Alerta("X1", "DESVIO_PERFIL", "ALTA", "a", "m", ops, 100_000_000),
        Alerta("X1", "FRACCIONAMIENTO", "ALTA", "b", "m", ops, 80_000_000),
    ]}
    e = estimar(alertas, [], {"X1": "Cliente"})
    assert e.por_falta_de_reporte == 100_000_000


def test_la_exposicion_separa_falta_de_reporte_de_otros_incumplimientos():
    ops = (Operacion("X1", date(2026, 3, 2), 1000),)
    alertas = {"X1": [Alerta("X1", "DESVIO_PERFIL", "ALTA", "a", "m", ops, 50_000_000)]}
    e = estimar(alertas, [], {"X1": "C"}, sin_perfil=["X2"], sin_beneficiario=["X3"])
    assert e.por_falta_de_reporte == 50_000_000
    assert e.por_incumplimientos == pesos(25) * 2
    assert e.total == e.por_falta_de_reporte + e.por_incumplimientos


def test_sin_hallazgos_la_exposicion_es_cero():
    e = estimar({}, [], {})
    assert e.total == 0
    assert e.cargos == []
