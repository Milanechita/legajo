"""Registro normalizado de designado y contrato de parser.

Toda lista, sin importar su formato de origen, se traduce a Designado. El
matcher nunca sabe de donde vino el dato. Agregar una lista nueva es agregar
un parser; el motor de cotejo no se toca.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import date
from typing import Iterable, Protocol


@dataclass(frozen=True)
class Designado:
    """Una persona o entidad incluida en una lista de control."""

    lista: str              # OFAC_SDN, ONU_CONSOLIDADA, PEP_AR, ...
    id_origen: str          # identificador en la lista de origen
    nombre: str
    tipo: str = "PERSONA"   # PERSONA | ENTIDAD | BUQUE | AERONAVE
    alias: tuple[str, ...] = ()
    fechas_nacimiento: tuple[str, ...] = ()
    nacionalidades: tuple[str, ...] = ()
    documentos: tuple[str, ...] = ()   # ya en forma canonica TIPO:NUMERO
    programas: tuple[str, ...] = ()    # SDGT, NPWMD, RES1718, ...

    @property
    def es_entidad(self) -> bool:
        return self.tipo != "PERSONA"

    @property
    def todos_los_nombres(self) -> list[str]:
        return [self.nombre, *self.alias]


@dataclass(frozen=True)
class VersionLista:
    """Identidad verificable de una version de lista.

    Sin esto, el expediente no sirve. "Screeneamos el 3 de marzo" no prueba
    nada si no consta contra que version de la lista se screeneo: si OFAC
    publico una actualizacion el 2 de marzo, el resultado es otro.
    """

    lista: str
    publicada: date | None
    descargada: date
    registros: int
    sha256: str

    def resumen(self) -> str:
        pub = self.publicada.isoformat() if self.publicada else "s/d"
        return f"{self.lista} pub={pub} reg={self.registros} sha256={self.sha256[:12]}"


def huella(contenido: bytes) -> str:
    return hashlib.sha256(contenido).hexdigest()


class Parser(Protocol):
    """Contrato que cumple toda fuente de lista."""

    nombre_lista: str

    def parsear(self, contenido: bytes) -> tuple[list[Designado], VersionLista]:
        """Traduce el formato nativo de la lista a registros normalizados."""
        ...


@dataclass
class Padron:
    """Conjunto de designados cargados, con sus versiones de origen."""

    designados: list[Designado] = field(default_factory=list)
    versiones: list[VersionLista] = field(default_factory=list)

    def incorporar(self, designados: Iterable[Designado], version: VersionLista) -> None:
        self.designados.extend(designados)
        self.versiones.append(version)

    @property
    def procedencia(self) -> list[str]:
        return [v.resumen() for v in self.versiones]

    def __len__(self) -> int:
        return len(self.designados)
