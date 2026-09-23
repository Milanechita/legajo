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
from datetime import date

from .paises import codigos

# ---------------------------------------------------------------------------
# Listas del GAFI, plenario del 19 de junio de 2026.
#
# El GAFI las actualiza tres veces al anio, tras los plenarios de febrero,
# junio y octubre. La fecha de abajo no es decorativa: si tiene mas de cuatro
# meses, la matriz esta desactualizada y hay clientes recibiendo el puntaje
# equivocado.
#
# Se guardan como codigos ISO porque el GAFI publica en ingles y el padron
# viene en castellano. Ver paises.py.
# ---------------------------------------------------------------------------

GAFI_PLENARIO = date(2026, 6, 19)

# El GAFI distingue dos tratamientos dentro de la lista negra, y la diferencia
# es de fondo: a Iran y Corea del Norte pide aplicar contramedidas, a Myanmar
# solo debida diligencia reforzada proporcional al riesgo. Colapsar las dos en
# una sola categoria pierde esa distincion.
GAFI_CONTRAMEDIDAS = codigos([
    "Democratic People's Republic of Korea",
    "Iran",
])

GAFI_DILIGENCIA_REFORZADA = codigos([
    "Myanmar",
])

JURISDICCIONES_ALTO_RIESGO = GAFI_CONTRAMEDIDAS | GAFI_DILIGENCIA_REFORZADA

# Lista gris. El GAFI aclara expresamente que NO pide diligencia reforzada
# sobre estas jurisdicciones, sino tenerlas en cuenta en el analisis de riesgo.
# Por eso suman puntos y no son elevador.
JURISDICCIONES_MONITOREO = codigos([
    "Angola", "Bolivia", "Bosnia and Herzegovina", "Bulgaria", "Cameroon",
    "Côte d'Ivoire", "Democratic Republic of the Congo", "Haiti", "Iraq",
    "Kenya", "Kuwait", "Lao PDR", "Lebanon", "Monaco", "Nepal",
    "Papua New Guinea", "South Sudan", "Syria", "Venezuela", "Vietnam",
    "Virgin Islands (UK)", "Yemen",
])

# ---------------------------------------------------------------------------
# Jurisdicciones no cooperantes a fines de transparencia fiscal.
# Decreto 862/2019, texto segun Decreto 398/2026, vigente para periodos
# fiscales iniciados desde el 28 de mayo de 2026.
#
# Es un criterio fiscal y no de PLA/FT, por eso va aparte del GAFI. Los
# manuales del sector lo usan para reforzar controles sobre transferencias
# desde y hacia el exterior.
# ---------------------------------------------------------------------------

ARCA_VIGENCIA = date(2026, 5, 28)

JURISDICCIONES_NO_COOPERANTES = codigos([
    "Brecqhou", "Estado de Eritrea", "Estado de la Ciudad del Vaticano",
    "Estado de Libia", "Estado Plurinacional de Bolivia", "Isla Ascensión",
    "Isla de Sark", "Isla Santa Elena", "Islas Salomón",
    "Los Estados Federados de Micronesia", "Reino de Bután", "Reino de Camboya",
    "Reino de Lesoto", "Reino de Tonga", "República Kirguisa",
    "República Árabe de Egipto", "República Árabe Siria",
    "República Argelina Democrática y Popular", "República Centroafricana",
    "República Cooperativa de Guyana", "República de Angola",
    "República de Bielorrusia", "República de Burundí",
    "República de Costa de Marfil", "República de Cuba", "República de Fiyi",
    "República de Gambia", "República de Guinea", "República de Guinea Ecuatorial",
    "República Democrática Popular Lao",
    "República Democrática Socialista de Sri Lanka", "República Federal de Somalia",
    "República Federal Democrática de Nepal", "República Gabonesa",
    "República Islámica de Afganistán", "República Islámica de Irán",
    "República Popular de Bangladés", "República de Guinea-Bisáu",
    "República de Haití", "República de Honduras", "República de Irak",
    "República de Kiribati", "República de la Unión de Myanmar",
    "República de Malaui", "República de Malí", "República de Mozambique",
    "República de Nicaragua", "República de Palaos", "República de Sierra Leona",
    "República de Sudán del Sur", "República de Surinam",
    "República de Tayikistán", "República de Uzbekistán", "República de Yemen",
    "República de Yibuti", "República de Zambia", "República de Zimbabue",
    "República del Chad", "República del Níger", "República del Sudán",
    "República Democrática de Santo Tomé y Príncipe",
    "República Democrática de Timor-Leste", "República del Congo",
    "República Democrática del Congo", "República Democrática Federal de Etiopía",
    "República Popular Democrática de Corea", "República Togolesa",
    "República Unida de Tanzania",
    "Territorio Británico de Ultramar Islas Pitcairn, Henderson, Ducie y Oeno",
    "Tristán da Cunha", "Tuvalu", "Unión de las Comoras",
])

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
    puntos_jurisdiccion_contramedidas: float = 45.0
    puntos_jurisdiccion_alto_riesgo: float = 40.0
    puntos_jurisdiccion_monitoreo: float = 18.0
    puntos_jurisdiccion_no_cooperante: float = 12.0
    puntos_pais_no_reconocido: float = 8.0
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
        # Los cuatro de abajo salen del monitoreo y de las fuentes externas,
        # asi que solo existen en la reevaluacion del item 3.6. Entran como
        # elevadores y no como puntos porque ponderarlos exigiria inventar
        # cuanto vale cada uno, y el proyecto ya tiene dos cortes sin calibrar.
        "CONGELAMIENTO_REQUERIDO",
        "CAPACIDAD_EXCEDIDA",
        "SITUACION_BCRA_IRREGULAR",
        "ACTIVIDAD_CAMBIADA_SIN_INFORMAR",
    })

    jurisdicciones_contramedidas: frozenset[str] = GAFI_CONTRAMEDIDAS
    jurisdicciones_alto_riesgo: frozenset[str] = JURISDICCIONES_ALTO_RIESGO
    jurisdicciones_monitoreo: frozenset[str] = JURISDICCIONES_MONITOREO
    jurisdicciones_no_cooperantes: frozenset[str] = JURISDICCIONES_NO_COOPERANTES
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
