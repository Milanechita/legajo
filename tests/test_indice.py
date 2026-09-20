"""Pruebas del score bidireccional y del indice invertido.

Las dos cosas se probaron juntas porque salieron del mismo trabajo: el
defecto del matcher aparecio construyendo el indice y preguntandose por que
los dos no devolvian lo mismo.

La propiedad que importa del indice es una sola: descarta trabajo, no
coincidencias. Cualquier ganancia de velocidad que cueste un falso negativo
esta mal hecha.
"""

from __future__ import annotations

import random
from datetime import date

import pytest

from legajo.config import POLITICA_POR_DEFECTO
from legajo.fuentes.base import Designado, Padron, VersionLista
from legajo.indice import Indice, MINIMO_TRIGRAMAS, trigramas
from legajo.matcher import PESO_COBERTURA_CORTA, score_nombres
from legajo.modelo import Cliente, Documento
from legajo.screening import cotejar_cliente

UMBRAL = POLITICA_POR_DEFECTO.umbral_revision


# --- el defecto que se arreglo ---------------------------------------------

def test_un_designado_de_una_palabra_no_matchea_cualquier_nombre():
    """El caso que aparecio midiendo, no leyendo codigo.

    Antes daba 79.2 y cruzaba el umbral de revision.
    """
    assert score_nombres("Ana Rodriguez Diaz", "Ajnad") < UMBRAL


@pytest.mark.parametrize("nombre", [
    "Juan Perez Gomez", "Maria Lopez Fernandez", "Carlos Martinez Sanchez",
    "Laura Benitez Acosta", "Diego Romero Torres",
])
def test_nombres_comunes_no_matchean_organizaciones_cortas(nombre):
    for designado in ("Ajnad", "Hamas", "KOMID", "Faiz"):
        assert score_nombres(nombre, designado) < UMBRAL, f"{nombre} vs {designado}"


def test_la_cobertura_se_mide_en_las_dos_direcciones():
    """Medir solo el lado corto es lo que producia los falsos positivos.

    "Ajnad" queda bien explicado por "Ana"; "Ana Rodriguez Diaz" queda
    explicado en un tercio por "Ajnad". La segunda mitad de la evidencia es
    la que decide.
    """
    assert 0.5 <= PESO_COBERTURA_CORTA <= 0.65


# --- lo que tenia que seguir funcionando ------------------------------------

@pytest.mark.parametrize("consulta,candidato,minimo", [
    ("Juan Perez", "Juan Carlos Perez Gomez", UMBRAL),
    ("Juan Perez", "Juan Carlos Alberto Perez Gomez Garcia", UMBRAL),
    ("Khaled Shaikh Mohamed", "Khalid Sheikh Mohammed", 85.0),
    ("Alireza Abbas", "ABBAS, Ali Reza", 85.0),
])
def test_los_casos_legitimos_sobreviven(consulta, candidato, minimo):
    assert score_nombres(consulta, candidato) >= minimo


def test_el_orden_de_los_tokens_sigue_siendo_irrelevante():
    assert score_nombres("JUAN PEREZ", "PEREZ JUAN") == 100.0


def test_las_entidades_siguen_ignorando_el_sufijo_societario():
    assert score_nombres("Acme S.A.", "ACME", es_entidad=True) == 100.0
    assert score_nombres("Eastern Trading Co", "EASTERN TRADING LIMITED",
                         es_entidad=True) == 100.0


# --- trigramas --------------------------------------------------------------

def test_los_trigramas_llevan_relleno_en_los_bordes():
    """El principio y el final del token son lo mas discriminante."""
    g = trigramas("ALI")
    assert "  A" in g and "LI " in g


def test_un_texto_vacio_no_genera_trigramas():
    assert trigramas("") == set()


# --- indice -----------------------------------------------------------------

def padron_de_prueba() -> Padron:
    padron = Padron()
    designados = [
        Designado(lista="TEST", id_origen="1", nombre="Khalid Sheikh Mohammed",
                  tipo="PERSONA", alias=("Khaled Shaikh Mohamed",),
                  documentos=("PASAPORTE:AB123456",)),
        Designado(lista="TEST", id_origen="2", nombre="Ajnad", tipo="ENTIDAD"),
        Designado(lista="TEST", id_origen="3", nombre="Eastern Trading Limited",
                  tipo="ENTIDAD"),
        Designado(lista="TEST", id_origen="4", nombre="Ali Reza Abbas",
                  tipo="PERSONA", documentos=("PASAPORTE:K1234567",)),
        Designado(lista="TEST", id_origen="5", nombre="Emraan Ali", tipo="PERSONA"),
    ]
    padron.incorporar(designados, VersionLista(
        lista="TEST", publicada=None, descargada=date(2026, 9, 1),
        registros=len(designados), sha256="0" * 64,
    ))
    return padron


def test_el_indice_se_construye_sobre_los_dos_caminos():
    idx = Indice(padron_de_prueba())
    assert idx.trigramas_indexados > 0
    assert idx.documentos_indexados == 2


def test_el_minimo_de_trigramas_es_uno_y_es_deliberado():
    """Con dos filtra mas pero pierde: RAHMAN contra EMRAAN comparte uno."""
    assert MINIMO_TRIGRAMAS == 1


def test_una_coincidencia_por_documento_entra_aunque_el_nombre_no_se_parezca():
    """El camino del documento no puede pasar por el indice de nombres."""
    padron = padron_de_prueba()
    idx = Indice(padron)
    cliente = Cliente(cliente_id="X1", nombre="Nombre Totalmente Distinto",
                      documentos=[Documento("PASAPORTE", "K1234567")])

    assert any(d.id_origen == "4" for d in idx.candidatos(cliente))
    hits = cotejar_cliente(cliente, padron, POLITICA_POR_DEFECTO, idx)
    assert hits and hits[0].criterio == "DOCUMENTO"


def test_el_indice_descarta_trabajo_no_coincidencias():
    """La propiedad que importa: equivalencia con la busqueda exhaustiva."""
    padron = padron_de_prueba()
    idx = Indice(padron)

    random.seed(3)
    nombres = ["Juan Perez", "Khaled Shaikh Mohamed", "Ana Rodriguez Diaz",
               "Eastern Trading Co", "Ali Reza Abbas", "Maria Gomez Lopez",
               "Emraan Ali", "Rahman Aziz Perez", "Carlos Martinez"]

    for nombre in nombres:
        cliente = Cliente(cliente_id="X1", nombre=nombre)
        exhaustivo = {(h.id_origen, h.criterio)
                      for h in cotejar_cliente(cliente, padron, POLITICA_POR_DEFECTO)}
        indexado = {(h.id_origen, h.criterio)
                    for h in cotejar_cliente(cliente, padron, POLITICA_POR_DEFECTO, idx)}
        assert exhaustivo == indexado, nombre


def test_la_selectividad_es_medible():
    """Sirve para saber si el indice esta trabajando o solo estorbando."""
    idx = Indice(padron_de_prueba())
    cliente = Cliente(cliente_id="X1", nombre="Zzz Yyy Www")
    assert 0.0 <= idx.selectividad(cliente) <= 1.0


def test_un_padron_vacio_no_rompe_el_indice():
    idx = Indice(Padron())
    cliente = Cliente(cliente_id="X1", nombre="Juan Perez")
    assert idx.candidatos(cliente) == []
    assert idx.selectividad(cliente) == 0.0
