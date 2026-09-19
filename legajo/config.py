"""Politica de screening.

Esto es politica, no mecanismo. Cambiar el apetito de riesgo se hace aca y no
toca una linea del motor de cotejo.

Los umbrales estan calibrados para recall, no para precision. La asimetria es
deliberada y es criterio de dominio: un falso negativo es un incumplimiento
regulatorio con sancion prevista en el Capitulo IV de la Ley 25.246; un falso
positivo es una hora de trabajo de un analista. No son errores comparables.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Politica:
    # Por debajo de esto no se genera coincidencia. Deliberadamente bajo.
    umbral_revision: float = 78.0

    # Por encima de esto la coincidencia se marca como probable y se prioriza.
    umbral_probable: float = 92.0

    # Una coincidencia exacta de documento no pasa por el motor difuso.
    # Un numero de pasaporte identico no admite interpretacion.
    score_documento: float = 100.0

    # Atenuantes. Restan puntaje, nunca descartan por si solos: los datos
    # secundarios de las listas son incompletos y contradictorios, y un
    # descarte automatico por fecha de nacimiento ausente seria un falso
    # negativo introducido por el propio sistema.
    penalidad_fecha_distinta: float = 12.0
    penalidad_nacionalidad_distinta: float = 6.0

    # Listas cuya coincidencia escala el caso sin pasar por scoring.
    listas_criticas: frozenset[str] = frozenset({"OFAC_SDN", "ONU_CONSOLIDADA"})


POLITICA_POR_DEFECTO = Politica()
