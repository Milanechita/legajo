"""Pruebas de la procedencia de los datos.

Lo que hay que garantizar es que el programa nunca confunda lo que el cliente
dijo con lo que se pudo verificar, y que una discrepancia sea una discrepancia
y no un campo que el cliente jamas completo.
"""

from __future__ import annotations

import dataclasses
from datetime import date

import pytest

from legajo.modelo import Cliente
from legajo.procedencia import (
    ORDEN_DE_PRECEDENCIA, Campo, Constatacion, LegajoCliente, Origen,
    Periodicidad, RegistroLegajos, Respaldo, Resultado, normalizar_campo,
)

HOY = date(2026, 9, 21)


def cliente(**cambios) -> Cliente:
    base = dict(cliente_id="CL001", nombre="Juan Pérez", tipo="PERSONA",
                nacionalidad="ARGENTINA", pais_residencia="ARGENTINA",
                actividad="Comercio minorista")
    base.update(cambios)
    return Cliente(**base)


def constatacion(campo: Campo, valor: str, origen=Origen.ARCA,
                 cuando: date = HOY, cliente_id: str = "CL001") -> Constatacion:
    return Constatacion(cliente_id=cliente_id, campo=campo, valor=valor,
                        origen=origen, fecha_consulta=cuando)


# --- el contrato entre Campo y Cliente -----------------------------------

def test_todo_campo_constatable_existe_en_cliente():
    # Es la prueba que justifica que Campo sea una enumeracion cerrada en vez
    # de un string libre. Si alguien renombra un campo de Cliente, esto tiene
    # que romper aca y no dejar el cotejo comparando contra None en silencio.
    atributos = {f.name for f in dataclasses.fields(Cliente)}
    for campo in Campo:
        assert campo.value in atributos, (
            f"Campo.{campo.name} apunta a '{campo.value}', que ya no existe "
            f"en Cliente"
        )


def test_todo_campo_constatable_tiene_su_normalizador():
    # Un campo sin normalizador reventaria recien al cotejarlo, con un cliente
    # real adelante.
    for campo in Campo:
        assert normalizar_campo(campo, "algo") is not None


# --- los tres resultados --------------------------------------------------

def test_el_dato_que_coincide_no_es_hallazgo():
    legajo = LegajoCliente("CL001")
    legajo.constatar(constatacion(Campo.ACTIVIDAD, "Comercio minorista"))
    cotejo = legajo.cotejar(cliente(), Campo.ACTIVIDAD)
    assert cotejo.resultado is Resultado.COINCIDE
    assert not cotejo.es_hallazgo


def test_la_actividad_inscripta_distinta_de_la_declarada_es_discrepancia():
    legajo = LegajoCliente("CL001")
    legajo.constatar(constatacion(Campo.ACTIVIDAD, "Servicios financieros"))
    cotejo = legajo.cotejar(cliente(), Campo.ACTIVIDAD)
    assert cotejo.resultado is Resultado.DISCREPA
    assert cotejo.es_hallazgo


def test_un_campo_que_el_cliente_no_declaro_se_completa_y_no_discrepa():
    # Es la distincion que pidio el ajuste 2. Un cliente que nunca declaro la
    # actividad no contradijo nada: la fuente aporta un dato, no descubre una
    # mentira. Mezclarlos infla las discrepancias con ruido.
    legajo = LegajoCliente("CL001")
    legajo.constatar(constatacion(Campo.ACTIVIDAD, "Servicios financieros"))
    cotejo = legajo.cotejar(cliente(actividad=None), Campo.ACTIVIDAD)
    assert cotejo.resultado is Resultado.COMPLETA
    assert not cotejo.es_hallazgo


def test_los_completados_no_aparecen_entre_las_discrepancias():
    legajo = LegajoCliente("CL001")
    legajo.constatar(constatacion(Campo.ACTIVIDAD, "Servicios financieros"))
    legajo.constatar(constatacion(Campo.NACIONALIDAD, "BRASIL"))
    sin_declarar = cliente(actividad=None, nacionalidad="ARGENTINA")

    discrepancias = {c.campo for c in legajo.discrepancias(sin_declarar)}
    completados = {c.campo for c in legajo.completados(sin_declarar)}
    assert discrepancias & completados == set()
    assert Campo.ACTIVIDAD in completados
    assert Campo.NACIONALIDAD in discrepancias


# --- normalizacion --------------------------------------------------------

def test_el_mismo_pais_escrito_distinto_no_es_discrepancia():
    # "Iran" contra "IRAN" contra "IR" son el mismo pais. Sin normalizar, cada
    # fuente que escribe distinto genera una discrepancia falsa.
    legajo = LegajoCliente("CL001")
    legajo.constatar(constatacion(Campo.PAIS_RESIDENCIA, "Argentina"))
    cotejo = legajo.cotejar(cliente(pais_residencia="ARGENTINA"), Campo.PAIS_RESIDENCIA)
    assert cotejo.resultado is Resultado.COINCIDE


def test_el_mismo_nombre_con_tildes_y_puntos_no_es_discrepancia():
    legajo = LegajoCliente("CL001")
    legajo.constatar(constatacion(Campo.NOMBRE, "JUAN PEREZ"))
    cotejo = legajo.cotejar(cliente(nombre="Juan Pérez"), Campo.NOMBRE)
    assert cotejo.resultado is Resultado.COINCIDE


def test_la_hora_de_una_fecha_no_la_convierte_en_otro_dia():
    legajo = LegajoCliente("CL001")
    legajo.constatar(constatacion(Campo.FECHA_NACIMIENTO, "1980-05-12T00:00:00"))
    cotejo = legajo.cotejar(cliente(fecha_nacimiento="1980-05-12"),
                            Campo.FECHA_NACIMIENTO)
    assert cotejo.resultado is Resultado.COINCIDE


# --- precedencia y append-only -------------------------------------------

def test_cuando_dos_fuentes_se_contradicen_gana_la_de_mayor_precedencia():
    legajo = LegajoCliente("CL001")
    legajo.constatar(constatacion(Campo.ACTIVIDAD, "Lo que dijo el informe",
                                  origen=Origen.INFORME_COMERCIAL))
    legajo.constatar(constatacion(Campo.ACTIVIDAD, "Lo que dice ARCA",
                                  origen=Origen.ARCA))
    assert legajo.vigente(Campo.ACTIVIDAD).origen is Origen.ARCA


def test_entre_dos_del_mismo_origen_gana_la_mas_reciente():
    # Asi es como una correccion tapa a la anterior sin borrarla.
    legajo = LegajoCliente("CL001")
    legajo.constatar(constatacion(Campo.ACTIVIDAD, "vieja", cuando=date(2026, 1, 10)))
    legajo.constatar(constatacion(Campo.ACTIVIDAD, "nueva", cuando=date(2026, 9, 1)))
    assert legajo.vigente(Campo.ACTIVIDAD).valor == "nueva"


def test_corregir_un_dato_no_borra_la_constatacion_anterior():
    # El legajo es append-only por el mismo motivo que el expediente: ante una
    # inspeccion hay que poder mostrar que se verifico y cuando, no solo el
    # estado final.
    legajo = LegajoCliente("CL001")
    legajo.constatar(constatacion(Campo.ACTIVIDAD, "vieja", cuando=date(2026, 1, 10)))
    legajo.constatar(constatacion(Campo.ACTIVIDAD, "nueva", cuando=date(2026, 9, 1)))
    assert len(legajo.historial(Campo.ACTIVIDAD)) == 2
    assert [c.valor for c in legajo.historial(Campo.ACTIVIDAD)] == ["vieja", "nueva"]


def test_el_legajo_no_expone_una_lista_que_se_pueda_vaciar_desde_afuera():
    legajo = LegajoCliente("CL001")
    legajo.constatar(constatacion(Campo.ACTIVIDAD, "algo"))
    with pytest.raises(AttributeError):
        legajo.constataciones.clear()
    assert len(legajo) == 1


def test_el_orden_de_precedencia_cubre_todos_los_origenes():
    # Un origen fuera del orden no tendria peso y reventaria al cotejar.
    assert set(ORDEN_DE_PRECEDENCIA) == set(Origen)


def test_una_constatacion_de_otro_cliente_no_entra_al_legajo():
    legajo = LegajoCliente("CL001")
    with pytest.raises(ValueError):
        legajo.constatar(constatacion(Campo.ACTIVIDAD, "x", cliente_id="CL999"))


# --- respaldos ------------------------------------------------------------

def test_un_recibo_mensual_y_un_balance_anual_no_acreditan_lo_mismo():
    # Es el ajuste 4. Sin periodicidad, $900.000 de un recibo y $900.000 de un
    # balance se sumarian igual y la capacidad anual saldria mal.
    assert Periodicidad.MENSUAL.factor_anual == 12
    assert Periodicidad.ANUAL.factor_anual == 1


def test_un_ingreso_de_unica_vez_no_se_anualiza_solo():
    # La venta de un inmueble no es ingreso anual. Cuanto pesa un ingreso de
    # unica vez es una regla por tipo de documento y se decide en el item 3.1.
    assert Periodicidad.UNICA.factor_anual is None


def test_un_respaldo_sin_vencimiento_declarado_se_considera_vigente():
    respaldo = Respaldo("CL001", "ESCRITURA", emitido=date(2020, 1, 1))
    assert respaldo.vigente(HOY)


def test_un_respaldo_vencido_deja_de_estar_vigente():
    respaldo = Respaldo("CL001", "RECIBO_SUELDO", emitido=date(2026, 1, 1),
                        vence=date(2026, 7, 1))
    assert not respaldo.vigente(HOY)


def test_el_legajo_separa_los_respaldos_vigentes_de_los_vencidos():
    legajo = LegajoCliente("CL001")
    legajo.agregar_respaldo(Respaldo("CL001", "RECIBO_SUELDO", date(2026, 8, 1),
                                     monto=900_000, periodicidad=Periodicidad.MENSUAL))
    legajo.agregar_respaldo(Respaldo("CL001", "RECIBO_SUELDO", date(2025, 1, 1),
                                     vence=date(2025, 7, 1)))
    assert len(legajo.respaldos) == 2
    assert len(legajo.respaldos_vigentes(HOY)) == 1


# --- el registro ----------------------------------------------------------

def test_un_cliente_sin_legajo_devuelve_uno_vacio_y_no_un_error():
    # Un cliente al que todavia no se le constato nada no es un error. Si
    # devolviera None, cada punto del codigo tendria que preguntarlo.
    registro = RegistroLegajos()
    legajo = registro.de("CL404")
    assert legajo.cliente_id == "CL404"
    assert len(legajo) == 0


def test_el_registro_devuelve_siempre_el_mismo_legajo_para_un_cliente():
    registro = RegistroLegajos()
    registro.de("CL001").constatar(constatacion(Campo.ACTIVIDAD, "algo"))
    assert len(registro.de("CL001")) == 1


def test_un_cliente_sin_constataciones_no_tiene_cotejos():
    legajo = LegajoCliente("CL001")
    assert legajo.cotejos(cliente()) == []
    assert legajo.cotejar(cliente(), Campo.NOMBRE) is None
