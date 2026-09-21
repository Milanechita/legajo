"""Interfaz de linea de comandos.

    python -m legajo screening --padron clientes.csv --listas listas/
    python -m legajo circuito  --padron clientes.csv --listas listas/ --societaria estructura.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .alertas import monitorear, reglas_inactivas
from .beneficiario import resolver
from .config import (
    POLITICA_POR_DEFECTO, Politica, parametros_con_listas, umbral_reporte_vigente,
)
from .circuito import Corrida, a_consola, correr
from .congelamiento import obligaciones
from .exportacion import escribir
from .fuentes.base import Padron
from .fuentes.descarga import actualizar
from .fuentes.ofac import ParserOFAC, incorporar_alias
from .fuentes.onu import ParserONU
from .fuentes.repet import ParserRePET
from .io_planilla import (
    agregar_hoja_alertas, agregar_hojas_etapa2, agregar_hojas_etapa4,
    agregar_hojas_etapa5, exportar, leer_decisiones, leer_estructura,
    leer_operaciones, leer_padron, leer_peps, leer_perfiles,
)
from .matriz import MATRIZ_POR_DEFECTO
from .modelo import Caso, Estado
from .operaciones import agrupar
from .ros import Resolucion, armar
from .sanciones import estimar
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
    """Etapas 1 a 4, con la planilla como salida."""
    preparado = _preparar(args)
    if preparado is None:
        return 2
    padron, clientes = preparado

    corrida = _correr_con_args(args, padron, clientes)

    # El expediente se escribe recien ahora, con la evidencia de las cuatro etapas.
    ruta = exportar(corrida.screening, corrida.casos, args.salida,
                    corrida.politica.umbral_probable)
    agregar_hojas_etapa2(ruta, corrida.resoluciones, corrida.evaluaciones, corrida.casos)
    agregar_hoja_alertas(ruta, corrida.alertas, corrida.casos,
                         corrida.evaluaciones, corrida.perfiles)
    agregar_hojas_etapa4(ruta, corrida.congelamientos, corrida.exposicion)

    _resumen(corrida)
    print(f"\nInforme: {ruta}")
    return 0


def _correr_con_args(args: argparse.Namespace, padron, clientes) -> Corrida:
    """Traduce los argumentos de la linea de comandos a una corrida."""
    politica = Politica(
        umbral_revision=args.umbral,
        umbral_probable=POLITICA_POR_DEFECTO.umbral_probable,
    )
    return correr(
        padron, clientes,
        politica=politica,
        societaria=getattr(args, "societaria", None),
        peps=getattr(args, "peps", None),
        operaciones=getattr(args, "operaciones", None),
        perfiles=getattr(args, "perfiles", None),
        umbral_reporte=getattr(args, "umbral_reporte", None),
        actor=args.actor,
        avisar=a_consola,
    )


def _resumen(corrida: Corrida) -> None:
    """Imprime el resumen de la corrida. Solo lee, no calcula nada."""
    conteo = {"ALTO": 0, "MEDIO": 0, "BAJO": 0}
    for ev in corrida.evaluaciones.values():
        conteo[ev.nivel] += 1

    print("\n  Distribucion de riesgo")
    for nivel in ("ALTO", "MEDIO", "BAJO"):
        print(f"    {nivel:8} {conteo[nivel]:3}")
    escalados = sum(1 for c in corrida.casos if c.estado is Estado.ESCALADO)
    print(f"    {'escalado':8} {escalados:3}"
          "   (no scoreados: coincidencia en lista critica)")

    altos = [(cid, ev) for cid, ev in corrida.evaluaciones.items() if ev.nivel == "ALTO"]
    if altos:
        nombres = corrida.nombres
        print("\n  Diligencia reforzada:")
        for cid, ev in sorted(altos, key=lambda kv: -kv[1].puntaje):
            motivo = ", ".join(ev.elevadores) or f"{ev.puntaje} pts"
            print(f"    {cid}  {nombres.get(cid, ''):28} {motivo}")

    if corrida.alertas:
        from collections import Counter
        conteo = Counter(a.codigo for lista in corrida.alertas.values() for a in lista)
        criticas = sum(1 for lista in corrida.alertas.values()
                       for a in lista if a.severidad == "ALTA")
        print(f"\n  Alertas de monitoreo: {sum(conteo.values())} "
              f"sobre {len(corrida.alertas)} cliente(s), {criticas} de severidad alta")
        for codigo, n in conteo.most_common():
            print(f"    {codigo:28} {n:3}")

        vencidas = [a for lista in corrida.alertas.values() for a in lista if a.vencida]
        if vencidas:
            print(f"\n  ATENCION: {len(vencidas)} alerta(s) con el plazo de reporte "
                  f"ya vencido")
            print("  El tope de 90 dias corre desde la operacion, no desde la deteccion.")

    exposicion = corrida.exposicion
    if exposicion is not None and exposicion.cargos:
        print(f"\n  Exposicion sancionatoria estimada: ${exposicion.total:,.0f}")
        print(f"    por falta de reporte      ${exposicion.por_falta_de_reporte:>16,.0f}")
        print(f"    por otros incumplimientos ${exposicion.por_incumplimientos:>16,.0f}")
        print("    (estimacion, no calculo de multa: la fija la UIF en sumario)")


def comando_exportar(args: argparse.Namespace) -> int:
    """Misma corrida que `circuito`, pero la salida es el JSON del visor."""
    preparado = _preparar(args)
    if preparado is None:
        return 2
    padron, clientes = preparado

    corrida = _correr_con_args(args, padron, clientes)
    _resumen(corrida)

    variable = "DEMO_DATOS" if getattr(args, "demo", False) else "DATOS"
    ruta, gemelo = escribir(corrida, args.salida, variable)
    print(f"\nDatos del visor: {ruta}")
    print(f"                  {gemelo.name}  (para abrir el visor sin servidor)")
    print(f"\nAbri visor/index.html con doble clic.")
    return 0


def comando_ros(args: argparse.Namespace) -> int:
    """Arma los borradores de ROS desde el informe que el analista completo.

    Vuelve a correr el circuito para reconstruir el contexto de cada alerta y
    lee del informe unicamente las columnas de decision. Reconstruir es mas
    barato que guardar estado entre corridas, y garantiza que el borrador se
    arme con los datos de hoy y no con los de la corrida anterior.
    """
    informe = Path(args.informe)
    if not informe.exists():
        print(f"error: no existe {informe}", file=sys.stderr)
        return 2

    decisiones = leer_decisiones(informe)
    if not decisiones:
        print(f"error: {informe} no tiene hoja Alertas", file=sys.stderr)
        return 2

    resueltas = {k: d for k, d in decisiones.items()
                 if d.resolucion is not Resolucion.PENDIENTE}
    print(f"Decisiones leidas: {len(decisiones)}, resueltas {len(resueltas)}")
    if not resueltas:
        print("\nNinguna alerta tiene resolucion cargada.")
        print("Completar en la hoja Alertas las columnas resolucion,")
        print("medidas_adoptadas, decision_final y fecha_decision.")
        return 1

    contexto = _reconstruir(args)
    if contexto is None:
        return 2
    casos, alertas, evaluaciones, perfiles, resoluciones, por_cliente = contexto

    clientes = {c.cliente.cliente_id: c.cliente for c in casos}
    resultado = armar(alertas, decisiones, clientes, evaluaciones, perfiles,
                      resoluciones, por_cliente)

    agregar_hojas_etapa5(informe, resultado)

    print(f"\n  Borradores de ROS      {len(resultado.borradores):3}")
    print(f"    presentables         {len(resultado.presentables):3}")
    print(f"    incompletos          {len(resultado.incompletos):3}")
    print(f"  Inusuales justificadas {len(resultado.justificadas):3}")
    print(f"  Pendientes de decision {len(resultado.pendientes):3}")

    fuera = [b for b in resultado.borradores if b.fuera_de_plazo]
    if fuera:
        print(f"\n  ATENCION: {len(fuera)} borrador(es) con el plazo vencido.")
        print("  La demora hay que explicarla en la presentacion.")

    if resultado.incompletos:
        print("\n  Borradores incompletos:")
        for b in resultado.incompletos:
            print(f"    {b.cliente.cliente_id}  {b.cliente.nombre[:26]:28} "
                  f"{'; '.join(b.faltantes())}")

    con_obs = [b for b in resultado.borradores if b.observaciones()]
    if con_obs:
        print("\n  Observaciones sobre los borradores:")
        for b in con_obs:
            for o in b.observaciones():
                print(f"    {b.cliente.cliente_id}  {o}")

    sin_doc = resultado.sin_documentar
    if sin_doc:
        print(f"\n  ATENCION: {len(sin_doc)} inusualidad(es) justificada(s) sin "
              f"analisis documentado.")
        print("  Un registro sin medidas ni motivo no distingue una alerta bien")
        print("  resuelta de una que nadie miro.")

    print(f"\nInforme: {informe}")
    return 0


def _reconstruir(args: argparse.Namespace):
    """Rehace el contexto del circuito para armar los borradores."""
    preparado = _preparar(args)
    if preparado is None:
        return None
    padron, clientes = preparado

    politica = Politica(umbral_revision=args.umbral,
                        umbral_probable=POLITICA_POR_DEFECTO.umbral_probable)
    casos = [Caso(caso_id=f"C{i:05d}", cliente=c) for i, c in enumerate(clientes, 1)]
    resultado = screenear(casos, padron, politica, actor=args.actor)

    por_cliente: dict[str, list] = {}
    for c in resultado.coincidencias:
        por_cliente.setdefault(c.cliente_id, []).append(c)

    estructura = leer_estructura(args.societaria, clientes) if args.societaria else None
    resoluciones = {}
    if estructura is not None:
        for cliente in clientes:
            if cliente.tipo != "PERSONA":
                resoluciones[cliente.cliente_id] = resolver(estructura, cliente.cliente_id)

    registro_pep = leer_peps(args.peps) if args.peps else None
    evaluaciones = evaluar_casos(casos, resoluciones, por_cliente,
                                 registro_pep=registro_pep,
                                 umbral_probable=politica.umbral_probable,
                                 matriz=MATRIZ_POR_DEFECTO, actor=args.actor)

    operatorias = agrupar(leer_operaciones(args.operaciones))
    perfiles = leer_perfiles(args.perfiles) if args.perfiles else {}
    alertas = monitorear(operatorias, perfiles,
                         parametros_con_listas(umbral_reporte=args.umbral_reporte))

    return casos, alertas, evaluaciones, perfiles, resoluciones, por_cliente


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


def comando_evaluar(args: argparse.Namespace) -> int:
    """Mide recall y falsas alertas del screening contra casos con respuesta conocida."""
    from . import evaluacion as ev

    print(f"Cargando listas de {args.listas}", end="\n\n")
    padron = cargar_listas(Path(args.listas))
    print(f"\n{len(padron)} designados. Corriendo {args.por_tipo} casos por tipo, "
          f"semilla {args.semilla}.", end="\n\n")

    sinteticos = ev.generar_sinteticos(padron, por_tipo=args.por_tipo, semilla=args.semilla)
    print(ev.informe(ev.correr(sinteticos, padron), "Conjunto sintetico"))

    if args.dificiles:
        casos, omitidos = ev.leer_dificiles(args.dificiles, padron)
        resultados = ev.correr(casos, padron, procesos=1)
        print("\n" + ev.detalle_dificiles(resultados, POLITICA_POR_DEFECTO.umbral_revision))
        print("\n" + ev.informe(resultados, "Conjunto dificil"))
        for o in omitidos:
            print(f"  omitido: {o}")
    return 0


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

    cir = sub.add_parser("circuito",
                         help="etapas 1 a 4: screening, beneficiario final, riesgo, "
                              "monitoreo, congelamiento y exposicion")
    comunes(cir)
    cir.add_argument("--societaria", help="CSV o XLSX con el grafo societario")
    cir.add_argument("--peps", help="CSV de declaraciones juradas de condicion PEP")
    cir.add_argument("--operaciones", help="CSV o XLSX con la operatoria de los clientes")
    cir.add_argument("--perfiles", help="CSV o XLSX con los perfiles transaccionales")
    cir.add_argument("--umbral-reporte", type=float, default=None,
                     help="umbral de reporte en pesos; por defecto, 40 SMVM segun "
                          "Res. UIF 78/2025")
    cir.add_argument("--salida", default="informe_circuito.xlsx")
    cir.set_defaults(func=comando_circuito)

    ros = sub.add_parser("ros",
                         help="etapa 5: borradores de ROS desde el informe completado")
    comunes(ros)
    ros.add_argument("--informe", required=True,
                     help="XLSX del circuito con las decisiones ya cargadas")
    ros.add_argument("--societaria", help="CSV o XLSX con el grafo societario")
    ros.add_argument("--peps", help="CSV de declaraciones juradas de condicion PEP")
    ros.add_argument("--operaciones", required=True, help="CSV o XLSX con la operatoria")
    ros.add_argument("--perfiles", help="CSV o XLSX con los perfiles transaccionales")
    ros.add_argument("--umbral-reporte", type=float, default=None,
                     help="umbral de reporte en pesos; por defecto, 40 SMVM")
    ros.set_defaults(func=comando_ros)

    act = sub.add_parser("actualizar-listas", help="bajar las listas desde las fuentes oficiales")
    act.add_argument("--listas", required=True, help="directorio destino")
    act.add_argument("--incluir-opcionales", action="store_true",
                     help="bajar tambien las listas no obligatorias para Argentina")
    act.set_defaults(func=comando_actualizar)

    exp = sub.add_parser("exportar",
                         help="etapas 1 a 4, con el visor web como salida")
    comunes(exp)
    exp.add_argument("--societaria", help="CSV o XLSX con el grafo societario")
    exp.add_argument("--peps", help="CSV de declaraciones juradas de condicion PEP")
    exp.add_argument("--operaciones", help="CSV o XLSX con la operatoria de los clientes")
    exp.add_argument("--perfiles", help="CSV o XLSX con los perfiles transaccionales")
    exp.add_argument("--umbral-reporte", type=float, default=None,
                     help="umbral de reporte en pesos; por defecto, 40 SMVM")
    exp.add_argument("--salida", default="visor/datos.json")
    exp.add_argument("--demo", action="store_true",
                     help="escribe el juego de demostracion que se publica, "
                          "en vez del export de trabajo")
    exp.set_defaults(func=comando_exportar)

    evl = sub.add_parser("evaluar",
                         help="recall y falsas alertas del screening contra casos etiquetados")
    evl.add_argument("--listas", required=True, help="directorio con las listas descargadas")
    evl.add_argument("--dificiles", help="CSV de casos dificiles escritos a mano")
    evl.add_argument("--por-tipo", type=int, default=40, help="casos sinteticos por tipo")
    evl.add_argument("--semilla", type=int, default=20260920)
    evl.set_defaults(func=comando_evaluar)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
