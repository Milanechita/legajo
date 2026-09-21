"""Pruebas de validacion de CUIT y CUIL.

Un CUIT mal tipeado deja de matchear contra ARCA y contra el BCRA, y el
cliente queda sin constatar sin que nadie se entere. Por eso se rechaza en la
carga y no mas adelante.
"""

from __future__ import annotations

import pytest

from legajo.modelo import (
    Documento, armar_cuit, digito_verificador_cuit, validar_cuit,
)


def test_el_verificador_se_calcula_sobre_los_primeros_diez_digitos():
    # 20-12345678-? Los pesos son 5,4,3,2,7,6,5,4,3,2 y el modulo es 11.
    assert digito_verificador_cuit("2012345678") == 6


def test_un_cuit_armado_por_el_programa_se_valida_a_si_mismo():
    # Si armar y validar no cerraran, el padron de ejemplo saldria con CUIT
    # invalidos y las pruebas de las fases siguientes arrancarian mintiendo.
    for documento in ("99000001", "99000123", "99123456", "12345678"):
        for prefijo in ("20", "27", "30", "33"):
            cuit = armar_cuit(prefijo, documento)
            if cuit:
                assert validar_cuit(cuit), f"{cuit} no se valida"


def test_un_digito_verificador_cambiado_no_pasa():
    cuit = armar_cuit("20", "12345678")
    ultimo = str((int(cuit[-1]) + 1) % 10)
    assert not validar_cuit(cuit[:-1] + ultimo)


def test_un_cuit_de_diez_digitos_dice_cuantos_tiene():
    resultado = validar_cuit("2012345678")
    assert not resultado
    assert "10 digitos" in resultado.motivo


def test_un_prefijo_que_no_existe_se_rechaza():
    resultado = validar_cuit("99123456789")
    assert not resultado
    assert "99" in resultado.motivo


def test_el_prefijo_de_persona_juridica_en_un_cliente_persona_es_un_error():
    # Es el segundo pedido del item 1.3: el prefijo tiene que ser coherente
    # con el tipo de persona. Si no lo es, uno de los dos datos esta mal
    # cargado y hay que verlo en el alta.
    cuit = armar_cuit("30", "71234567")
    resultado = validar_cuit(cuit, tipo_persona="PERSONA")
    assert not resultado
    assert "persona juridica" in resultado.motivo


def test_el_prefijo_de_persona_humana_en_una_entidad_es_un_error():
    cuit = armar_cuit("20", "12345678")
    resultado = validar_cuit(cuit, tipo_persona="ENTIDAD")
    assert not resultado
    assert "persona humana" in resultado.motivo


def test_el_prefijo_coherente_con_el_tipo_pasa():
    assert validar_cuit(armar_cuit("20", "12345678"), tipo_persona="PERSONA")
    assert validar_cuit(armar_cuit("27", "27998877"), tipo_persona="PERSONA")
    assert validar_cuit(armar_cuit("30", "71234567"), tipo_persona="ENTIDAD")


def test_el_cuit_se_valida_con_guiones_y_sin_guiones():
    cuit = armar_cuit("20", "12345678")
    con_guiones = f"{cuit[:2]}-{cuit[2:10]}-{cuit[10]}"
    assert validar_cuit(con_guiones)


def test_la_combinacion_que_obligaria_a_cambiar_el_prefijo_no_tiene_verificador():
    # Cuando el calculo da 10, AFIP no emite ese CUIT: pasa el 20 o el 27 a 23
    # y recalcula. Devolver un digito igual haria pasar CUIT que no existen.
    sin_verificador = [d for d in range(10_000_000, 10_000_200)
                       if digito_verificador_cuit(f"20{d}") is None]
    assert sin_verificador, "el caso existe y la prueba tiene que encontrarlo"
    for d in sin_verificador:
        assert armar_cuit("20", str(d)) == ""


# --- desde el Documento ---------------------------------------------------

def test_un_documento_cuit_se_valida():
    bueno = Documento("CUIT", armar_cuit("30", "71234567"))
    assert bueno.validar("ENTIDAD")
    assert not Documento("CUIT", "30-71234567-8").validar("ENTIDAD")


def test_un_pasaporte_no_se_marca_invalido_porque_no_sabemos_validarlo():
    # Inventarle una regla de validacion a un pasaporte extranjero seria
    # inventar un hallazgo.
    assert Documento("PASAPORTE", "K1234567").validar()
    assert Documento("TAX_ID", "88991122").validar()


def test_un_dni_suelto_no_se_valida_como_cuit():
    assert Documento("DNI", "28456123").validar("PERSONA")
