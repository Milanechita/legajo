"""Pruebas de normalizacion de paises y de las listas cargadas.

El riesgo que cubren estas pruebas es el peor de todos: que el sistema corra
sin errores y no detecte nada, porque los nombres de pais no coinciden entre
la lista y el padron.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from legajo.config import SMVM, SMVM_VIGENCIA, UMBRALES, pesos
from legajo.matriz import (
    ARCA_VIGENCIA, GAFI_CONTRAMEDIDAS, GAFI_DILIGENCIA_REFORZADA, GAFI_PLENARIO,
    JURISDICCIONES_ALTO_RIESGO, JURISDICCIONES_MONITOREO,
    JURISDICCIONES_NO_COOPERANTES,
)
from legajo.modelo import Cliente
from legajo.paises import codigos, desconocidos, iso, nombre
from legajo.riesgo import evaluar


# --- normalizacion ---------------------------------------------------------

@pytest.mark.parametrize("a,b", [
    ("Democratic Republic of the Congo", "República Democrática del Congo"),
    ("Virgin Islands (UK)", "Islas Vírgenes Británicas"),
    ("Lao PDR", "República Democrática Popular Lao"),
    ("Democratic People's Republic of Korea", "Corea del Norte"),
    ("Côte d'Ivoire", "República de Costa de Marfil"),
    ("Iran", "República Islámica de Irán"),
])
def test_las_tres_fuentes_convergen_al_mismo_codigo(a, b):
    """GAFI publica en ingles, ARCA en castellano formal, el padron como sea."""
    assert iso(a) == iso(b) is not None


def test_la_tilde_no_rompe_el_cotejo():
    """Una sola tilde alcanzaba para perder un factor de riesgo entero."""
    assert iso("Líbano") == iso("Libano") == "LB"
    assert iso("Perú") == iso("PERU") == "PE"


def test_el_apostrofo_no_rompe_el_cotejo():
    assert iso("Côte d'Ivoire") == iso("Cote dIvoire") == "CI"


def test_el_codigo_iso_se_acepta_directo():
    assert iso("AR") == "AR"
    assert iso("kp") == "KP"


def test_pais_desconocido_devuelve_none_y_no_se_asume_bajo_riesgo():
    assert iso("Wakanda") is None
    assert desconocidos(["Argentina", "Wakanda"]) == ["Wakanda"]


def test_cargar_una_lista_con_un_pais_desconocido_falla_ruidosamente():
    """Una lista de riesgo cargada a medias es peor que ninguna."""
    with pytest.raises(ValueError, match="no reconocidos"):
        codigos(["Argentina", "Wakanda"])


# --- listas cargadas -------------------------------------------------------

def test_lista_negra_del_plenario_de_junio_2026():
    assert {nombre(c) for c in JURISDICCIONES_ALTO_RIESGO} == {
        "Corea del Norte", "Iran", "Myanmar",
    }


def test_contramedidas_y_diligencia_reforzada_son_categorias_distintas():
    """El GAFI pide contramedidas a Iran y Corea, solo DDR a Myanmar."""
    assert {nombre(c) for c in GAFI_CONTRAMEDIDAS} == {"Corea del Norte", "Iran"}
    assert {nombre(c) for c in GAFI_DILIGENCIA_REFORZADA} == {"Myanmar"}
    assert not (GAFI_CONTRAMEDIDAS & GAFI_DILIGENCIA_REFORZADA)


def test_lista_gris_tiene_veintidos_jurisdicciones():
    assert len(JURISDICCIONES_MONITOREO) == 22


def test_nigeria_ya_no_esta_en_la_lista_gris():
    """Estuvo, y dejarla produce falsos positivos sobre clientes nigerianos."""
    assert iso("Nigeria") not in JURISDICCIONES_MONITOREO


def test_monaco_y_las_virgenes_britanicas_estan_en_la_lista_gris():
    """Dos plazas relevantes para estructuras societarias."""
    assert iso("Monaco") in JURISDICCIONES_MONITOREO
    assert iso("Islas Vírgenes Británicas") in JURISDICCIONES_MONITOREO


def test_gafi_y_arca_son_criterios_separados():
    """Uno es PLA/FT y el otro fiscal. Hay paises en uno y no en el otro."""
    solo_gafi = JURISDICCIONES_MONITOREO - JURISDICCIONES_NO_COOPERANTES
    solo_arca = JURISDICCIONES_NO_COOPERANTES - JURISDICCIONES_MONITOREO
    assert solo_gafi and solo_arca


def test_las_listas_llevan_fecha_de_corte():
    """Sin fecha no hay forma de saber si la matriz esta vencida."""
    assert GAFI_PLENARIO == date(2026, 6, 19)
    assert ARCA_VIGENCIA == date(2026, 5, 28)


# --- efecto sobre el scoring -----------------------------------------------

def cliente(**kw) -> Cliente:
    base = dict(cliente_id="X1", nombre="Test", tipo="PERSONA", actividad="Comercio")
    base.update(kw)
    return Cliente(**base)


def test_contramedidas_puntua_mas_que_diligencia_reforzada():
    corea = evaluar(cliente(pais_residencia="Corea del Norte"))
    myanmar = evaluar(cliente(pais_residencia="Myanmar"))
    assert corea.puntaje > myanmar.puntaje
    assert corea.nivel == myanmar.nivel == "ALTO"


def test_lista_gris_suma_pero_no_eleva():
    """El GAFI aclara que no pide diligencia reforzada sobre la lista gris."""
    ev = evaluar(cliente(pais_residencia="Kenia"))
    assert any(f.codigo == "JURISDICCION_MONITOREO" for f in ev.factores)
    assert ev.elevadores == []


def test_no_cooperante_suma_como_factor_propio():
    ev = evaluar(cliente(pais_residencia="Isla de Sark"))
    assert any(f.codigo == "JURISDICCION_NO_COOPERANTE" for f in ev.factores)


def test_pais_sin_normalizar_se_marca_en_vez_de_ignorarse():
    """Silencio no es lo mismo que bajo riesgo."""
    ev = evaluar(cliente(pais_residencia="Wakanda"))
    assert any(f.codigo == "PAIS_NO_RECONOCIDO" for f in ev.factores)


def test_el_nombre_formal_de_arca_produce_el_mismo_resultado_que_el_comun():
    formal = evaluar(cliente(pais_residencia="República Popular Democrática de Corea"))
    comun = evaluar(cliente(pais_residencia="Corea del Norte"))
    assert formal.puntaje == comun.puntaje
    assert formal.nivel == comun.nivel


# --- SMVM ------------------------------------------------------------------

def test_los_umbrales_se_expresan_en_smvm_no_en_pesos():
    """Al actualizar el salario, los montos se recalculan solos."""
    assert UMBRALES.cliente_habitual == 700.0
    assert UMBRALES.en_pesos("cliente_habitual") == pesos(700.0) == 700.0 * SMVM


def test_el_smvm_lleva_fecha_de_vigencia():
    assert SMVM_VIGENCIA == date(2026, 9, 1)
    assert SMVM > 0
