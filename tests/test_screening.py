"""Pruebas del motor de screening.

Los casos estan escritos como escenarios de dominio, no como pruebas de
funciones sueltas: lo que hay que garantizar es que el sistema no deje pasar
un designado y no ahogue al analista en ruido.
"""

from __future__ import annotations

import pytest

from legajo.config import Politica
from legajo.fuentes.base import Designado, Padron, VersionLista
from legajo.matcher import jaro_winkler, score_nombres
from legajo.modelo import Caso, Cliente, Documento, Estado, TransicionInvalida
from legajo.normalizar import normalizar
from legajo.screening import cotejar_cliente, screenear

from datetime import date


def padron_de(*designados: Designado) -> Padron:
    p = Padron()
    p.incorporar(
        list(designados),
        VersionLista(lista="TEST", publicada=None, descargada=date.today(),
                     registros=len(designados), sha256="0" * 64),
    )
    return p


# --- normalizacion ---------------------------------------------------------

def test_acentos_no_impiden_coincidencia():
    assert normalizar("Pérez") == normalizar("PEREZ")


def test_sufijo_societario_se_descarta_solo_en_entidades():
    assert normalizar("Acme S.A.", es_entidad=True) == "ACME"
    # En personas no se toca: un apellido puede coincidir con un sufijo.
    assert "CO" in normalizar("Juan Co", es_entidad=False)


def test_nombre_que_es_solo_sufijo_no_queda_vacio():
    # Preferimos un match ruidoso a perder la entidad del padron.
    assert normalizar("Holding Group", es_entidad=True) != ""


# --- matcher ---------------------------------------------------------------

def test_jaro_winkler_identico_es_uno():
    assert jaro_winkler("PEREZ", "PEREZ") == 1.0


def test_orden_de_tokens_es_irrelevante():
    # Las listas alternan apellido-nombre y nombre-apellido.
    assert score_nombres("JUAN PEREZ", "PEREZ JUAN") == 100.0


def test_nombre_incompleto_puntua_alto():
    # El padron rara vez trae el nombre completo de la lista.
    assert score_nombres("Juan Perez", "Juan Carlos Perez Gomez") >= 78.0


def test_nombres_distintos_puntuan_bajo():
    assert score_nombres("Maria Gonzalez", "Khalid Sheikh Mohammed") < 60.0


def test_transliteracion_alternativa_se_detecta():
    assert score_nombres("Khaled Shaikh Mohamed", "Khalid Sheikh Mohammed") >= 85.0


# --- cotejo ----------------------------------------------------------------

def test_documento_exacto_no_pasa_por_el_motor_difuso():
    """Un pasaporte identico es coincidencia, aunque el nombre no se parezca."""
    cliente = Cliente(
        cliente_id="X1",
        nombre="Nombre Totalmente Distinto",
        documentos=[Documento("PASAPORTE", "K123-4567")],
    )
    padron = padron_de(Designado(
        lista="TEST", id_origen="1", nombre="Ali Reza Abbas",
        documentos=("PASAPORTE:K1234567",),
    ))

    hits = cotejar_cliente(cliente, padron)
    assert len(hits) == 1
    assert hits[0].criterio == "DOCUMENTO"
    assert hits[0].score == 100.0


def test_nombre_comun_no_genera_falso_positivo():
    cliente = Cliente(cliente_id="X2", nombre="Maria Gonzalez")
    padron = padron_de(Designado(lista="TEST", id_origen="1",
                                 nombre="Khalid Sheikh Mohammed"))
    assert cotejar_cliente(cliente, padron) == []


def test_alias_produce_coincidencia():
    cliente = Cliente(cliente_id="X3", nombre="Alireza Abbas")
    padron = padron_de(Designado(
        lista="TEST", id_origen="1", nombre="ABBAS, Ali Reza",
        alias=("ABAS, Ali R.", "Alireza Abbas"),
    ))
    hits = cotejar_cliente(cliente, padron)
    assert hits and hits[0].score == 100.0


def test_atenuante_resta_pero_no_descarta():
    """Nacionalidad discordante baja el puntaje; no elimina la coincidencia.

    Las listas tienen datos secundarios incompletos y contradictorios. Un
    descarte automatico seria un falso negativo introducido por el sistema.
    """
    cliente = Cliente(cliente_id="X4", nombre="Carlos Alberto Gomez Rivera",
                      nacionalidad="ARGENTINA")
    padron = padron_de(Designado(
        lista="TEST", id_origen="1", nombre="GOMEZ RIVERA, Carlos Alberto",
        nacionalidades=("Colombia",),
    ))
    hits = cotejar_cliente(cliente, padron)
    assert hits
    assert hits[0].atenuantes
    assert hits[0].score < 100.0


def test_dato_ausente_no_penaliza():
    """Si el cliente o la lista no tienen el dato, no se castiga."""
    cliente = Cliente(cliente_id="X5", nombre="Ali Reza Abbas")  # sin nacionalidad
    padron = padron_de(Designado(lista="TEST", id_origen="1", nombre="Ali Reza Abbas",
                                 nacionalidades=("Iran",)))
    hits = cotejar_cliente(cliente, padron)
    assert hits[0].score == 100.0
    assert hits[0].atenuantes == ()


def test_umbral_es_politica_no_mecanismo():
    """Subir el umbral filtra sin tocar el motor."""
    cliente = Cliente(cliente_id="X6", nombre="Juan Perez")
    padron = padron_de(Designado(lista="TEST", id_origen="1",
                                 nombre="Juan Carlos Perez Gomez"))
    assert cotejar_cliente(cliente, padron, Politica(umbral_revision=70.0))
    assert not cotejar_cliente(cliente, padron, Politica(umbral_revision=99.0))


# --- circuito --------------------------------------------------------------

def test_coincidencia_en_lista_critica_escala():
    caso = Caso(caso_id="C1", cliente=Cliente(cliente_id="X7", nombre="Ali Reza Abbas"))
    padron = padron_de(Designado(lista="OFAC_SDN", id_origen="1", nombre="Ali Reza Abbas"))
    screenear([caso], padron)
    assert caso.estado is Estado.ESCALADO


def test_sin_coincidencias_avanza_a_scoring():
    caso = Caso(caso_id="C2", cliente=Cliente(cliente_id="X8", nombre="Ana Rodriguez"))
    padron = padron_de(Designado(lista="OFAC_SDN", id_origen="1",
                                 nombre="Khalid Sheikh Mohammed"))
    screenear([caso], padron)
    assert caso.estado is Estado.SCORING


def test_transicion_invalida_se_rechaza():
    caso = Caso(caso_id="C3", cliente=Cliente(cliente_id="X9", nombre="Test"))
    with pytest.raises(TransicionInvalida):
        caso.transicionar(Estado.CERRADO, "test", "salto ilegal desde ALTA")


def test_estado_solo_cambia_dejando_rastro():
    caso = Caso(caso_id="C4", cliente=Cliente(cliente_id="X10", nombre="Test"))
    caso.transicionar(Estado.SCREENING, "tester", "motivo")
    transiciones = [e for e in caso.evidencia if e.accion == "TRANSICION"]
    assert len(transiciones) == 1
    assert transiciones[0].detalle["motivo"] == "motivo"


def test_expediente_registra_procedencia_de_listas():
    """Sin version de lista, el registro de screening no es oponible."""
    caso = Caso(caso_id="C5", cliente=Cliente(cliente_id="X11", nombre="Test"))
    padron = padron_de(Designado(lista="TEST", id_origen="1", nombre="Otro"))
    screenear([caso], padron)
    ejecucion = next(e for e in caso.evidencia if e.accion == "SCREENING_EJECUTADO")
    assert ejecucion.detalle["listas"]
    assert "sha256" in ejecucion.detalle["listas"][0]


def test_evidencia_es_append_only():
    caso = Caso(caso_id="C6", cliente=Cliente(cliente_id="X12", nombre="Test"))
    caso.registrar("a", "UNO")
    caso.registrar("b", "DOS")
    assert [e.accion for e in caso.evidencia] == ["UNO", "DOS"]
    # Las entradas son inmutables.
    with pytest.raises(Exception):
        caso.evidencia[0].accion = "MODIFICADO"
