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
