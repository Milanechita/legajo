"""Interfaz de linea de comandos.

    python -m legajo screening --padron clientes.csv --listas listas/ --salida informe.xlsx
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import POLITICA_POR_DEFECTO, Politica
from .fuentes.base import Padron
from .fuentes.ofac import ParserOFAC, incorporar_alias
from .fuentes.onu import ParserONU
from .io_planilla import exportar, leer_padron
from .modelo import Caso
from .screening import screenear

PARSERS = {
    "SDN.CSV": ParserOFAC(),
    "consolidated.xml": ParserONU(),
}


def cargar_listas(directorio: Path) -> Padron:
    """Carga todas las listas reconocidas de un directorio.

    Un archivo cuyo nombre no este mapeado se ignora con aviso, en lugar de
    romper la corrida: perder una lista es grave, pero abortar el screening
    completo por un archivo suelto lo es mas.
    """
    padron = Padron()

    for nombre, parser in PARSERS.items():
        ruta = directorio / nombre
        if not ruta.exists():
            print(f"  aviso: {nombre} no encontrado, se omite", file=sys.stderr)
            continue

        contenido = ruta.read_bytes()
        designados, version = parser.parsear(contenido)

        if nombre == "SDN.CSV":
            alt = directorio / "ALT.CSV"
            if alt.exists():
                designados = incorporar_alias(designados, alt.read_bytes())

        padron.incorporar(designados, version)
        print(f"  {version.resumen()}")

    return padron


def comando_screening(args: argparse.Namespace) -> int:
    directorio = Path(args.listas)
    if not directorio.is_dir():
        print(f"error: {directorio} no es un directorio", file=sys.stderr)
        return 2

    print("Cargando listas...")
    padron = cargar_listas(directorio)
    if not padron.designados:
        print("error: ninguna lista pudo cargarse", file=sys.stderr)
        return 2

    clientes = leer_padron(args.padron)
    if not clientes:
        print(f"error: el padron {args.padron} no tiene registros validos", file=sys.stderr)
        return 2

    print(f"\nScreening: {len(clientes)} cliente(s) contra {len(padron)} designado(s)")

    politica = Politica(
        umbral_revision=args.umbral,
        umbral_probable=POLITICA_POR_DEFECTO.umbral_probable,
    )

    casos = [Caso(caso_id=f"C{i:05d}", cliente=c) for i, c in enumerate(clientes, 1)]
    resultado = screenear(casos, padron, politica, actor=args.actor)

    ruta = exportar(resultado, casos, args.salida, politica.umbral_probable)

    escalados = [c for c in casos if c.estado.value == "ESCALADO"]
    print(f"\n  Coincidencias:        {len(resultado.coincidencias)}")
    print(f"  Clientes alcanzados:  {resultado.clientes_con_coincidencia}")
    print(f"  Casos escalados:      {len(escalados)}")
    print(f"\nInforme: {ruta}")

    if escalados:
        print("\nEscalados:")
        for caso in escalados:
            print(f"  {caso.caso_id}  {caso.cliente.nombre}")

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="legajo",
        description="Circuito PLA/FT. Etapa 1: screening contra listas.",
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    scr = sub.add_parser("screening", help="cotejar un padron contra listas de control")
    scr.add_argument("--padron", required=True, help="CSV o XLSX de clientes")
    scr.add_argument("--listas", required=True, help="directorio con las listas descargadas")
    scr.add_argument("--salida", default="informe_screening.xlsx", help="XLSX de salida")
    scr.add_argument("--umbral", type=float, default=POLITICA_POR_DEFECTO.umbral_revision,
                     help="umbral minimo de revision (0-100)")
    scr.add_argument("--actor", default="sistema/screening",
                     help="identificacion del ejecutor, para el expediente")
    scr.set_defaults(func=comando_screening)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
