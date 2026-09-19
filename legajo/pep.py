"""Personas expuestas politicamente.

La Res. UIF 192/2024 no define una categoria unica, y la diferencia importa
para el resultado: una PEP extranjera es cliente de alto riesgo siempre, por
definicion normativa. Una PEP nacional se evalua por riesgo, como cualquier
otro cliente.

Tratar a todas por igual produce dos errores en direcciones opuestas: deja
pasar una PEP extranjera que sumo pocos puntos, y manda a diligencia
reforzada a un concejal municipal sin ningun otro factor.

La otra regla que se suele pasar por alto es el vencimiento. La condicion se
mantiene mientras se ejerce el cargo y hasta DOS anios despues del cese
(art. 6). Un ex funcionario que ceso en 2019 no es PEP hoy, y seguir
tratandolo como tal es ruido que le cuesta horas al analista.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

ANIOS_VIGENCIA_TRAS_CESE = 2


@dataclass(frozen=True)
class PEP:
    """Condicion de PEP declarada para un cliente."""

    cliente_id: str
    tipo: str                      # EXTRANJERA | NACIONAL
    cargo: str = ""
    fecha_cese: date | None = None
    por_parentesco: bool = False

    @property
    def extranjera(self) -> bool:
        return self.tipo.strip().upper() == "EXTRANJERA"

    def vigente(self, al: date | None = None) -> bool:
        """La condicion se mantiene hasta dos anios despues del cese."""
        if self.fecha_cese is None:
            return True
        referencia = al or date.today()
        anios = (referencia - self.fecha_cese).days / 365.25
        return anios < ANIOS_VIGENCIA_TRAS_CESE

    def descripcion(self) -> str:
        partes = ["PEP extranjera" if self.extranjera else "PEP nacional"]
        if self.por_parentesco:
            partes.append("por parentesco o cercania")
        if self.cargo:
            partes.append(f"({self.cargo})")
        if self.fecha_cese:
            partes.append(f"ceso {self.fecha_cese.isoformat()}")
        return " ".join(partes)


class RegistroPEP:
    """Consulta de condicion PEP por cliente."""

    def __init__(self, peps: list[PEP] | None = None) -> None:
        self._por_cliente: dict[str, PEP] = {}
        for p in peps or []:
            self._por_cliente[p.cliente_id] = p

    def consultar(self, cliente_id: str, al: date | None = None) -> PEP | None:
        """Devuelve la condicion si esta vigente. Una vencida es un no-PEP."""
        pep = self._por_cliente.get(cliente_id)
        if pep is None or not pep.vigente(al):
            return None
        return pep

    def vencidas(self, al: date | None = None) -> list[PEP]:
        """Condiciones declaradas que ya caducaron. Utiles para el expediente."""
        return [p for p in self._por_cliente.values() if not p.vigente(al)]

    def __len__(self) -> int:
        return len(self._por_cliente)
