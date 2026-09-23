"""Pruebas del recalculo del riesgo con lo que encontro el monitoreo.

Lo que tienen que garantizar es que el riesgo no sea un trinquete. Si un
elevador se pudiera apilar sobre la evaluacion anterior, un cliente que mejoro
su situacion en el BCRA o que presento el documento que faltaba quedaria en
ALTO para siempre, y nadie se enteraria de que el motivo ya no existe.
"""

from __future__ import annotations

from datetime import date

from legajo.alertas import Alerta
from legajo.modelo import Caso, Cliente, Estado
from legajo.riesgo import evaluar, reevaluar_casos


def cliente(cid="CL001") -> Cliente:
    return Cliente(cliente_id=cid, nombre="Sofia Ramirez", tipo="PERSONA",
                   nacionalidad="ARGENTINA", pais_residencia="ARGENTINA",
                   actividad="Comercio minorista")


def caso(cid="CL001", estado=Estado.ANALISIS) -> Caso:
    c = Caso(caso_id="C00001", cliente=cliente(cid))
    c.estado = estado
    return c


def alerta_capacidad(severidad="ALTA") -> Alerta:
    return Alerta(cliente_id="CL001", codigo="CAPACIDAD_EXCEDIDA",
                  severidad=severidad, descripcion="x", metodologia="y",
                  monto_involucrado=1_000_000, generada=date(2026, 9, 22))


# --- no es un trinquete ---------------------------------------------------

def test_el_riesgo_puede_bajar_cuando_el_hecho_que_lo_elevo_desaparece():
    # Es la prueba que justifica recalcular entero en vez de apilar. Si se
    # apilaran elevadores, este cliente quedaria en ALTO para siempre.
    base = evaluar(cliente())
    assert base.nivel != "ALTO"

    con_hallazgo = evaluar(cliente(), bcra_irregular=True)
    assert con_hallazgo.nivel == "ALTO"

    # El hecho desaparece: mejoro la situacion en el BCRA.
    sin_hallazgo = evaluar(cliente(), bcra_irregular=False)
    assert sin_hallazgo.nivel == base.nivel
    assert "SITUACION_BCRA_IRREGULAR" not in sin_hallazgo.elevadores


def test_la_reevaluacion_baja_el_nivel_y_lo_deja_asentado():
    # El cliente venia en ALTO por el BCRA. Este mes el BCRA no lo informa
    # irregular, pero si cambio de actividad. Al recalcular entero, el
    # elevador viejo no se arrastra y el nuevo aparece.
    c = caso()
    previa = evaluar(cliente(), bcra_irregular=True)
    c.evaluacion = previa
    assert previa.nivel == "ALTO"

    resultado = reevaluar_casos([c], {"CL001": previa},
                                bcra_irregulares=set(),
                                actividades_cambiadas={"CL001"})
    nueva = resultado["CL001"]
    assert "SITUACION_BCRA_IRREGULAR" not in nueva.elevadores
    assert "ACTIVIDAD_CAMBIADA_SIN_INFORMAR" in nueva.elevadores


def test_una_lista_de_alertas_vacia_no_cuenta_como_hallazgo():
    c = caso()
    previa = evaluar(cliente())
    resultado = reevaluar_casos([c], {"CL001": previa}, alertas={"CL001": []})
    assert resultado["CL001"] is previa
    assert c.evidencia == []


def test_los_factores_base_tambien_se_recalculan():
    # No se reusan los de la evaluacion anterior. Un cliente que resolvio su
    # beneficiario final tiene que perder ese elevador.
    from legajo.beneficiario import Beneficiario, Resolucion
    sin_bf = Resolucion(entidad_id="CL900")
    con_bf = Resolucion(entidad_id="CL900", beneficiarios=[
        Beneficiario("P1", "Alguien", 0.6, 0.6, "PARTICIPACION")])

    entidad = Cliente("CL900", "Nodo Sur S.A.S.", tipo="ENTIDAD")
    assert "BENEFICIARIO_NO_IDENTIFICADO" in evaluar(entidad, resolucion=sin_bf).elevadores
    assert "BENEFICIARIO_NO_IDENTIFICADO" not in evaluar(entidad, resolucion=con_bf).elevadores


# --- los cuatro elevadores ------------------------------------------------

def test_los_cuatro_hallazgos_elevan_a_alto():
    for kwargs in ({"congelado": True},
                   {"alertas": [alerta_capacidad()]},
                   {"bcra_irregular": True},
                   {"actividad_cambiada": True}):
        assert evaluar(cliente(), **kwargs).nivel == "ALTO", kwargs


def test_ninguno_suma_puntos():
    # Elevan el piso, no ponderan. Ponderarlos exigiria inventar cuanto vale
    # cada uno, y el proyecto ya tiene dos cortes sin calibrar.
    base = evaluar(cliente())
    con_todo = evaluar(cliente(), congelado=True, bcra_irregular=True,
                       actividad_cambiada=True, alertas=[alerta_capacidad()])
    assert con_todo.puntaje == base.puntaje
    assert con_todo.nivel == "ALTO"


def test_una_alerta_de_capacidad_media_no_eleva():
    # Solo la severidad ALTA, cuyo corte sale del umbral de reporte. La MEDIA
    # tiene un corte discutible y elevaria por ruido.
    assert evaluar(cliente(), alertas=[alerta_capacidad("MEDIA")]).nivel != "ALTO"


def test_el_elevador_queda_escrito_en_la_evaluacion():
    # Si no figurara, el informe y el visor no podrian mostrar por que el
    # cliente quedo en ALTO.
    ev = evaluar(cliente(), bcra_irregular=True)
    assert "SITUACION_BCRA_IRREGULAR" in ev.elevadores


# --- el registro no se puede saltear --------------------------------------

def test_cambiar_la_evaluacion_deja_siempre_una_entrada_en_el_expediente():
    # Misma relacion que hay entre estado y transicionar: el valor actual y el
    # registro se escriben juntos.
    c = caso()
    c.evaluacion = evaluar(cliente())
    antes = len(c.evidencia)

    assert c.reevaluar(evaluar(cliente(), bcra_irregular=True), "x", "motivo")
    assert len(c.evidencia) == antes + 1
    assert c.evidencia[-1].accion == "REEVALUACION_EBR"
    assert c.evidencia[-1].detalle["nivel"] == "ALTO"
    assert c.evidencia[-1].detalle["nivel_anterior"] != "ALTO"


def test_una_reevaluacion_identica_no_ensucia_el_expediente():
    # Apendear lo mismo en cada corrida convierte el expediente en un latido
    # en vez de un registro de cambios.
    c = caso()
    ev = evaluar(cliente())
    c.evaluacion = ev
    antes = len(c.evidencia)
    assert not c.reevaluar(evaluar(cliente()), "x", "motivo")
    assert len(c.evidencia) == antes


def test_el_puntaje_del_alta_sigue_en_el_expediente_despues_de_recalcular():
    # Es lo que hace innecesario un segundo campo. Una inspeccion que pregunte
    # por que el cliente entro como BAJO lo encuentra en el log.
    c = caso()
    c.evaluacion = evaluar(cliente())
    nivel_alta = c.evaluacion.nivel
    c.reevaluar(evaluar(cliente(), congelado=True), "x", "motivo")
    assert c.evaluacion.nivel == "ALTO"
    assert c.evidencia[-1].detalle["nivel_anterior"] == nivel_alta


# --- a quien se reevalua --------------------------------------------------

def test_un_caso_escalado_no_se_scorea_al_recalcular():
    # Un caso que se escalo por coincidencia en lista critica no baja a un
    # tramo porque el monitoreo salio limpio.
    c = caso(estado=Estado.ESCALADO)
    resultado = reevaluar_casos([c], {}, actividades_cambiadas={"CL001"})
    assert "CL001" not in resultado
    assert c.evaluacion is None


def test_sin_hallazgos_no_se_toca_a_nadie():
    c = caso()
    previa = evaluar(cliente())
    resultado = reevaluar_casos([c], {"CL001": previa})
    assert resultado == {"CL001": previa}
    assert c.evidencia == []


# --- la periodicidad sigue al nivel ---------------------------------------

def test_subir_de_nivel_acorta_la_revision_del_legajo():
    # Art. 30 de la Res. 78/2023: 1 anio en alto, 3 en medio, 5 en bajo. Sale
    # solo porque nadie guarda la periodicidad, se deriva del nivel.
    base = evaluar(cliente())
    elevado = evaluar(cliente(), congelado=True)
    assert base.meses_hasta_revision == 60
    assert elevado.meses_hasta_revision == 12


def test_seguir_en_alto_por_otro_motivo_cuenta_como_cambio():
    # Si la comparacion mirara solo el nivel y el puntaje, el expediente
    # seguiria diciendo que el cliente esta en ALTO por el BCRA cuando el BCRA
    # ya esta limpio y lo que cambio es la actividad. El analista iria a mirar
    # el lugar equivocado.
    c = caso()
    c.evaluacion = evaluar(cliente(), bcra_irregular=True)
    nueva = evaluar(cliente(), actividad_cambiada=True)

    assert c.evaluacion.nivel == nueva.nivel == "ALTO"
    assert c.evaluacion.puntaje == nueva.puntaje
    assert c.reevaluar(nueva, "x", "motivo"), "el motivo cambio, es un cambio"
    assert c.evaluacion.elevadores == ["ACTIVIDAD_CAMBIADA_SIN_INFORMAR"]
