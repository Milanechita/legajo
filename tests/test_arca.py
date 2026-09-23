"""Pruebas del importador de constancias de ARCA y del cotejo que habilita.

El item 3.4 es el que pone a prueba el modelo de procedencia del 1.1: si esta
bien puesto, comparar la actividad declarada contra la inscripta no necesita
codigo propio, sale de cotejar. Salio asi, y de paso mostro que comparar texto
libre no sirve.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from legajo.io_planilla import leer_arca, leer_padron
from legajo.procedencia import Campo, Origen, RegistroLegajos, Resultado

EJEMPLOS = Path(__file__).resolve().parent.parent / "ejemplos"
ARCA = EJEMPLOS / "arca_ar.csv"


def padron():
    return {c.cliente_id: c for c in leer_padron(EJEMPLOS / "clientes_ar.csv")}


# --- el importador --------------------------------------------------------

def test_cada_constancia_produce_constataciones_con_origen_arca():
    registro = leer_arca(ARCA)
    legajo = registro.de("AR016")
    assert len(legajo) >= 2
    assert all(c.origen is Origen.ARCA for c in legajo.constataciones)


def test_la_constatacion_guarda_cuando_se_consulto():
    # Sin la fecha, "ARCA dice que es RI" no dice nada: puede ser de hoy o de
    # hace dos anios.
    legajo = leer_arca(ARCA).de("AR016")
    assert all(c.fecha_consulta == date(2026, 9, 20) for c in legajo.constataciones)


def test_una_fila_sin_fecha_de_consulta_se_descarta(tmp_path):
    ruta = tmp_path / "arca.csv"
    ruta.write_text(
        "cliente_id,cuit,consultado,condicion_iva,actividad_codigo\n"
        "CL001,20990000019,2026-09-20,RI,620100\n"
        "CL002,27990000021,,RI,620100\n",
        encoding="utf-8")
    registro = leer_arca(ruta)
    assert len(registro.de("CL001")) == 2
    assert len(registro.de("CL002")) == 0


def test_las_constancias_se_acumulan_sobre_el_legajo_que_ya_existe():
    # Dos registros paralelos por cliente, uno con respaldos y otro con
    # constataciones, se despegan solos.
    from legajo.io_planilla import leer_respaldos
    registro = leer_respaldos(EJEMPLOS / "respaldos_ar.csv")
    leer_arca(ARCA, registro)
    legajo = registro.de("AR016")
    assert len(legajo.respaldos) >= 1
    assert len(legajo.constataciones) >= 1


def test_el_padron_no_se_toca_al_importar():
    # El padron sigue siendo lo que declaro el cliente. Lo de ARCA entra
    # aparte, y compararlos es lo que produce la discrepancia.
    antes = padron()["AR016"].actividad_codigo
    leer_arca(ARCA)
    assert padron()["AR016"].actividad_codigo == antes


# --- el cotejo ------------------------------------------------------------

def test_el_cambio_de_actividad_sale_como_hallazgo_afirmable():
    # AR016 se dio de alta con 477320 y ARCA hoy dice 649999. Cambio de rubro
    # y no lo informo.
    registro = leer_arca(ARCA)
    cliente = padron()["AR016"]
    campos = {c.campo for c in registro.de("AR016").hallazgos(cliente)}
    assert Campo.ACTIVIDAD_CODIGO in campos


def test_la_condicion_de_iva_distinta_sale_como_hallazgo():
    registro = leer_arca(ARCA)
    cliente = padron()["AR005"]
    campos = {c.campo for c in registro.de("AR005").hallazgos(cliente)}
    assert Campo.CONDICION_IVA in campos


def test_comparar_texto_libre_da_muchos_mas_falsos_que_el_codigo():
    # Es la medicion que corrigio el diseno. Sobre las constancias de ejemplo,
    # el texto marca diez diferencias y solo tres son cambios reales. El
    # codigo marca esas tres y ninguna de mas.
    registro = leer_arca(ARCA)
    clientes = padron()

    por_texto = por_codigo = 0
    for legajo in registro.existentes():
        cliente = clientes[legajo.cliente_id]
        for d in legajo.discrepancias(cliente):
            if d.campo is Campo.ACTIVIDAD:
                por_texto += 1
            elif d.campo is Campo.ACTIVIDAD_CODIGO:
                por_codigo += 1

    assert por_texto == 10
    assert por_codigo == 3
    assert por_texto > por_codigo * 3, "si esto deja de valer, revisar el diseno"


def test_las_diferencias_de_texto_no_contaminan_los_hallazgos():
    registro = leer_arca(ARCA)
    clientes = padron()
    for legajo in registro.existentes():
        cliente = clientes[legajo.cliente_id]
        campos = {c.campo for c in legajo.hallazgos(cliente)}
        assert Campo.ACTIVIDAD not in campos
        assert Campo.NOMBRE not in campos


def test_un_cliente_que_no_declaro_actividad_la_completa_y_no_discrepa():
    # AR003 no tenia codigo al alta. ARCA lo trae: es informacion nueva, no una
    # contradiccion.
    registro = leer_arca(ARCA)
    cliente = padron()["AR003"]
    cotejo = registro.de("AR003").cotejar(cliente, Campo.ACTIVIDAD_CODIGO)
    assert cotejo.resultado is Resultado.COMPLETA
    assert not cotejo.es_hallazgo


def test_el_cotejo_no_necesito_codigo_propio_para_el_item_34():
    # La prueba que valida el modelo de 1.1: la comparacion "actividad
    # declarada contra inscripta" sale de cotejar, sin una regla dedicada.
    from legajo import procedencia
    assert not hasattr(procedencia, "comparar_actividad")
    registro = leer_arca(ARCA)
    assert registro.de("AR016").cotejar(padron()["AR016"], Campo.ACTIVIDAD_CODIGO)
