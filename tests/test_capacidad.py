"""Pruebas de la capacidad economica documentada.

El error que estas pruebas existen para impedir es el mas caro del modulo:
sumar el balance de una sociedad a la capacidad de la persona que la integra.
Eso sobreestima por un orden de magnitud y produce un falso negativo justo en
el caso que mas importa, el que usa una sociedad para justificar movimientos
propios.
"""

from __future__ import annotations

from datetime import date

from legajo.capacidad import Capacidad, MotivoNoComputa, calcular
from legajo.modelo import Cliente
from legajo.procedencia import LegajoCliente, Periodicidad, Respaldo

HOY = date(2026, 9, 22)


def persona(cid="CL001") -> Cliente:
    return Cliente(cliente_id=cid, nombre="Sofia Ramirez", tipo="PERSONA")


def sociedad(cid="CL900") -> Cliente:
    return Cliente(cliente_id=cid, nombre="Nodo Sur S.A.S.", tipo="ENTIDAD")


def legajo_con(*respaldos: Respaldo, cliente_id="CL001") -> LegajoCliente:
    legajo = LegajoCliente(cliente_id)
    for r in respaldos:
        legajo.agregar_respaldo(r)
    return legajo


def recibo(monto=3_000_000.0, hasta=date(2026, 8, 31), cid="CL001") -> Respaldo:
    return Respaldo(cid, "RECIBO_SUELDO", emitido=date(2026, 9, 5), monto=monto,
                    periodicidad=Periodicidad.MENSUAL,
                    periodo_desde=date(2026, 8, 1), periodo_hasta=hasta)


def balance(monto=180_000_000.0, cid="CL001", referencia="Nodo Sur S.A.S.") -> Respaldo:
    return Respaldo(cid, "BALANCE", emitido=date(2026, 9, 15), monto=monto,
                    periodicidad=Periodicidad.ANUAL,
                    periodo_desde=date(2025, 1, 1), periodo_hasta=date(2025, 12, 31),
                    referencia=referencia)


def escritura(monto=200_000_000.0, cid="CL001") -> Respaldo:
    return Respaldo(cid, "ESCRITURA", emitido=date(2026, 5, 20), monto=monto,
                    periodicidad=Periodicidad.UNICA,
                    periodo_desde=date(2026, 5, 18), periodo_hasta=date(2026, 5, 18))


# --- el error que hay que impedir -----------------------------------------

def test_el_balance_de_una_sociedad_no_suma_a_la_capacidad_de_su_socio():
    # Sumarlo daria $216.000.000 de capacidad donde hay $36.000.000. Un cliente
    # que opera $100.000.000 quedaria "dentro de su capacidad" sin haber
    # documentado nada que lo explique.
    c = calcular(persona(), legajo_con(recibo(), balance()))
    assert c.capacidad_anual == 36_000_000
    assert c.respaldo_puntual == 0


def test_el_descarte_del_balance_dice_primero_lo_que_el_documento_si_acredita():
    # Descartar en silencio le haria creer al analista que el papel no vale
    # nada. Acredita algo real, aunque no sea lo que se esta midiendo.
    c = calcular(persona(), legajo_con(balance()))
    [d] = c.descartados
    assert d.motivo is MotivoNoComputa.DE_UN_TERCERO
    assert "acredita que Nodo Sur S.A.S. existe y opero" in d.mensaje
    assert "180,000,000" in d.mensaje


def test_el_descarte_del_balance_dice_tambien_que_documento_falta():
    # El mensaje tiene que terminar en algo accionable, no en un no.
    c = calcular(persona(), legajo_con(balance()))
    [d] = c.descartados
    assert "No acredita capacidad personal" in d.mensaje
    assert "distribucion de utilidades o de retiro" in d.mensaje


def test_el_mismo_balance_si_acredita_la_capacidad_de_la_sociedad():
    # El documento no es malo. Esta en el legajo equivocado.
    c = calcular(sociedad("CL900"),
                 legajo_con(balance(cid="CL900"), cliente_id="CL900"))
    assert c.capacidad_anual == 180_000_000
    assert c.descartados == ()


# --- flujo contra stock ----------------------------------------------------

def test_un_recibo_mensual_se_anualiza_por_doce():
    c = calcular(persona(), legajo_con(recibo(3_000_000)))
    assert c.capacidad_anual == 36_000_000


def test_la_venta_de_un_inmueble_no_entra_en_la_capacidad_anual():
    # Quien vendio una casa en $200.000.000 tiene esa plata una vez, no por
    # anio. Anualizarla multiplicaria por la nada.
    c = calcular(persona(), legajo_con(escritura()))
    assert c.capacidad_anual == 0
    assert c.respaldo_puntual == 200_000_000


def test_las_dos_cifras_no_se_mezclan():
    # Es lo que permite distinguir un exceso sostenido de un pico explicable
    # por una venta puntual. Con una sola cifra, el item 3.2 no puede.
    c = calcular(persona(), legajo_con(recibo(), escritura()))
    assert c.capacidad_anual == 36_000_000
    assert c.respaldo_puntual == 200_000_000


def test_dos_recibos_de_dos_empleadores_suman():
    # Mismo titular, misma naturaleza, misma clase. Ahi si se suma.
    c = calcular(persona(), legajo_con(recibo(3_000_000), recibo(1_500_000)))
    assert c.capacidad_anual == 54_000_000


# --- confiabilidad, sin coeficientes --------------------------------------

def test_la_certificacion_de_contador_computa_marcada_como_derivada():
    # Computa, porque es un documento valido. Queda marcada porque el contador
    # la firma en buena parte sobre lo que le conto el cliente.
    cert = Respaldo("CL001", "CERTIFICACION_INGRESOS", emitido=date(2026, 9, 1),
                    monto=4_000_000, periodicidad=Periodicidad.MENSUAL,
                    periodo_hasta=date(2026, 8, 31))
    c = calcular(persona(), legajo_con(cert))
    assert c.capacidad_anual == 48_000_000
    assert c.derivado_de_declarado == 48_000_000
    assert c.proporcion_derivada == 1.0


def test_el_recibo_de_sueldo_no_es_derivado_de_lo_declarado():
    c = calcular(persona(), legajo_con(recibo()))
    assert c.derivado_de_declarado == 0
    assert c.proporcion_derivada == 0.0


def test_la_proporcion_derivada_permite_el_segundo_hallazgo():
    # Una cosa es exceder la capacidad documentada, y otra que esa capacidad
    # se apoye casi entera en papeles que no se cruzan contra un tercero.
    cert = Respaldo("CL001", "CERTIFICACION_INGRESOS", emitido=date(2026, 9, 1),
                    monto=9_000_000, periodicidad=Periodicidad.MENSUAL,
                    periodo_hasta=date(2026, 8, 31))
    c = calcular(persona(), legajo_con(recibo(1_000_000), cert))
    assert c.capacidad_anual == 120_000_000
    assert c.proporcion_derivada == 0.9


def test_ningun_monto_se_multiplica_por_un_coeficiente_de_confiabilidad():
    # La confiabilidad viaja con la cifra, no la modifica. Un coeficiente
    # seria un numero inventado y ademas no arreglaria la titularidad.
    cert = Respaldo("CL001", "CERTIFICACION_INGRESOS", emitido=date(2026, 9, 1),
                    monto=4_000_000, periodicidad=Periodicidad.MENSUAL,
                    periodo_hasta=date(2026, 8, 31))
    c = calcular(persona(), legajo_con(cert))
    assert c.capacidad_anual == 4_000_000 * 12


# --- antiguedad, expuesta y no aplicada -----------------------------------

def test_un_respaldo_viejo_computa_igual_y_se_ve_que_es_viejo():
    # Cortar en doce meses inventaria el umbral exacto que el proyecto evita, y
    # dejaria en cero a un cliente con documentacion vieja, igual que a uno sin
    # documentacion. No son lo mismo.
    viejo = recibo(3_000_000, hasta=date(2019, 8, 31))
    c = calcular(persona(), legajo_con(viejo))
    assert c.capacidad_anual == 36_000_000
    assert c.antiguedad_maxima_en_meses(HOY) > 84


def test_la_composicion_expone_la_fecha_de_cada_respaldo_computado():
    c = calcular(persona(), legajo_con(recibo(), escritura()))
    filas = c.composicion(HOY)
    assert len(filas) == 2
    assert [f["tipo"] for f in filas] == ["RECIBO_SUELDO", "ESCRITURA"]
    assert all("fecha_dato" in f and "antiguedad_meses" in f for f in filas)


def test_sin_computos_no_hay_antiguedad_que_reportar():
    c = calcular(persona(), legajo_con())
    assert c.antiguedad_maxima_en_meses(HOY) is None
    assert not c.documentada


# --- descartes que no son hallazgos ---------------------------------------

def test_un_estatuto_no_suma_ni_es_un_problema():
    estatuto = Respaldo("CL900", "ESTATUTO", emitido=date(2020, 1, 1))
    c = calcular(sociedad("CL900"), legajo_con(estatuto, cliente_id="CL900"))
    [d] = c.descartados
    assert d.motivo is MotivoNoComputa.NO_ACREDITA_CAPACIDAD
    assert "No suma ni resta" in d.mensaje


def test_un_documento_sin_monto_no_computa_pero_tampoco_acusa():
    sin_monto = Respaldo("CL001", "RECIBO_SUELDO", emitido=date(2026, 9, 5),
                         periodicidad=Periodicidad.MENSUAL)
    c = calcular(persona(), legajo_con(sin_monto))
    [d] = c.descartados
    assert d.motivo is MotivoNoComputa.SIN_MONTO
    assert "tampoco es un hallazgo" in d.mensaje


def test_un_tipo_fuera_del_catalogo_lo_dice_en_vez_de_ignorarlo():
    raro = Respaldo("CL001", "PAPEL_CUALQUIERA", emitido=date(2026, 1, 1),
                    monto=5_000_000)
    c = calcular(persona(), legajo_con(raro))
    [d] = c.descartados
    assert d.motivo is MotivoNoComputa.FUERA_DEL_CATALOGO
    assert c.capacidad_anual == 0


def test_un_cliente_sin_legajo_tiene_capacidad_cero_y_no_revienta():
    c = calcular(persona(), None)
    assert c.capacidad_anual == 0
    assert c.respaldo_puntual == 0
    assert not c.documentada
