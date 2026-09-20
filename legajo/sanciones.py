"""Exposicion sancionatoria.

El Capitulo IV de la Ley 25.246 expresa las multas en modulos. El valor del
modulo lo actualiza la UIF en cada ejercicio presupuestario, aplicando la tasa
pasiva promedio del BCRA a las multas impagas.

La Res. UIF 129/2024 art. 35 fija la liquidacion del procedimiento abreviado,
y ahi esta el numero que importa:

    no reportar un ROS, o reportarlo fuera de plazo
        ... UNA VEZ el valor total de los bienes u operaciones

No es una multa fija ni un porcentaje. Es el monto completo de la operacion
que no se reporto. Una alerta de ciento treinta y siete millones sin reportar
cuesta ciento treinta y siete millones.

Calcular esto no es un adorno. Una alerta suelta es un pendiente mas en una
cola; una alerta con su exposicion al lado es un argumento que un directorio
entiende, y es lo que consigue que el area de cumplimiento tenga presupuesto.

Aclaracion necesaria: esto es una estimacion de exposicion, no un calculo de
multa. La sancion efectiva la determina la UIF en un sumario, ponderando
naturaleza y riesgo del incumplimiento, tamano de la organizacion,
antecedentes, volumen de negocios y reincidencia.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

# Res. UIF 95/2025. Se actualiza por ejercicio presupuestario, asi que la
# fecha no es decorativa.
MODULO = 54_140.0
MODULO_VIGENCIA = date(2025, 6, 19)
MODULO_NORMA = "Res. UIF 95/2025"


def pesos(modulos: float) -> float:
    return modulos * MODULO


# Res. UIF 129/2024 art. 35. Materias con cargo agravado.
MATERIAS_AGRAVADAS = (
    "Monitoreo", "Listados de Terroristas", "Personas Expuestas Politicamente",
    "Beneficiario Final", "Registracion y designacion de Oficial de Cumplimiento",
    "Deber de Colaboracion", "Debida Diligencia Intensificada",
)

MODULOS_INCUMPLIMIENTO_TOTAL = 30.0
MODULOS_INCUMPLIMIENTO_PARCIAL = 25.0
MODULOS_OTROS = 15.0


@dataclass(frozen=True)
class Cargo:
    """Un cargo de la liquidacion."""

    concepto: str
    materia: str
    modulos: float | None      # None cuando el cargo es por valor de operacion
    monto: float
    fundamento: str

    def resumen(self) -> str:
        unidad = f"{self.modulos:g} modulos" if self.modulos else "valor de operacion"
        return f"{self.concepto}: ${self.monto:,.0f} ({unidad}, {self.fundamento})"


@dataclass
class Exposicion:
    """Exposicion sancionatoria estimada de un sujeto obligado."""

    cargos: list[Cargo]
    modulo_aplicado: float = MODULO
    modulo_vigencia: date = MODULO_VIGENCIA

    @property
    def total(self) -> float:
        return sum(c.monto for c in self.cargos)

    @property
    def por_falta_de_reporte(self) -> float:
        return sum(c.monto for c in self.cargos if c.modulos is None)

    @property
    def por_incumplimientos(self) -> float:
        return sum(c.monto for c in self.cargos if c.modulos is not None)


def cargo_por_no_reportar(cliente: str, monto_operacion: float) -> Cargo:
    """Una vez el valor total de la operacion no reportada."""
    return Cargo(
        concepto=f"ROS no emitido, {cliente}",
        materia="Reporte de Operaciones Sospechosas",
        modulos=None,
        monto=monto_operacion,
        fundamento="Res. UIF 129/2024 art. 35 inc. 1, Ley 25.246 art. 21 inc. b",
    )


def cargo_por_incumplimiento(materia: str, total: bool = True) -> Cargo:
    """Cargo por incumplimiento en una materia del regimen preventivo."""
    modulos = (MODULOS_INCUMPLIMIENTO_TOTAL if total
               else MODULOS_INCUMPLIMIENTO_PARCIAL)
    grado = "total" if total else "parcial"
    return Cargo(
        concepto=f"Incumplimiento {grado} en {materia}",
        materia=materia,
        modulos=modulos,
        monto=pesos(modulos),
        fundamento=f"Res. UIF 129/2024 art. 35 inc. {2 if total else 3}",
    )


def estimar(
    alertas_por_cliente: dict,
    congelamientos: list,
    nombres: dict[str, str],
    sin_perfil: list[str] | None = None,
    sin_beneficiario: list[str] | None = None,
) -> Exposicion:
    """Estima la exposicion si nada de lo detectado se reportara.

    Es el escenario de omision total, no un pronostico. Sirve para dimensionar
    lo que hay sobre la mesa, no para negociar con la UIF.
    """
    cargos: list[Cargo] = []

    # Cada cliente con alertas, por el mayor monto involucrado. Se toma el
    # mayor y no la suma porque las tipologias se superponen sobre las mismas
    # operaciones, y sumarlas contaria el mismo dinero varias veces.
    for cliente_id, alertas in alertas_por_cliente.items():
        if not alertas:
            continue
        monto = max(a.monto_involucrado for a in alertas)
        if monto <= 0:
            continue
        cargos.append(cargo_por_no_reportar(nombres.get(cliente_id, cliente_id), monto))

    # Un congelamiento omitido es incumplimiento total en listados.
    for c in congelamientos:
        cargos.append(cargo_por_incumplimiento("Listados de Terroristas", total=True))

    for _ in (sin_perfil or []):
        cargos.append(cargo_por_incumplimiento("Monitoreo", total=False))

    for _ in (sin_beneficiario or []):
        cargos.append(cargo_por_incumplimiento("Beneficiario Final", total=False))

    return Exposicion(cargos=cargos)
