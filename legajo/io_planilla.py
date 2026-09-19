"""Entrada y salida en los formatos que el area ya usa.

El equipo de cumplimiento trabaja en Excel. Una herramienta que lo obligue a
abandonarlo es la solucion teoricamente correcta e inutil en la practica.
Entra CSV o XLSX, sale XLSX. La automatizacion pasa por debajo; el analista
no cambia de entorno.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import TYPE_CHECKING

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

if TYPE_CHECKING:
    from .beneficiario import Resolucion
    from .riesgo import Evaluacion

from .modelo import Caso, Cliente, Documento
from .pep import PEP, RegistroPEP
from .screening import Coincidencia, ResultadoScreening
from .societaria import Administracion, Control, Estructura, Nodo, Participacion

FUENTE = "Arial"

_ENCABEZADO = Font(name=FUENTE, bold=True, color="FFFFFF", size=10)
_RELLENO_ENCABEZADO = PatternFill("solid", start_color="1F3864")
_CUERPO = Font(name=FUENTE, size=10)
_PROBABLE = PatternFill("solid", start_color="F8CBAD")
_REVISION = PatternFill("solid", start_color="FFF2CC")

COLUMNAS_PADRON = [
    "cliente_id", "nombre", "tipo", "documento_tipo", "documento_numero",
    "fecha_nacimiento", "nacionalidad", "pais_residencia", "actividad",
    "oferta_publica",
]


def _booleano(valor: str) -> bool:
    return (valor or "").strip().lower() in {"si", "sí", "s", "true", "1", "x", "yes"}


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
        oferta_publica=_booleano(fila.get("oferta_publica", "")),
    )


def _leer_tabla(ruta: Path) -> list[dict[str, str]]:
    """Lee CSV o XLSX a una lista de diccionarios. Un solo camino para ambos."""
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
        return registros

    with ruta.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def leer_padron(ruta: str | Path) -> list[Cliente]:
    """Lee el padron de clientes desde CSV o XLSX."""
    clientes = [_fila_a_cliente(r) for r in _leer_tabla(Path(ruta))]
    return [c for c in clientes if c.cliente_id and c.nombre]


COLUMNAS_ESTRUCTURA = [
    "relacion", "origen_id", "origen_nombre", "origen_tipo", "origen_jurisdiccion",
    "origen_oferta_publica", "destino_id", "capital", "voto", "detalle",
]

COLUMNAS_PEP = ["cliente_id", "tipo", "cargo", "fecha_cese", "por_parentesco"]


def leer_peps(ruta: str | Path) -> RegistroPEP:
    """Lee las declaraciones juradas de condicion PEP.

    Una condicion cesada hace mas de dos anios ya no es PEP, pero el archivo
    la conserva igual: el dato sirve para el expediente, y borrarlo obligaria
    a volver a pedirle la declaracion al cliente.
    """
    from datetime import datetime

    peps: list[PEP] = []
    for fila in _leer_tabla(Path(ruta)):
        cliente_id = (fila.get("cliente_id") or "").strip()
        if not cliente_id:
            continue

        cese = None
        crudo = (fila.get("fecha_cese") or "").strip()
        if crudo:
            try:
                cese = datetime.fromisoformat(crudo.split("T")[0]).date()
            except ValueError:
                cese = None

        peps.append(PEP(
            cliente_id=cliente_id,
            tipo=(fila.get("tipo") or "NACIONAL").strip().upper() or "NACIONAL",
            cargo=(fila.get("cargo") or "").strip(),
            fecha_cese=cese,
            por_parentesco=_booleano(fila.get("por_parentesco", "")),
        ))

    return RegistroPEP(peps)


def _fraccion(valor: str) -> float:
    """Acepta 0.60, 60 y 60% como la misma cosa."""
    texto = (valor or "").strip().replace("%", "").replace(",", ".")
    if not texto:
        return 0.0
    numero = float(texto)
    return numero / 100.0 if numero > 1.0 else numero


def leer_estructura(ruta: str | Path, clientes: list[Cliente] | None = None) -> Estructura:
    """Lee el grafo societario.

    Una sola tabla con una columna `relacion` que despacha el tipo. Agregar un
    tipo de vinculo nuevo es agregar una rama en el despacho, no un archivo
    de entrada nuevo ni un formato paralelo.
    """
    estructura = Estructura()

    for cliente in clientes or []:
        estructura.agregar_nodo(Nodo(
            id=cliente.cliente_id,
            nombre=cliente.nombre,
            tipo=cliente.tipo,
            jurisdiccion=(cliente.pais_residencia or "AR").strip().upper() or "AR",
            oferta_publica=cliente.oferta_publica,
        ))

    for fila in _leer_tabla(Path(ruta)):
        relacion = (fila.get("relacion") or "").strip().upper()
        origen = (fila.get("origen_id") or "").strip()
        destino = (fila.get("destino_id") or "").strip()
        if not relacion or not origen or not destino:
            continue

        estructura.agregar_nodo(Nodo(
            id=origen,
            nombre=(fila.get("origen_nombre") or origen).strip(),
            tipo=(fila.get("origen_tipo") or "PERSONA").strip().upper() or "PERSONA",
            jurisdiccion=(fila.get("origen_jurisdiccion") or "AR").strip().upper() or "AR",
            oferta_publica=_booleano(fila.get("origen_oferta_publica", "")),
        ))

        detalle = (fila.get("detalle") or "").strip()

        if relacion == "PARTICIPACION":
            capital = _fraccion(fila.get("capital", ""))
            voto_crudo = (fila.get("voto") or "").strip()
            estructura.agregar_participacion(Participacion(
                propietario=origen,
                participada=destino,
                capital=capital,
                voto=_fraccion(voto_crudo) if voto_crudo else None,
            ))
        elif relacion == "CONTROL":
            estructura.agregar_control(Control(
                persona=origen, entidad=destino,
                motivo=detalle or "control final por otros medios",
            ))
        elif relacion == "ADMINISTRACION":
            estructura.agregar_administracion(Administracion(
                persona=origen, entidad=destino,
                cargo=detalle or "administrador",
            ))

    return estructura


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


_NIVEL_RELLENO = {
    "ALTO": PatternFill("solid", start_color="F4B6B0"),
    "MEDIO": PatternFill("solid", start_color="FFE599"),
    "BAJO": PatternFill("solid", start_color="D9EAD3"),
}


def agregar_hojas_etapa2(
    ruta: str | Path,
    resoluciones: dict[str, "Resolucion"],
    evaluaciones: dict[str, "Evaluacion"],
    casos: list[Caso],
) -> Path:
    """Agrega las hojas de beneficiario final y riesgo al informe existente.

    Se escribe sobre el mismo libro que produjo la etapa 1 en lugar de emitir
    un segundo archivo: el analista recibe un informe, no una carpeta.
    """
    ruta = Path(ruta)
    libro = load_workbook(ruta)
    nombres = {c.cliente.cliente_id: c.cliente.nombre for c in casos}

    # --- Beneficiario final ---
    hoja = libro.create_sheet("Beneficiario final")
    _escribir_encabezado(hoja, [
        "cliente_id", "cliente", "beneficiario", "capital", "voto",
        "via", "detalle", "umbral", "niveles", "titularidad_opaca", "observaciones",
    ])

    for cliente_id, r in resoluciones.items():
        obs = "; ".join(r.observaciones)
        etiqueta = "EXCEPTUADA (oferta publica)" if r.exceptuada else "NO IDENTIFICADO"
        if not r.beneficiarios:
            hoja.append([
                cliente_id, nombres.get(cliente_id, ""), etiqueta,
                None, None, "", "", r.umbral_aplicado, r.profundidad_maxima,
                r.titularidad_opaca, obs,
            ])
        for b in r.beneficiarios:
            hoja.append([
                cliente_id, nombres.get(cliente_id, ""), b.nombre,
                b.capital, b.voto, b.via, b.detalle, r.umbral_aplicado,
                r.profundidad_maxima, r.titularidad_opaca, obs,
            ])

    for fila in hoja.iter_rows(min_row=2):
        for celda in fila:
            celda.font = _CUERPO
        for idx in (4, 5, 8, 10):  # capital, voto, umbral, opaca
            fila[idx - 1].number_format = "0.00%"
    _ajustar_anchos(hoja, [12, 26, 28, 10, 10, 14, 46, 9, 9, 16, 50])

    # --- Riesgo ---
    hoja = libro.create_sheet("Riesgo")
    _escribir_encabezado(hoja, [
        "cliente_id", "cliente", "puntaje", "nivel", "regimen",
        "proxima_revision", "elevadores", "factores aplicados",
    ])

    orden = {"ALTO": 0, "MEDIO": 1, "BAJO": 2}
    for cliente_id, ev in sorted(
        evaluaciones.items(), key=lambda kv: (orden[kv[1].nivel], -kv[1].puntaje)
    ):
        hoja.append([
            cliente_id, nombres.get(cliente_id, ""), ev.puntaje, ev.nivel, ev.regimen,
            ev.proxima_revision().isoformat(), "; ".join(ev.elevadores),
            " | ".join(f"{f.codigo} (+{f.puntos:g}) {f.descripcion}" for f in ev.factores),
        ])
        relleno = _NIVEL_RELLENO.get(ev.nivel)
        for celda in hoja[hoja.max_row]:
            celda.font = _CUERPO
            if relleno:
                celda.fill = relleno
    _ajustar_anchos(hoja, [12, 26, 9, 9, 18, 16, 30, 110])

    libro.save(ruta)
    return ruta
