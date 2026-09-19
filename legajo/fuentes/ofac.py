"""Parser de la lista OFAC SDN (formato CSV publico del Tesoro de EE.UU.).

Fuente: https://sanctionslist.ofac.treas.gov/  (SDN.CSV / ALT.CSV)

El CSV de OFAC no trae encabezados y usa "-0-" como marcador de campo vacio.
Toda esa suciedad se absorbe aca y no sale de este archivo.
"""

from __future__ import annotations

import csv
import io
import re
from datetime import date

from .base import Designado, VersionLista, huella

VACIO = "-0-"

# Los identificadores vienen embebidos en texto libre en el campo de remarks.
_DOC = re.compile(
    r"\b(Passport|Cedula No\.|D\.?N\.?I\.?|R\.?U\.?C\.?|Tax ID No\.|C\.?U\.?I\.?T\.?)\s*"
    r"([A-Z0-9\-\.]{4,20})",
    re.IGNORECASE,
)
_FECHA = re.compile(r"DOB\s+(\d{1,2}\s+\w{3}\s+\d{4}|\d{4})", re.IGNORECASE)
_NACIONALIDAD = re.compile(r"nationality\s+([A-Za-z ]+?)(?:;|$)", re.IGNORECASE)

_TIPO = {
    "individual": "PERSONA",
    "-0-": "ENTIDAD",
    "vessel": "BUQUE",
    "aircraft": "AERONAVE",
}

_MAPA_DOC = {
    "passport": "PASAPORTE",
    "cedula no.": "CEDULA",
    "dni": "DNI",
    "d.n.i.": "DNI",
    "ruc": "RUC",
    "r.u.c.": "RUC",
    "tax id no.": "TAX_ID",
    "cuit": "CUIT",
    "c.u.i.t.": "CUIT",
}


def _limpio(valor: str) -> str:
    valor = (valor or "").strip()
    return "" if valor == VACIO else valor


def _canonico(tipo_crudo: str, numero: str) -> str:
    tipo = _MAPA_DOC.get(tipo_crudo.lower().strip(), tipo_crudo.upper().strip())
    limpio = "".join(c for c in numero if c.isalnum()).upper()
    return f"{tipo}:{limpio}"


class ParserOFAC:
    nombre_lista = "OFAC_SDN"

    def parsear(self, contenido: bytes) -> tuple[list[Designado], VersionLista]:
        texto = contenido.decode("utf-8", errors="replace")
        lector = csv.reader(io.StringIO(texto))

        designados: list[Designado] = []
        for fila in lector:
            if len(fila) < 12:
                continue

            ent_num = _limpio(fila[0])
            nombre = _limpio(fila[1])
            if not ent_num or not nombre:
                continue

            tipo = _TIPO.get(_limpio(fila[2]).lower(), "ENTIDAD")
            programa = _limpio(fila[3])
            remarks = _limpio(fila[11])

            documentos = tuple(
                _canonico(t, n) for t, n in _DOC.findall(remarks)
            )
            fechas = tuple(f.strip() for f in _FECHA.findall(remarks))
            nacionalidades = tuple(n.strip() for n in _NACIONALIDAD.findall(remarks))

            designados.append(
                Designado(
                    lista=self.nombre_lista,
                    id_origen=ent_num,
                    nombre=nombre,
                    tipo=tipo,
                    fechas_nacimiento=fechas,
                    nacionalidades=nacionalidades,
                    documentos=documentos,
                    programas=(programa,) if programa else (),
                )
            )

        version = VersionLista(
            lista=self.nombre_lista,
            publicada=None,  # el CSV de OFAC no trae fecha embebida
            descargada=date.today(),
            registros=len(designados),
            sha256=huella(contenido),
        )
        return designados, version


def incorporar_alias(designados: list[Designado], contenido_alt: bytes) -> list[Designado]:
    """Fusiona ALT.CSV (alias) sobre los designados ya parseados.

    OFAC publica los alias en un archivo separado, vinculado por ent_num.
    """
    texto = contenido_alt.decode("utf-8", errors="replace")
    por_entidad: dict[str, list[str]] = {}

    for fila in csv.reader(io.StringIO(texto)):
        if len(fila) < 4:
            continue
        ent_num = _limpio(fila[0])
        alias = _limpio(fila[3])
        if ent_num and alias:
            por_entidad.setdefault(ent_num, []).append(alias)

    fusionados = []
    for d in designados:
        extra = por_entidad.get(d.id_origen)
        if extra:
            d = Designado(**{**d.__dict__, "alias": tuple({*d.alias, *extra})})
        fusionados.append(d)
    return fusionados
