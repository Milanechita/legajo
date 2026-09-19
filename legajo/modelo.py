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
    Estado.CERRADO: frozenset(),
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


@dataclass(frozen=True)
class Documento:
    """Identificador de una persona o entidad."""

    tipo: str  # DNI, CUIT, PASAPORTE, TAX_ID, ...
    numero: str

    def clave(self) -> str:
        """Forma canonica para comparacion exacta."""
        limpio = "".join(c for c in self.numero if c.isalnum()).upper()
        return f"{self.tipo.upper()}:{limpio}"


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


@dataclass
class Caso:
    """Un cliente atravesando el circuito.

    `evidencia` solo crece. No hay metodo para borrar ni modificar entradas.
    """

    caso_id: str
    cliente: Cliente
    estado: Estado = Estado.ALTA
    evidencia: list[Evidencia] = field(default_factory=list)

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

    @property
    def abierto(self) -> bool:
        return self.estado is not Estado.CERRADO
