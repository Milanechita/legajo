"""Pruebas de la regla que compara la categoria declarada contra lo operado.

Es la pregunta central del proyecto sobre el caso mas simple que hay. Lo que
tiene que garantizar el archivo es que la alerta describa una inconsistencia y
no una evasion, y que no dispare cuando no tiene con que.
"""

from __future__ import annotations

from datetime import date, timedelta

from legajo.alertas import monitorear
from legajo.config import PARAMETROS_POR_DEFECTO, ParametrosMonitoreo
from legajo.modelo import Cliente
from legajo.operaciones import Operacion, Operatoria

INICIO = date(2026, 1, 15)


def cliente(categoria="A", condicion="MONOTRIBUTO") -> Cliente:
    return Cliente(cliente_id="CL001", nombre="Sofia Ramirez", tipo="PERSONA",
                   condicion_iva=condicion, categoria_monotributo=categoria)


def operatoria(total: float, meses: int = 6, cantidad: int = 12) -> Operatoria:
    """Reparte un total en operaciones a lo largo de varios meses."""
    paso = timedelta(days=int(meses * 30 / max(cantidad - 1, 1)))
    return Operatoria(cliente_id="CL001", operaciones=[
        Operacion(cliente_id="CL001", fecha=INICIO + paso * i,
                  monto=total / cantidad)
        for i in range(cantidad)
    ])


def correr(cli, op, parametros=PARAMETROS_POR_DEFECTO):
    alertas = monitorear({"CL001": op}, {}, parametros,
                         clientes={"CL001": cli} if cli else None)
    return [a for a in alertas.get("CL001", []) if a.codigo == "MONOTRIBUTO_EXCEDIDO"]


# --- dispara cuando tiene que disparar ------------------------------------

def test_un_monotributista_que_opera_muy_por_encima_de_su_tope_alerta():
    # Categoria A tiene tope de $12.009.410 anuales. Operar $60.000.000 en seis
    # meses proyecta $120.000.000, diez veces el tope.
    [alerta] = correr(cliente("A"), operatoria(60_000_000, meses=6))
    assert alerta.severidad == "ALTA"
    assert "categoria A" in alerta.descripcion
    assert "12,009,410" in alerta.descripcion


def test_el_exceso_moderado_es_medio_y_el_grande_es_alto():
    # Un exceso chico se explica por estacionalidad. Duplicar el tope no.
    # Si los dos fueran ALTA, el analista no sabria por cual empezar.
    moderado = correr(cliente("A"), operatoria(7_500_000, meses=6))
    grave = correr(cliente("A"), operatoria(30_000_000, meses=6))
    assert moderado and moderado[0].severidad == "MEDIA"
    assert grave and grave[0].severidad == "ALTA"


def test_la_alerta_dice_cuantas_veces_el_tope_para_poder_priorizar():
    [alerta] = correr(cliente("A"), operatoria(60_000_000, meses=6))
    assert "veces el tope" in alerta.descripcion


def test_la_metodologia_cita_la_escala_y_su_vigencia():
    # Si manana cambian los topes, el expediente tiene que decir contra cual
    # se comparo. Es la misma regla que las versiones de lista del screening.
    [alerta] = correr(cliente("A"), operatoria(60_000_000, meses=6))
    assert "2026-08-01" in alerta.metodologia
    assert "ARCA" in alerta.metodologia


# --- no dispara cuando no corresponde -------------------------------------

def test_operar_dentro_del_tope_no_alerta():
    assert correr(cliente("A"), operatoria(5_000_000, meses=6)) == []


def test_un_responsable_inscripto_no_tiene_tope_de_categoria():
    assert correr(cliente(condicion="RI"), operatoria(90_000_000, meses=6)) == []


def test_sin_categoria_declarada_no_se_evalua():
    # No evaluar es distinto de dar por bueno. Sin categoria no hay tope contra
    # que comparar, y elegir uno seria inventarlo.
    assert correr(cliente(categoria=""), operatoria(90_000_000, meses=6)) == []


def test_una_categoria_que_no_existe_no_se_evalua():
    assert correr(cliente(categoria="Z"), operatoria(90_000_000, meses=6)) == []


def test_sin_cliente_la_regla_no_dispara():
    # El monitoreo se puede correr sin padron. Que falte el dato no es lo mismo
    # que tenerlo y que no cierre.
    assert correr(None, operatoria(90_000_000, meses=6)) == []


def test_una_ventana_corta_no_se_anualiza():
    # Anualizar dos meses y multiplicar por seis da un numero que no significa
    # nada. Una alerta que no significa nada entrena al analista a ignorarlas.
    corta = Operatoria(cliente_id="CL001", operaciones=[
        Operacion(cliente_id="CL001", fecha=INICIO, monto=9_000_000),
        Operacion(cliente_id="CL001", fecha=INICIO + timedelta(days=20),
                  monto=9_000_000),
    ])
    assert corta.meses < 3
    assert correr(cliente("A"), corta) == []


def test_el_minimo_de_meses_es_politica_y_se_puede_mover():
    corta = Operatoria(cliente_id="CL001", operaciones=[
        Operacion(cliente_id="CL001", fecha=INICIO, monto=9_000_000),
        Operacion(cliente_id="CL001", fecha=INICIO + timedelta(days=20),
                  monto=9_000_000),
    ])
    permisivo = ParametrosMonitoreo(meses_minimos_para_anualizar=1.0)
    assert correr(cliente("A"), corta, permisivo)


# --- lo que la alerta no puede decir --------------------------------------

def test_la_alerta_no_acusa_de_evadir():
    # El volumen que ve el banco incluye transferencias entre cuentas propias,
    # prestamos y devoluciones. No es facturacion, asi que el programa describe
    # una inconsistencia y deja la conclusion al analista.
    [alerta] = correr(cliente("A"), operatoria(60_000_000, meses=6))
    texto = (alerta.descripcion + " " + alerta.metodologia).lower()
    for palabra in ("evad", "evasion", "fraude", "delito", "ilicit"):
        assert palabra not in texto, f"la alerta dice {palabra!r}"


def test_la_alerta_distingue_lo_operado_de_lo_proyectado():
    # Confundir los dos numeros haria que el analista discuta con el cliente
    # sobre una cifra que el cliente no movio.
    [alerta] = correr(cliente("A"), operatoria(60_000_000, meses=6))
    assert "Opero $60,000,000" in alerta.descripcion
    assert "anualizado" in alerta.descripcion
