"""Pruebas del padron de ejemplo argentino.

El repo es publico. Un CUIT real metido en un padron de ejemplo asocia a una
persona de verdad con una alerta de lavado, asi que la prueba que importa aca
no es de formato: es que los identificadores esten fuera del rango asignado y
que sigan estandolo despues de que alguien edite el archivo.
"""

from __future__ import annotations

from pathlib import Path

from legajo.io_planilla import leer_padron
from legajo.modelo import (
    PREFIJOS_PERSONA_HUMANA, PREFIJOS_PERSONA_JURIDICA, solo_digitos,
    validar_cuit,
)

PADRON = Path(__file__).resolve().parent.parent / "ejemplos" / "clientes_ar.csv"

# Debajo de esto hay DNI reales. Es el piso que fijo el roadmap.
PRIMER_DNI_SIN_ASIGNAR = 99_000_000


def clientes():
    return leer_padron(PADRON)


def cuit_de(cliente) -> str:
    for d in cliente.documentos:
        if d.tipo.upper() == "CUIT":
            return solo_digitos(d.numero)
    return ""


def test_el_padron_tiene_entre_treinta_y_cuarenta_clientes():
    assert 30 <= len(clientes()) <= 40


def test_ningun_cuit_del_ejemplo_cae_en_el_rango_de_dni_asignados():
    # Es la regla dura del roadmap y la unica que protege a una persona real
    # de aparecer en una demo publica de lavado.
    for c in clientes():
        cuerpo = int(cuit_de(c)[2:10])
        assert cuerpo >= PRIMER_DNI_SIN_ASIGNAR, (
            f"{c.cliente_id} tiene el cuerpo de CUIT {cuerpo}, que cae en el "
            f"rango de DNI asignados"
        )


def test_todos_los_cuit_del_ejemplo_tienen_verificador_valido():
    # Un CUIT sintetico con verificador roto haria fallar las fuentes de la
    # Fase 2 por un motivo que no tiene nada que ver con lo que se esta
    # probando.
    for c in clientes():
        resultado = validar_cuit(cuit_de(c), c.tipo)
        assert resultado, f"{c.cliente_id}: {resultado.motivo}"


def test_el_prefijo_del_cuit_coincide_con_el_tipo_de_persona():
    for c in clientes():
        prefijo = cuit_de(c)[:2]
        esperados = (PREFIJOS_PERSONA_HUMANA if c.tipo == "PERSONA"
                     else PREFIJOS_PERSONA_JURIDICA)
        assert prefijo in esperados, f"{c.cliente_id} tiene prefijo {prefijo}"


def test_el_dni_de_las_personas_tambien_esta_fuera_del_rango_asignado():
    for c in clientes():
        for d in c.documentos:
            if d.tipo.upper() == "DNI":
                assert int(solo_digitos(d.numero)) >= PRIMER_DNI_SIN_ASIGNAR


def test_hay_clientes_de_los_tipos_que_pidio_el_roadmap():
    # Si el padron fuera todo empleados en relacion de dependencia, las reglas
    # de la Fase 3 no tendrian contra que correr.
    condiciones = {c.condicion_iva for c in clientes()}
    assert {"MONOTRIBUTO", "RI", "CF"} <= condiciones

    categorias = {c.categoria_monotributo for c in clientes() if c.categoria_monotributo}
    assert len(categorias) >= 4, "hacen falta varias categorias de monotributo"

    tipos = {c.tipo for c in clientes()}
    assert tipos == {"PERSONA", "ENTIDAD"}


def test_el_padron_conserva_casos_que_el_screening_tiene_que_encontrar():
    # El screening baja de protagonismo, no se elimina. Si el padron nuevo no
    # tuviera ningun hit, la primera corrida daria cero coincidencias y
    # pareceria que el cotejo dejo de andar.
    nombres = {c.nombre.upper() for c in clientes()}
    assert any("ABBAS" in n for n in nombres)
    assert any("PETROQUIMICA" in n or "PETROQUÍMICA" in n for n in nombres)


def test_hay_clientes_que_declaran_ser_sujetos_obligados():
    # Hace falta para la senal del item 4.2.
    assert sum(1 for c in clientes() if c.es_sujeto_obligado) >= 3


def test_hay_domicilio_y_telefono_compartidos_entre_clientes_distintos():
    # La senal del item 4.3 necesita el caso en los datos, si no se escribe a
    # ciegas y nadie sabe si anda.
    lista = clientes()

    domicilios = {}
    for c in lista:
        if c.domicilio:
            clave = (c.domicilio.upper(), (c.localidad or "").upper())
            domicilios.setdefault(clave, []).append(c.cliente_id)
    assert any(len(v) > 1 for v in domicilios.values()), "falta un domicilio repetido"

    telefonos = {}
    for c in lista:
        if c.telefono:
            telefonos.setdefault(c.telefono, []).append(c.cliente_id)
    assert any(len(v) > 1 for v in telefonos.values()), "falta un telefono repetido"


def test_hay_clientes_en_provincias_de_frontera():
    # Para el item 4.1. La lista de zonas la fija el Decreto 253/2018 y todavia
    # no esta cargada, pero los clientes tienen que existir para cuando este.
    provincias = {(c.provincia or "").upper() for c in clientes()}
    assert provincias & {"SALTA", "MISIONES", "CORRIENTES", "NEUQUEN", "RIO NEGRO"}


def test_el_padron_viejo_se_sigue_leyendo_igual():
    # Las columnas nuevas son opcionales. Si el lector las exigiera, romperia
    # todas las pruebas que usan el padron original.
    viejo = leer_padron(PADRON.parent / "clientes.csv")
    assert len(viejo) == 15
    assert viejo[0].condicion_iva is None
