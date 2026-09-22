"""Pruebas de la regla que compara la capacidad documentada contra lo operado.

Es la pregunta central del proyecto. Lo que estas pruebas garantizan es que la
regla no confunda dos cosas distintas: un cliente que no puede justificar lo
que opera, y un cliente al que nadie le cargo los papeles. El segundo es un
legajo incompleto y le toca al item 5.1.
"""

from __future__ import annotations

from datetime import date, timedelta

from legajo.alertas import monitorear
from legajo.capacidad import calcular
from legajo.config import ParametrosMonitoreo, parametros_con_listas
from legajo.modelo import Cliente
from legajo.operaciones import Operacion, Operatoria
from legajo.procedencia import LegajoCliente, Periodicidad, Respaldo

INICIO = date(2026, 1, 15)
# El umbral de reporte real sale de los 40 SMVM, no del dataclass pelado:
# PARAMETROS_POR_DEFECTO lo deja en cero y eso apaga el corte de severidad.
PARAMETROS = parametros_con_listas()


def cliente() -> Cliente:
    return Cliente(cliente_id="CL001", nombre="Sofia Ramirez", tipo="PERSONA")


def operatoria(total: float, meses: float = 6, cantidad: int = 12) -> Operatoria:
    # El paso se calcula para que el lapso entre la primera y la ultima sea de
    # `meses` meses. Con 30 dias exactos la ventana queda apenas corta y el
    # minimo para anualizar la descarta, que es un fallo de la prueba y no de
    # la regla.
    paso = timedelta(days=meses * 30.44 / max(cantidad - 1, 1))
    return Operatoria(cliente_id="CL001", operaciones=[
        Operacion(cliente_id="CL001", fecha=INICIO + paso * i, monto=total / cantidad)
        for i in range(cantidad)
    ])


def legajo(*respaldos: Respaldo) -> LegajoCliente:
    l = LegajoCliente("CL001")
    for r in respaldos:
        l.agregar_respaldo(r)
    return l


def recibo(mensual: float) -> Respaldo:
    return Respaldo("CL001", "RECIBO_SUELDO", emitido=date(2026, 6, 5),
                    monto=mensual, periodicidad=Periodicidad.MENSUAL,
                    periodo_hasta=date(2026, 5, 31))


def venta(monto: float) -> Respaldo:
    return Respaldo("CL001", "ESCRITURA", emitido=date(2026, 3, 20), monto=monto,
                    periodicidad=Periodicidad.UNICA,
                    periodo_hasta=date(2026, 3, 18))


def correr(op, leg, parametros=PARAMETROS):
    cap = {"CL001": calcular(cliente(), leg)} if leg is not None else None
    alertas = monitorear({"CL001": op}, {}, parametros,
                         clientes={"CL001": cliente()}, capacidades=cap)
    return [a for a in alertas.get("CL001", []) if a.codigo == "CAPACIDAD_EXCEDIDA"]


# --- dispara cuando corresponde -------------------------------------------

def test_operar_muy_por_encima_de_lo_documentado_alerta():
    # Documenta $500.000 por mes, o sea $6.000.000 anuales. En seis meses eso
    # justifica $3.000.000. Opero $80.000.000.
    [a] = correr(operatoria(80_000_000, meses=6), legajo(recibo(500_000)))
    assert a.severidad == "ALTA"
    assert "sin respaldo documental" in a.descripcion


def test_el_excedente_es_lo_que_queda_sin_justificar_y_no_el_total():
    # Si el monto fuera el total operado, la exposicion sancionatoria contaria
    # tambien la parte que el cliente si justifico.
    [a] = correr(operatoria(80_000_000, meses=6), legajo(recibo(500_000)))
    assert a.monto_involucrado < 80_000_000
    assert a.monto_involucrado > 76_000_000


def test_la_alerta_dice_cuanto_justifica_la_documentacion():
    [a] = correr(operatoria(80_000_000, meses=6), legajo(recibo(500_000)))
    assert "6,000,000 anuales prorrateados" in a.descripcion


def test_la_metodologia_dice_cuantos_respaldos_y_que_tan_viejos():
    # Si manana se discute la alerta, el expediente tiene que decir contra que
    # se comparo, igual que con las versiones de lista del screening.
    [a] = correr(operatoria(80_000_000, meses=6), legajo(recibo(500_000)))
    assert "1 respaldo(s) computado(s)" in a.metodologia
    assert "el mas antiguo de hace" in a.metodologia


# --- las dos cifras hacen su trabajo --------------------------------------

def test_una_venta_puntual_explica_un_pico_y_no_genera_alerta():
    # Es el caso que el modelo de dos cifras existe para distinguir. Con una
    # sola cifra, esta venta o no explicaba nada o inflaba la capacidad anual
    # para siempre.
    assert correr(operatoria(95_000_000, meses=6),
                  legajo(recibo(500_000), venta(95_000_000))) == []


def test_la_misma_venta_no_justifica_un_nivel_sostenido_mucho_mayor():
    # La venta explica su monto una vez, no un volumen sostenido de varias
    # veces ese monto.
    assert correr(operatoria(300_000_000, meses=6),
                  legajo(recibo(500_000), venta(95_000_000))) != []


def test_el_flujo_se_prorratea_por_el_periodo_observado():
    # Documenta $2.000.000 mensuales, o sea $24.000.000 anuales. En tres meses
    # eso justifica $6.000.000 y no $24.000.000.
    assert correr(operatoria(5_000_000, meses=3), legajo(recibo(2_000_000))) == []
    assert correr(operatoria(9_000_000, meses=3), legajo(recibo(2_000_000))) != []


# --- no dispara cuando no corresponde -------------------------------------

def test_sin_documentacion_no_alerta_porque_es_otro_hallazgo():
    # Un cliente sin respaldos cargados no es un cliente que no puede
    # justificar: es un legajo incompleto, que le toca al item 5.1. Confundirlos
    # convertiria cada legajo a medio cargar en una alerta de lavado.
    assert correr(operatoria(80_000_000, meses=6), legajo()) == []
    assert correr(operatoria(80_000_000, meses=6), None) == []


def test_operar_dentro_de_lo_documentado_no_alerta():
    assert correr(operatoria(10_000_000, meses=6), legajo(recibo(2_000_000))) == []


def test_una_ventana_corta_no_se_compara():
    corta = Operatoria(cliente_id="CL001", operaciones=[
        Operacion(cliente_id="CL001", fecha=INICIO, monto=40_000_000),
        Operacion(cliente_id="CL001", fecha=INICIO + timedelta(days=20),
                  monto=40_000_000),
    ])
    assert corta.meses < 3
    assert correr(corta, legajo(recibo(500_000))) == []


def test_un_documento_que_no_acredita_capacidad_no_habilita_la_comparacion():
    # Un estatuto en el legajo no convierte a un cliente en documentado.
    estatuto = Respaldo("CL001", "CONSTANCIA_CUIT", emitido=date(2026, 1, 1))
    assert correr(operatoria(80_000_000, meses=6), legajo(estatuto)) == []


# --- severidad, con un corte normativo ------------------------------------

def test_la_severidad_sale_del_umbral_de_reporte_y_no_de_un_numero_elegido():
    # 40 SMVM, Res. UIF 78/2025. Un excedente por debajo de ese umbral no
    # habria sido reportable ni como operacion suelta. Asi el corte no es un
    # parametro sin calibrar mas.
    umbral = PARAMETROS.umbral_reporte
    assert umbral > 0

    chico = correr(operatoria(6_000_000 / 2 + umbral * 0.4, meses=6),
                   legajo(recibo(500_000)))
    grande = correr(operatoria(6_000_000 / 2 + umbral * 3, meses=6),
                    legajo(recibo(500_000)))
    assert chico and chico[0].severidad == "MEDIA"
    assert grande and grande[0].severidad == "ALTA"


def test_sin_umbral_de_reporte_la_alerta_no_se_marca_grave_por_las_dudas():
    sin_umbral = ParametrosMonitoreo(umbral_reporte=0.0)
    [a] = correr(operatoria(80_000_000, meses=6), legajo(recibo(500_000)), sin_umbral)
    assert a.severidad == "MEDIA"


# --- el segundo hallazgo --------------------------------------------------

def test_cuando_la_capacidad_se_apoya_en_lo_declarado_la_alerta_lo_dice():
    # Es un hallazgo distinto del primero: una cosa es exceder la capacidad
    # documentada y otra es que esa capacidad salga de papeles que un tercero
    # firma sobre lo que conto el propio cliente.
    cert = Respaldo("CL001", "CERTIFICACION_INGRESOS", emitido=date(2026, 6, 1),
                    monto=500_000, periodicidad=Periodicidad.MENSUAL,
                    periodo_hasta=date(2026, 5, 31))
    [a] = correr(operatoria(80_000_000, meses=6), legajo(cert))
    assert "declaro el propio cliente" in a.descripcion


def test_con_documentacion_de_tercero_verificable_no_aparece_esa_frase():
    [a] = correr(operatoria(80_000_000, meses=6), legajo(recibo(500_000)))
    assert "declaro el propio cliente" not in a.descripcion


# --- lo que la alerta no puede decir --------------------------------------

def test_la_alerta_no_acusa_de_nada():
    # El programa marca que la documentacion no alcanza. Por que no alcanza lo
    # resuelve el analista pidiendo los papeles que faltan.
    [a] = correr(operatoria(80_000_000, meses=6), legajo(recibo(500_000)))
    texto = (a.descripcion + " " + a.metodologia).lower()
    for palabra in ("evad", "fraude", "delito", "ilicit", "lavado", "sospech"):
        assert palabra not in texto, f"la alerta dice {palabra!r}"
