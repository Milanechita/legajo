"""Pruebas de las escalas del Regimen Simplificado.

La tabla esta completa, A a K. Igual se prueba la maquinaria que distingue
saber de no saber, porque en febrero de 2027 estos topes quedan viejos y
alguien va a cargar los nuevos. Si esa maquinaria se rompe sin que nadie se
entere, una tabla a medias va a responder como si estuviera completa.
"""

from __future__ import annotations

from datetime import date

import pytest

from legajo import monotributo


def test_las_escalas_cargadas_son_las_verificadas_contra_la_fuente():
    assert monotributo.tope_anual("A") == 12_009_410.45
    assert monotributo.tope_anual("E") == 36_028_231.33
    assert monotributo.tope_anual("K") == 126_610_838.75


def test_estan_las_once_categorias_del_regimen():
    assert monotributo.TABLA_COMPLETA
    assert monotributo.CATEGORIAS_FALTANTES == ()
    assert len(monotributo.TOPES_ANUALES) == 11


def test_los_topes_crecen_de_la_a_a_la_k():
    # Un tope fuera de orden haria que categoria_por_ingresos devuelva una
    # categoria mas baja de la que corresponde, y el cliente quedaria en regla
    # sin estarlo. Es el tipo de error que un dedo cambiado produce.
    topes = [monotributo.TOPES_ANUALES[c] for c in monotributo.CATEGORIAS]
    assert topes == sorted(topes)
    assert len(set(topes)) == len(topes)


def test_se_detecta_el_exceso_sobre_la_categoria_declarada():
    assert monotributo.excede("A", 12_009_411) is True
    assert monotributo.excede("A", 12_000_000) is False
    assert monotributo.excede("K", 126_610_839) is True


def test_la_categoria_se_deduce_del_nivel_de_ingresos():
    assert monotributo.categoria_por_ingresos(10_000_000) == "A"
    assert monotributo.categoria_por_ingresos(12_009_410.45) == "A"
    assert monotributo.categoria_por_ingresos(12_009_411) == "B"
    assert monotributo.categoria_por_ingresos(126_610_838.75) == "K"


def test_por_encima_del_tope_de_k_no_hay_categoria():
    # Arriba de K el contribuyente no puede estar en el regimen simplificado.
    # Devolver K seria decir que esta en la categoria mas alta, cuando lo que
    # pasa es que quedo afuera.
    assert monotributo.categoria_por_ingresos(200_000_000) is None


def test_la_escala_dice_hasta_cuando_vale():
    assert monotributo.vigente(date(2026, 9, 22))
    assert monotributo.vigente(date(2027, 1, 31))
    assert not monotributo.vigente(date(2027, 2, 1))
    assert not monotributo.vigente(date(2026, 7, 31))


# --- la maquinaria de "no se" --------------------------------------------

def test_una_categoria_que_no_esta_en_la_tabla_no_devuelve_cero(monkeypatch):
    # Cero se leeria como tope cero y cualquier ingreso lo excederia. None
    # obliga a que el que llama decida que hacer.
    monkeypatch.setattr(monotributo, "TOPES_ANUALES", {"A": 12_009_410.45})
    assert monotributo.tope_anual("D") is None
    assert monotributo.excede("D", 50_000_000) is None


def test_con_la_tabla_incompleta_no_se_deduce_la_categoria(monkeypatch):
    # Al faltar categorias intermedias, un cliente caeria en la ultima cargada
    # y quedaria con un tope que no le corresponde.
    monkeypatch.setattr(monotributo, "TOPES_ANUALES", {"A": 12_009_410.45})
    monkeypatch.setattr(monotributo, "TABLA_COMPLETA", False)
    assert monotributo.categoria_por_ingresos(20_000_000) is None


def test_el_estado_de_la_tabla_se_puede_mostrar_al_analista():
    texto = monotributo.estado_de_la_tabla()
    assert "11 categorias" in texto
    assert "2027-01-31" in texto
