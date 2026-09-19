"""Interfaz de linea de comandos.

    python -m legajo screening --padron clientes.csv --listas listas/
    python -m legajo circuito  --padron clientes.csv --listas listas/ --societaria estructura.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .beneficiario import resolver
from .config import POLITICA_POR_DEFECTO, Politica
from .fuentes.base import Padron
from .fuentes.descarga import actualizar
from .fuentes.ofac import ParserOFAC, incorporar_alias
from .fuentes.onu import ParserONU
from .fuentes.repet import ParserRePET
from .io_planilla import (
    agregar_hojas_etapa2, exportar, leer_estructura, leer_padron, leer_peps,
)
from .matriz import MATRIZ_POR_DEFECTO
from .modelo import Caso, Estado
from .riesgo import evaluar_casos
from .screening import screenear

# Cada lista logica puede venir en varios archivos, y en varios formatos
# alternativos. Se agrupan asi para avisar una sola vez por lista faltante:
# un aviso falso repetido entrena al analista a ignorar los avisos.
FUENTES_LOCALES = (
    ("OFAC SDN", ("SDN.CSV",), ParserOFAC()),
    ("Lista Consolidada ONU", ("consolidated.xml",), ParserONU()),
    ("RePET", ("repet_personas.json", "repet_entidades.json",
               "repet.json", "repet.csv"), ParserRePET()),
)


def cargar_listas(directorio: Path) -> Padron:
    """Carga todas las listas reconocidas de un directorio.

    Un archivo cuyo nombre no este mapeado se ignora con aviso, en lugar de
    romper la corrida: perder una lista es grave, pero abortar el screening
    completo por un archivo suelto lo es mas.
    """
    padron = Padron()

    for etiqueta, archivos, parser in FUENTES_LOCALES:
        encontrados = [directorio / a for a in archivos if (directorio / a).exists()]
        if not encontrados:
            print(f"  aviso: {etiqueta} no encontrada, se omite", file=sys.stderr)
            continue

        for ruta in encontrados:
            contenido = ruta.read_bytes()
            designados, version = parser.parsear(contenido)

            if ruta.name == "SDN.CSV":
                alt = directorio / "ALT.CSV"
                if alt.exists():
                    designados = incorporar_alias(designados, alt.read_bytes())

            padron.incorporar(designados, version)
            print(f"  {version.resumen()}")

    _avisar_duplicados(padron)
    return padron


def _avisar_duplicados(padron: Padron) -> None:
    """Informa nombres repetidos dentro del padron de designados.

    RePET lista a la misma persona mas de una vez cuando hubo varias
    resoluciones sobre ella. No se fusionan, porque cada asiento es una
    designacion distinta, pero conviene decirlo: si no, el analista ve el
    mismo nombre tres veces y cree que el programa esta roto.
    """
    from collections import Counter

    from .normalizar import normalizar

    conteo = Counter(
        normalizar(d.nombre, es_entidad=d.es_entidad) for d in padron.designados
    )
    repetidos = {n: c for n, c in conteo.items() if c > 1 and n}
    if repetidos:
        extra = sum(repetidos.values()) - len(repetidos)
        print(f"  aviso: {len(repetidos)} nombre(s) repetido(s) en el origen "
              f"({extra} asiento(s) adicional(es)); no se fusionan")


def _preparar(args: argparse.Namespace):
    """Carga listas y padron. Comun a los dos comandos."""
    directorio = Path(args.listas)
    if not directorio.is_dir():
        print(f"error: {directorio} no es un directorio", file=sys.stderr)
        return None

    print("Cargando listas...")
    padron = cargar_listas(directorio)
    if not padron.designados:
        print("error: ninguna lista pudo cargarse", file=sys.stderr)
        return None

    clientes = leer_padron(args.padron)
    if not clientes:
        print(f"error: el padron {args.padron} no tiene registros validos", file=sys.stderr)
        return None

    return padron, clientes


def comando_screening(args: argparse.Namespace) -> int:
    preparado = _preparar(args)
    if preparado is None:
        return 2
    padron, clientes = preparado

    print(f"\nScreening: {len(clientes)} cliente(s) contra {len(padron)} designado(s)")

    politica = Politica(
        umbral_revision=args.umbral,
        umbral_probable=POLITICA_POR_DEFECTO.umbral_probable,
    )
    casos = [Caso(caso_id=f"C{i:05d}", cliente=c) for i, c in enumerate(clientes, 1)]
    resultado = screenear(casos, padron, politica, actor=args.actor)
    ruta = exportar(resultado, casos, args.salida, politica.umbral_probable)

    escalados = [c for c in casos if c.estado is Estado.ESCALADO]
    print(f"\n  Coincidencias:        {len(resultado.coincidencias)}")
    print(f"  Clientes alcanzados:  {resultado.clientes_con_coincidencia}")
    print(f"  Casos escalados:      {len(escalados)}")
    print(f"\nInforme: {ruta}")

    if escalados:
        print("\nEscalados:")
        for caso in escalados:
            print(f"  {caso.caso_id}  {caso.cliente.nombre}")
    return 0


def comando_circuito(args: argparse.Namespace) -> int:
    """Etapa 1 + Etapa 2 encadenadas."""
    preparado = _preparar(args)
    if preparado is None:
        return 2
    padron, clientes = preparado

    politica = Politica(
        umbral_revision=args.umbral,
        umbral_probable=POLITICA_POR_DEFECTO.umbral_probable,
    )
    casos = [Caso(caso_id=f"C{i:05d}", cliente=c) for i, c in enumerate(clientes, 1)]

    # --- Etapa 1 ---
    print(f"\n[1/2] Screening: {len(clientes)} cliente(s) contra {len(padron)} designado(s)")
    resultado = screenear(casos, padron, politica, actor=args.actor)
    print(f"      {len(resultado.coincidencias)} coincidencia(s), "
          f"{sum(1 for c in casos if c.estado is Estado.ESCALADO)} escalado(s)")

    por_cliente: dict[str, list] = {}
    for c in resultado.coincidencias:
        por_cliente.setdefault(c.cliente_id, []).append(c)

    # --- Etapa 2 ---
    print("\n[2/2] Beneficiario final y scoring EBR")

    estructura = leer_estructura(args.societaria, clientes) if args.societaria else None
    resoluciones = {}
    if estructura is not None:
        for cliente in clientes:
            if cliente.tipo == "PERSONA":
                continue
            resoluciones[cliente.cliente_id] = resolver(estructura, cliente.cliente_id)
        print(f"      {len(resoluciones)} estructura(s) analizada(s)")

    registro_pep = leer_peps(args.peps) if args.peps else None
    if registro_pep is not None:
        vencidas = registro_pep.vencidas()
        print(f"      {len(registro_pep)} declaracion(es) de PEP", end="")
        print(f", {len(vencidas)} vencida(s) por el plazo de 2 anios" if vencidas else "")

    evaluaciones = evaluar_casos(
        casos, resoluciones, por_cliente,
        registro_pep=registro_pep,
        umbral_probable=politica.umbral_probable,
        matriz=MATRIZ_POR_DEFECTO,
        actor=args.actor,
    )

    # El expediente se escribe recien ahora, con la evidencia de las dos etapas.
    ruta = exportar(resultado, casos, args.salida, politica.umbral_probable)
    agregar_hojas_etapa2(ruta, resoluciones, evaluaciones, casos)

    conteo = {"ALTO": 0, "MEDIO": 0, "BAJO": 0}
    for ev in evaluaciones.values():
        conteo[ev.nivel] += 1

    print("\n  Distribucion de riesgo")
    for nivel in ("ALTO", "MEDIO", "BAJO"):
        print(f"    {nivel:8} {conteo[nivel]:3}")
    print(f"    {'escalado':8} {sum(1 for c in casos if c.estado is Estado.ESCALADO):3}"
          "   (no scoreados: coincidencia en lista critica)")

    altos = [(cid, ev) for cid, ev in evaluaciones.items() if ev.nivel == "ALTO"]
    if altos:
        nombres = {c.cliente.cliente_id: c.cliente.nombre for c in casos}
        print("\n  Diligencia reforzada:")
        for cid, ev in sorted(altos, key=lambda kv: -kv[1].puntaje):
            motivo = ", ".join(ev.elevadores) or f"{ev.puntaje} pts"
            print(f"    {cid}  {nombres.get(cid, ''):28} {motivo}")

    print(f"\nInforme: {ruta}")
    return 0


def comando_actualizar(args: argparse.Namespace) -> int:
    """Baja las listas desde las fuentes oficiales."""
    print(f"Descargando listas a {args.listas}\n")
    resultados = actualizar(args.listas, incluir_opcionales=args.incluir_opcionales)

    for r in resultados:
        print(f"  {r.resumen()}")

    fallidas = [r for r in resultados if not r.ok]
    print()
    if fallidas:
        print(f"{len(fallidas)} de {len(resultados)} fuentes fallaron.")
        print("Las listas anteriores quedaron intactas: screenear con una lista")
        print("vieja es malo, pero screenear con una lista a medias es peor.")

    print("\nRePET no se descarga aca porque no publica un endpoint de datos,")
    print("solo buscador web en repet.jus.gob.ar. Ver fuentes/repet.py para")
    print("los dos caminos posibles.")

    return 1 if fallidas else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="legajo",
        description="Circuito de analisis PLA/FT.",
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    def comunes(p: argparse.ArgumentParser) -> None:
        p.add_argument("--padron", required=True, help="CSV o XLSX de clientes")
        p.add_argument("--listas", required=True, help="directorio con las listas descargadas")
        p.add_argument("--umbral", type=float, default=POLITICA_POR_DEFECTO.umbral_revision,
                       help="umbral minimo de revision (0-100)")
        p.add_argument("--actor", default="sistema/legajo",
                       help="identificacion del ejecutor, para el expediente")

    scr = sub.add_parser("screening", help="etapa 1: cotejo contra listas de control")
    comunes(scr)
    scr.add_argument("--salida", default="informe_screening.xlsx")
    scr.set_defaults(func=comando_screening)

    cir = sub.add_parser("circuito", help="etapas 1 y 2: screening, beneficiario final y riesgo")
    comunes(cir)
    cir.add_argument("--societaria", help="CSV o XLSX con el grafo societario")
    cir.add_argument("--peps", help="CSV de declaraciones juradas de condicion PEP")
    cir.add_argument("--salida", default="informe_circuito.xlsx")
    cir.set_defaults(func=comando_circuito)

    act = sub.add_parser("actualizar-listas", help="bajar las listas desde las fuentes oficiales")
    act.add_argument("--listas", required=True, help="directorio destino")
    act.add_argument("--incluir-opcionales", action="store_true",
                     help="bajar tambien las listas no obligatorias para Argentina")
    act.set_defaults(func=comando_actualizar)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
