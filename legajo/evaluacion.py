"""Evaluacion del screening contra casos con respuesta conocida.

Hasta ahora "calibrado para recall" era una afirmacion. Este modulo la
convierte en un numero: arma clientes cuya respuesta correcta se conoce de
antemano, los pasa por el mismo cotejar_cliente que usa el circuito, y cuenta.

Hay dos conjuntos y se reportan por separado, porque miden cosas distintas:

    sintetico   Se genera desde la lista real con una semilla fija. Los
                positivos son designados reales con el error de tipeo, el
                orden o el faltante que tiene un padron de verdad. Los
                negativos son nombres argentinos comunes y homonimos parciales.
                Da volumen, pero quien inventa las perturbaciones decide que es
                dificil: el recall que sale es contra ese modelo de error.

    dificil     Un csv escrito a mano (evaluacion/casos_dificiles.csv) con
                transliteraciones y variantes que un analista reconoceria.
                Son pocos casos, sin valor estadistico, y por eso se muestran
                uno por uno.

No hay forma de medir el recall real contra el mundo sin un padron etiquetado
por analistas. Esto acota el problema, no lo cierra.
"""

from __future__ import annotations

import csv
import random
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .config import POLITICA_POR_DEFECTO, Politica
from .fuentes.base import Designado, Padron
from .indice import Indice
from .modelo import Cliente, Documento
from .screening import Coincidencia, cotejar_cliente

SEMILLA = 20260920

# Piso de la barrida. Se corre una sola vez a este umbral y se filtra hacia
# arriba: el descuento por atenuantes se aplica antes del corte, asi que
# filtrar el score final por t equivale a correr el motor con umbral t.
PISO_BARRIDA = 60.0
UMBRALES_BARRIDA = (60.0, 70.0, 78.0, 85.0, 92.0, 96.0)

NOMBRES_AR = (
    "Juan", "Maria", "Carlos", "Ana", "Luis", "Laura", "Jorge", "Marta", "Pablo",
    "Sofia", "Diego", "Lucia", "Martin", "Carolina", "Hector", "Silvia", "Ricardo",
    "Patricia", "Fernando", "Gabriela", "Alejandro", "Romina", "Sergio", "Valeria",
    "Miguel", "Claudia", "Oscar", "Mariana", "Raul", "Natalia", "Facundo", "Julieta",
    "Nicolas", "Florencia", "Gustavo", "Paula", "Andres", "Cecilia", "Hugo", "Agustina",
)
APELLIDOS_AR = (
    "Gonzalez", "Rodriguez", "Gomez", "Fernandez", "Lopez", "Diaz", "Martinez",
    "Perez", "Garcia", "Sanchez", "Romero", "Sosa", "Alvarez", "Torres", "Ruiz",
    "Ramirez", "Flores", "Benitez", "Acosta", "Medina", "Herrera", "Suarez",
    "Aguirre", "Gimenez", "Gutierrez", "Pereyra", "Rojas", "Molina", "Castro",
    "Ortiz", "Silva", "Nunez", "Luna", "Juarez", "Cabrera", "Rios", "Morales",
    "Dominguez", "Vazquez", "Ledesma",
)
RUBROS = (
    "Distribuidora", "Transportes", "Constructora", "Agropecuaria", "Panificadora",
    "Ferreteria", "Servicios Contables", "Estudio Juridico", "Inmobiliaria",
    "Textil", "Metalurgica", "Farmacia", "Libreria", "Consultora", "Maderera",
)
ZONAS = (
    "del Sur", "Norte", "Cuyo", "Patagonia", "del Litoral", "Central", "Pampeana",
    "Andina", "Rioplatense", "del Plata", "Mediterranea", "Austral",
)

# Tipos de caso. Los positivos tienen designado esperado, los negativos no.
POSITIVOS = ("exacto", "sin_medio", "iniciales", "typo", "alias", "entidad_sin_ultimo_token")
NEGATIVOS = ("comun_argentino", "homonimo_parcial", "entidad_argentina")


@dataclass(frozen=True)
class CasoEvaluacion:
    cliente: Cliente
    tipo_caso: str
    esperados: frozenset[tuple[str, str]]   # {(lista, id_origen)}; vacio si es negativo
    origen: str = "sintetico"

    @property
    def positivo(self) -> bool:
        return bool(self.esperados)


# ---------------------------------------------------------------------------
# Generacion
# ---------------------------------------------------------------------------

def _partir(nombre: str) -> list[str]:
    """Pasa 'APELLIDO, Nombre Medio' a ['Nombre', 'Medio', 'APELLIDO'].

    OFAC guarda apellido primero y ONU guarda nombre primero. Un padron real
    de clientes casi siempre viene nombre primero, asi que se lleva a esa forma.
    """
    if "," in nombre:
        apellido, resto = nombre.split(",", 1)
        return [*resto.split(), *apellido.split()]
    return nombre.split()


def _typo(token: str, rng: random.Random) -> str:
    """Un error de tipeo: sustitucion, omision o transposicion adyacente."""
    i = rng.randrange(1, len(token) - 1)
    modo = rng.choice(("sustituir", "omitir", "transponer"))
    if modo == "omitir":
        return token[:i] + token[i + 1:]
    if modo == "transponer":
        return token[:i] + token[i + 1] + token[i] + token[i + 2:]
    reemplazo = rng.choice([c for c in "abcdefghijklmnopqrstuvwxyz" if c != token[i].lower()])
    return token[:i] + reemplazo + token[i + 1:]


def _anio(fechas: tuple[str, ...]) -> str | None:
    for f in fechas:
        anio = f.strip()[-4:] if len(f.strip()) >= 4 and f.strip()[-4:].isdigit() else f.strip()[:4]
        if anio.isdigit():
            return anio
    return None


def _cliente_desde(d: Designado, nombre: str, cid: str) -> Cliente:
    """Cliente con los datos secundarios verdaderos del designado, si los hay.

    Un cliente real trae fecha de nacimiento y nacionalidad. Incluirlos hace
    que los atenuantes jueguen: si restaran de mas sobre un dato correcto, el
    recall lo mostraria.
    """
    anio = _anio(d.fechas_nacimiento)
    return Cliente(
        cliente_id=cid,
        nombre=nombre,
        tipo="ENTIDAD" if d.es_entidad else "PERSONA",
        fecha_nacimiento=f"{anio}-01-01" if anio and not d.es_entidad else None,
        nacionalidad=d.nacionalidades[0].upper() if d.nacionalidades and not d.es_entidad else None,
    )


def generar_sinteticos(padron: Padron, por_tipo: int = 60, semilla: int = SEMILLA) -> list[CasoEvaluacion]:
    rng = random.Random(semilla)
    # Orden fijo antes de muestrear: la semilla solo reproduce si la entrada
    # tiene un orden determinista.
    personas = sorted((d for d in padron.designados if d.tipo == "PERSONA" and len(_partir(d.nombre)) >= 2),
                      key=lambda d: (d.lista, d.id_origen))
    entidades = sorted((d for d in padron.designados if d.tipo == "ENTIDAD" and len(d.nombre.split()) >= 3),
                       key=lambda d: (d.lista, d.id_origen))
    con_alias = [d for d in personas if d.alias]
    con_medio = [d for d in personas if len(_partir(d.nombre)) >= 3]
    largos = [d for d in personas if all(len(t) >= 5 for t in _partir(d.nombre)[:1])]

    def muestra(pool: list[Designado]) -> list[Designado]:
        # Con una lista chica el pool puede tener menos designados que casos
        # pedidos, o ninguno (sin entidades, sin alias).
        return rng.sample(pool, min(por_tipo, len(pool)))

    casos: list[CasoEvaluacion] = []
    n = 0

    def nuevo(d: Designado, nombre: str, tipo_caso: str) -> None:
        nonlocal n
        n += 1
        casos.append(CasoEvaluacion(
            cliente=_cliente_desde(d, nombre, f"S{n:05d}"),
            tipo_caso=tipo_caso,
            esperados=frozenset({(d.lista, d.id_origen)}),
        ))

    for d in muestra(personas):
        nuevo(d, " ".join(_partir(d.nombre)), "exacto")

    for d in muestra(con_medio):
        t = _partir(d.nombre)
        nuevo(d, f"{t[0]} {t[-1]}", "sin_medio")

    for d in muestra(con_medio):
        t = _partir(d.nombre)
        nuevo(d, " ".join([f"{t[0][0]}.", *t[1:]]), "iniciales")

    for d in muestra(largos):
        t = _partir(d.nombre)
        j = rng.choice([k for k, x in enumerate(t) if len(x) >= 5] or [0])
        if len(t[j]) >= 5:
            t[j] = _typo(t[j], rng)
        nuevo(d, " ".join(t), "typo")

    for d in muestra(con_alias):
        nuevo(d, " ".join(_partir(rng.choice(d.alias))), "alias")

    for d in muestra(entidades):
        t = d.nombre.split()
        nuevo(d, " ".join(t[:-1]), "entidad_sin_ultimo_token")

    # Negativos. Por construccion no son ningun designado: cualquier alerta
    # sobre ellos cuenta como falso positivo, incluso si resulta ser un
    # homonimo genuino de alguien listado, porque el costo para el analista es
    # el mismo.
    for _ in range(por_tipo * 2):
        n += 1
        casos.append(CasoEvaluacion(
            cliente=Cliente(
                cliente_id=f"S{n:05d}",
                nombre=f"{rng.choice(NOMBRES_AR)} {rng.choice(NOMBRES_AR)} {rng.choice(APELLIDOS_AR)}"
                       if rng.random() < 0.4 else f"{rng.choice(NOMBRES_AR)} {rng.choice(APELLIDOS_AR)}",
                tipo="PERSONA",
                fecha_nacimiento=f"{rng.randint(1950, 2000)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
                nacionalidad="ARGENTINA",
            ),
            tipo_caso="comun_argentino",
            esperados=frozenset(),
        ))

    # Homonimo parcial: el nombre de pila de un designado real con un apellido
    # argentino. Es la fuente clasica de falsos positivos.
    for d in muestra(personas):
        n += 1
        t = _partir(d.nombre)
        casos.append(CasoEvaluacion(
            cliente=Cliente(
                cliente_id=f"S{n:05d}",
                nombre=f"{t[0]} {rng.choice(APELLIDOS_AR)}",
                tipo="PERSONA",
                fecha_nacimiento=f"{rng.randint(1950, 2000)}-06-15",
                nacionalidad="ARGENTINA",
            ),
            tipo_caso="homonimo_parcial",
            esperados=frozenset(),
        ))

    for _ in range(por_tipo):
        n += 1
        casos.append(CasoEvaluacion(
            cliente=Cliente(
                cliente_id=f"S{n:05d}",
                nombre=f"{rng.choice(RUBROS)} {rng.choice(ZONAS)} S.A.",
                tipo="ENTIDAD",
            ),
            tipo_caso="entidad_argentina",
            esperados=frozenset(),
        ))

    return casos


def leer_dificiles(ruta: str | Path, padron: Padron) -> tuple[list[CasoEvaluacion], list[str]]:
    """Lee el csv escrito a mano y resuelve los designados esperados.

    Los esperados se guardan como LISTA:ID y no como nombre, porque el mismo
    nombre puede tener varios asientos. Si una lista se actualiza y el ID
    desaparece, el caso se informa como no aplicable en lugar de contarse como
    un falso negativo que el motor no cometio.
    """
    existentes = {(d.lista, d.id_origen) for d in padron.designados}
    casos: list[CasoEvaluacion] = []
    omitidos: list[str] = []
    with open(ruta, newline="", encoding="utf-8") as f:
        for i, fila in enumerate(csv.DictReader(f), start=1):
            esperados = frozenset(
                tuple(x.split(":", 1)) for x in fila["esperados"].split("|") if x.strip()
            )
            if esperados and not (esperados & existentes):
                omitidos.append(f"{fila['nombre']} ({fila['esperados']} ya no esta en las listas)")
                continue
            es_entidad = fila["tipo"].strip().upper() == "ENTIDAD"
            docs = []
            if fila.get("documento", "").strip():
                docs.append(Documento(fila["documento_tipo"].strip(), fila["documento"].strip()))
            casos.append(CasoEvaluacion(
                cliente=Cliente(
                    cliente_id=f"D{i:03d}",
                    nombre=fila["nombre"].strip(),
                    tipo="ENTIDAD" if es_entidad else "PERSONA",
                    documentos=docs,
                    fecha_nacimiento=fila.get("fecha_nacimiento", "").strip() or None,
                    nacionalidad=fila.get("nacionalidad", "").strip().upper() or None,
                ),
                tipo_caso=fila["tipo_caso"].strip(),
                esperados=esperados,
                origen="dificil",
            ))
    return casos, omitidos


# ---------------------------------------------------------------------------
# Medicion
# ---------------------------------------------------------------------------

@dataclass
class ResultadoCaso:
    caso: CasoEvaluacion
    coincidencias: list[Coincidencia]

    def mejor_score_esperado(self) -> float | None:
        """Score del mejor acierto sobre el designado esperado, o None si no salio."""
        puntajes = [c.score for c in self.coincidencias if (c.lista, c.id_origen) in self.caso.esperados]
        return max(puntajes) if puntajes else None

    def alerta_a(self, umbral: float) -> bool:
        return any(c.score >= umbral for c in self.coincidencias)


@dataclass
class Metricas:
    umbral: float
    positivos: int = 0
    detectados: int = 0
    negativos: int = 0
    negativos_con_alerta: int = 0

    @property
    def recall(self) -> float:
        return self.detectados / self.positivos if self.positivos else 0.0

    @property
    def precision(self) -> float:
        alertas = self.detectados + self.negativos_con_alerta
        return self.detectados / alertas if alertas else 0.0

    @property
    def tasa_falsa_alerta(self) -> float:
        """Fraccion de clientes limpios que le llegan a un analista."""
        return self.negativos_con_alerta / self.negativos if self.negativos else 0.0


_PADRON_PROCESO: Padron | None = None
_INDICE_PROCESO: Indice | None = None
_POLITICA_PROCESO: Politica | None = None


def _iniciar_proceso(padron: Padron, politica: Politica) -> None:
    global _PADRON_PROCESO, _INDICE_PROCESO, _POLITICA_PROCESO
    _PADRON_PROCESO, _POLITICA_PROCESO = padron, politica
    _INDICE_PROCESO = Indice(padron)


def _cotejar_en_proceso(caso: CasoEvaluacion) -> ResultadoCaso:
    return ResultadoCaso(caso, cotejar_cliente(caso.cliente, _PADRON_PROCESO, _POLITICA_PROCESO, _INDICE_PROCESO))


def correr(
    casos: list[CasoEvaluacion],
    padron: Padron,
    politica: Politica | None = None,
    procesos: int | None = None,
) -> list[ResultadoCaso]:
    """Corre cotejar_cliente sobre cada caso, con el indice como en el circuito.

    Con las listas reales el indice deja unos 10.000 candidatos por cliente
    (MINIMO_TRIGRAMAS = 1) y cada cliente tarda alrededor de un segundo. Se
    reparte entre procesos porque los casos son independientes. El resultado
    es el mismo que en serie y el orden se conserva.
    """
    politica = politica or Politica(umbral_revision=PISO_BARRIDA)
    if procesos == 1 or len(casos) < 8:
        indice = Indice(padron)
        return [ResultadoCaso(c, cotejar_cliente(c.cliente, padron, politica, indice)) for c in casos]

    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=procesos, initializer=_iniciar_proceso,
                             initargs=(padron, politica)) as pool:
        return list(pool.map(_cotejar_en_proceso, casos, chunksize=4))


def metricas(resultados: list[ResultadoCaso], umbral: float) -> Metricas:
    m = Metricas(umbral)
    for r in resultados:
        if r.caso.positivo:
            m.positivos += 1
            s = r.mejor_score_esperado()
            if s is not None and s >= umbral:
                m.detectados += 1
        else:
            m.negativos += 1
            if r.alerta_a(umbral):
                m.negativos_con_alerta += 1
    return m


def recall_por_tipo(resultados: list[ResultadoCaso], umbral: float) -> dict[str, tuple[int, int]]:
    """{tipo_caso: (detectados, total)} para los positivos."""
    acumulado: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for r in resultados:
        if not r.caso.positivo:
            continue
        acumulado[r.caso.tipo_caso][1] += 1
        s = r.mejor_score_esperado()
        if s is not None and s >= umbral:
            acumulado[r.caso.tipo_caso][0] += 1
    return {k: (v[0], v[1]) for k, v in acumulado.items()}


def falsas_alertas_por_tipo(resultados: list[ResultadoCaso], umbral: float) -> dict[str, tuple[int, int]]:
    acumulado: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for r in resultados:
        if r.caso.positivo:
            continue
        acumulado[r.caso.tipo_caso][1] += 1
        if r.alerta_a(umbral):
            acumulado[r.caso.tipo_caso][0] += 1
    return {k: (v[0], v[1]) for k, v in acumulado.items()}


def informe(resultados: list[ResultadoCaso], titulo: str, politica: Politica = POLITICA_POR_DEFECTO) -> str:
    lineas = [titulo, "=" * len(titulo), ""]
    lineas.append(f"{'umbral':>7} {'recall':>8} {'precision':>10} {'falsa alerta':>13}")
    for u in sorted({*UMBRALES_BARRIDA, politica.umbral_revision, politica.umbral_probable}):
        m = metricas(resultados, u)
        marca = "  <- revision" if u == politica.umbral_revision else "  <- probable" if u == politica.umbral_probable else ""
        lineas.append(f"{u:>7.0f} {m.recall:>8.1%} {m.precision:>10.1%} {m.tasa_falsa_alerta:>13.1%}{marca}")

    u = politica.umbral_revision
    lineas += ["", f"Recall por tipo de caso (umbral {u:.0f})"]
    for tipo, (ok, total) in sorted(recall_por_tipo(resultados, u).items()):
        lineas.append(f"  {tipo:<28} {ok:>4}/{total:<4} {ok / total:>7.1%}")
    lineas += ["", f"Falsas alertas por tipo de caso (umbral {u:.0f})"]
    for tipo, (mal, total) in sorted(falsas_alertas_por_tipo(resultados, u).items()):
        lineas.append(f"  {tipo:<28} {mal:>4}/{total:<4} {mal / total:>7.1%}")
    return "\n".join(lineas)


def detalle_dificiles(resultados: list[ResultadoCaso], umbral: float) -> str:
    lineas = ["Casos dificiles, uno por uno", ""]
    for r in resultados:
        s = r.mejor_score_esperado()
        if r.caso.positivo:
            estado = "DETECTADO" if s is not None and s >= umbral else "PERDIDO  "
            puntaje = f"{s:.1f}" if s is not None else "sin coincidencia"
        else:
            hit = max((c.score for c in r.coincidencias), default=None)
            estado = "ALERTA   " if hit is not None and hit >= umbral else "limpio   "
            puntaje = f"{hit:.1f}" if hit is not None else "-"
        lineas.append(f"  {estado} {r.caso.tipo_caso:<22} {r.caso.cliente.nombre:<36} {puntaje}")
    return "\n".join(lineas)
