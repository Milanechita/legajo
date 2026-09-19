"""Parser de la Lista Consolidada del Consejo de Seguridad de la ONU (XML).

Fuente: https://scsanctions.un.org/resources/xml/en/consolidated.xml

Relevante para la Res. UIF 3/2026: las designaciones bajo las resoluciones
1718 (Corea del Norte) y las relativas a Iran son las que activan el regimen
de financiamiento de la proliferacion (FPADM) y el congelamiento sin demora.
"""

from __future__ import annotations

from datetime import date, datetime
from xml.etree import ElementTree

from .base import Designado, VersionLista, huella


def _texto(nodo, etiqueta: str) -> str:
    hijo = nodo.find(etiqueta)
    return (hijo.text or "").strip() if hijo is not None and hijo.text else ""


def _nombre_completo(nodo) -> str:
    partes = [
        _texto(nodo, "FIRST_NAME"),
        _texto(nodo, "SECOND_NAME"),
        _texto(nodo, "THIRD_NAME"),
        _texto(nodo, "FOURTH_NAME"),
    ]
    return " ".join(p for p in partes if p)


class ParserONU:
    nombre_lista = "ONU_CONSOLIDADA"

    def parsear(self, contenido: bytes) -> tuple[list[Designado], VersionLista]:
        raiz = ElementTree.fromstring(contenido)
        designados: list[Designado] = []

        for etiqueta, tipo in (("INDIVIDUALS/INDIVIDUAL", "PERSONA"),
                               ("ENTITIES/ENTITY", "ENTIDAD")):
            for nodo in raiz.findall(etiqueta):
                nombre = _nombre_completo(nodo)
                if not nombre:
                    continue

                alias = tuple(
                    a for a in (
                        _texto(n, "ALIAS_NAME")
                        for n in nodo.findall("INDIVIDUAL_ALIAS")
                        + nodo.findall("ENTITY_ALIAS")
                    ) if a
                )

                fechas = tuple(
                    f for f in (
                        _texto(n, "DATE") or _texto(n, "YEAR")
                        for n in nodo.findall("INDIVIDUAL_DATE_OF_BIRTH")
                    ) if f
                )

                nacionalidades = tuple(
                    n for n in (
                        _texto(x, "VALUE")
                        for x in nodo.findall("NATIONALITY")
                    ) if n
                )

                documentos = tuple(
                    f"PASAPORTE:{num.replace(' ', '').upper()}"
                    for num in (
                        _texto(n, "NUMBER")
                        for n in nodo.findall("INDIVIDUAL_DOCUMENT")
                    ) if num
                )

                comite = _texto(nodo, "UN_LIST_TYPE")

                designados.append(
                    Designado(
                        lista=self.nombre_lista,
                        id_origen=_texto(nodo, "DATAID") or nombre,
                        nombre=nombre,
                        tipo=tipo,
                        alias=alias,
                        fechas_nacimiento=fechas,
                        nacionalidades=nacionalidades,
                        documentos=documentos,
                        programas=(comite,) if comite else (),
                    )
                )

        publicada = None
        crudo = raiz.get("dateGenerated", "")
        if crudo:
            try:
                publicada = datetime.fromisoformat(crudo.split("T")[0]).date()
            except ValueError:
                publicada = None

        version = VersionLista(
            lista=self.nombre_lista,
            publicada=publicada,
            descargada=date.today(),
            registros=len(designados),
            sha256=huella(contenido),
        )
        return designados, version
