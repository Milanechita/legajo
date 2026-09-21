"""Pruebas del volcado al visor.

Lo que hay que garantizar es que el visor muestre lo mismo que la planilla y
que la nota no diga de mas. Una nota que concluye que un cliente es
sospechoso convierte una inusualidad en una sospecha sin que intervenga una
persona, y eso es exactamente lo que la Res. 56/2024 reserva al criterio
humano.
"""

from __future__ import annotations

import json
from datetime import date

from legajo import exportacion
from legajo.circuito import correr
from legajo.config import Politica
from legajo.fuentes.base import Designado, Padron, VersionLista
from legajo.modelo import Cliente, Documento


def padron_de(*designados: Designado) -> Padron:
    p = Padron()
    p.incorporar(list(designados), VersionLista("OFAC_SDN", None, date.today(),
                                                len(designados), "0" * 64))
    return p


def _corrida_minima():
    padron = padron_de(
        Designado("OFAC_SDN", "36", "ABBAS, Ali Reza", documentos=("PASAPORTE:K1234567",)),
        Designado("OFAC_SDN", "99", "OTRO DESIGNADO CUALQUIERA"),
    )
    clientes = [
        Cliente("CL001", "Alireza Abbas", tipo="PERSONA",
                documentos=[Documento("PASAPORTE", "K1234567")],
                nacionalidad="IRAN", pais_residencia="IRAN"),
        Cliente("CL002", "Marta Gonzalez", tipo="PERSONA",
                documentos=[Documento("DNI", "27998877")],
                nacionalidad="ARGENTINA", pais_residencia="ARGENTINA"),
    ]
    return correr(padron, clientes, politica=Politica())


def _ficha_base(**cambios) -> dict:
    ficha = {
        "tipo": "PERSONA", "estado": "ANALISIS",
        "riesgo": {"nivel": "BAJO", "puntaje": 5, "regimen": "DD_SIMPLIFICADA",
                   "revision_meses": 60},
        "coincidencias": [], "congelamiento": None, "beneficiario": None,
        "pep": None, "alertas": [], "exposicion": 0.0,
    }
    ficha.update(cambios)
    return ficha


# --- la nota -------------------------------------------------------------

def test_la_nota_nunca_afirma_que_una_operacion_es_sospechosa():
    # El sistema no convierte una inusualidad en una sospecha. Si la nota lo
    # hiciera, estaria emitiendo el juicio que la norma le reserva a una
    # persona.
    alerta = {"vencida": False, "monto": 1_000_000.0}
    nota = exportacion.nota_de(_ficha_base(alertas=[alerta]))
    assert "sospechosa" not in nota.lower()
    assert "decidir si la inusualidad se convierte en sospecha" in nota


def test_la_nota_de_un_caso_escalado_no_lo_hace_parecer_de_riesgo_bajo():
    # Un escalado no tiene puntaje. Decir "riesgo SIN_SCORE, 0 puntos" haria
    # leer como inofensivo lo mas grave que produce el circuito.
    ficha = _ficha_base(
        estado="ESCALADO",
        riesgo={"nivel": "SIN_SCORE", "puntaje": 0, "regimen": "", "revision_meses": 0},
    )
    nota = exportacion.nota_de(ficha)
    assert "0 puntos" not in nota
    assert "escalado" in nota


def test_la_nota_avisa_cuando_el_plazo_de_reporte_ya_vencio():
    vencida = {"vencida": True, "monto": 5_000_000.0}
    nota = exportacion.nota_de(_ficha_base(alertas=[vencida]))
    assert "vencido" in nota
    assert "desde la operacion" in nota


def test_la_nota_trata_al_beneficiario_no_identificado_como_impedimento():
    bf = {"identificado": False, "exceptuada": False, "opaco": 1.0,
          "profundidad": 2, "beneficiarios": []}
    nota = exportacion.nota_de(_ficha_base(beneficiario=bf))
    assert "impedimento para operar" in nota


def test_la_nota_de_un_congelamiento_recuerda_la_prohibicion_de_informar():
    cong = {"regimen": "FT", "norma": "Res. UIF 3/2026"}
    nota = exportacion.nota_de(_ficha_base(congelamiento=cong))
    assert "Prohibido informar al cliente" in nota
    assert "24 horas" in nota


def test_la_nota_siempre_termina_en_lo_que_decide_una_persona():
    cong = {"regimen": "FT", "norma": "Res. UIF 3/2026"}
    nota = exportacion.nota_de(_ficha_base(congelamiento=cong))
    assert "Queda a criterio del analista" in nota


def test_un_cliente_sin_nada_pendiente_no_le_inventa_tareas_al_analista():
    nota = exportacion.nota_de(_ficha_base())
    assert "Queda a criterio del analista" not in nota


# --- el volcado ----------------------------------------------------------

def test_el_json_conserva_el_expediente_completo_de_cada_caso():
    # El expediente es el producto. Un volcado que pierde entradas deja al
    # visor mostrando un expediente incompleto, que es peor que no mostrarlo.
    corrida = _corrida_minima()
    datos = exportacion.a_diccionario(corrida)
    por_id = {f["id"]: f for f in datos["clientes"]}
    for caso in corrida.casos:
        assert len(por_id[caso.cliente.cliente_id]["expediente"]) == len(caso.evidencia)


def test_el_volcado_es_json_valido_sin_tipos_del_dominio_sueltos():
    # Si una fecha o un Enum se cuela sin convertir, json.dumps explota. La
    # prueba existe porque el detalle de una evidencia es un diccionario libre
    # y cada etapa nueva mete lo que quiere adentro.
    datos = exportacion.a_diccionario(_corrida_minima())
    assert json.loads(json.dumps(datos, ensure_ascii=False)) == datos


def test_toda_arista_del_grafo_apunta_a_nodos_que_existen():
    datos = exportacion.a_diccionario(_corrida_minima())
    ids = {n["id"] for n in datos["grafo"]["nodos"]}
    for a in datos["grafo"]["aristas"]:
        assert a["origen"] in ids, a
        assert a["destino"] in ids, a


def test_el_grafo_une_al_cliente_con_el_designado_que_le_matcheo():
    datos = exportacion.a_diccionario(_corrida_minima())
    coincidencias = [a for a in datos["grafo"]["aristas"] if a["tipo"] == "COINCIDENCIA"]
    assert any(a["origen"] == "cli:CL001" and a["destino"].startswith("des:OFAC_SDN")
               for a in coincidencias)


def test_el_cliente_limpio_no_queda_unido_a_ningun_designado():
    datos = exportacion.a_diccionario(_corrida_minima())
    tocan_cl002 = [a for a in datos["grafo"]["aristas"]
                   if a["tipo"] == "COINCIDENCIA" and a["origen"] == "cli:CL002"]
    assert tocan_cl002 == []


def test_el_resumen_del_volcado_coincide_con_lo_que_conto_el_circuito():
    corrida = _corrida_minima()
    datos = exportacion.a_diccionario(corrida)
    assert datos["resumen"]["coincidencias"] == len(corrida.screening.coincidencias)
    assert datos["resumen"]["congelamientos"] == len(corrida.congelamientos)


def test_el_js_lleva_los_mismos_datos_que_el_json(tmp_path):
    # El .js existe porque file:// bloquea fetch. Si los dos archivos pudieran
    # quedar desfasados, el visor abierto con doble clic mostraria una corrida
    # distinta a la que se sirve por http.
    ruta, gemelo = exportacion.escribir(_corrida_minima(), tmp_path / "datos.json")
    crudo = gemelo.read_text(encoding="utf-8")
    assert crudo.startswith("window.DATOS = ") and crudo.endswith(";")
    assert json.loads(crudo[len("window.DATOS = "):-1]) == json.loads(
        ruta.read_text(encoding="utf-8"))


def test_la_exposicion_por_cliente_solo_reparte_lo_que_se_puede_atribuir():
    # Los cargos por incumplimiento se liquidan por materia y no por cliente.
    # Repartirlos seria inventar un numero, asi que la suma de lo atribuido
    # nunca puede pasar el total.
    datos = exportacion.a_diccionario(_corrida_minima())
    atribuido = sum(f["exposicion"] for f in datos["clientes"])
    assert atribuido <= datos["exposicion"]["total"]


def test_el_export_de_trabajo_y_la_demo_usan_variables_distintas(tmp_path):
    # El visor prefiere DATOS y cae en DEMO_DATOS. Si los dos definieran la
    # misma variable, publicar la demo en GitHub Pages pisaria la corrida del
    # analista, o peor, una corrida con clientes reales terminaria commiteada
    # bajo el nombre de la demo.
    corrida = _corrida_minima()
    _, trabajo = exportacion.escribir(corrida, tmp_path / "datos.json")
    _, demo = exportacion.escribir(corrida, tmp_path / "demo.json", "DEMO_DATOS")
    assert trabajo.read_text(encoding="utf-8").startswith("window.DATOS = ")
    assert demo.read_text(encoding="utf-8").startswith("window.DEMO_DATOS = ")
