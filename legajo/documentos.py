"""Vocabulario de documentos del legajo.

Aca vive que es cada documento y que acredita. Quien lo puede pedir y quien no
vive en `sujeto_obligado.py`, porque depende de la resolucion que le aplica a
la entidad y no del documento en si. La dependencia va en un solo sentido:
sujeto_obligado importa documentos, nunca al reves.

Las materias salen del art. 33 de la Res. UIF 78/2023, que arma el perfil
transaccional con documentacion de la situacion economica, patrimonial,
financiera y tributaria. Agrupar asi no es una taxonomia inventada: es como lo
escribe la norma, y permite declarar la exigibilidad por materia en vez de
enumerar documento por documento.

La vigencia de cada documento va en None. La norma fija cada cuanto se
actualiza el legajo, no cuantos meses vale un recibo de sueldo: eso lo define
la politica de cada entidad. Poner un numero aca seria inventar un
vencimiento y marcar documentacion vencida que nadie declaro vencida.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Materia(str, Enum):
    """Que aspecto del cliente acredita el documento. Art. 33, Res. 78/2023."""

    IDENTIDAD = "IDENTIDAD"
    ECONOMICA = "ECONOMICA"        # ingresos, flujo
    PATRIMONIAL = "PATRIMONIAL"    # bienes
    FINANCIERA = "FINANCIERA"      # cuentas y movimientos
    TRIBUTARIA = "TRIBUTARIA"      # declaraciones y constancias ante ARCA
    SOCIETARIA = "SOCIETARIA"      # estatuto, autoridades, composicion


class TipoDocumento(str, Enum):
    # --- identidad ---
    DOCUMENTO_IDENTIDAD = "DOCUMENTO_IDENTIDAD"
    CONSTANCIA_CUIT = "CONSTANCIA_CUIT"

    # --- economica ---
    RECIBO_SUELDO = "RECIBO_SUELDO"
    CERTIFICACION_INGRESOS = "CERTIFICACION_INGRESOS"
    RECIBO_JUBILACION = "RECIBO_JUBILACION"
    FACTURACION = "FACTURACION"

    # --- tributaria ---
    # Las tres declaraciones juradas impositivas. Se enumeran por separado y no
    # como una sola porque la prohibicion de la Res. 78/2025 alcanza a las
    # declaraciones juradas y no a toda la materia tributaria: una constancia
    # de inscripcion no es una declaracion jurada.
    DDJJ_GANANCIAS = "DDJJ_GANANCIAS"
    DDJJ_BIENES_PERSONALES = "DDJJ_BIENES_PERSONALES"
    DDJJ_IVA = "DDJJ_IVA"
    CONSTANCIA_MONOTRIBUTO = "CONSTANCIA_MONOTRIBUTO"

    # --- patrimonial ---
    ESCRITURA = "ESCRITURA"
    TITULO_AUTOMOTOR = "TITULO_AUTOMOTOR"
    COMPROBANTE_VENTA_BIENES = "COMPROBANTE_VENTA_BIENES"

    # --- financiera ---
    RESUMEN_BANCARIO = "RESUMEN_BANCARIO"
    BALANCE = "BALANCE"

    # --- societaria ---
    ESTATUTO = "ESTATUTO"
    ACTA_AUTORIDADES = "ACTA_AUTORIDADES"
    NOMINA_ACCIONISTAS = "NOMINA_ACCIONISTAS"
    CONSTANCIA_INSCRIPCION_UIF = "CONSTANCIA_INSCRIPCION_UIF"


@dataclass(frozen=True)
class Ficha:
    """Que es un documento, independientemente de quien lo pida."""

    tipo: TipoDocumento
    materia: Materia
    descripcion: str
    # Si sirve para acreditar capacidad economica documentada (item 3.1). Un
    # estatuto prueba quien es la sociedad y no cuanto factura.
    acredita_capacidad: bool = False
    # Cuantos meses vale antes de tener que renovarlo. None es "no verificado
    # contra ninguna norma": lo fija la politica de la entidad.
    vigencia_meses: int | None = None
    # Solo para personas humanas, solo para juridicas, o para las dos.
    aplica_a: str = "AMBOS"          # PERSONA | ENTIDAD | AMBOS


CATALOGO: dict[TipoDocumento, Ficha] = {
    f.tipo: f for f in (
        Ficha(TipoDocumento.DOCUMENTO_IDENTIDAD, Materia.IDENTIDAD,
              "DNI, libreta o pasaporte", aplica_a="PERSONA"),
        Ficha(TipoDocumento.CONSTANCIA_CUIT, Materia.IDENTIDAD,
              "Constancia de inscripcion ante ARCA"),

        Ficha(TipoDocumento.RECIBO_SUELDO, Materia.ECONOMICA,
              "Recibo de haberes", acredita_capacidad=True, aplica_a="PERSONA"),
        Ficha(TipoDocumento.CERTIFICACION_INGRESOS, Materia.ECONOMICA,
              "Certificacion de ingresos por contador publico",
              acredita_capacidad=True, aplica_a="PERSONA"),
        Ficha(TipoDocumento.RECIBO_JUBILACION, Materia.ECONOMICA,
              "Recibo de haberes previsionales", acredita_capacidad=True,
              aplica_a="PERSONA"),
        Ficha(TipoDocumento.FACTURACION, Materia.ECONOMICA,
              "Facturacion emitida del periodo", acredita_capacidad=True),

        Ficha(TipoDocumento.DDJJ_GANANCIAS, Materia.TRIBUTARIA,
              "Declaracion jurada del impuesto a las ganancias",
              acredita_capacidad=True),
        Ficha(TipoDocumento.DDJJ_BIENES_PERSONALES, Materia.TRIBUTARIA,
              "Declaracion jurada de bienes personales"),
        Ficha(TipoDocumento.DDJJ_IVA, Materia.TRIBUTARIA,
              "Declaracion jurada de IVA", acredita_capacidad=True),
        Ficha(TipoDocumento.CONSTANCIA_MONOTRIBUTO, Materia.TRIBUTARIA,
              "Constancia de opcion al Regimen Simplificado",
              aplica_a="PERSONA"),

        Ficha(TipoDocumento.ESCRITURA, Materia.PATRIMONIAL,
              "Escritura traslativa de dominio", acredita_capacidad=True),
        Ficha(TipoDocumento.TITULO_AUTOMOTOR, Materia.PATRIMONIAL,
              "Titulo de propiedad de automotor"),
        Ficha(TipoDocumento.COMPROBANTE_VENTA_BIENES, Materia.PATRIMONIAL,
              "Comprobante de venta de bienes registrables",
              acredita_capacidad=True),

        Ficha(TipoDocumento.RESUMEN_BANCARIO, Materia.FINANCIERA,
              "Resumen de cuenta bancaria"),
        Ficha(TipoDocumento.BALANCE, Materia.FINANCIERA,
              "Estados contables certificados", acredita_capacidad=True,
              aplica_a="ENTIDAD"),

        Ficha(TipoDocumento.ESTATUTO, Materia.SOCIETARIA,
              "Contrato social o estatuto inscripto", aplica_a="ENTIDAD"),
        Ficha(TipoDocumento.ACTA_AUTORIDADES, Materia.SOCIETARIA,
              "Acta de designacion de autoridades vigentes", aplica_a="ENTIDAD"),
        Ficha(TipoDocumento.NOMINA_ACCIONISTAS, Materia.SOCIETARIA,
              "Nomina de accionistas o socios", aplica_a="ENTIDAD"),
        Ficha(TipoDocumento.CONSTANCIA_INSCRIPCION_UIF, Materia.SOCIETARIA,
              "Constancia de inscripcion ante la UIF, Res. 70/2011"),
    )
}


def ficha(documento: TipoDocumento | str) -> Ficha | None:
    try:
        return CATALOGO[TipoDocumento(str(getattr(documento, "value", documento)))]
    except (KeyError, ValueError):
        return None


def materia_de(documento: TipoDocumento | str) -> Materia | None:
    f = ficha(documento)
    return f.materia if f else None


def de_materia(materia: Materia) -> tuple[TipoDocumento, ...]:
    return tuple(t for t, f in CATALOGO.items() if f.materia is materia)


def acreditan_capacidad(tipo_persona: str | None = None) -> tuple[TipoDocumento, ...]:
    """Los documentos que sirven para el calculo de capacidad del item 3.1."""
    return tuple(
        t for t, f in CATALOGO.items()
        if f.acredita_capacidad and _aplica(f, tipo_persona)
    )


def _aplica(f: Ficha, tipo_persona: str | None) -> bool:
    if not tipo_persona or f.aplica_a == "AMBOS":
        return True
    humana = tipo_persona.strip().upper() == "PERSONA"
    return f.aplica_a == ("PERSONA" if humana else "ENTIDAD")


def para(tipo_persona: str) -> tuple[TipoDocumento, ...]:
    """Los documentos que tienen sentido para ese tipo de cliente.

    Pedirle un estatuto a una persona humana o un recibo de sueldo a una SRL
    es ruido que el analista tiene que descartar a mano.
    """
    return tuple(t for t, f in CATALOGO.items() if _aplica(f, tipo_persona))
