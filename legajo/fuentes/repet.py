"""Parser del RePET argentino.

El Registro Publico de Personas y Entidades vinculadas a actos de Terrorismo y
su Financiamiento (Decreto 918/2012, incorporado por el 489/2019) es la lista
que la normativa argentina nombra por su nombre. Los manuales de prevencion
la exigen en el alta de todo cliente, junto con las listas de la ONU.

El problema practico: RePET no publica un endpoint de datos. Solo tiene
buscador web en repet.jus.gob.ar. Para cotejar un padron entero hay dos
caminos, y ninguno es la fuente oficial en formato maquina:

  1. Exportar desde un redistribuidor (OpenSanctions publica el dataset
     ar_repet en JSON y CSV, actualizado a diario).
  2. Cargar a mano el listado consultado en el buscador.

Conviene corregir una suposicion habitual, porque los datos la desmienten.
Se suele decir que RePET es una copia del listado consolidado de la ONU y que
por lo tanto no aporta nada sobre lo que ya se cotea. No es asi.

Sobre el export de septiembre de 2026, de 718 registros:

    Al-Qaida y Taliban ......... 469   vienen de la ONU
    resto ...................... 249   designaciones de origen local

Ese resto son congelamientos ordenados por la UIF, Notificaciones Rojas de
INTERPOL, la causa AMIA, actuaciones de PROCELAC y resoluciones del Ministerio
de Justicia y de Seguridad. Un tercio del registro que no figura en ninguna
otra lista del mundo. Omitir RePET no es un atajo aceptable.

El parser acepta tres formatos: el JSON exportado del propio registro (que usa
los nombres de campo del XML de la ONU), el JSON de OpenSanctions, y un CSV
minimo propio para carga manual.
"""

from __future__ import annotations

import csv
import io
import json
from datetime import date, datetime

from .base import Designado, VersionLista, huella

COLUMNAS_CSV = ["nombre", "tipo", "alias", "documento", "origen"]

# Comites del Consejo de Seguridad. Todo lo que no sea uno de estos es una
# designacion de origen argentino, y esa distincion importa: es la parte del
# registro que no esta en ninguna otra lista.
COMITES_ONU = frozenset({"AL-QAIDA", "TALIBAN", "ISIL (DA'ESH) & AL-QAIDA"})

_MAPA_DOC = {
    "PASSPORT": "PASAPORTE",
    "PASAPORTE": "PASAPORTE",
    "NATIONAL IDENTIFICATION NUMBER": "DOC",
    "ID": "DOC",
    "IDENTITY CARD": "DOC",
}


def origen(comite: str) -> str:
    """Clasifica la designacion por su procedencia."""
    return "ONU" if comite.strip().upper() in COMITES_ONU else "LOCAL"


def _documento(tipo: str, numero: str) -> str:
    etiqueta = _MAPA_DOC.get((tipo or "").strip().upper(), "DOC")
    limpio = "".join(c for c in (numero or "") if c.isalnum()).upper()
    return f"{etiqueta}:{limpio}"


def _fecha_dmy(crudo: str | None) -> date | None:
    """El registro publica las fechas como DD/MM/AAAA."""
    if not crudo or not crudo.strip():
        return None
    try:
        return datetime.strptime(crudo.strip(), "%d/%m/%Y").date()
    except ValueError:
        return None


def _fecha(crudo: str | None) -> date | None:
    if not crudo:
        return None
    try:
        return datetime.fromisoformat(crudo.split("T")[0]).date()
    except ValueError:
        return None


class ParserRePET:
    """Lee el RePET en formato OpenSanctions (JSON por lineas) o CSV propio."""

    nombre_lista = "REPET"

    def parsear(self, contenido: bytes) -> tuple[list[Designado], VersionLista]:
        texto = contenido.decode("utf-8", errors="replace").lstrip()
        if texto.startswith("{") or texto.startswith("["):
            if '"DATAID"' in texto[:4000] or '"FIRST_NAME"' in texto[:4000]:
                designados, publicada = self._json_repet(texto)
            else:
                designados, publicada = self._json(texto)
        else:
            designados, publicada = self._csv(texto)

        version = VersionLista(
            lista=self.nombre_lista,
            publicada=publicada,
            descargada=date.today(),
            registros=len(designados),
            sha256=huella(contenido),
        )
        return designados, version

    # --- Export nativo del registro: campos del XML de la ONU en JSON ---
    def _json_repet(self, texto: str) -> tuple[list[Designado], date | None]:
        try:
            registros = json.loads(texto)
        except json.JSONDecodeError:
            return [], None
        if isinstance(registros, dict):
            registros = [registros]

        designados: list[Designado] = []
        publicada: date | None = None

        for r in registros:
            # Una baja sigue figurando en el archivo con DELISTED_ON cargado.
            # Cotejar contra una persona dada de baja produce un falso
            # positivo que le cuesta una hora al analista.
            if (r.get("DELISTED_ON") or "").strip():
                continue

            nombre = " ".join(
                (r.get(c) or "").strip()
                for c in ("FIRST_NAME", "SECOND_NAME", "THIRD_NAME", "FOURTH_NAME")
            ).strip()
            nombre = " ".join(nombre.split())
            if not nombre:
                continue

            es_entidad = "ENTITY_ALIAS" in r or "ENTITY_ADDRESS" in r
            tipo = "ENTIDAD" if es_entidad else "PERSONA"

            # Se conservan los alias de baja calidad. Generan ruido, pero
            # descartarlos es introducir un falso negativo a mano, y en
            # screening ese es el error caro.
            clave_alias = "ENTITY_ALIAS" if es_entidad else "INDIVIDUAL_ALIAS"
            alias = tuple(dict.fromkeys(
                (a.get("ALIAS_NAME") or "").strip()
                for a in r.get(clave_alias, []) or []
                if (a.get("ALIAS_NAME") or "").strip()
            ))

            fechas = tuple(
                f for f in (
                    (d.get("DATE") or d.get("YEAR") or d.get("FROM_YEAR") or "").strip()
                    for d in r.get("INDIVIDUAL_DATE_OF_BIRTH", []) or []
                ) if f
            )

            nacionalidades = tuple(
                v for v in (
                    (n.get("VALUE") or "").strip()
                    for n in r.get("NATIONALITY", []) or []
                ) if v
            )

            documentos = tuple(
                _documento(d.get("TYPE_OF_DOCUMENT", ""), d.get("NUMBER", ""))
                for d in r.get("INDIVIDUAL_DOCUMENT", []) or []
                if (d.get("NUMBER") or "").strip()
            )

            comite = (r.get("UN_LIST_TYPE") or "").strip()
            referencia = (r.get("REFERENCE_NUMBER") or "").strip()

            designados.append(
                Designado(
                    lista=self.nombre_lista,
                    id_origen=str(r.get("DATAID") or referencia or nombre),
                    nombre=nombre,
                    tipo=tipo,
                    alias=alias,
                    fechas_nacimiento=fechas,
                    nacionalidades=nacionalidades,
                    documentos=documentos,
                    programas=tuple(p for p in (origen(comite), comite, referencia) if p),
                )
            )

            fecha = _fecha_dmy(r.get("LISTED_ON"))
            if fecha and (publicada is None or fecha > publicada):
                publicada = fecha

        return designados, publicada

    # --- OpenSanctions: un objeto JSON por linea ---
    def _json(self, texto: str) -> tuple[list[Designado], date | None]:
        designados: list[Designado] = []
        publicada: date | None = None

        lineas = [texto] if texto.startswith("[") else texto.splitlines()
        registros: list[dict] = []
        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue
            try:
                dato = json.loads(linea)
            except json.JSONDecodeError:
                continue
            registros.extend(dato if isinstance(dato, list) else [dato])

        for r in registros:
            props = r.get("properties", {}) or {}
            nombres = props.get("name") or []
            if not nombres:
                continue

            esquema = (r.get("schema") or "").lower()
            tipo = "PERSONA" if esquema == "person" else "ENTIDAD"

            documentos = tuple(
                f"PASAPORTE:{n.replace(' ', '').upper()}"
                for n in (props.get("passportNumber") or [])
            ) + tuple(
                f"DOC:{n.replace(' ', '').upper()}"
                for n in (props.get("idNumber") or [])
            )

            designados.append(
                Designado(
                    lista=self.nombre_lista,
                    id_origen=str(r.get("id") or nombres[0]),
                    nombre=nombres[0],
                    tipo=tipo,
                    alias=tuple(dict.fromkeys(nombres[1:] + (props.get("alias") or []))),
                    fechas_nacimiento=tuple(props.get("birthDate") or []),
                    nacionalidades=tuple(props.get("nationality") or []),
                    documentos=documentos,
                    programas=tuple(props.get("topics") or ()),
                )
            )

            fecha = _fecha((r.get("last_change") or r.get("last_seen")))
            if fecha and (publicada is None or fecha > publicada):
                publicada = fecha

        return designados, publicada

    # --- CSV propio, para carga manual ---
    def _csv(self, texto: str) -> tuple[list[Designado], date | None]:
        designados: list[Designado] = []

        for i, fila in enumerate(csv.DictReader(io.StringIO(texto)), start=1):
            nombre = (fila.get("nombre") or "").strip()
            if not nombre:
                continue

            alias = tuple(
                a.strip() for a in (fila.get("alias") or "").split(";") if a.strip()
            )
            documento = (fila.get("documento") or "").strip()

            designados.append(
                Designado(
                    lista=self.nombre_lista,
                    id_origen=str(i),
                    nombre=nombre,
                    tipo=(fila.get("tipo") or "PERSONA").strip().upper() or "PERSONA",
                    alias=alias,
                    documentos=(documento,) if documento else (),
                    programas=((fila.get("origen") or "").strip(),)
                    if (fila.get("origen") or "").strip()
                    else (),
                )
            )

        return designados, None
