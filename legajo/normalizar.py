"""Normalizacion de nombres para cotejo.

El 80% de la calidad del screening se define aca, no en el algoritmo de
similitud. Un matcher excelente sobre nombres mal normalizados rinde peor
que un matcher mediocre sobre nombres bien normalizados.
"""

from __future__ import annotations

import re
from functools import lru_cache
import unicodedata

# Sufijos societarios. Se eliminan porque "ACME SA" y "ACME S.A." y "ACME"
# son la misma entidad, y dejarlos hace que el sufijo aporte similitud
# espuria entre entidades distintas ("X SA" vs "Y SA" comparten un token).
SUFIJOS_SOCIETARIOS = frozenset({
    "SA", "SAU", "SAS", "SRL", "SCA", "SCS", "SH", "SAIC", "SACI", "SAICF",
    "LTD", "LTDA", "LIMITED", "INC", "INCORPORATED", "CORP", "CORPORATION",
    "LLC", "LLP", "PLC", "GMBH", "MBH", "AG", "BV", "NV", "SPA", "SARL",
    "PTY", "PTE", "CO", "COMPANY", "TRUST", "FUND", "HOLDING", "HOLDINGS",
    "GROUP", "GRUPO", "INTERNATIONAL", "INTL",
})

# Particulas que no aportan poder discriminante en nombres de personas.
PARTICULAS = frozenset({"DE", "DEL", "LA", "LAS", "LOS", "EL", "Y", "DA", "DOS",
                        "VAN", "VON", "BIN", "IBN", "AL", "EL-", "ABU"})

_NO_ALFANUM = re.compile(r"[^A-Z0-9\s]")
_ESPACIOS = re.compile(r"\s+")

# Punto que sigue a una letra sola: marca de abreviatura.
# Debe resolverse ANTES de barrer la puntuacion, o "S.A." se parte en los
# tokens "S" y "A" y deja de reconocerse como sufijo societario.
_ABREVIATURA = re.compile(r"\b([A-Z])\.")


def sin_acentos(texto: str) -> str:
    """Descompone y descarta marcas diacriticas. PEREZ == PÉREZ."""
    descompuesto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in descompuesto if not unicodedata.combining(c))


@lru_cache(maxsize=200_000)
def normalizar(nombre: str, *, es_entidad: bool = False) -> str:
    """Devuelve la forma canonica de un nombre para comparacion.

    No se elimina ninguna particula en personas: "BIN LADEN" pierde sentido
    sin el "BIN". Solo se descartan sufijos societarios, y solo en entidades.
    """
    if not nombre:
        return ""

    texto = sin_acentos(nombre).upper()
    # "S.A." -> "SA" antes de barrer puntuacion, para no partir la abreviatura.
    texto = _ABREVIATURA.sub(r"\1", texto)
    texto = _NO_ALFANUM.sub(" ", texto)
    texto = _ESPACIOS.sub(" ", texto).strip()

    if not texto:
        return ""

    tokens = texto.split()
    if es_entidad:
        tokens = [t for t in tokens if t not in SUFIJOS_SOCIETARIOS]
        # Si el nombre era puro sufijo, conservamos el original: es preferible
        # un match ruidoso a perder la entidad por completo.
        if not tokens:
            tokens = texto.split()

    return " ".join(tokens)


def tokens(nombre: str, *, es_entidad: bool = False) -> list[str]:
    normalizado = normalizar(nombre, es_entidad=es_entidad)
    return normalizado.split() if normalizado else []
