"""Pruebas de la evaluacion del screening.

Verifican que la vara con la que se mide es correcta: que las cuentas de
recall y falsas alertas dan lo que dicen, que la semilla reproduce, y que un
caso cuyo designado desaparecio de la lista no se cuenta como un fallo del
motor. Los numeros contra las listas reales no se prueban aca porque cambian
cada semana, se corren con `python -m legajo evaluar`.
"""

from __future__ import annotations

from datetime import date

from legajo import evaluacion as ev
from legajo.config import Politica
from legajo.fuentes.base import Designado, Padron, VersionLista
from legajo.modelo import Cliente
from legajo.screening import Coincidencia


def padron_de(*designados: Designado) -> Padron:
    p = Padron()
    p.incorporar(list(designados), VersionLista("TEST", None, date.today(), len(designados), "0" * 64))
    return p


def _padron_chico() -> Padron:
    nombres = [
        "ABBAS, Ali Reza", "MOHAMMED, Khalid Shaikh", "HAQQANI, Sirajuddin Jalaluddin",
        "QADHAFI, Muammar Abu Minyar", "GUZMAN LOERA, Joaquin Archivaldo",
        "SAEED, Hafiz Muhammad", "ZAWAHIRI, Ayman Mohamed", "MADURO MOROS, Nicolas Jose",
    ]
    return padron_de(*[Designado("OFAC_SDN", str(i), n) for i, n in enumerate(nombres, start=1)])


def _resultado(esperados: set[tuple[str, str]], scores: list[tuple[str, float]], tipo: str = "x") -> ev.ResultadoCaso:
    caso = ev.CasoEvaluacion(Cliente("C", "Cliente"), tipo, frozenset(esperados))
    coincidencias = [
        Coincidencia("C", "OFAC_SDN", id_, "N", "N", score, "NOMBRE") for id_, score in scores
    ]
    return ev.ResultadoCaso(caso, coincidencias)


def test_un_positivo_cuenta_como_detectado_solo_si_sale_el_designado_esperado():
    esperado = {("OFAC_SDN", "1")}
    acierto = _resultado(esperado, [("1", 90.0)])
    error = _resultado(esperado, [("2", 99.0)])
    m = ev.metricas([acierto, error], umbral=78)
    assert (m.positivos, m.detectados) == (2, 1)


def test_un_positivo_por_debajo_del_umbral_es_un_falso_negativo():
    r = _resultado({("OFAC_SDN", "1")}, [("1", 80.0)])
    assert ev.metricas([r], umbral=78).recall == 1.0
    assert ev.metricas([r], umbral=85).recall == 0.0


def test_la_falsa_alerta_se_mide_por_cliente_limpio_y_no_por_coincidencia():
    # Un cliente limpio con cinco coincidencias le cuesta una revision al
    # analista, no cinco: es la unidad de trabajo.
    ruidoso = _resultado(set(), [(str(i), 85.0) for i in range(5)])
    limpio = _resultado(set(), [])
    m = ev.metricas([ruidoso, limpio], umbral=78)
    assert (m.negativos, m.negativos_con_alerta) == (2, 1)
    assert m.tasa_falsa_alerta == 0.5


def test_la_precision_cuenta_detectados_sobre_todas_las_alertas():
    acierto = _resultado({("OFAC_SDN", "1")}, [("1", 95.0)])
    falsa = _resultado(set(), [("9", 90.0)])
    m = ev.metricas([acierto, falsa], umbral=78)
    assert m.precision == 0.5


def test_filtrar_por_umbral_equivale_a_correr_el_motor_con_ese_umbral():
    # La barrida corre una sola vez y filtra hacia arriba. Si los atenuantes
    # se aplicaran despues del corte esto dejaria de ser cierto.
    padron = _padron_chico()
    casos = ev.generar_sinteticos(padron, por_tipo=3, semilla=1)
    una_vez = ev.correr(casos, padron, procesos=1)
    for umbral in (78.0, 90.0):
        directo = ev.correr(casos, padron, Politica(umbral_revision=umbral), procesos=1)
        assert ev.metricas(una_vez, umbral).detectados == ev.metricas(directo, umbral).detectados
        assert ev.metricas(una_vez, umbral).negativos_con_alerta == ev.metricas(directo, umbral).negativos_con_alerta


def test_la_misma_semilla_genera_los_mismos_casos():
    padron = _padron_chico()
    a = ev.generar_sinteticos(padron, por_tipo=3, semilla=7)
    b = ev.generar_sinteticos(padron, por_tipo=3, semilla=7)
    assert [(c.cliente.nombre, c.tipo_caso) for c in a] == [(c.cliente.nombre, c.tipo_caso) for c in b]


def test_los_positivos_sinteticos_apuntan_a_un_designado_que_existe():
    padron = _padron_chico()
    existentes = {(d.lista, d.id_origen) for d in padron.designados}
    for c in ev.generar_sinteticos(padron, por_tipo=3, semilla=3):
        if c.positivo:
            assert c.esperados <= existentes


def test_un_caso_cuyo_designado_salio_de_la_lista_se_omite_y_no_cuenta_como_fallo(tmp_path):
    ruta = tmp_path / "casos.csv"
    ruta.write_text(
        "nombre,tipo,fecha_nacimiento,nacionalidad,documento_tipo,documento,tipo_caso,esperados\n"
        "Ali Reza Abbas,PERSONA,,,,,orden_invertido,OFAC_SDN:1\n"
        "Persona Retirada,PERSONA,,,,,exacto,OFAC_SDN:99999\n"
        "Juan Perez,PERSONA,,,,,homonimo_duro,\n",
        encoding="utf-8",
    )
    casos, omitidos = ev.leer_dificiles(ruta, _padron_chico())
    assert [c.cliente.nombre for c in casos] == ["Ali Reza Abbas", "Juan Perez"]
    assert len(omitidos) == 1 and "Persona Retirada" in omitidos[0]


def test_el_nombre_exacto_en_otro_orden_se_detecta_al_umbral_de_revision():
    padron = _padron_chico()
    caso = ev.CasoEvaluacion(Cliente("C", "Ali Reza Abbas"), "orden_invertido", frozenset({("OFAC_SDN", "1")}))
    [r] = ev.correr([caso], padron, procesos=1)
    assert r.mejor_score_esperado() is not None and r.mejor_score_esperado() >= 78
