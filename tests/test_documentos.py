"""Pruebas del catalogo de documentos por sujeto obligado.

La regla que gobierna este archivo: el sistema nunca marca como faltante un
documento que la norma no permite pedir, y nunca afirma que algo es exigible
si no se verifico contra el texto.

El caso que obliga a separar por sujeto obligado son las declaraciones juradas
impositivas. Para un banco estan prohibidas y para una ALYC son exigibles. Es
la misma pregunta con respuesta opuesta.
"""

from __future__ import annotations

import pytest

from legajo import documentos
from legajo.documentos import CATALOGO, Materia, TipoDocumento
from legajo.matriz import MESES_HASTA_REVISION
from legajo.sujeto_obligado import (
    ALYC, BANCO, MESES_ACTUALIZACION_LEGAJO, POR_DEFECTO, Exigibilidad,
    TipoSujetoObligado, de,
)

DDJJ = (TipoDocumento.DDJJ_GANANCIAS,
        TipoDocumento.DDJJ_BIENES_PERSONALES,
        TipoDocumento.DDJJ_IVA)


# --- la diferencia entre banco y ALYC -------------------------------------

def test_la_ddjj_impositiva_esta_prohibida_en_banco_y_es_exigible_en_alyc():
    # Es el caso que justifica todo el modulo. Asumir la regla del banco para
    # los dos deja a la ALYC sin pedir documentacion que la norma le manda, y
    # aplicar la de la ALYC al banco lo hace incumplir.
    for documento in DDJJ:
        assert BANCO.exigibilidad(documento) is Exigibilidad.PROHIBIDO
        assert ALYC.exigibilidad(documento) is Exigibilidad.EXIGIBLE


def test_el_banco_no_puede_requerir_la_ddjj_y_la_alyc_si():
    for documento in DDJJ:
        assert not BANCO.puede_requerir(documento)
        assert ALYC.puede_requerir(documento)


def test_cada_regla_viene_con_la_norma_que_la_respalda():
    # Cuando alguien discuta por que el programa pide o no pide un documento,
    # la respuesta tiene que salir del mismo lugar que la decision.
    assert "78/2025" in BANCO.regla(TipoDocumento.DDJJ_GANANCIAS).norma
    assert "14/2023" in BANCO.regla(TipoDocumento.DDJJ_GANANCIAS).norma
    assert "78/2023" in ALYC.regla(TipoDocumento.DDJJ_GANANCIAS).norma
    assert "art. 33" in ALYC.regla(TipoDocumento.DDJJ_GANANCIAS).norma


def test_la_prohibicion_del_banco_alcanza_a_las_ddjj_y_no_a_toda_la_materia():
    # Una constancia de inscripcion no es una declaracion jurada. Prohibirla
    # dejaria al banco sin poder pedir un documento que la norma no menciona.
    assert BANCO.exigibilidad(TipoDocumento.CONSTANCIA_CUIT) is not Exigibilidad.PROHIBIDO
    assert BANCO.exigibilidad(TipoDocumento.CONSTANCIA_MONOTRIBUTO) is not Exigibilidad.PROHIBIDO


def test_un_documento_prohibido_nunca_figura_entre_los_exigibles():
    # Si estuviera en las dos listas, el checklist del legajo lo pediria y el
    # analista incumpliria por seguir al programa.
    for sujeto in (BANCO, ALYC):
        assert set(sujeto.prohibidos()) & set(sujeto.exigibles()) == set()
    assert TipoDocumento.DDJJ_GANANCIAS in BANCO.prohibidos()
    assert TipoDocumento.DDJJ_GANANCIAS not in BANCO.exigibles()


def test_la_alyc_exige_las_cuatro_materias_del_articulo_33():
    for materia in (Materia.ECONOMICA, Materia.PATRIMONIAL,
                    Materia.FINANCIERA, Materia.TRIBUTARIA):
        documentos_materia = documentos.de_materia(materia)
        assert documentos_materia, f"{materia.value} no tiene documentos"
        for documento in documentos_materia:
            assert ALYC.exigibilidad(documento) is Exigibilidad.EXIGIBLE


def test_lo_que_el_articulo_33_no_nombra_queda_sin_verificar_en_alyc():
    # El art. 33 habla de economica, patrimonial, financiera y tributaria. No
    # dice nada de identidad ni de societaria, asi que el programa tampoco.
    assert ALYC.exigibilidad(TipoDocumento.ESTATUTO) is Exigibilidad.SIN_VERIFICAR
    assert ALYC.exigibilidad(TipoDocumento.DOCUMENTO_IDENTIDAD) is Exigibilidad.SIN_VERIFICAR


# --- lo no verificado ------------------------------------------------------

def test_un_documento_que_no_se_verifico_no_se_da_por_opcional():
    regla = BANCO.regla(TipoDocumento.BALANCE)
    assert regla.exigibilidad is Exigibilidad.SIN_VERIFICAR
    assert regla.exigibilidad is not Exigibilidad.OPCIONAL


def test_lo_no_verificado_se_puede_pedir():
    # Prohibido es solo lo que la norma prohibe expresamente. Tratar como
    # prohibido todo lo no verificado dejaria al analista sin poder pedir nada.
    assert BANCO.puede_requerir(TipoDocumento.BALANCE)


def test_un_documento_fuera_del_catalogo_no_rompe_la_consulta():
    regla = BANCO.regla("INVENTADO_POR_ALGUIEN")
    assert regla.exigibilidad is Exigibilidad.SIN_VERIFICAR


def test_ningun_catalogo_se_declara_completo_todavia():
    # Que ninguno diga estar completo evita que el checklist del item 5.1 se
    # crea exhaustivo antes de tiempo.
    assert not BANCO.catalogo_completo
    assert not ALYC.catalogo_completo


# --- el vocabulario --------------------------------------------------------

def test_todo_documento_del_catalogo_tiene_materia_y_descripcion():
    for tipo, ficha in CATALOGO.items():
        assert ficha.materia in Materia
        assert ficha.descripcion.strip(), tipo


def test_no_se_le_pide_un_estatuto_a_una_persona_humana():
    # Pedirle un estatuto a una persona o un recibo de sueldo a una SRL es
    # ruido que el analista descarta a mano.
    de_persona = documentos.para("PERSONA")
    de_entidad = documentos.para("ENTIDAD")
    assert TipoDocumento.ESTATUTO not in de_persona
    assert TipoDocumento.ESTATUTO in de_entidad
    assert TipoDocumento.RECIBO_SUELDO in de_persona
    assert TipoDocumento.RECIBO_SUELDO not in de_entidad


def test_los_documentos_que_acreditan_capacidad_son_los_de_ingresos_y_patrimonio():
    # Es la lista que va a consumir el item 3.1. Un estatuto prueba quien es la
    # sociedad, no cuanto factura.
    acreditan = documentos.acreditan_capacidad()
    assert TipoDocumento.RECIBO_SUELDO in acreditan
    assert TipoDocumento.BALANCE in acreditan
    assert TipoDocumento.ESCRITURA in acreditan
    assert TipoDocumento.ESTATUTO not in acreditan
    assert TipoDocumento.DOCUMENTO_IDENTIDAD not in acreditan


def test_ningun_documento_tiene_vencimiento_inventado():
    # La norma fija cada cuanto se actualiza el legajo, no cuantos meses vale
    # un recibo. Poner un numero seria marcar vencida documentacion que nadie
    # declaro vencida.
    for tipo, ficha in CATALOGO.items():
        assert ficha.vigencia_meses is None, tipo


# --- actualizacion del legajo ---------------------------------------------

def test_la_cadencia_de_actualizacion_del_legajo_coincide_con_la_del_scoring():
    # Art. 30 de la Res. 78/2023: 1 anio en alto, 3 en medio, 5 en bajo. Es lo
    # mismo que el programa ya calcula para banco. Si una de las dos cambia sin
    # la otra, esta prueba lo agarra.
    assert MESES_ACTUALIZACION_LEGAJO == {"ALTO": 12, "MEDIO": 36, "BAJO": 60}
    assert MESES_ACTUALIZACION_LEGAJO == MESES_HASTA_REVISION


# --- eleccion del sujeto obligado -----------------------------------------

def test_el_sujeto_obligado_por_defecto_es_el_banco():
    assert POR_DEFECTO is BANCO
    assert POR_DEFECTO.resolucion == "Res. UIF 14/2023"


def test_se_elige_por_nombre():
    assert de("BANCO") is BANCO
    assert de("alyc") is ALYC
    assert de(TipoSujetoObligado.ALYC) is ALYC


def test_un_sujeto_obligado_desconocido_falla_y_no_cae_al_banco():
    with pytest.raises(ValueError) as e:
        de("ESCRIBANIA")
    assert "BANCO" in str(e.value) and "ALYC" in str(e.value)


def test_cada_sujeto_obligado_dice_cuando_se_consulto_su_norma():
    for sujeto in (BANCO, ALYC):
        assert sujeto.vigencia_consultada is not None
        assert sujeto.resolucion


def test_los_umbrales_del_banco_son_los_que_ya_estaban_verificados():
    assert BANCO.umbrales.reporte_efectivo == 40.0
