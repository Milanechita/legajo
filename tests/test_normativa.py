"""Pruebas de las reglas que salen de los manuales de prevencion.

Cada caso de aca corresponde a una regla escrita en la normativa que una
implementacion ingenua se saltea.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from legajo.beneficiario import UMBRAL_GENERAL, resolver, umbral_aplicable
from legajo.matriz import MESES_HASTA_REVISION
from legajo.modelo import Cliente
from legajo.pep import PEP, RegistroPEP
from legajo.riesgo import evaluar
from legajo.societaria import Estructura, Nodo, Participacion


def estructura(nodos, participaciones=()):
    e = Estructura()
    for n in nodos:
        e.agregar_nodo(n)
    for propietario, participada, capital in participaciones:
        e.agregar_participacion(Participacion(propietario, participada, capital))
    return e


# --- el umbral no es una constante ---------------------------------------

def test_entidad_argentina_usa_el_umbral_general():
    assert umbral_aplicable(Nodo("X", "X", "ENTIDAD", jurisdiccion="AR")) == UMBRAL_GENERAL


def test_entidad_del_exterior_sin_oferta_publica_no_tiene_umbral():
    """Se identifica a la totalidad de los beneficiarios, sin piso."""
    assert umbral_aplicable(Nodo("X", "X", "ENTIDAD", jurisdiccion="VG")) == 0.0


def test_entidad_del_exterior_con_oferta_publica_vuelve_al_general():
    nodo = Nodo("X", "X", "ENTIDAD", jurisdiccion="US", oferta_publica=True)
    assert umbral_aplicable(nodo) == UMBRAL_GENERAL


def test_el_umbral_cambia_quien_es_beneficiario():
    """La misma estructura da distinto segun donde este constituida la entidad.

    Un tenedor del 6% es participe menor en una sociedad argentina y
    beneficiario final en una offshore.
    """
    nodos_ar = [
        Nodo("A", "Ana", "PERSONA"), Nodo("B", "Beto", "PERSONA"),
        Nodo("X", "X", "ENTIDAD", jurisdiccion="AR"),
    ]
    nodos_ex = [
        Nodo("A", "Ana", "PERSONA"), Nodo("B", "Beto", "PERSONA"),
        Nodo("X", "X", "ENTIDAD", jurisdiccion="VG"),
    ]
    participaciones = [("A", "X", 0.60), ("B", "X", 0.06)]

    local = resolver(estructura(nodos_ar, participaciones), "X")
    exterior = resolver(estructura(nodos_ex, participaciones), "X")

    assert [b.nombre for b in local.beneficiarios] == ["Ana"]
    assert [b.nombre for b in local.participes_menores] == ["Beto"]
    assert {b.nombre for b in exterior.beneficiarios} == {"Ana", "Beto"}


def test_sociedad_con_oferta_publica_queda_exceptuada():
    e = estructura([Nodo("X", "Cotizante SA", "ENTIDAD", oferta_publica=True)])
    r = resolver(e, "X")
    assert r.exceptuada
    assert r.identificado          # no es un caso sin resolver
    assert not r.beneficiarios     # pero tampoco hay que listar beneficiarios


# --- PEP: la categoria cambia el resultado --------------------------------

def cliente(**kw) -> Cliente:
    base = dict(cliente_id="X1", nombre="Test", tipo="PERSONA",
                nacionalidad="ARGENTINA", pais_residencia="ARGENTINA",
                actividad="Docencia")
    base.update(kw)
    return Cliente(**base)


def test_pep_extranjera_es_alto_riesgo_por_definicion():
    ev = evaluar(cliente(), pep=PEP("X1", "EXTRANJERA", "Ministro"))
    assert ev.nivel == "ALTO"
    assert "PEP_EXTRANJERA" in ev.elevadores


def test_pep_nacional_no_eleva_por_si_sola():
    """Se evalua por riesgo. Un concejal sin otros factores no es alto riesgo."""
    ev = evaluar(cliente(), pep=PEP("X1", "NACIONAL", "Concejal"))
    assert ev.nivel != "ALTO"
    assert ev.elevadores == []
    assert any(f.codigo == "PEP_NACIONAL" for f in ev.factores)


def test_pep_nacional_suma_y_puede_llegar_a_alto_con_otros_factores():
    ev = evaluar(
        cliente(tipo="ENTIDAD", nacionalidad="BOLIVIA", actividad="Criptoactivos"),
        pep=PEP("X1", "NACIONAL", "Legislador"),
    )
    assert ev.nivel == "ALTO"


def test_parentesco_suma_sobre_el_tipo_base():
    solo = evaluar(cliente(), pep=PEP("X1", "NACIONAL"))
    con_vinculo = evaluar(cliente(), pep=PEP("X1", "NACIONAL", por_parentesco=True))
    assert con_vinculo.puntaje > solo.puntaje


# --- vigencia de la condicion ---------------------------------------------

def test_condicion_pep_vigente_mientras_ejerce():
    assert PEP("X1", "NACIONAL").vigente()


def test_condicion_pep_vence_a_los_dos_anios_del_cese():
    hace_tres = date.today() - timedelta(days=365 * 3)
    hace_uno = date.today() - timedelta(days=365)
    assert not PEP("X1", "EXTRANJERA", fecha_cese=hace_tres).vigente()
    assert PEP("X1", "EXTRANJERA", fecha_cese=hace_uno).vigente()


def test_pep_vencida_no_se_aplica_pero_queda_registrada():
    """El dato no se borra: sirve para el expediente."""
    vencida = PEP("X1", "EXTRANJERA", fecha_cese=date.today() - timedelta(days=365 * 4))
    registro = RegistroPEP([vencida])
    assert registro.consultar("X1") is None
    assert registro.vencidas() == [vencida]
    assert len(registro) == 1


def test_una_pep_extranjera_vencida_no_eleva():
    registro = RegistroPEP([
        PEP("X1", "EXTRANJERA", fecha_cese=date.today() - timedelta(days=365 * 5))
    ])
    ev = evaluar(cliente(), pep=registro.consultar("X1"))
    assert ev.nivel == "BAJO"


# --- periodicidad de revision ---------------------------------------------

@pytest.mark.parametrize("nivel,meses", [("ALTO", 12), ("MEDIO", 36), ("BAJO", 60)])
def test_la_revision_sale_del_nivel_de_riesgo(nivel, meses):
    assert MESES_HASTA_REVISION[nivel] == meses


def test_proxima_revision_se_calcula_del_nivel():
    alto = evaluar(cliente(), pep=PEP("X1", "EXTRANJERA"))
    bajo = evaluar(cliente())
    assert alto.nivel == "ALTO" and bajo.nivel == "BAJO"
    assert alto.proxima_revision(date(2026, 1, 15)) == date(2027, 1, 15)
    assert bajo.proxima_revision(date(2026, 1, 15)) == date(2031, 1, 15)
