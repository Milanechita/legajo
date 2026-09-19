"""Pruebas del parser de RePET contra el export real del registro.

Los fixtures de ejemplos/listas son el export de septiembre de 2026, 718
registros. No son datos sinteticos: por eso estas pruebas verifican tambien
las caracteristicas del origen, que es lo que hay que conocer antes de
confiar en la lista.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

from legajo.fuentes.repet import COMITES_ONU, ParserRePET, origen

FIXTURES = Path(__file__).resolve().parent.parent / "ejemplos" / "listas"


@pytest.fixture(scope="module")
def designados():
    parser = ParserRePET()
    todos = []
    for archivo in ("repet_personas.json", "repet_entidades.json"):
        d, _ = parser.parsear((FIXTURES / archivo).read_bytes())
        todos += d
    return todos


def test_parsea_el_export_completo(designados):
    assert len(designados) == 718


def test_un_tercio_del_registro_es_de_origen_local(designados):
    """RePET NO es una copia de la lista de la ONU.

    Se suele suponer que si, y por eso se omite el cotejo. Los datos lo
    desmienten: casi 250 designaciones vienen de la UIF, INTERPOL, la causa
    AMIA y PROCELAC, y no figuran en ninguna otra lista del mundo.
    """
    conteo = Counter(d.programas[0] for d in designados if d.programas)
    assert conteo["ONU"] == 469
    assert conteo["LOCAL"] == 249
    assert conteo["LOCAL"] / len(designados) > 0.30


def test_clasificacion_de_origen():
    assert origen("Al-Qaida") == "ONU"
    assert origen("Taliban") == "ONU"
    assert origen("Unidad de Información Financiera") == "LOCAL"
    assert origen("Notificación Roja de INTERPOL") == "LOCAL"
    assert origen("UFI AMIA") == "LOCAL"
    assert origen("") == "LOCAL"


def test_los_comites_de_la_onu_estan_declarados():
    assert "AL-QAIDA" in COMITES_ONU
    assert "TALIBAN" in COMITES_ONU


def test_separa_personas_de_entidades(designados):
    conteo = Counter(d.tipo for d in designados)
    assert conteo["PERSONA"] == 607
    assert conteo["ENTIDAD"] == 111


def test_arma_el_nombre_desde_los_cuatro_campos(designados):
    """El registro parte el nombre en FIRST, SECOND, THIRD y FOURTH_NAME."""
    con_varios = [d for d in designados if len(d.nombre.split()) >= 3]
    assert con_varios
    assert all("  " not in d.nombre for d in designados)


def test_rescata_alias_documentos_y_nacionalidades(designados):
    assert sum(1 for d in designados if d.alias) > 400
    assert sum(1 for d in designados if d.documentos) > 100
    assert sum(1 for d in designados if d.nacionalidades) > 300


def test_los_documentos_quedan_en_forma_canonica(designados):
    docs = [x for d in designados for x in d.documentos]
    assert docs
    assert all(":" in x for x in docs)
    assert any(x.startswith("PASAPORTE:") for x in docs)


def test_la_version_registra_fecha_y_hash(designados):
    parser = ParserRePET()
    contenido = (FIXTURES / "repet_personas.json").read_bytes()
    _, version = parser.parsear(contenido)
    assert version.lista == "REPET"
    assert version.publicada is not None
    assert len(version.sha256) == 64


def test_excluye_las_bajas():
    """Cotejar contra una persona dada de baja es un falso positivo."""
    import json

    crudo = json.dumps([
        {"DATAID": "1", "FIRST_NAME": "Vigente", "UN_LIST_TYPE": "Al-Qaida",
         "DELISTED_ON": "", "INDIVIDUAL_ALIAS": []},
        {"DATAID": "2", "FIRST_NAME": "Dado de baja", "UN_LIST_TYPE": "Al-Qaida",
         "DELISTED_ON": "12/03/2024", "INDIVIDUAL_ALIAS": []},
    ]).encode("utf-8")

    designados, _ = ParserRePET().parsear(crudo)
    assert [d.nombre for d in designados] == ["Vigente"]
