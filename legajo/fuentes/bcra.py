"""Central de Deudores del BCRA.

Tres endpoints publicos, sin autenticacion, documentados en
https://deudores.bcra.apidocs.ar/ :

    GET /centraldedeudores/v1.0/Deudas/{cuit}
    GET /centraldedeudores/v1.0/Deudas/Historicas/{cuit}
    GET /centraldedeudores/v1.0/Deudas/ChequesRechazados/{cuit}

Dos reglas gobiernan este archivo:

1. Las pruebas nunca llaman al BCRA. La descarga entra por parametro, asi que
   una prueba inyecta un fixture y no hay forma de que se escape una llamada
   real. Una suite que depende de una API de terceros falla los dias que el
   tercero esta caido, y despues nadie la mira.

2. Todo lo que se baja queda en cache con su fecha de consulta. Sin la fecha,
   "el cliente esta en situacion 3" no dice nada: puede ser de hoy o de hace
   dos anios, y para el legajo importa cuando se lo fue a buscar.

La situacion es el numero que publica el BCRA, del 1 al 6. No se le pone
etiqueta de texto porque seria ponerle nombre a una clasificacion normativa
sin haberla verificado. Lo unico que se deriva es `irregular`, que es de 3
para arriba y es el corte que usa la senal del item 4.5.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable

HOST = "https://api.bcra.gob.ar"
BASE = "/centraldedeudores/v1.0/Deudas"
AGENTE = "legajo/0.3 (herramienta de cumplimiento PLA-FT)"
TIMEOUT = 30

# De 3 para arriba el BCRA considera la asistencia irregular. Es el corte que
# pide el item 4.5 del roadmap.
SITUACION_IRREGULAR = 3

ENDPOINTS = {
    "deudas": BASE + "/{cuit}",
    "historicas": BASE + "/Historicas/{cuit}",
    "cheques": BASE + "/ChequesRechazados/{cuit}",
}


class ErrorBCRA(Exception):
    """La consulta no se pudo completar."""


@dataclass(frozen=True)
class Asistencia:
    """Una linea de deuda informada por una entidad en un periodo."""

    entidad: str
    situacion: int
    monto: float                    # en miles de pesos, como lo informa el BCRA
    periodo: str                    # AAAAMM
    fecha_situacion_1: str = ""
    dias_atraso: int = 0
    refinanciaciones: bool = False
    recategorizacion_obligatoria: bool = False
    situacion_juridica: bool = False
    irrecuperable_disposicion_tecnica: bool = False
    en_revision: bool = False
    proceso_judicial: bool = False

    @property
    def irregular(self) -> bool:
        return self.situacion >= SITUACION_IRREGULAR


@dataclass(frozen=True)
class ChequeRechazado:
    entidad: str
    numero: str
    fecha_rechazo: str
    monto: float
    causal: str = ""
    pagado: bool = False


@dataclass
class InformeBCRA:
    """Lo que el BCRA sabe de un CUIT, con la fecha en que se lo consulto."""

    cuit: str
    consultado: date
    denominacion: str = ""
    asistencias: list[Asistencia] = field(default_factory=list)
    cheques: list[ChequeRechazado] = field(default_factory=list)
    sin_datos: bool = False

    @property
    def peor_situacion(self) -> int:
        """La peor situacion informada. Cero cuando no hay deuda informada.

        Se toma la peor y no el promedio: un cliente en situacion 1 con cinco
        bancos y en 5 con el sexto tiene un problema, y promediar lo esconde.
        """
        return max((a.situacion for a in self.asistencias), default=0)

    @property
    def irregular(self) -> bool:
        return self.peor_situacion >= SITUACION_IRREGULAR

    @property
    def deuda_total(self) -> float:
        """Suma de montos del periodo mas reciente, en miles de pesos.

        Se suma un solo periodo. Sumar todos contaria la misma deuda una vez
        por mes informado.
        """
        if not self.asistencias:
            return 0.0
        ultimo = max(a.periodo for a in self.asistencias)
        return sum(a.monto for a in self.asistencias if a.periodo == ultimo)

    @property
    def entidades(self) -> tuple[str, ...]:
        return tuple(sorted({a.entidad for a in self.asistencias}))

    def antiguedad_en_dias(self, al: date | None = None) -> int:
        return ((al or date.today()) - self.consultado).days


# ---------------------------------------------------------------------------
# Parseo
# ---------------------------------------------------------------------------

def _texto(valor: Any) -> str:
    return "" if valor is None else str(valor).strip()


def parsear_deudas(payload: dict) -> tuple[str, list[Asistencia]]:
    """Traduce la respuesta de Deudas o de Historicas.

    Las dos tienen la misma forma: resultados con periodos, y cada periodo con
    sus entidades. Por eso hay un solo parser y no dos que se despeguen.
    """
    resultados = (payload or {}).get("results") or {}
    denominacion = _texto(resultados.get("denominacion"))

    asistencias: list[Asistencia] = []
    for periodo in resultados.get("periodos") or []:
        nombre = _texto(periodo.get("periodo"))
        for e in periodo.get("entidades") or []:
            asistencias.append(Asistencia(
                entidad=_texto(e.get("entidad")),
                situacion=int(e.get("situacion") or 0),
                monto=float(e.get("monto") or 0.0),
                periodo=nombre,
                fecha_situacion_1=_texto(e.get("fechaSit1")),
                dias_atraso=int(e.get("diasAtrasoPago") or 0),
                refinanciaciones=bool(e.get("refinanciaciones")),
                recategorizacion_obligatoria=bool(e.get("recategorizacionOblig")),
                situacion_juridica=bool(e.get("situacionJuridica")),
                irrecuperable_disposicion_tecnica=bool(e.get("irrecDisposicionTecnica")),
                en_revision=bool(e.get("enRevision")),
                proceso_judicial=bool(e.get("procesoJud")),
            ))
    return denominacion, asistencias


def parsear_cheques(payload: dict) -> list[ChequeRechazado]:
    """Traduce la respuesta de ChequesRechazados.

    El anidado de esta respuesta es mas profundo y menos estable que el de
    deudas, asi que se recorre defensivamente: lo que no venga queda vacio en
    vez de romper la consulta entera.
    """
    resultados = (payload or {}).get("results") or {}
    cheques: list[ChequeRechazado] = []

    for causal in resultados.get("causales") or []:
        nombre_causal = _texto(causal.get("causal"))
        for entidad in causal.get("entidades") or []:
            nombre_entidad = _texto(entidad.get("entidad"))
            for detalle in entidad.get("detalle") or []:
                cheques.append(ChequeRechazado(
                    entidad=nombre_entidad,
                    numero=_texto(detalle.get("nroCheque")),
                    fecha_rechazo=_texto(detalle.get("fechaRechazo")),
                    monto=float(detalle.get("monto") or 0.0),
                    causal=nombre_causal,
                    pagado=bool(detalle.get("fechaPago")),
                ))
    return cheques


# ---------------------------------------------------------------------------
# Descarga y cache
# ---------------------------------------------------------------------------

# El BCRA limita la tasa de consultas y no lo documenta. Medido contra la API
# real el 22/09/2026: diez pedidos seguidos pasan y el once devuelve 429. No
# manda Retry-After ni ninguna cabecera de limite, asi que no hay forma de
# saber cuanto esperar salvo probando. Se libera entre 17 y 37 segundos
# despues.
#
# Con un segundo de pausa entre pedidos no aparece el 429. Se deja ese valor
# en vez de uno mas agresivo porque correr un padron de 5.000 clientes contra
# un servicio publico gratuito sin espaciar los pedidos es abusar de el.
PAUSA_ENTRE_PEDIDOS = 1.0
ESPERA_TRAS_429 = 40.0
REINTENTOS_429 = 2

_ultimo_pedido = 0.0


def descargar(url: str, dormir: Callable[[float], None] = time.sleep) -> dict:
    """Trae un endpoint del BCRA. Es la unica funcion que toca la red.

    `dormir` entra por parametro para poder probar el reintento sin esperar
    cuarenta segundos de verdad.
    """
    global _ultimo_pedido

    for intento in range(REINTENTOS_429 + 1):
        falta = PAUSA_ENTRE_PEDIDOS - (time.monotonic() - _ultimo_pedido)
        if falta > 0:
            dormir(falta)
        _ultimo_pedido = time.monotonic()

        pedido = urllib.request.Request(url, headers={
            "User-Agent": AGENTE, "Accept": "application/json",
        })
        try:
            with urllib.request.urlopen(pedido, timeout=TIMEOUT) as respuesta:
                return json.loads(respuesta.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            # 404 es "este CUIT no tiene deuda informada", que es un resultado
            # y no un error. Cualquier otro codigo si lo es.
            if e.code == 404:
                return {"status": 404, "results": {}}
            if e.code == 429 and intento < REINTENTOS_429:
                dormir(ESPERA_TRAS_429)
                continue
            raise ErrorBCRA(f"{url}: HTTP {e.code}") from e
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
            raise ErrorBCRA(f"{url}: {e}") from e

    raise ErrorBCRA(f"{url}: HTTP 429 despues de {REINTENTOS_429} reintentos")


def _ruta_cache(directorio: Path, recurso: str, cuit: str) -> Path:
    return Path(directorio) / f"{cuit}-{recurso}.json"


def _leer_cache(ruta: Path, vigencia_dias: int, hoy: date) -> dict | None:
    if not ruta.exists():
        return None
    try:
        guardado = json.loads(ruta.read_text(encoding="utf-8"))
        consultado = date.fromisoformat(guardado["consultado"])
    except (ValueError, KeyError, OSError):
        return None
    if (hoy - consultado).days > vigencia_dias:
        return None
    return guardado


def _escribir_cache(ruta: Path, payload: dict, hoy: date) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(
        json.dumps({"consultado": hoy.isoformat(), "payload": payload},
                   ensure_ascii=False, indent=1),
        encoding="utf-8",
    )


def consultar(
    cuit: str,
    cache: str | Path,
    *,
    vigencia_dias: int = 30,
    hoy: date | None = None,
    bajar: Callable[[str], dict] = descargar,
    incluir_cheques: bool = True,
) -> InformeBCRA:
    """Consulta el BCRA para un CUIT, usando la cache cuando sigue vigente.

    `bajar` entra por parametro para que las pruebas inyecten un fixture. Es
    la unica forma de garantizar que la suite no salga a la red: si la funcion
    de descarga estuviera cableada adentro, alcanzaria un descuido para que
    una prueba empiece a depender de que el BCRA este arriba.
    """
    hoy = hoy or date.today()
    limpio = "".join(c for c in cuit if c.isdigit())
    if len(limpio) != 11:
        raise ValueError(f"{cuit!r} no es un CUIT de 11 digitos")

    directorio = Path(cache)
    recursos = ["deudas", "cheques"] if incluir_cheques else ["deudas"]
    payloads: dict[str, dict] = {}
    consultado = hoy

    for recurso in recursos:
        ruta = _ruta_cache(directorio, recurso, limpio)
        guardado = _leer_cache(ruta, vigencia_dias, hoy)
        if guardado is not None:
            payloads[recurso] = guardado["payload"]
            # La fecha del informe es la de la consulta mas vieja que se esta
            # usando. Decir que es de hoy cuando media respuesta sale de una
            # cache de hace tres semanas seria mentir sobre la antiguedad.
            consultado = min(consultado, date.fromisoformat(guardado["consultado"]))
            continue

        url = HOST + ENDPOINTS[recurso].format(cuit=limpio)
        payload = bajar(url)
        payloads[recurso] = payload
        _escribir_cache(ruta, payload, hoy)

    denominacion, asistencias = parsear_deudas(payloads.get("deudas", {}))
    cheques = parsear_cheques(payloads.get("cheques", {}))

    return InformeBCRA(
        cuit=limpio,
        consultado=consultado,
        denominacion=denominacion,
        asistencias=asistencias,
        cheques=cheques,
        sin_datos=not asistencias and not cheques,
    )
