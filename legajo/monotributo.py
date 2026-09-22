"""Escalas del Regimen Simplificado, con su vigencia.

Igual que el SMVM: el valor va con la fecha al lado. Si la fecha esta vieja,
los resultados estan mal y el programa no avisa solo.

La tabla esta completa: las once categorias, A a K, verificadas contra la
fuente oficial. Igual se conserva la maquinaria que distingue saber de no
saber, porque en febrero de 2027 estos topes quedan viejos y alguien va a
tener que cargar los nuevos. Una categoria que no este en la tabla no se puede
evaluar, y el modulo lo dice en vez de devolver un cero que parezca un
resultado.
"""

from __future__ import annotations

from datetime import date

# ---------------------------------------------------------------------------
# Escalas vigentes de agosto 2026 a enero 2027, segun ARCA.
#
# La proxima actualizacion es en febrero de 2027. Pasada esa fecha los topes
# de abajo son viejos y hay que reemplazarlos.
# ---------------------------------------------------------------------------

FUENTE = "ARCA, afip.gob.ar/monotributo/categorias.asp"
VIGENCIA_DESDE = date(2026, 8, 1)
VIGENCIA_HASTA = date(2027, 1, 31)
PROXIMA_ACTUALIZACION = date(2027, 2, 1)

# Las once categorias que tiene el regimen.
CATEGORIAS: tuple[str, ...] = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K")

# Tope de ingresos brutos anuales por categoria. Solo las verificadas.
TOPES_ANUALES: dict[str, float] = {
    "A": 12_009_410.45,
    "B": 17_595_182.74,
    "C": 24_670_494.31,
    "D": 30_628_651.43,
    "E": 36_028_231.33,
    "F": 45_151_659.41,
    "G": 53_995_798.87,
    "H": 81_924_660.37,
    "I": 91_699_761.90,
    "J": 105_012_519.20,
    "K": 126_610_838.75,
}

CATEGORIAS_FALTANTES: tuple[str, ...] = tuple(
    c for c in CATEGORIAS if c not in TOPES_ANUALES
)
TABLA_COMPLETA = not CATEGORIAS_FALTANTES


def vigente(al: date | None = None) -> bool:
    """Si la escala cargada sigue siendo la que corresponde a esa fecha."""
    cuando = al or date.today()
    return VIGENCIA_DESDE <= cuando <= VIGENCIA_HASTA


def tope_anual(categoria: str) -> float | None:
    """Tope de ingresos brutos anuales, o None si esa categoria no se cargo."""
    return TOPES_ANUALES.get((categoria or "").strip().upper())


def excede(categoria: str, ingresos_anuales: float) -> bool | None:
    """Si los ingresos superan el tope de la categoria declarada.

    Devuelve None cuando no se puede responder, que pasa si la categoria no
    esta en la tabla. Devolver False ahi seria afirmar que el cliente esta en
    regla sin haberlo verificado, que es peor que no contestar.
    """
    tope = tope_anual(categoria)
    if tope is None:
        return None
    return ingresos_anuales > tope


def categoria_por_ingresos(ingresos_anuales: float) -> str | None:
    """La categoria que corresponde a un nivel de ingresos.

    Exige la tabla completa. Con categorias faltantes el resultado seria
    sistematicamente alto: al no estar C a J, un cliente de veinte millones
    caeria en K, que es la ultima cargada, y quedaria como si tuviera el tope
    mas alto del regimen.
    """
    if not TABLA_COMPLETA:
        return None
    for categoria in CATEGORIAS:
        tope = TOPES_ANUALES[categoria]
        if ingresos_anuales <= tope:
            return categoria
    return None


def estado_de_la_tabla() -> str:
    """Texto para el informe y para la interfaz."""
    if TABLA_COMPLETA:
        return (f"{len(CATEGORIAS)} categorias cargadas, vigencia "
                f"{VIGENCIA_DESDE.isoformat()} a {VIGENCIA_HASTA.isoformat()}")
    faltan = ", ".join(CATEGORIAS_FALTANTES)
    return (f"tabla incompleta: faltan {faltan}. Las cargadas rigen de "
            f"{VIGENCIA_DESDE.isoformat()} a {VIGENCIA_HASTA.isoformat()}")
