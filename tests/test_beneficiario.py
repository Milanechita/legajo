"""Pruebas de beneficiario final y scoring EBR.

Los dos primeros casos son los que separan una implementacion correcta de una
que pierde beneficiarios en silencio.
"""

from __future__ import annotations

import pytest

from legajo.beneficiario import UMBRAL_BENEFICIARIO, resolver
from legajo.matriz import MATRIZ_POR_DEFECTO, MatrizRiesgo
from legajo.modelo import Cliente
from legajo.riesgo import evaluar
from legajo.screening import Coincidencia
from legajo.societaria import (
    Administracion, Control, Estructura, Nodo, Participacion,
)


def estructura(nodos, participaciones=(), controles=(), administraciones=()):
    e = Estructura()
    for nid, nombre, tipo in nodos:
        e.agregar_nodo(Nodo(nid, nombre, tipo))
    for p in participaciones:
        propietario, participada, capital = p[:3]
        voto = p[3] if len(p) > 3 else None
        e.agregar_participacion(Participacion(propietario, participada, capital, voto))
    for persona, entidad, motivo in controles:
        e.agregar_control(Control(persona, entidad, motivo))
    for persona, entidad, cargo in administraciones:
        e.agregar_administracion(Administracion(persona, entidad, cargo))
    return e


# --- los dos errores clasicos ---------------------------------------------

def test_umbral_se_aplica_a_la_suma_no_a_cada_arista():
    """Juan: 15% de A, A tiene 40% de X, mas 8% directo. Total 14%: es BF.

    Podar la arista del 8% por estar bajo el umbral haria desaparecer al
    beneficiario. El umbral va al final, sobre el acumulado.
    """
    e = estructura(
        [("J", "Juan", "PERSONA"), ("A", "Soc A", "ENTIDAD"), ("X", "Cliente X", "ENTIDAD")],
        [("J", "A", 0.15), ("A", "X", 0.40), ("J", "X", 0.08)],
    )
    r = resolver(e, "X")
    assert [b.nombre for b in r.beneficiarios] == ["Juan"]
    assert r.beneficiarios[0].capital == pytest.approx(0.14)


def test_diamante_suma_las_dos_ramas():
    """Juan llega a X por dos sociedades distintas: las tenencias suman.

    Un conjunto de visitados global lo contaria una sola vez y daria 15%.
    La deteccion de ciclos tiene que ser sobre el camino, no global.
    """
    e = estructura(
        [("J", "Juan", "PERSONA"), ("A", "Soc A", "ENTIDAD"),
         ("B", "Soc B", "ENTIDAD"), ("X", "Cliente X", "ENTIDAD")],
        [("J", "A", 0.50), ("J", "B", 0.50), ("A", "X", 0.30), ("B", "X", 0.30)],
    )
    r = resolver(e, "X")
    assert r.beneficiarios[0].capital == pytest.approx(0.30)


# --- definicion de la Res. 112/2021 ---------------------------------------

def test_voto_califica_aunque_el_capital_no_alcance():
    """5% de capital con 45% de los votos es beneficiario final.

    La resolucion dice capital O derechos de voto. Colapsar ambos en un solo
    numero pierde el caso de las acciones preferidas sin voto.
    """
    e = estructura(
        [("P", "Laura", "PERSONA"), ("X", "Cliente X", "ENTIDAD")],
        [("P", "X", 0.05, 0.45)],
    )
    r = resolver(e, "X")
    assert [b.nombre for b in r.beneficiarios] == ["Laura"]
    assert r.beneficiarios[0].capital == pytest.approx(0.05)
    assert r.beneficiarios[0].voto == pytest.approx(0.45)


def test_control_por_otros_medios_no_necesita_porcentaje():
    e = estructura(
        [("P", "Ana", "PERSONA"), ("X", "Cliente X", "ENTIDAD")],
        controles=[("P", "X", "acuerdo de accionistas")],
    )
    r = resolver(e, "X")
    assert r.beneficiarios[0].via == "CONTROL"
    assert r.beneficiarios[0].capital == 0.0


def test_supletorio_solo_si_no_hay_beneficiario_y_registra_la_causa():
    e = estructura(
        [("P", "Hector", "PERSONA"), ("X", "Cliente X", "ENTIDAD")],
        administraciones=[("P", "X", "presidente del directorio")],
    )
    r = resolver(e, "X")
    assert r.beneficiarios[0].via == "SUPLETORIO"
    assert "causa:" in r.beneficiarios[0].detalle


def test_supletorio_no_se_usa_si_hay_beneficiario():
    e = estructura(
        [("P", "Juan", "PERSONA"), ("H", "Hector", "PERSONA"), ("X", "X", "ENTIDAD")],
        [("P", "X", 0.90)],
        administraciones=[("H", "X", "presidente")],
    )
    r = resolver(e, "X")
    assert [b.via for b in r.beneficiarios] == ["PARTICIPACION"]


def test_participe_menor_se_registra_aparte_no_se_descarta():
    """Quien no alcanza el umbral igual queda documentado."""
    e = estructura(
        [("P", "Juan", "PERSONA"), ("X", "X", "ENTIDAD")],
        [("P", "X", 0.04)],
    )
    r = resolver(e, "X")
    assert not r.beneficiarios or r.beneficiarios[0].via == "SUPLETORIO"
    assert [b.nombre for b in r.participes_menores] == ["Juan"]


# --- opacidad y ciclos -----------------------------------------------------

def test_capital_no_declarado_cuenta_como_opaco():
    e = estructura(
        [("P", "Juan", "PERSONA"), ("X", "X", "ENTIDAD")],
        [("P", "X", 0.60)],
    )
    r = resolver(e, "X")
    assert r.titularidad_opaca == pytest.approx(0.40)


def test_ciclo_no_cuelga_y_se_registra():
    e = estructura(
        [("A", "Soc A", "ENTIDAD"), ("B", "Soc B", "ENTIDAD"), ("X", "X", "ENTIDAD")],
        [("A", "B", 1.0), ("B", "A", 1.0), ("A", "X", 1.0)],
    )
    r = resolver(e, "X")
    assert r.ciclos


def test_titularidad_en_ciclo_cuenta_como_no_identificada():
    """Lo que entra en un ciclo nunca llega a una persona humana."""
    e = estructura(
        [("A", "Soc A", "ENTIDAD"), ("B", "Soc B", "ENTIDAD"), ("X", "X", "ENTIDAD")],
        [("A", "B", 1.0), ("B", "A", 1.0), ("A", "X", 1.0)],
    )
    r = resolver(e, "X")
    assert r.titularidad_opaca == pytest.approx(1.0)


@pytest.mark.parametrize("participaciones", [
    pytest.param([("J", "A", 0.15), ("A", "X", 0.40), ("J", "X", 0.08)], id="cadena-mas-directo"),
    pytest.param([("J", "A", 0.50), ("A", "X", 0.30)], id="cadena-simple"),
    pytest.param([("J", "X", 0.60)], id="directo-parcial"),
])
def test_la_titularidad_se_conserva(participaciones):
    """BF + participes menores + opaca siempre cierra en 100%.

    Si no cierra, hay titularidad perdida en el recorrido.
    """
    e = estructura(
        [("J", "Juan", "PERSONA"), ("A", "Soc A", "ENTIDAD"), ("X", "X", "ENTIDAD")],
        participaciones,
    )
    r = resolver(e, "X")
    total = (
        sum(b.capital for b in r.beneficiarios if b.via == "PARTICIPACION")
        + sum(b.capital for b in r.participes_menores)
        + r.titularidad_opaca
    )
    assert total == pytest.approx(1.0)


def test_persona_humana_no_tiene_cadena():
    e = estructura([("P", "Juan", "PERSONA")])
    r = resolver(e, "P")
    assert not r.beneficiarios
    assert "persona humana" in r.observaciones[0]


def test_id_sin_nodo_declarado_no_se_asume_persona():
    """Un id desconocido es una entidad opaca, no un beneficiario final."""
    e = estructura([("X", "X", "ENTIDAD")], [("DESCONOCIDO", "X", 0.80)])
    r = resolver(e, "X")
    assert not any(b.via == "PARTICIPACION" for b in r.beneficiarios)


# --- scoring EBR -----------------------------------------------------------

def cliente(**kw) -> Cliente:
    base = dict(cliente_id="X1", nombre="Test", tipo="PERSONA")
    base.update(kw)
    return Cliente(**base)


def test_cliente_limpio_es_riesgo_bajo():
    ev = evaluar(cliente(nacionalidad="ARGENTINA", pais_residencia="ARGENTINA",
                         actividad="Docencia"))
    assert ev.nivel == "BAJO"
    assert ev.regimen == "DD_SIMPLIFICADA"


def test_pep_eleva_a_alto_aunque_el_puntaje_no_alcance():
    """El elevador fija un piso. Sin el, esto seria un if disperso."""
    ev = evaluar(cliente(nacionalidad="ARGENTINA", pais_residencia="ARGENTINA",
                         actividad="Docencia"), es_pep=True)
    assert ev.puntaje < MATRIZ_POR_DEFECTO.umbral_alto
    assert ev.nivel == "ALTO"
    assert "PEP" in ev.elevadores


def test_jurisdiccion_de_alto_riesgo_eleva():
    ev = evaluar(cliente(nacionalidad="IRAN", pais_residencia="IRAN"))
    assert ev.nivel == "ALTO"


def test_coincidencia_probable_eleva():
    hit = Coincidencia(
        cliente_id="X1", lista="OFAC_SDN", id_origen="1",
        nombre_designado="Alguien", nombre_matcheado="Alguien",
        score=97.0, criterio="NOMBRE",
    )
    ev = evaluar(cliente(actividad="Docencia"), coincidencias=[hit])
    assert ev.nivel == "ALTO"
    assert "COINCIDENCIA_PROBABLE" in ev.elevadores


def test_beneficiario_no_identificado_eleva():
    e = estructura([("X", "X", "ENTIDAD")])
    r = resolver(e, "X")
    ev = evaluar(cliente(tipo="ENTIDAD", actividad="Comercio"), resolucion=r)
    assert ev.nivel == "ALTO"
    assert "BENEFICIARIO_NO_IDENTIFICADO" in ev.elevadores


def test_todo_punto_queda_desglosado():
    """Un nivel de riesgo sin desglose no es justificable."""
    ev = evaluar(cliente(tipo="ENTIDAD", nacionalidad="BOLIVIA",
                         pais_residencia="ARGENTINA", actividad="Criptoactivos"))
    assert ev.puntaje == pytest.approx(sum(f.puntos for f in ev.factores))
    assert {f.codigo for f in ev.factores} >= {
        "PERSONA_JURIDICA", "JURISDICCION_MONITOREO", "ACTIVIDAD_SENSIBLE",
    }


def test_matriz_es_politica_no_codigo():
    """Cambiar la matriz cambia el resultado sin tocar el evaluador."""
    c = cliente(tipo="ENTIDAD", actividad="Docencia")
    laxa = MatrizRiesgo(umbral_medio=500.0, umbral_alto=900.0)
    estricta = MatrizRiesgo(umbral_medio=1.0, umbral_alto=2.0)
    assert evaluar(c, matriz=laxa).nivel == "BAJO"
    assert evaluar(c, matriz=estricta).nivel == "ALTO"


def test_elevador_nunca_baja_el_nivel():
    hit = Coincidencia(
        cliente_id="X1", lista="OFAC_SDN", id_origen="1",
        nombre_designado="A", nombre_matcheado="A", score=99.0, criterio="NOMBRE",
    )
    ev = evaluar(cliente(nacionalidad="IRAN", pais_residencia="IRAN"),
                 coincidencias=[hit], es_pep=True)
    assert ev.nivel == "ALTO"
    assert ev.puntaje > MATRIZ_POR_DEFECTO.umbral_alto


def test_umbral_de_la_resolucion_es_diez_por_ciento():
    assert UMBRAL_BENEFICIARIO == 0.10
