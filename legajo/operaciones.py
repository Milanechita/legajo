"""Operatoria del cliente y perfil transaccional.

El perfil es prospectivo: se arma al alta, con lo que el cliente declara sobre
el proposito de la relacion, los montos esperados y su situacion patrimonial.
El monitoreo compara ese perfil contra lo que efectivamente ocurrio.

Una aclaracion que conviene dejar escrita. La normativa admite recalibrar el
perfil segun las operaciones realmente realizadas, y eso tiene una trampa
evidente: si el perfil se ajusta solo hacia arriba cada vez que el cliente
opera de mas, el desvio desaparece justo cuando empieza a importar. Por eso
aca la recalibracion se sugiere y nunca se aplica sola.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Iterator

INGRESO = "INGRESO"
EGRESO = "EGRESO"
EFECTIVO = "EFECTIVO"


@dataclass(frozen=True)
class Operacion:
    """Una operacion del cliente. El monto va siempre positivo."""

    cliente_id: str
    fecha: date
    monto: float
    sentido: str = INGRESO          # INGRESO | EGRESO
    instrumento: str = "TRANSFERENCIA"  # EFECTIVO | TRANSFERENCIA | CHEQUE | ...
    canal: str = "ELECTRONICO"      # PRESENCIAL | ELECTRONICO | ...
    contraparte: str = ""
    pais_contraparte: str = ""
    referencia: str = ""

    @property
    def es_efectivo(self) -> bool:
        return self.instrumento.strip().upper() == EFECTIVO

    def resumen(self) -> str:
        return (f"{self.fecha.isoformat()} {self.sentido[:3]} "
                f"${self.monto:,.0f} {self.instrumento}")


@dataclass(frozen=True)
class Perfil:
    """Perfil transaccional declarado, ex ante.

    `monto_mensual` y `operaciones_mensuales` son lo esperado, no un tope
    contractual. Superarlos no es una infraccion: es una inusualidad que hay
    que analizar y que puede quedar justificada.
    """

    cliente_id: str
    monto_mensual: float = 0.0
    operaciones_mensuales: int = 0
    proporcion_efectivo: float = 0.0     # fraccion esperada [0, 1]
    paises: tuple[str, ...] = ()         # codigos ISO esperados
    origen_fondos: str = ""              # texto declarado
    proposito: str = ""

    @property
    def declarado(self) -> bool:
        return self.monto_mensual > 0 or self.operaciones_mensuales > 0


@dataclass(frozen=True)
class Ventana:
    """Operaciones de un cliente dentro de un periodo contiguo."""

    cliente_id: str
    desde: date
    hasta: date
    operaciones: tuple[Operacion, ...]

    @property
    def total(self) -> float:
        return sum(o.monto for o in self.operaciones)

    @property
    def cantidad(self) -> int:
        return len(self.operaciones)


@dataclass
class Operatoria:
    """Todas las operaciones de un cliente, ordenadas, con sus agregados.

    Las ventanas deslizantes se calculan aca y una sola vez. Si cada regla
    armara la suya, se recorreria la operatoria N veces y cada regla definiria
    "ventana de cinco dias" a su manera.
    """

    cliente_id: str
    operaciones: list[Operacion] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.operaciones.sort(key=lambda o: (o.fecha, o.monto))

    # --- agregados ---------------------------------------------------------

    @property
    def total(self) -> float:
        return sum(o.monto for o in self.operaciones)

    @property
    def cantidad(self) -> int:
        return len(self.operaciones)

    @property
    def desde(self) -> date | None:
        return self.operaciones[0].fecha if self.operaciones else None

    @property
    def hasta(self) -> date | None:
        return self.operaciones[-1].fecha if self.operaciones else None

    @property
    def meses(self) -> float:
        """Duracion de la operatoria en meses, minimo uno."""
        if not self.operaciones:
            return 0.0
        dias = (self.hasta - self.desde).days + 1
        return max(dias / 30.44, 1.0)

    @property
    def total_efectivo(self) -> float:
        return sum(o.monto for o in self.operaciones if o.es_efectivo)

    @property
    def proporcion_efectivo(self) -> float:
        return self.total_efectivo / self.total if self.total else 0.0

    def por_mes(self) -> dict[tuple[int, int], list[Operacion]]:
        """Operaciones agrupadas por anio y mes calendario."""
        agrupadas: dict[tuple[int, int], list[Operacion]] = {}
        for o in self.operaciones:
            agrupadas.setdefault((o.fecha.year, o.fecha.month), []).append(o)
        return agrupadas

    def paises(self) -> set[str]:
        return {o.pais_contraparte for o in self.operaciones if o.pais_contraparte}

    # --- ventanas ----------------------------------------------------------

    def ventanas(self, dias: int) -> Iterator[Ventana]:
        """Ventanas deslizantes de `dias` corridos, una por operacion inicial.

        Dos punteros sobre la lista ya ordenada. El puntero de cierre solo
        avanza, asi que el recorrido completo es lineal y no cuadratico.
        """
        ops = self.operaciones
        fin = 0
        for inicio in range(len(ops)):
            if fin < inicio:
                fin = inicio
            while fin < len(ops) and (ops[fin].fecha - ops[inicio].fecha).days < dias:
                fin += 1
            if fin - inicio < 1:
                continue
            yield Ventana(
                cliente_id=self.cliente_id,
                desde=ops[inicio].fecha,
                hasta=ops[inicio].fecha + timedelta(days=dias - 1),
                operaciones=tuple(ops[inicio:fin]),
            )

    def ultimos(self, dias: int, al: date | None = None) -> list[Operacion]:
        """Operaciones dentro de los ultimos `dias` corridos."""
        if not self.operaciones:
            return []
        corte = (al or self.hasta) - timedelta(days=dias)
        return [o for o in self.operaciones if o.fecha > corte]


def agrupar(operaciones: list[Operacion]) -> dict[str, Operatoria]:
    """Arma una Operatoria por cliente."""
    por_cliente: dict[str, list[Operacion]] = {}
    for o in operaciones:
        por_cliente.setdefault(o.cliente_id, []).append(o)
    return {
        cid: Operatoria(cliente_id=cid, operaciones=ops)
        for cid, ops in por_cliente.items()
    }


def recalibracion_sugerida(operatoria: Operatoria, perfil: Perfil) -> Perfil | None:
    """Perfil que reflejaria la operatoria real, para que un humano decida.

    Se devuelve como sugerencia y no se aplica. Ajustar el perfil solo, hacia
    arriba, hace desaparecer el desvio en el momento exacto en que el desvio
    es la senial que importa.
    """
    if not operatoria.operaciones:
        return None

    mensual = operatoria.total / operatoria.meses
    cantidad = round(operatoria.cantidad / operatoria.meses)
    if mensual <= perfil.monto_mensual and cantidad <= perfil.operaciones_mensuales:
        return None

    return Perfil(
        cliente_id=perfil.cliente_id,
        monto_mensual=round(mensual, 2),
        operaciones_mensuales=cantidad,
        proporcion_efectivo=round(operatoria.proporcion_efectivo, 4),
        paises=tuple(sorted(operatoria.paises())),
        origen_fondos=perfil.origen_fondos,
        proposito=perfil.proposito,
    )
