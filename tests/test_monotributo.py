"""Pruebas de las escalas del Regimen Simplificado.

La tabla esta incompleta: estan A, B y K y faltan C a J. Lo que hay que
garantizar es que el programa no responda igual cuando sabe y cuando no sabe.
Un cero o un False ahi se leen como "el cliente esta en regla", que es
exactamente lo contrario de lo que pasa.
"""

from __future__ import annotations

from datetime import date

from legajo import monotributo


def test_las_escalas_cargadas_son_las_verificadas_contra_la_fuente():
    assert monotributo.tope_anual("A") == 12_009_410.45
    assert monotributo.tope_anual("B") == 17_595_182.00
    assert monotributo.tope_anual("K") == 126_610_838.75


def test_la_tabla_sabe_que_esta_incompleta():
    # Si TABLA_COMPLETA diera True con categorias faltantes, el item 3.3
    # arrancaria a calcular con una tabla con agujeros.
    assert not monotributo.TABLA_COMPLETA
    assert set(monotributo.CATEGORIAS_FALTANTES) == set("CDEFGHIJ")


def test_una_categoria_que_no_esta_cargada_no_devuelve_cero():
    # Devolver cero se leeria como "tope cero" y cualquier ingreso lo
    # excederia. Devolver None obliga a que el que llama decida.
    assert monotributo.tope_anual("D") is None
    assert monotributo.excede("D", 50_000_000) is None


def test_se_detecta_el_exceso_sobre_una_categoria_conocida():
    assert monotributo.excede("A", 12_009_411) is True
    assert monotributo.excede("A", 12_000_000) is False
    assert monotributo.excede("K", 200_000_000) is True


def test_la_categoria_no_se_deduce_con_la_tabla_incompleta():
    # Al no estar C a J, un cliente de veinte millones caeria en K, que es la
    # ultima cargada, y quedaria como si tuviera el tope mas alto del regimen.
    assert monotributo.categoria_por_ingresos(20_000_000) is None


def test_la_escala_dice_hasta_cuando_vale():
    assert monotributo.vigente(date(2026, 9, 22))
    assert monotributo.vigente(date(2027, 1, 31))
    assert not monotributo.vigente(date(2027, 2, 1))
    assert not monotributo.vigente(date(2026, 7, 31))


def test_el_estado_de_la_tabla_se_puede_mostrar_al_analista():
    texto = monotributo.estado_de_la_tabla()
    assert "incompleta" in texto
    assert "2027-01-31" in texto
