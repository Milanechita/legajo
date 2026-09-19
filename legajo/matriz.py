"""Matriz de riesgo del enfoque basado en riesgo.

Esto es politica. Es un archivo de datos que quedo escrito en Python por
comodidad, no un motor. El evaluador de riesgo.py no contiene ningun umbral
ni ninguna lista: los lee de aca.

La consecuencia practica es que recalibrar el apetito de riesgo de un sujeto
obligado no requiere tocar logica, y que la matriz efectivamente aplicada
puede mostrarse tal cual ante una supervision.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Jurisdicciones bajo llamado a la accion del GAFI. Historicamente estables,
# pero la lista es dinamica: debe actualizarse contra la publicacion vigente
# del GAFI en cada revision de la matriz.
JURISDICCIONES_ALTO_RIESGO = frozenset({
    "IRAN", "COREA DEL NORTE", "REPUBLICA POPULAR DEMOCRATICA DE COREA",
    "MYANMAR",
})

# Jurisdicciones bajo monitoreo intensificado ("lista gris"). Igual que arriba:
# es un parametro, no una verdad permanente.
JURISDICCIONES_MONITOREO = frozenset({
    "BOLIVIA", "HAITI", "LIBANO", "NIGERIA", "SIRIA", "VENEZUELA", "YEMEN",
})

# Actividades con exposicion elevada segun tipologias GAFI y UIF.
ACTIVIDADES_SENSIBLES = frozenset({
    "CAMBIO", "CASA DE CAMBIO", "CRIPTOACTIVOS", "ACTIVOS VIRTUALES",
    "JUEGOS DE AZAR", "CASINO", "METALES PRECIOSOS", "JOYERIA", "ARTE",
    "INMOBILIARIA", "ARMAS", "COMERCIO EXTERIOR", "IMPORTACION",
})


@dataclass(frozen=True)
class Factor:
    """Un factor de riesgo que aplico a un cliente concreto.

    Cada factor que suma puntos queda registrado con su descripcion. Un
    puntaje sin desglose no es justificable: la resolucion exige poder
    explicar por que un cliente quedo en determinado nivel.
    """

    codigo: str
    dimension: str      # CLIENTE | GEOGRAFICO | ACTIVIDAD | CANAL | CONTROL
    descripcion: str
    puntos: float


@dataclass(frozen=True)
class MatrizRiesgo:
    # --- Dimension cliente ---
    puntos_persona_juridica: float = 8.0
    puntos_estructura_multicapa: float = 12.0   # por nivel por encima del primero
    puntos_beneficiario_no_identificado: float = 25.0
    puntos_titularidad_opaca: float = 20.0      # escalado por fraccion opaca
    puntos_participacion_circular: float = 15.0
    puntos_pep_nacional: float = 20.0
    puntos_pep_extranjera: float = 35.0
    puntos_pep_parentesco: float = 10.0   # se suma al tipo que corresponda

    # --- Dimension geografica ---
    puntos_jurisdiccion_alto_riesgo: float = 40.0
    puntos_jurisdiccion_monitoreo: float = 18.0
    puntos_residencia_distinta_nacionalidad: float = 5.0

    # --- Dimension actividad ---
    puntos_actividad_sensible: float = 15.0
    puntos_actividad_no_declarada: float = 10.0

    # --- Dimension canal ---
    puntos_canal_no_presencial: float = 8.0

    # --- Resultado de controles (etapa 1) ---
    puntos_coincidencia_probable: float = 45.0
    puntos_coincidencia_revision: float = 15.0

    # --- Umbrales de nivel ---
    umbral_medio: float = 25.0
    umbral_alto: float = 55.0

    # --- Elevadores ---
    # Condiciones que fijan un piso de nivel sin importar el puntaje. Existen
    # para que ninguna suma de factores bajos pueda dejar en riesgo bajo a un
    # cliente que la normativa considera de riesgo alto por definicion.
    # PEP_EXTRANJERA esta y PEP_NACIONAL no, y no es un descuido: la
    # normativa califica de alto riesgo a la PEP extranjera por definicion,
    # mientras que la nacional se evalua segun su riesgo concreto.
    eleva_a_alto: frozenset[str] = frozenset({
        "COINCIDENCIA_PROBABLE",
        "PEP_EXTRANJERA",
        "BENEFICIARIO_NO_IDENTIFICADO",
        "JURISDICCION_ALTO_RIESGO",
    })

    jurisdicciones_alto_riesgo: frozenset[str] = JURISDICCIONES_ALTO_RIESGO
    jurisdicciones_monitoreo: frozenset[str] = JURISDICCIONES_MONITOREO
    actividades_sensibles: frozenset[str] = ACTIVIDADES_SENSIBLES


MATRIZ_POR_DEFECTO = MatrizRiesgo()

NIVELES = ("BAJO", "MEDIO", "ALTO")

REGIMEN = {
    "BAJO": "DD_SIMPLIFICADA",
    "MEDIO": "DD_MEDIA",
    "ALTO": "DD_REFORZADA",
}

# Cada cuanto hay que volver a mirar el legajo, segun el nivel de riesgo.
# La periodicidad tiene que ser proporcional al riesgo; estos son los plazos
# que usan los manuales del sector como techo.
MESES_HASTA_REVISION = {
    "ALTO": 12,
    "MEDIO": 36,
    "BAJO": 60,
}
