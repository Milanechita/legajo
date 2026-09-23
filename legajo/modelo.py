"""Modelo de datos del circuito PLA/FT.

El objeto central es el Caso. Todo lo demas son transformaciones sobre el.

Dos decisiones estructurales que eliminan casos especiales aguas abajo:

1. La evidencia es append-only. No se corrige un analisis previo: se agrega
   una entrada nueva. El historial es inmutable por construccion, no por
   disciplina del que escribe el codigo.

2. Las transiciones de estado son declarativas. Un caso no avanza si le falta
   la evidencia que el estado destino exige. No hay que preguntar si falta
   documentacion en cada punto del codigo: la transicion simplemente se rechaza.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Estado(str, Enum):
    """Estados del circuito. El orden del enum no implica el orden del flujo."""

    ALTA = "ALTA"
    SCREENING = "SCREENING"
    SCORING = "SCORING"
    ANALISIS = "ANALISIS"
    ESPERA_INFO = "ESPERA_INFO"
    ESCALADO = "ESCALADO"
    CERRADO = "CERRADO"


# Transiciones permitidas. Cualquier par que no este aca es invalido.
TRANSICIONES: dict[Estado, frozenset[Estado]] = {
    Estado.ALTA: frozenset({Estado.SCREENING}),
    Estado.SCREENING: frozenset({Estado.SCORING, Estado.ESCALADO}),
    Estado.SCORING: frozenset({Estado.ANALISIS, Estado.CERRADO}),
    Estado.ANALISIS: frozenset({Estado.ESPERA_INFO, Estado.ESCALADO, Estado.CERRADO}),
    Estado.ESPERA_INFO: frozenset({Estado.ANALISIS, Estado.ESCALADO}),
    Estado.ESCALADO: frozenset({Estado.CERRADO}),
    # CERRADO no es terminal. El legajo se cierra para el alta, pero la debida
    # diligencia continuada alcanza a todos los clientes y no solo a los de
    # riesgo alto: una alerta de monitoreo reabre un caso cerrado. Dejarlo
    # terminal obligaria a no cerrar nunca, que es peor.
    Estado.CERRADO: frozenset({Estado.ANALISIS}),
}


class TransicionInvalida(Exception):
    """El caso no puede pasar del estado actual al solicitado."""


def ahora() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class Evidencia:
    """Una entrada del expediente. Inmutable.

    `fuente` importa tanto como `resultado`: en una inspeccion, "screeneamos
    el 3 de marzo" no significa nada sin "contra la lista OFAC version X".
    """

    momento: datetime
    actor: str
    accion: str
    detalle: dict[str, Any] = field(default_factory=dict)

    def como_fila(self) -> dict[str, Any]:
        return {
            "momento": self.momento.isoformat(timespec="seconds"),
            "actor": self.actor,
            "accion": self.accion,
            "detalle": self.detalle,
        }


# --- CUIT y CUIL -----------------------------------------------------------
#
# El digito verificador es modulo 11 sobre los primeros diez digitos. No es un
# valor normativo que cambie con una resolucion: es un algoritmo fijo, asi que
# va escrito y no parametrizado.
#
# Sirve para lo que importa aca: un CUIT mal tipeado deja de matchear contra
# las fuentes externas, y el cliente queda sin constatar sin que nadie se
# entere. Es mejor rechazarlo en la carga.

_PESOS_CUIT = (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)

# El prefijo dice que clase de persona es. Un 30 con tipo PERSONA es un error
# de carga, y uno de los dos datos esta mal.
PREFIJOS_PERSONA_HUMANA = frozenset({"20", "23", "24", "25", "26", "27"})
PREFIJOS_PERSONA_JURIDICA = frozenset({"30", "33", "34"})


def solo_digitos(texto: str) -> str:
    return "".join(c for c in (texto or "") if c.isdigit())


def digito_verificador_cuit(primeros_diez: str) -> int | None:
    """Digito verificador de los primeros diez digitos de un CUIT.

    Devuelve None cuando el calculo da 10, que no es un digito. Ese caso no
    produce un CUIT invalido sino que obliga a cambiar el prefijo: AFIP pasa
    el 20 o el 27 a 23 y recalcula. Por eso ningun CUIT valido puede tener
    como verificador el resultado 10.
    """
    if len(primeros_diez) != 10 or not primeros_diez.isdigit():
        return None
    suma = sum(int(d) * p for d, p in zip(primeros_diez, _PESOS_CUIT))
    resto = suma % 11
    if resto == 0:
        return 0
    if resto == 1:
        return None
    return 11 - resto


@dataclass(frozen=True)
class Validacion:
    """Resultado de validar un identificador.

    Lleva el motivo y no solo un booleano porque el analista tiene que poder
    corregir la carga, y "CUIT invalido" no le dice si es el largo, el digito
    o el prefijo.
    """

    valido: bool
    motivo: str = ""

    def __bool__(self) -> bool:
        return self.valido


def validar_cuit(numero: str, tipo_persona: str | None = None) -> Validacion:
    """Valida largo, digito verificador y, si se pasa, coherencia del prefijo.

    `tipo_persona` es el tipo del cliente: PERSONA o cualquier otro valor, que
    aguas arriba significa persona juridica.
    """
    limpio = solo_digitos(numero)
    if not limpio:
        return Validacion(False, "sin numero")
    if len(limpio) != 11:
        return Validacion(False, f"tiene {len(limpio)} digitos y un CUIT tiene 11")

    prefijo = limpio[:2]
    if prefijo not in (PREFIJOS_PERSONA_HUMANA | PREFIJOS_PERSONA_JURIDICA):
        return Validacion(False, f"prefijo {prefijo} no esta asignado")

    esperado = digito_verificador_cuit(limpio[:10])
    if esperado is None or esperado != int(limpio[10]):
        return Validacion(False, "digito verificador incorrecto")

    if tipo_persona:
        humana = tipo_persona.strip().upper() == "PERSONA"
        if humana and prefijo in PREFIJOS_PERSONA_JURIDICA:
            return Validacion(False, f"prefijo {prefijo} es de persona juridica")
        if not humana and prefijo in PREFIJOS_PERSONA_HUMANA:
            return Validacion(False, f"prefijo {prefijo} es de persona humana")

    return Validacion(True)


def armar_cuit(prefijo: str, documento: str) -> str:
    """Arma un CUIT con su digito verificador. Para generar datos de prueba.

    Devuelve cadena vacia cuando la combinacion no admite verificador, que es
    el caso en que AFIP cambiaria el prefijo.
    """
    base = f"{prefijo}{solo_digitos(documento).zfill(8)}"
    dv = digito_verificador_cuit(base)
    return "" if dv is None else f"{base}{dv}"


@dataclass(frozen=True)
class Documento:
    """Identificador de una persona o entidad."""

    tipo: str  # DNI, CUIT, PASAPORTE, TAX_ID, ...
    numero: str

    def clave(self) -> str:
        """Forma canonica para comparacion exacta."""
        limpio = "".join(c for c in self.numero if c.isalnum()).upper()
        return f"{self.tipo.upper()}:{limpio}"

    def validar(self, tipo_persona: str | None = None) -> Validacion:
        """Valida el identificador cuando se sabe como hacerlo.

        Un pasaporte o un tax id extranjero no tienen regla de validacion
        conocida, asi que se dan por validos. Marcarlos como invalidos seria
        inventar un hallazgo.
        """
        if self.tipo.strip().upper() in {"CUIT", "CUIL"}:
            return validar_cuit(self.numero, tipo_persona)
        return Validacion(True)


@dataclass
class Cliente:
    """Persona humana o juridica sujeta a debida diligencia."""

    cliente_id: str
    nombre: str
    tipo: str = "PERSONA"  # PERSONA | ENTIDAD
    documentos: list[Documento] = field(default_factory=list)
    fecha_nacimiento: str | None = None  # ISO, o None para entidades
    nacionalidad: str | None = None
    pais_residencia: str | None = None
    actividad: str | None = None
    oferta_publica: bool = False  # exceptuada de identificar beneficiario final

    # --- datos del cliente argentino ---
    #
    # Todos son lo que el cliente declaro en el alta, igual que los de arriba.
    # Lo que despues se verifique contra ARCA, el BCRA o un informe comercial
    # entra como constatacion y no pisa estos campos: la gracia del modelo es
    # poder comparar los dos.
    #
    # No esta el codigo de actividad de ARCA, a proposito. Un cliente declara
    # su actividad en palabras, no en codigo CLAE. El codigo lo trae ARCA y
    # por ahora vive como constatacion, no como declaracion.
    condicion_iva: str | None = None        # RI | MONOTRIBUTO | EXENTO | CF
    # Codigo de actividad CLAE tal como figuraba en la constancia de ARCA al
    # momento del alta. No es una declaracion en palabras del cliente: es lo
    # que el analista transcribio del papel. Por eso se puede comparar de forma
    # exacta contra lo que ARCA diga hoy, y la diferencia significa que el
    # cliente cambio de actividad y no lo informo.
    actividad_codigo: str | None = None
    categoria_monotributo: str | None = None
    provincia: str | None = None
    localidad: str | None = None
    domicilio: str | None = None
    codigo_postal: str | None = None
    telefono: str | None = None
    email: str | None = None
    fecha_alta: str | None = None           # ISO, cuando se abrio la relacion
    # Cuando se constituyo la sociedad, que sale del estatuto. No es lo mismo
    # que fecha_alta: una sociedad de 2005 puede haberse hecho cliente ayer, y
    # una constituida el mes pasado puede operar desde el primer dia. La
    # tipologia de riesgo mira la constitucion, no la vinculacion.
    fecha_constitucion: str | None = None   # ISO, solo para personas juridicas
    es_sujeto_obligado: bool = False        # declarado, Ley 25.246 art. 20


def _mismo_analisis(a, b) -> bool:
    """Si dos evaluaciones dicen lo mismo, incluido el porque."""
    return (a.nivel == b.nivel
            and a.puntaje == b.puntaje
            and list(a.elevadores) == list(b.elevadores)
            and [f.codigo for f in a.factores] == [f.codigo for f in b.factores])


@dataclass
class Caso:
    """Un cliente atravesando el circuito.

    `evidencia` solo crece. No hay metodo para borrar ni modificar entradas.
    """

    caso_id: str
    cliente: Cliente
    estado: Estado = Estado.ALTA
    evidencia: list[Evidencia] = field(default_factory=list)
    # La evaluacion de riesgo vigente. Se escribe unicamente desde
    # `reevaluar`, que ademas la asienta en la evidencia. Es la misma relacion
    # que hay entre `estado` y `transicionar`.
    evaluacion: Any = None

    def registrar(self, actor: str, accion: str, **detalle: Any) -> Evidencia:
        """Agrega una entrada al expediente."""
        ev = Evidencia(momento=ahora(), actor=actor, accion=accion, detalle=detalle)
        self.evidencia.append(ev)
        return ev

    def transicionar(self, destino: Estado, actor: str, motivo: str) -> None:
        """Mueve el caso a otro estado, o falla.

        Toda transicion queda registrada. No existe forma de cambiar el estado
        sin dejar rastro: `estado` se modifica unicamente aca.
        """
        permitidos = TRANSICIONES[self.estado]
        if destino not in permitidos:
            raise TransicionInvalida(
                f"{self.caso_id}: {self.estado.value} -> {destino.value} no permitida. "
                f"Permitidas: {sorted(e.value for e in permitidos) or 'ninguna (estado terminal)'}"
            )
        origen = self.estado
        self.estado = destino
        self.registrar(
            actor,
            "TRANSICION",
            origen=origen.value,
            destino=destino.value,
            motivo=motivo,
        )

    def reevaluar(self, evaluacion, actor: str, motivo: str) -> bool:
        """Reemplaza la evaluacion de riesgo vigente y lo deja asentado.

        Misma forma que `transicionar`: el valor actual y el registro se
        escriben juntos, asi que no hay manera de cambiar uno sin el otro. Por
        eso el riesgo no necesita un campo paralelo ni un segundo puntaje. El
        vigente es este, y el del alta sigue entero en el expediente para
        cuando una inspeccion pregunte por que el cliente entro como BAJO.

        Devuelve False y no escribe nada cuando el resultado no cambio.
        Apendear una evaluacion identica en cada corrida convertiria el
        expediente en un latido en vez de un registro de cambios, que es el
        mismo motivo por el que `transicionar` rechaza ir al estado actual.
        """
        # La comparacion incluye el porque y no solo el resultado. Un cliente
        # que sigue en ALTO pero por otro motivo cambio: si solo se miraran el
        # nivel y el puntaje, el expediente y el informe seguirian diciendo
        # que esta en ALTO por su situacion en el BCRA cuando el BCRA ya esta
        # limpio y lo que cambio es la actividad. El analista iria a mirar el
        # lugar equivocado.
        anterior = self.evaluacion
        if anterior is not None and _mismo_analisis(anterior, evaluacion):
            return False

        self.evaluacion = evaluacion
        self.registrar(
            actor,
            "REEVALUACION_EBR",
            nivel_anterior=anterior.nivel if anterior else "",
            nivel=evaluacion.nivel,
            puntaje_anterior=anterior.puntaje if anterior else "",
            puntaje=evaluacion.puntaje,
            regimen=evaluacion.regimen,
            elevadores=list(evaluacion.elevadores),
            motivo=motivo,
        )
        return True

    @property
    def abierto(self) -> bool:
        return self.estado is not Estado.CERRADO
