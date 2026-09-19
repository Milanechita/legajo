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

Vale decirlo sin vueltas: RePET incorpora el listado consolidado del Consejo
de Seguridad de la ONU, asi que en la practica se superpone casi por completo
con lo que ya cotejamos. La diferencia son las designaciones de origen local:
personas con resolucion judicial o del Ministerio Publico Fiscal, y aquellas
sobre las que la UIF ordeno congelamiento administrativo. Esas no estan en
ninguna otra lista.

Este parser acepta el formato JSON de OpenSanctions y un CSV minimo propio,
para quien prefiera cargar el listado a mano sin depender de un tercero.
"""

from __future__ import annotations

import csv
import io
import json
from datetime import date, datetime

from .base import Designado, VersionLista, huella

COLUMNAS_CSV = ["nombre", "tipo", "alias", "documento", "origen"]


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
