"""Motor de similitud de nombres.

Devuelve un puntaje. No toma decisiones: los umbrales son politica y viven
en config.py. Separar mecanismo de politica permite recalibrar el apetito de
riesgo sin tocar una linea de este archivo.

Jaro-Winkler esta implementado a mano a proposito. Son cuarenta lineas, es un
algoritmo cerrado, y una dependencia externa para esto es una dependencia que
hay que auditar, versionar y justificar ante un supervisor.
"""

from __future__ import annotations

from .normalizar import normalizar

_PESO_PREFIJO = 0.1
_MAX_PREFIJO = 4


def jaro(a: str, b: str) -> float:
    """Similitud de Jaro entre dos cadenas. Rango [0, 1]."""
    if a == b:
        return 1.0
    la, lb = len(a), len(b)
    if la == 0 or lb == 0:
        return 0.0

    # Dos caracteres se consideran coincidentes si estan dentro de esta ventana.
    ventana = max(la, lb) // 2 - 1
    if ventana < 0:
        ventana = 0

    usado_a = [False] * la
    usado_b = [False] * lb
    coincidencias = 0

    for i in range(la):
        inicio = max(0, i - ventana)
        fin = min(i + ventana + 1, lb)
        for j in range(inicio, fin):
            if usado_b[j] or a[i] != b[j]:
                continue
            usado_a[i] = usado_b[j] = True
            coincidencias += 1
            break

    if coincidencias == 0:
        return 0.0

    # Transposiciones: caracteres coincidentes en distinto orden relativo.
    transposiciones = 0
    j = 0
    for i in range(la):
        if not usado_a[i]:
            continue
        while not usado_b[j]:
            j += 1
        if a[i] != b[j]:
            transposiciones += 1
        j += 1
    transposiciones //= 2

    m = coincidencias
    return (m / la + m / lb + (m - transposiciones) / m) / 3


def jaro_winkler(a: str, b: str) -> float:
    """Jaro con bonificacion por prefijo comun.

    La bonificacion refleja que los errores de tipeo y las transliteraciones
    tienden a divergir hacia el final, no al principio.
    """
    base = jaro(a, b)
    if base == 0.0:
        return 0.0

    prefijo = 0
    for ca, cb in zip(a[:_MAX_PREFIJO], b[:_MAX_PREFIJO]):
        if ca != cb:
            break
        prefijo += 1

    return base + prefijo * _PESO_PREFIJO * (1 - base)


def score_nombres(consulta: str, candidato: str, *, es_entidad: bool = False) -> float:
    """Puntaje de similitud entre dos nombres. Rango [0, 100].

    Compara por tokens, no como cadena unica. Esto hace el cotejo
    independiente del orden: "PEREZ JUAN" y "JUAN PEREZ" son el mismo nombre,
    y el orden apellido-nombre varia entre fuentes.

    Los nombres incompletos son la regla, no la excepcion: el padron tiene
    "JUAN PEREZ" y la lista tiene "JUAN CARLOS PEREZ GOMEZ". Por eso se
    promedia sobre el conjunto mas corto y la penalizacion por tokens
    faltantes es leve.
    """
    na = normalizar(consulta, es_entidad=es_entidad)
    nb = normalizar(candidato, es_entidad=es_entidad)

    if not na or not nb:
        return 0.0
    if na == nb:
        return 100.0

    ta, tb = na.split(), nb.split()
    corto, largo = (ta, tb) if len(ta) <= len(tb) else (tb, ta)

    total = sum(max(jaro_winkler(t, u) for u in largo) for t in corto)
    base = total / len(corto)

    # Penalizacion por diferencia de cantidad de tokens: leve y acotada.
    # Perder un match por un segundo nombre ausente seria un falso negativo,
    # que en screening es el error grave.
    ratio = len(corto) / len(largo)
    ajustado = base * (0.85 + 0.15 * ratio)

    return round(ajustado * 100, 1)


def mejor_alias(consulta: str, nombres: list[str], *, es_entidad: bool = False) -> tuple[float, str]:
    """Mejor puntaje entre la consulta y un conjunto de nombres o alias.

    Devuelve (puntaje, nombre_que_matcheo) para que el expediente registre
    contra que alias especifico se produjo la coincidencia.
    """
    if not nombres:
        return 0.0, ""
    puntajes = [(score_nombres(consulta, n, es_entidad=es_entidad), n) for n in nombres]
    return max(puntajes, key=lambda p: p[0])
