"""Pruebas de la Central de Deudores del BCRA.

Ninguna sale a la red. La descarga entra por parametro y las pruebas inyectan
fixtures, asi que la suite no depende de que el BCRA este arriba. Hay una
prueba que verifica justamente eso: si alguien cablea la descarga adentro,
revienta.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from legajo.fuentes import bcra

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "bcra"
HOY = date(2026, 9, 21)
CUIT = "20990000019"


def fixture(nombre: str) -> dict:
    return json.loads((FIXTURES / f"{nombre}.json").read_text(encoding="utf-8"))


def respondedor(**por_recurso):
    """Descarga falsa que responde segun el endpoint, y cuenta llamadas."""
    llamadas = []

    def bajar(url: str) -> dict:
        llamadas.append(url)
        if "ChequesRechazados" in url:
            return por_recurso.get("cheques", {"status": 404, "results": {}})
        if "Historicas" in url:
            return por_recurso.get("historicas", {"status": 404, "results": {}})
        return por_recurso.get("deudas", {"status": 404, "results": {}})

    bajar.llamadas = llamadas
    return bajar


def explota(url: str) -> dict:
    raise AssertionError(f"no se puede salir a la red en una prueba: {url}")


# --- parseo ---------------------------------------------------------------

def test_se_leen_todas_las_asistencias_de_todos_los_periodos():
    denominacion, asistencias = bcra.parsear_deudas(fixture("deudas_irregular"))
    assert denominacion == "PEREZ JUAN IGNACIO"
    assert len(asistencias) == 3
    assert {a.periodo for a in asistencias} == {"202608", "202607"}


def test_la_peor_situacion_manda_y_no_el_promedio():
    # Un cliente en situacion 1 con cinco bancos y en 5 con el sexto tiene un
    # problema. Promediar lo esconde.
    informe = bcra.InformeBCRA(
        cuit=CUIT, consultado=HOY,
        asistencias=bcra.parsear_deudas(fixture("deudas_irregular"))[1],
    )
    assert informe.peor_situacion == 3
    assert informe.irregular


def test_situacion_uno_no_es_irregular():
    informe = bcra.InformeBCRA(
        cuit=CUIT, consultado=HOY,
        asistencias=bcra.parsear_deudas(fixture("deudas_normal"))[1],
    )
    assert informe.peor_situacion == 1
    assert not informe.irregular


def test_la_deuda_total_suma_un_solo_periodo():
    # Sumar todos los periodos contaria la misma deuda una vez por mes
    # informado, y el monto saldria multiplicado por la cantidad de meses.
    informe = bcra.InformeBCRA(
        cuit=CUIT, consultado=HOY,
        asistencias=bcra.parsear_deudas(fixture("deudas_irregular"))[1],
    )
    assert informe.deuda_total == pytest.approx(4820.5 + 310.0)


def test_se_leen_los_cheques_rechazados_con_su_causal():
    cheques = bcra.parsear_cheques(fixture("cheques"))
    assert len(cheques) == 2
    impago = next(c for c in cheques if c.numero == "00012345")
    assert not impago.pagado
    assert "SIN FONDOS" in impago.causal
    assert next(c for c in cheques if c.numero == "00012399").pagado


def test_una_respuesta_vacia_no_rompe_el_parseo():
    # El BCRA devuelve 404 cuando el CUIT no tiene deuda informada, que es un
    # resultado y no un error.
    assert bcra.parsear_deudas(fixture("sin_datos")) == ("", [])
    assert bcra.parsear_cheques(fixture("sin_datos")) == []


def test_una_respuesta_a_medias_no_tira_la_consulta_entera():
    # El anidado de cheques es profundo. Si falta una rama, se pierde esa y no
    # las demas.
    roto = {"results": {"causales": [{"causal": "X", "entidades": None}]}}
    assert bcra.parsear_cheques(roto) == []


# --- consulta y cache -----------------------------------------------------

def test_la_primera_consulta_baja_y_deja_la_cache(tmp_path):
    bajar = respondedor(deudas=fixture("deudas_irregular"), cheques=fixture("cheques"))
    informe = bcra.consultar(CUIT, tmp_path, hoy=HOY, bajar=bajar)

    assert informe.denominacion == "PEREZ JUAN IGNACIO"
    assert informe.irregular
    assert len(bajar.llamadas) == 2
    assert (tmp_path / f"{CUIT}-deudas.json").exists()
    assert (tmp_path / f"{CUIT}-cheques.json").exists()


def test_la_segunda_consulta_sale_de_la_cache_y_no_toca_la_red(tmp_path):
    bajar = respondedor(deudas=fixture("deudas_irregular"), cheques=fixture("cheques"))
    bcra.consultar(CUIT, tmp_path, hoy=HOY, bajar=bajar)

    # Si esta llamada saliera a la red, `explota` lo haria fallar.
    informe = bcra.consultar(CUIT, tmp_path, hoy=HOY, bajar=explota)
    assert informe.peor_situacion == 3
    assert len(informe.cheques) == 2


def test_una_cache_vencida_se_vuelve_a_bajar(tmp_path):
    bajar = respondedor(deudas=fixture("deudas_irregular"))
    bcra.consultar(CUIT, tmp_path, hoy=date(2026, 1, 1), bajar=bajar,
                   incluir_cheques=False)
    assert len(bajar.llamadas) == 1

    bcra.consultar(CUIT, tmp_path, hoy=HOY, bajar=bajar, vigencia_dias=30,
                   incluir_cheques=False)
    assert len(bajar.llamadas) == 2, "una cache de nueve meses no puede servir"


def test_el_informe_dice_cuando_se_consulto_y_no_cuando_se_leyo(tmp_path):
    # "El cliente esta en situacion 3" no dice nada sin la fecha: puede ser de
    # hoy o de hace dos anios.
    bajar = respondedor(deudas=fixture("deudas_irregular"))
    bcra.consultar(CUIT, tmp_path, hoy=date(2026, 9, 1), bajar=bajar,
                   incluir_cheques=False)

    informe = bcra.consultar(CUIT, tmp_path, hoy=HOY, bajar=explota,
                             incluir_cheques=False)
    assert informe.consultado == date(2026, 9, 1)
    assert informe.antiguedad_en_dias(HOY) == 20


def test_un_cuit_sin_deuda_informada_queda_marcado_sin_datos(tmp_path):
    bajar = respondedor()
    informe = bcra.consultar("27990000021", tmp_path, hoy=HOY, bajar=bajar)
    assert informe.sin_datos
    assert informe.peor_situacion == 0
    assert not informe.irregular


def test_un_cuit_mal_formado_falla_antes_de_salir_a_la_red():
    with pytest.raises(ValueError):
        bcra.consultar("1234", "/tmp/nada", bajar=explota)


def test_la_cache_corrupta_se_ignora_y_se_vuelve_a_bajar(tmp_path):
    (tmp_path / f"{CUIT}-deudas.json").write_text("{ esto no es json",
                                                  encoding="utf-8")
    bajar = respondedor(deudas=fixture("deudas_irregular"))
    informe = bcra.consultar(CUIT, tmp_path, hoy=HOY, bajar=bajar,
                             incluir_cheques=False)
    assert informe.peor_situacion == 3
    assert len(bajar.llamadas) == 1


def test_las_urls_que_se_arman_son_las_tres_documentadas(tmp_path):
    bajar = respondedor()
    bcra.consultar(CUIT, tmp_path, hoy=HOY, bajar=bajar)
    assert bajar.llamadas == [
        f"https://api.bcra.gob.ar/centraldedeudores/v1.0/Deudas/{CUIT}",
        f"https://api.bcra.gob.ar/centraldedeudores/v1.0/Deudas/ChequesRechazados/{CUIT}",
    ]


def test_el_corte_de_irregular_es_el_que_pide_el_roadmap():
    # Situacion 3 o peor, item 4.5. Si el corte cambiara sin querer, la senal
    # entera se corre.
    assert bcra.SITUACION_IRREGULAR == 3
    assert bcra.Asistencia("X", 2, 0, "202608").irregular is False
    assert bcra.Asistencia("X", 3, 0, "202608").irregular is True


# --- limite de tasa -------------------------------------------------------

class _RespuestaFalsa:
    """Minimo para que urlopen sirva como context manager en la prueba."""

    def __init__(self, cuerpo: bytes):
        self._cuerpo = cuerpo

    def read(self):
        return self._cuerpo

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


def test_un_429_se_reintenta_en_vez_de_dar_el_cliente_por_perdido(monkeypatch):
    # Medido contra la API real: a los diez pedidos seguidos devuelve 429 sin
    # Retry-After. Si se tomara como error definitivo, un padron mediano
    # quedaria con la mitad de los clientes sin consultar y el informe diria
    # que no tienen deuda, que es lo peor que puede pasar.
    import urllib.error

    respuestas = [429, 429, 200]
    dormidas = []

    def urlopen_falso(pedido, timeout=None):
        codigo = respuestas.pop(0)
        if codigo == 429:
            raise urllib.error.HTTPError(pedido.full_url, 429, "Too Many Requests",
                                         {}, None)
        return _RespuestaFalsa(b'{"status": 200, "results": {}}')

    monkeypatch.setattr(bcra.urllib.request, "urlopen", urlopen_falso)
    monkeypatch.setattr(bcra, "_ultimo_pedido", 0.0)

    resultado = bcra.descargar("https://api.bcra.gob.ar/x", dormir=dormidas.append)
    assert resultado["status"] == 200
    assert respuestas == []
    assert any(d >= bcra.ESPERA_TRAS_429 for d in dormidas), "no espero tras el 429"


def test_un_429_que_no_cede_termina_en_error_y_no_en_silencio(monkeypatch):
    import urllib.error

    def urlopen_falso(pedido, timeout=None):
        raise urllib.error.HTTPError(pedido.full_url, 429, "Too Many Requests", {}, None)

    monkeypatch.setattr(bcra.urllib.request, "urlopen", urlopen_falso)
    monkeypatch.setattr(bcra, "_ultimo_pedido", 0.0)

    with pytest.raises(bcra.ErrorBCRA) as e:
        bcra.descargar("https://api.bcra.gob.ar/x", dormir=lambda _: None)
    assert "429" in str(e.value)


def test_los_pedidos_se_espacian_para_no_abusar_del_servicio(monkeypatch):
    import urllib.error

    def urlopen_falso(pedido, timeout=None):
        raise urllib.error.HTTPError(pedido.full_url, 404, "Not Found", {}, None)

    dormidas = []
    monkeypatch.setattr(bcra.urllib.request, "urlopen", urlopen_falso)
    monkeypatch.setattr(bcra, "_ultimo_pedido", 0.0)

    bcra.descargar("https://api.bcra.gob.ar/a", dormir=dormidas.append)
    bcra.descargar("https://api.bcra.gob.ar/b", dormir=dormidas.append)
    assert any(0 < d <= bcra.PAUSA_ENTRE_PEDIDOS for d in dormidas)
