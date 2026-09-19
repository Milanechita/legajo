"""Descarga de listas desde las fuentes oficiales.

Las tres listas que importan para un sujeto obligado argentino son publicas y
no piden credenciales. No hay que registrarse, no hay API key, no hay cuota.

La excepcion es RePET, que no publica un endpoint de datos: solo tiene
buscador web. Ver fuentes/repet.py.

Cada descarga guarda el archivo tal cual vino y calcula su SHA-256. Ese hash
es el que termina en el expediente. Si alguien pregunta contra que version se
screeneo un cliente en marzo, la respuesta esta en el hash, no en la memoria
de nadie.
"""

from __future__ import annotations

import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .base import huella

AGENTE = "legajo/0.2 (herramienta de cumplimiento PLA-FT)"
TIMEOUT = 60


@dataclass(frozen=True)
class Fuente:
    archivo: str
    url: str
    descripcion: str
    obligatoria: bool = True


FUENTES: tuple[Fuente, ...] = (
    Fuente(
        archivo="SDN.CSV",
        url="https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/SDN.CSV",
        descripcion="OFAC Specially Designated Nationals, Tesoro de EE.UU.",
    ),
    Fuente(
        archivo="ALT.CSV",
        url="https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/ALT.CSV",
        descripcion="Alias de la lista OFAC SDN",
    ),
    Fuente(
        archivo="consolidated.xml",
        url="https://scsanctions.un.org/resources/xml/en/consolidated.xml",
        descripcion="Lista Consolidada del Consejo de Seguridad de la ONU",
    ),
    Fuente(
        archivo="uk-sanctions.xml",
        url="https://sanctionslist.fcdo.gov.uk/docs/UK-Sanctions-List.xml",
        descripcion="UK Sanctions List, FCDO",
        obligatoria=False,
    ),
)


@dataclass
class Descarga:
    fuente: Fuente
    ruta: Path | None
    bytes_recibidos: int
    sha256: str
    momento: datetime
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None

    def resumen(self) -> str:
        if not self.ok:
            return f"{self.fuente.archivo}: FALLO ({self.error})"
        kb = self.bytes_recibidos / 1024
        return f"{self.fuente.archivo}: {kb:,.0f} KB  sha256={self.sha256[:12]}"


def _descargar(url: str) -> bytes:
    pedido = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(pedido, timeout=TIMEOUT) as respuesta:
        return respuesta.read()


def actualizar(
    directorio: str | Path,
    *,
    incluir_opcionales: bool = False,
) -> list[Descarga]:
    """Baja las listas al directorio indicado.

    El archivo anterior no se pisa hasta que la descarga nueva termino bien.
    Quedarse con una lista vieja es malo; quedarse sin lista porque se corto
    la conexion a mitad de camino es peor.
    """
    destino = Path(directorio)
    destino.mkdir(parents=True, exist_ok=True)
    resultados: list[Descarga] = []

    for fuente in FUENTES:
        if not fuente.obligatoria and not incluir_opcionales:
            continue

        momento = datetime.now(timezone.utc)
        try:
            contenido = _descargar(fuente.url)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
            resultados.append(Descarga(fuente, None, 0, "", momento, error=str(e)))
            continue

        if not contenido:
            resultados.append(
                Descarga(fuente, None, 0, "", momento, error="respuesta vacia")
            )
            continue

        parcial = destino / f"{fuente.archivo}.parcial"
        parcial.write_bytes(contenido)
        final = destino / fuente.archivo
        parcial.replace(final)

        resultados.append(
            Descarga(fuente, final, len(contenido), huella(contenido), momento)
        )

    return resultados
