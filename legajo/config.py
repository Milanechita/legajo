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
from datetime import date


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


# ---------------------------------------------------------------------------
# Salario Minimo, Vital y Movil.
#
# Buena parte de la normativa no fija umbrales en pesos sino en SMVM, asi que
# el valor vigente es un parametro del sistema y no un dato de color. Lo fija
# el Consejo Nacional del Empleo, la Productividad y el SMVM, y rige el valor
# al 31 de diciembre del anio anterior o al 30 de junio del corriente, segun
# corresponda.
#
# Si la fecha de abajo tiene mas de seis meses, los umbrales estan mal.
# ---------------------------------------------------------------------------

SMVM = 383_800.0
SMVM_VIGENCIA = date(2026, 9, 1)


def pesos(cantidad_smvm: float) -> float:
    """Convierte un umbral expresado en SMVM a pesos."""
    return cantidad_smvm * SMVM


@dataclass(frozen=True)
class UmbralesSMVM:
    """Umbrales normativos, en cantidad de SMVM.

    Se guardan en SMVM y no en pesos porque asi los escribe la norma. Al
    actualizar el salario, los montos se recalculan solos.
    """

    cliente_habitual: float = 700.0          # Res. 43/2024
    locacion_alcanzada: float = 300.0        # Res. 43/2024
    revision_externa: float = 875.0          # Res. 43/2024 art. 17
    compraventa_inmuebles: float = 700.0     # Ley 25.246 art. 20 inc. 17 a)
    administracion_bienes: float = 150.0     # Ley 25.246 art. 20 inc. 17 b)
    administracion_cuentas: float = 50.0     # Ley 25.246 art. 20 inc. 17 c)

    def en_pesos(self, nombre: str) -> float:
        return pesos(getattr(self, nombre))


UMBRALES = UmbralesSMVM()


# ---------------------------------------------------------------------------
# Parametros de monitoreo transaccional.
#
# Igual que la matriz de riesgo: esto es politica, no motor. Las reglas de
# alertas.py no contienen ningun numero, los leen de aca.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ParametrosMonitoreo:
    # --- umbral de reporte ---
    # Lo fija la UIF por resolucion y se actualiza. Sin este numero la regla
    # de fraccionamiento no corre, y eso es correcto: detectar evasion de un
    # umbral que no se sabe cual es seria inventar el resultado.
    umbral_reporte: float = 0.0
    umbral_vigencia: date | None = None

    # --- desvio del perfil ---
    tolerancia_desvio: float = 0.25      # cuanto se admite por encima
    desvio_severo: float = 3.0           # multiplo que eleva la severidad

    # --- fraccionamiento ---
    ventana_fraccionamiento: int = 7     # dias corridos
    minimo_operaciones_fraccionadas: int = 3
    cercania_umbral_severa: float = 0.70  # la mayor a >=70% del umbral
    piso_fraccionamiento: float = 0.10   # por debajo, no es parte del reparto

    # --- efectivo ---
    tolerancia_efectivo: float = 0.15
    efectivo_sin_perfil: float = 0.40    # referencia cuando no hay perfil
    efectivo_severo: float = 0.75

    # --- aceleracion ---
    ventana_aceleracion: int = 30        # dias
    factor_aceleracion: float = 3.0
    minimo_operaciones_para_linea_base: int = 8

    # --- montos redondos ---
    multiplo_redondo: float = 100_000.0
    proporcion_redondos: float = 0.70

    # --- generales ---
    pais_local: str = "AR"
    minimo_operaciones_para_exigir_perfil: int = 3
    jurisdicciones_de_riesgo: frozenset[str] = frozenset()


def parametros_con_listas(umbral_reporte: float = 0.0,
                          umbral_vigencia: date | None = None) -> ParametrosMonitoreo:
    """Parametros con las jurisdicciones de riesgo ya cargadas desde la matriz.

    Se arma con funcion y no como valor por defecto del dataclass para no
    importar matriz.py desde aca: config no depende de la matriz, la matriz
    depende de config.
    """
    from .matriz import (
        JURISDICCIONES_ALTO_RIESGO, JURISDICCIONES_MONITOREO,
        JURISDICCIONES_NO_COOPERANTES,
    )

    return ParametrosMonitoreo(
        umbral_reporte=umbral_reporte,
        umbral_vigencia=umbral_vigencia,
        jurisdicciones_de_riesgo=(
            JURISDICCIONES_ALTO_RIESGO
            | JURISDICCIONES_MONITOREO
            | JURISDICCIONES_NO_COOPERANTES
        ),
    )


PARAMETROS_POR_DEFECTO = ParametrosMonitoreo()
