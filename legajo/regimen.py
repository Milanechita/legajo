"""Regimen de reporte y plazos.

La Res. UIF 56/2024 fija tres plazos distintos y no son intercambiables:

    Lavado de activos .......... 24hs desde que se concluye que la operacion
                                 reviste tal caracter, y nunca mas de 90 dias
                                 corridos desde que fue realizada o tentada
    Financiacion del terrorismo  24hs desde la operacion
    Financiamiento de la
    proliferacion (FPADM) ...... 24hs desde la operacion

La diferencia entre "desde que se concluye" y "desde la operacion" es de
fondo. En lavado el reloj arranca con el analisis y tiene un techo absoluto.
En terrorismo y proliferacion arranca con la operacion, sin analisis previo
que valga: la ventana es de un dia.

Por eso el plazo no se declara en la alerta. Se deriva del regimen, y el
regimen se deriva de por que disparo la alerta. Un campo `plazo_dias` que
alguien carga a mano es un campo que alguien va a cargar mal, y el error solo
se descubre cuando la UIF pregunta por que un reporte de terrorismo salio a
los tres meses.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum


class Regimen(str, Enum):
    LA = "LA"          # lavado de activos
    FT = "FT"          # financiacion del terrorismo
    FPADM = "FPADM"    # financiamiento de la proliferacion


@dataclass(frozen=True)
class Plazo:
    """Reglas de plazo de un regimen.

    `horas_desde_conclusion` es la ventana que corre una vez que el sujeto
    obligado concluyo que hay que reportar. `dias_tope_desde_operacion` es el
    techo absoluto, que existe solo en lavado: no importa cuanto tarde el
    analisis, el reporte no puede salir despues.
    """

    regimen: Regimen
    horas_desde_conclusion: int
    dias_tope_desde_operacion: int | None
    norma: str

    @property
    def urgente(self) -> bool:
        """Sin tope significa que la ventana es de un dia y punto."""
        return self.dias_tope_desde_operacion is None


PLAZOS: dict[Regimen, Plazo] = {
    Regimen.LA: Plazo(
        regimen=Regimen.LA,
        horas_desde_conclusion=24,
        dias_tope_desde_operacion=90,
        norma="Res. UIF 56/2024",
    ),
    Regimen.FT: Plazo(
        regimen=Regimen.FT,
        horas_desde_conclusion=24,
        dias_tope_desde_operacion=None,
        norma="Res. UIF 207/2025 art. 2",
    ),
    Regimen.FPADM: Plazo(
        regimen=Regimen.FPADM,
        horas_desde_conclusion=24,
        dias_tope_desde_operacion=None,
        norma="Res. UIF 3/2026 art. 3",
    ),
}

# Comites del Consejo de Seguridad que determinan el regimen.
# 1267 y sucesivas: terrorismo. 1718 (RPDC) y 1737 (Iran): proliferacion.
_COMITES_FPADM = ("1718", "1737", "2231", "DPRK", "RPDC", "IRAN", "NPWMD", "RES1718")
_COMITES_FT = ("1267", "AL-QAIDA", "TALIBAN", "SDGT", "ISIL", "DA'ESH")


def regimen_de_coincidencia(lista: str, programas: tuple[str, ...]) -> Regimen:
    """Deriva el regimen de una coincidencia en lista de control.

    Se mira el comite o programa que motivo la designacion, no la lista de
    origen: la Consolidada de la ONU contiene designaciones de terrorismo y
    de proliferacion mezcladas, y no son el mismo regimen ni el mismo
    procedimiento.
    """
    texto = " ".join(programas).upper()

    if any(c in texto for c in _COMITES_FPADM):
        return Regimen.FPADM
    if any(c in texto for c in _COMITES_FT):
        return Regimen.FT

    # RePET existe por el Decreto 918/2012, que reglamenta el congelamiento
    # por financiacion del terrorismo.
    if lista.upper() == "REPET":
        return Regimen.FT

    return Regimen.LA


# Tipologias de monitoreo. Ninguna es de terrorismo ni proliferacion por si
# sola: esas surgen de las listas, no del comportamiento transaccional.
REGIMEN_POR_ALERTA: dict[str, Regimen] = {
    "DESVIO_PERFIL": Regimen.LA,
    "FRACCIONAMIENTO": Regimen.LA,
    "EFECTIVO_DESPROPORCIONADO": Regimen.LA,
    "JURISDICCION_NO_DECLARADA": Regimen.LA,
    "ACELERACION": Regimen.LA,
    "MONTOS_REDONDOS": Regimen.LA,
    "SIN_PERFIL": Regimen.LA,
}


def regimen_de_alerta(codigo: str) -> Regimen:
    return REGIMEN_POR_ALERTA.get(codigo, Regimen.LA)


@dataclass(frozen=True)
class Vencimiento:
    """Cuando vence el reporte y por que."""

    regimen: Regimen
    fecha_operacion: date
    fecha_deteccion: date
    vence: date
    norma: str
    urgente: bool

    @property
    def dias_restantes_desde(self) -> int:
        return (self.vence - self.fecha_deteccion).days

    def resumen(self) -> str:
        etiqueta = "24hs" if self.urgente else f"vence {self.vence.isoformat()}"
        return f"{self.regimen.value}: {etiqueta} ({self.norma})"


def vencimiento(
    regimen: Regimen,
    fecha_operacion: date,
    fecha_deteccion: date | None = None,
) -> Vencimiento:
    """Calcula el vencimiento del reporte.

    En lavado se toma el menor entre el dia siguiente a la deteccion y el
    tope de 90 dias desde la operacion. Ese minimo es la regla completa: un
    analisis que empieza el dia 89 tiene un dia, no veinticuatro horas
    contadas desde donde uno quiera.
    """
    plazo = PLAZOS[regimen]
    deteccion = fecha_deteccion or date.today()

    # Las horas se redondean hacia arriba a dias corridos. Sumar
    # timedelta(hours=24) a un date funciona por casualidad, porque son
    # exactamente un dia; con 23 horas daria cero.
    dias_conclusion = -(-plazo.horas_desde_conclusion // 24)
    limite = deteccion + timedelta(days=dias_conclusion)

    if plazo.dias_tope_desde_operacion is not None:
        tope = fecha_operacion + timedelta(days=plazo.dias_tope_desde_operacion)
        limite = min(limite, tope)

    return Vencimiento(
        regimen=regimen,
        fecha_operacion=fecha_operacion,
        fecha_deteccion=deteccion,
        vence=limite,
        norma=plazo.norma,
        urgente=plazo.urgente,
    )
