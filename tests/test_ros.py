"""Pruebas del armado de ROS y del registro de inusuales.

Lo que se verifica es la frontera: que el sistema arme todo lo que puede
armar, y que no arme lo que decide una persona. Un borrador que se presenta
solo, con una conclusion que nadie escribio, es peor que no tener borrador.
"""

from __future__ import annotations

from datetime import date

import pytest

from legajo.alertas import Alerta
from legajo.modelo import Cliente, Documento
from legajo.operaciones import Operacion, Perfil
from legajo.regimen import Regimen
from legajo.ros import BorradorROS, Decision, Resolucion, armar

OPERACION = date(2026, 7, 13)
HOY = date(2026, 7, 20)


def alerta(codigo="FRACCIONAMIENTO", cliente="X1", monto=70_000_000.0, fecha=OPERACION):
    return Alerta(
        cliente_id=cliente, codigo=codigo, severidad="ALTA",
        descripcion=f"{codigo} detectado", metodologia="ventana deslizante",
        operaciones=(Operacion(cliente, fecha, monto, instrumento="EFECTIVO"),),
        monto_involucrado=monto, generada=HOY,
    )


def cliente(cliente_id="X1", tipo="PERSONA", con_documento=True):
    return Cliente(
        cliente_id=cliente_id, nombre="Cliente de prueba", tipo=tipo,
        documentos=[Documento("DNI", "28456123")] if con_documento else [],
        nacionalidad="ARGENTINA", pais_residencia="ARGENTINA", actividad="Comercio",
    )


def decision(resolucion=Resolucion.REPORTAR, medidas="Se pidio documentacion.",
             motivo="No justifico el origen.", fecha=HOY, alerta_id="abc123"):
    return Decision(alerta_id=alerta_id, cliente_id="X1",
                    codigo_alerta="FRACCIONAMIENTO", resolucion=resolucion,
                    medidas=medidas, motivo=motivo, fecha=fecha)


def perfil():
    return Perfil("X1", monto_mensual=900_000, operaciones_mensuales=4,
                  proporcion_efectivo=0.10, paises=("AR",),
                  origen_fondos="Sueldo en relacion de dependencia",
                  proposito="Caja de ahorro")


def borrador(**kw):
    base = dict(cliente=cliente(), regimen=Regimen.LA, nivel_riesgo="ALTO",
                alertas=[alerta()], decision=decision(), perfil=perfil())
    base.update(kw)
    return BorradorROS(**base)


# --- identidad de la alerta ------------------------------------------------

def test_la_alerta_tiene_identidad_estable():
    """El circuito se vuelve a correr entre exportar y leer las decisiones."""
    a = alerta()
    b = alerta()
    assert a.identificador == b.identificador


def test_la_identidad_distingue_alertas_de_la_misma_tipologia():
    """La clave (cliente, codigo) no alcanza: la tipologia dispara varias veces."""
    a = alerta(monto=70_000_000)
    b = alerta(monto=40_000_000)
    assert a.codigo == b.codigo and a.cliente_id == b.cliente_id
    assert a.identificador != b.identificador


def test_la_identidad_no_depende_de_la_redaccion():
    a = alerta()
    b = Alerta(a.cliente_id, a.codigo, a.severidad, "otra descripcion",
               "otra metodologia", a.operaciones, a.monto_involucrado, a.generada)
    assert a.identificador == b.identificador


# --- la frontera con el criterio humano ------------------------------------

def test_sin_conclusion_del_analista_el_borrador_esta_incompleto():
    """La conversion de inusual a sospechosa no se automatiza."""
    b = borrador(decision=decision(motivo=""))
    assert not b.completo
    assert "decision final motivada" in b.faltantes()


def test_sin_medidas_tampoco_esta_completo():
    """Un motivo sin medidas es una decision sin analisis detras."""
    b = borrador(decision=decision(medidas=""))
    assert not b.completo


def test_el_fundamento_marca_lo_que_falta_en_vez_de_rellenarlo():
    b = borrador(decision=decision(motivo=""))
    texto = b.fundamento()
    assert "[PENDIENTE" in texto
    assert "no se justifico" in texto


def test_con_la_conclusion_cargada_el_borrador_es_presentable():
    assert borrador().completo


# --- contenido del fundamento ----------------------------------------------

def test_el_fundamento_describe_la_inusualidad_con_su_metodologia():
    texto = borrador().fundamento()
    assert "INUSUALIDADES DETECTADAS" in texto
    assert "FRACCIONAMIENTO" in texto
    assert "Metodologia" in texto


def test_el_fundamento_contrasta_contra_el_perfil_declarado():
    texto = borrador().fundamento()
    assert "PERFIL TRANSACCIONAL DECLARADO" in texto
    assert "Sueldo en relacion de dependencia" in texto


def test_sin_perfil_el_fundamento_lo_dice():
    texto = borrador(perfil=None).fundamento()
    assert "no tiene perfil transaccional declarado" in texto


def test_el_fundamento_incluye_las_medidas_y_la_conclusion():
    texto = borrador().fundamento()
    assert "MEDIDAS ADOPTADAS" in texto
    assert "Se pidio documentacion." in texto
    assert "FUNDAMENTO DE LA SOSPECHA" in texto
    assert "No justifico el origen." in texto


# --- plazo ------------------------------------------------------------------

def test_un_borrador_fuera_de_plazo_lo_deja_asentado():
    """La demora tiene su propia sancion y hay que explicarla."""
    vieja = alerta(fecha=date(2026, 1, 1))
    b = borrador(alertas=[vieja])
    assert b.fuera_de_plazo
    assert "CONSTANCIA DE DEMORA" in b.fundamento()


def test_dentro_de_plazo_no_hay_constancia_de_demora():
    assert "CONSTANCIA DE DEMORA" not in borrador().fundamento()


# --- datos que exige la norma -----------------------------------------------

def test_un_cliente_sin_documento_no_se_puede_reportar():
    b = borrador(cliente=cliente(con_documento=False))
    assert "identificacion del cliente sin documento" in b.faltantes()


def test_una_persona_juridica_sin_beneficiario_final_no_se_puede_reportar():
    b = borrador(cliente=cliente(tipo="ENTIDAD"), beneficiarios=[])
    assert "beneficiario final no identificado" in b.faltantes()


# --- observaciones ----------------------------------------------------------

def test_reportar_a_un_cliente_de_riesgo_bajo_es_una_inconsistencia():
    """Es lo primero que encuentra una inspeccion."""
    b = borrador(nivel_riesgo="BAJO")
    assert b.completo  # no impide presentar
    assert any("riesgo bajo" in o for o in b.observaciones())


def test_un_cliente_de_riesgo_alto_no_genera_esa_observacion():
    assert not any("riesgo bajo" in o for o in borrador().observaciones())


# --- separacion de resoluciones ---------------------------------------------

def contexto(alertas, decisiones):
    clientes = {"X1": cliente()}
    return armar(alertas, decisiones, clientes, {}, {"X1": perfil()}, {}, {})


def test_las_reportadas_van_a_borrador_y_las_justificadas_al_registro():
    a1, a2 = alerta("FRACCIONAMIENTO"), alerta("DESVIO_PERFIL", monto=30_000_000)
    r = contexto(
        {"X1": [a1, a2]},
        {a1.identificador: decision(alerta_id=a1.identificador),
         a2.identificador: decision(Resolucion.JUSTIFICADA, alerta_id=a2.identificador)},
    )
    assert len(r.borradores) == 1
    assert len(r.justificadas) == 1


def test_varias_alertas_del_mismo_cliente_y_regimen_son_un_solo_ros():
    """Un ROS cubre la operatoria del cliente, no una alerta por reporte."""
    a1, a2 = alerta("FRACCIONAMIENTO"), alerta("EFECTIVO_DESPROPORCIONADO", monto=50_000_000)
    r = contexto(
        {"X1": [a1, a2]},
        {a1.identificador: decision(alerta_id=a1.identificador),
         a2.identificador: decision(alerta_id=a2.identificador)},
    )
    assert len(r.borradores) == 1
    assert len(r.borradores[0].alertas) == 2


def test_una_alerta_sin_decision_queda_pendiente():
    a = alerta()
    r = contexto({"X1": [a]}, {})
    assert r.pendientes and not r.borradores and not r.justificadas


def test_una_resolucion_pendiente_no_se_toma_como_justificada():
    """Cerrar por omision seria exactamente lo contrario de documentar."""
    a = alerta()
    r = contexto({"X1": [a]},
                 {a.identificador: decision(Resolucion.PENDIENTE, alerta_id=a.identificador)})
    assert r.pendientes and not r.justificadas


# --- registro de inusuales --------------------------------------------------

def test_una_justificada_sin_analisis_documentado_se_marca():
    """Sin medidas ni motivo no se distingue de una alerta que nadie miro."""
    a = alerta()
    r = contexto({"X1": [a]}, {a.identificador: Decision(
        alerta_id=a.identificador, cliente_id="X1", codigo_alerta=a.codigo,
        resolucion=Resolucion.JUSTIFICADA, medidas="", motivo="", fecha=None,
    )})
    assert r.justificadas and not r.justificadas[0].documentada
    assert r.sin_documentar


def test_una_justificada_con_analisis_no_aparece_como_hallazgo():
    a = alerta()
    r = contexto({"X1": [a]},
                 {a.identificador: decision(Resolucion.JUSTIFICADA, alerta_id=a.identificador)})
    assert r.justificadas[0].documentada
    assert not r.sin_documentar


def test_sin_hallazgos_el_resultado_queda_vacio():
    r = contexto({}, {})
    assert not r.borradores and not r.justificadas and not r.pendientes
