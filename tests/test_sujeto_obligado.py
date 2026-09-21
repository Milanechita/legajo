"""Pruebas del tipo de sujeto obligado como parametro.

La regla que gobierna este archivo: el sistema nunca marca como faltante un
documento que la norma no permite pedir, y nunca afirma que algo es exigible
si todavia no se verifico contra el texto.
"""

from __future__ import annotations

import pytest

from legajo.sujeto_obligado import (
    ALYC, BANCO, POR_DEFECTO, Exigibilidad, TipoSujetoObligado, de,
)


def test_el_banco_no_puede_requerir_la_ddjj_impositiva():
    # La Res. UIF 78/2025 sustituyo el art. 37 de la Res. 14/2023 y la
    # prohibio para entidades financieras. Pedirla es el incumplimiento.
    assert not BANCO.puede_requerir("DDJJ_IMPOSITIVA")
    assert BANCO.exigibilidad("DDJJ_IMPOSITIVA") is Exigibilidad.PROHIBIDO


def test_un_documento_prohibido_nunca_figura_entre_los_exigibles():
    # Si apareciera en las dos listas, el checklist del legajo lo pediria y el
    # analista incumpliria por seguir al programa.
    assert "DDJJ_IMPOSITIVA" in BANCO.prohibidos()
    assert "DDJJ_IMPOSITIVA" not in BANCO.exigibles()


def test_un_documento_que_no_se_verifico_no_se_da_por_opcional():
    # SIN_VERIFICAR le dice al analista que vaya a la norma. OPCIONAL le diria
    # que ya se miro y no hace falta, que es una afirmacion que nadie hizo.
    assert BANCO.exigibilidad("BALANCE") is Exigibilidad.SIN_VERIFICAR
    assert BANCO.exigibilidad("BALANCE") is not Exigibilidad.OPCIONAL


def test_lo_no_verificado_se_puede_pedir():
    # Prohibido es solo lo que la norma prohibe expresamente. Tratar como
    # prohibido todo lo que no se verifico dejaria al analista sin poder pedir
    # nada.
    assert BANCO.puede_requerir("BALANCE")


def test_la_alyc_no_afirma_nada_sobre_sus_documentos():
    # La Res. 78/2023 todavia no se verifico. El programa no inventa el
    # catalogo de una resolucion que nadie leyo.
    assert ALYC.documentos == {}
    assert ALYC.exigibilidad("DDJJ_IMPOSITIVA") is Exigibilidad.SIN_VERIFICAR
    assert ALYC.exigibles() == ()


def test_ningun_catalogo_se_declara_completo_todavia():
    # El catalogo entero es el item 1.4. Que ninguno diga estar completo evita
    # que el checklist del item 5.1 se crea exhaustivo antes de tiempo.
    assert not BANCO.catalogo_completo
    assert not ALYC.catalogo_completo


def test_el_sujeto_obligado_por_defecto_es_el_banco():
    assert POR_DEFECTO is BANCO
    assert POR_DEFECTO.resolucion == "Res. UIF 14/2023"


def test_cada_sujeto_obligado_dice_cuando_se_consulto_su_norma():
    # Misma regla que el SMVM: si la fecha esta vieja, los umbrales pueden
    # estar mal y el programa no avisa solo.
    for sujeto in (BANCO, ALYC):
        assert sujeto.vigencia_consultada is not None
        assert sujeto.resolucion


def test_se_elige_por_nombre():
    assert de("BANCO") is BANCO
    assert de("alyc") is ALYC
    assert de(TipoSujetoObligado.ALYC) is ALYC


def test_un_sujeto_obligado_desconocido_falla_y_no_cae_al_banco():
    # Correr un analisis de ALYC bajo los umbrales de un banco da resultados
    # que parecen correctos y no lo son. Mejor que reviente.
    with pytest.raises(ValueError) as e:
        de("ESCRIBANIA")
    assert "BANCO" in str(e.value) and "ALYC" in str(e.value)


def test_los_umbrales_del_banco_son_los_que_ya_estaban_verificados():
    # Los umbrales en SMVM del repo citan la Res. 14/2023 segun Res. 78/2025,
    # que es la del banco. Cambiarlos por otros sin verificar seria inventar.
    assert BANCO.umbrales.reporte_efectivo == 40.0
