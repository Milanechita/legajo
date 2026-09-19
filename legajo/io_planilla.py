"""Entrada y salida en los formatos que el area ya usa.

El equipo de cumplimiento trabaja en Excel. Una herramienta que lo obligue a
abandonarlo es la solucion teoricamente correcta e inutil en la practica.
Entra CSV o XLSX, sale XLSX. La automatizacion pasa por debajo; el analista
no cambia de entorno.
"""

from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from .modelo import Caso, Cliente, Documento
from .screening import Coincidencia, ResultadoScreening

FUENTE = "Arial"

_ENCABEZADO = Font(name=FUENTE, bold=True, color="FFFFFF", size=10)
_RELLENO_ENCABEZADO = PatternFill("solid", start_color="1F3864")
_CUERPO = Font(name=FUENTE, size=10)
_PROBABLE = PatternFill("solid", start_color="F8CBAD")
_REVISION = PatternFill("solid", start_color="FFF2CC")

COLUMNAS_PADRON = [
    "cliente_id", "nombre", "tipo", "documento_tipo", "documento_numero",
    "fecha_nacimiento", "nacionalidad", "pais_residencia", "actividad",
]


def _fila_a_cliente(fila: dict[str, str]) -> Cliente:
    documentos = []
    tipo_doc = (fila.get("documento_tipo") or "").strip()
    num_doc = (fila.get("documento_numero") or "").strip()
    if tipo_doc and num_doc:
        documentos.append(Documento(tipo=tipo_doc, numero=num_doc))

    def opcional(clave: str) -> str | None:
        valor = (fila.get(clave) or "").strip()
        return valor or None

    return Cliente(
        cliente_id=(fila.get("cliente_id") or "").strip(),
        nombre=(fila.get("nombre") or "").strip(),
        tipo=(fila.get("tipo") or "PERSONA").strip().upper() or "PERSONA",
        documentos=documentos,
        fecha_nacimiento=opcional("fecha_nacimiento"),
        nacionalidad=opcional("nacionalidad"),
        pais_residencia=opcional("pais_residencia"),
        actividad=opcional("actividad"),
    )


def leer_padron(ruta: str | Path) -> list[Cliente]:
    """Lee el padron de clientes desde CSV o XLSX."""
    ruta = Path(ruta)

    if ruta.suffix.lower() in {".xlsx", ".xlsm"}:
        libro = load_workbook(ruta, read_only=True, data_only=True)
        hoja = libro.active
        filas = hoja.iter_rows(values_only=True)
        encabezados = [str(c or "").strip() for c in next(filas)]
        registros = [
            dict(zip(encabezados, [("" if v is None else str(v)) for v in fila]))
            for fila in filas
        ]
        libro.close()
    else:
        with ruta.open(encoding="utf-8-sig", newline="") as f:
            registros = list(csv.DictReader(f))

    clientes = [_fila_a_cliente(r) for r in registros]
    return [c for c in clientes if c.cliente_id and c.nombre]


def _ajustar_anchos(hoja, anchos: list[int]) -> None:
    for i, ancho in enumerate(anchos, start=1):
        hoja.column_dimensions[get_column_letter(i)].width = ancho


def _escribir_encabezado(hoja, columnas: list[str]) -> None:
    hoja.append(columnas)
    for celda in hoja[1]:
        celda.font = _ENCABEZADO
        celda.fill = _RELLENO_ENCABEZADO
        celda.alignment = Alignment(vertical="center", wrap_text=True)
    hoja.freeze_panes = "A2"


def exportar(
    resultado: ResultadoScreening,
    casos: list[Caso],
    ruta: str | Path,
    umbral_probable: float,
) -> Path:
    """Escribe el informe de screening en XLSX.

    Tres hojas: resumen, coincidencias, y expediente completo. La tercera es
    la que importa en una inspeccion.
    """
    ruta = Path(ruta)
    libro = Workbook()

    # --- Hoja 1: resumen ---
    resumen = libro.active
    resumen.title = "Resumen"
    _escribir_encabezado(resumen, ["Concepto", "Valor"])
    por_lista: dict[str, int] = {}
    for c in resultado.coincidencias:
        por_lista[c.lista] = por_lista.get(c.lista, 0) + 1

    filas_resumen = [
        ("Clientes evaluados", resultado.clientes_evaluados),
        ("Designados en padron", resultado.designados_evaluados),
        ("Coincidencias totales", len(resultado.coincidencias)),
        ("Clientes con coincidencia", resultado.clientes_con_coincidencia),
        ("Casos escalados", sum(1 for c in casos if c.estado.value == "ESCALADO")),
        ("Umbral de revision", min((c.score for c in resultado.coincidencias), default=0)),
        ("Umbral de probable", umbral_probable),
    ]
    for lista, cantidad in sorted(por_lista.items()):
        filas_resumen.append((f"Coincidencias en {lista}", cantidad))

    for fila in filas_resumen:
        resumen.append(list(fila))
    for fila in resumen.iter_rows(min_row=2):
        for celda in fila:
            celda.font = _CUERPO
    _ajustar_anchos(resumen, [34, 18])

    # --- Hoja 2: coincidencias ---
    hoja = libro.create_sheet("Coincidencias")
    columnas = [
        "cliente_id", "lista", "id_origen", "designado", "matcheo_contra",
        "score", "criterio", "programas", "atenuantes", "prioridad",
    ]
    _escribir_encabezado(hoja, columnas)

    for c in resultado.coincidencias:
        prioridad = "PROBABLE" if c.score >= umbral_probable else "REVISAR"
        hoja.append([
            c.cliente_id, c.lista, c.id_origen, c.nombre_designado,
            c.nombre_matcheado, c.score, c.criterio,
            "; ".join(c.programas), "; ".join(c.atenuantes), prioridad,
        ])
        relleno = _PROBABLE if prioridad == "PROBABLE" else _REVISION
        for celda in hoja[hoja.max_row]:
            celda.font = _CUERPO
            celda.fill = relleno
    _ajustar_anchos(hoja, [14, 18, 12, 34, 30, 9, 12, 20, 40, 12])

    # --- Hoja 3: expediente ---
    exp = libro.create_sheet("Expediente")
    _escribir_encabezado(exp, ["caso_id", "cliente", "momento", "actor", "accion", "detalle"])
    for caso in casos:
        for ev in caso.evidencia:
            exp.append([
                caso.caso_id,
                caso.cliente.nombre,
                ev.momento.isoformat(timespec="seconds"),
                ev.actor,
                ev.accion,
                "; ".join(f"{k}={v}" for k, v in ev.detalle.items()),
            ])
    for fila in exp.iter_rows(min_row=2):
        for celda in fila:
            celda.font = _CUERPO
    _ajustar_anchos(exp, [12, 28, 22, 20, 22, 90])

    libro.save(ruta)
    return ruta
