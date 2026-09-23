"""Procedencia de los datos del cliente.

El padron es lo declarado. Una fila de padron es, por definicion, lo que el
cliente dijo en el alta, asi que `Cliente` no lleva envoltorios: sus campos
son la declaracion.

Lo verificado entra aparte, como constataciones. Una constatacion dice que tal
dia se consulto tal fuente y que el valor hallado fue tal otro. Comparar eso
contra lo declarado es lo que produce la discrepancia, y por eso "actividad
declarada contra actividad inscripta" no necesita una regla propia: sale de
comparar, igual que cualquier otro campo.

Tres decisiones que conviene tener a mano:

1. Las constataciones son append-only, como el expediente. Una correccion es
   una constatacion nueva que tapa a la anterior, nunca un borrado. Sin eso no
   se puede mostrar que se verifico y cuando, que es lo que pide una
   inspeccion.

2. `campo` es una enumeracion cerrada y no un string libre. Hay una prueba que
   exige que cada valor exista como atributo de Cliente: si alguien renombra un
   campo, rompe la prueba y no el analisis en silencio.

3. Comparar no es restar strings. Cada campo tiene su normalizador, porque
   "Iran" y "IRAN" son el mismo pais y "ACME S.A." y "ACME SA" son la misma
   sociedad. La tabla de normalizadores esta abajo y es el unico lugar donde se
   toca eso.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Any, Callable

from .modelo import Cliente
from .normalizar import normalizar
from .paises import iso


class Origen(str, Enum):
    """De donde salio un dato.

    El orden de declaracion es el orden de precedencia, de mas fuerte a mas
    debil, y lo usa `ORDEN_DE_PRECEDENCIA`.
    """

    LISTA_OFICIAL = "LISTA_OFICIAL"
    ARCA = "ARCA"
    BCRA = "BCRA"
    INFORME_COMERCIAL = "INFORME_COMERCIAL"
    RESPALDO = "RESPALDO"
    ANALISTA = "ANALISTA"
    DECLARADO = "DECLARADO"


# Cuando dos constataciones del mismo campo se contradicen, gana la de origen
# mas fuerte. Es politica y vive en un solo lugar para poder discutirla sin
# tocar el motor.
#
# La precedencia manda sobre la fecha, a proposito: un organismo del Estado no
# deja de tener razon porque alguien cargo algo despues. El efecto secundario
# esta anotado en el README y hay una prueba que lo fija.
ORDEN_DE_PRECEDENCIA: tuple[Origen, ...] = tuple(Origen)

_PESO = {origen: posicion for posicion, origen in enumerate(ORDEN_DE_PRECEDENCIA)}


class Campo(str, Enum):
    """Campos de Cliente que se pueden constatar contra una fuente.

    Cada valor es el nombre exacto del atributo en Cliente. La prueba
    `test_todo_campo_constatable_existe_en_cliente` lo verifica.

    `documentos` no esta: es una lista y no un valor suelto, y verificar un
    CUIT es validarlo contra su digito verificador antes que cotejarlo contra
    una fuente. Eso es el item 1.3 y vive en modelo.py.
    """

    NOMBRE = "nombre"
    TIPO = "tipo"
    FECHA_NACIMIENTO = "fecha_nacimiento"
    NACIONALIDAD = "nacionalidad"
    PAIS_RESIDENCIA = "pais_residencia"
    ACTIVIDAD = "actividad"
    OFERTA_PUBLICA = "oferta_publica"
    # Los dos de abajo son categoricos y se comparan exacto, a diferencia de
    # ACTIVIDAD, que es texto libre. Esa diferencia es la que decide si una
    # discrepancia se puede afirmar o solo se puede mostrar.
    ACTIVIDAD_CODIGO = "actividad_codigo"
    CONDICION_IVA = "condicion_iva"


# Campos cuya discrepancia se puede afirmar, porque son categoricos y se
# comparan exacto. Los demas son texto libre: una diferencia ahi puede ser un
# cambio real o la misma cosa escrita distinto, y el programa no tiene como
# saberlo.
#
# Medido sobre 10 constancias de ARCA contra el padron de ejemplo: comparar la
# actividad por texto libre da 10 discrepancias de las cuales 3 son cambios
# reales, o sea 30% de precision. Cinco tienen el mismo codigo CLAE y otra
# redaccion ("MEDICO" contra "SERVICIOS DE MEDICOS ESPECIALISTAS") y dos no
# tienen codigo al alta, asi que no se pueden verificar. Comparando el codigo
# salen las 3 reales y ninguna de mas.
#
# Por eso una diferencia de texto no se afirma como hallazgo: se muestra al
# lado de lo declarado y la conclusion la saca el analista.
CAMPOS_AFIRMABLES: frozenset = frozenset()   # se completa abajo, con Campo ya definido


class Resultado(str, Enum):
    """Como quedo un campo despues de compararlo contra lo declarado."""

    COINCIDE = "COINCIDE"
    DISCREPA = "DISCREPA"
    # El cliente no declaro el dato y la fuente lo trae. Es informacion nueva y
    # no un hallazgo: mezclarlo con DISCREPA inflaria las discrepancias con
    # campos que el cliente nunca contradijo porque nunca los completo.
    COMPLETA = "COMPLETA"


CAMPOS_AFIRMABLES = frozenset({
    Campo.TIPO,
    Campo.FECHA_NACIMIENTO,
    Campo.NACIONALIDAD,
    Campo.PAIS_RESIDENCIA,
    Campo.OFERTA_PUBLICA,
    Campo.ACTIVIDAD_CODIGO,
    Campo.CONDICION_IVA,
})
# NOMBRE y ACTIVIDAD quedan afuera. Los dos son texto libre y dos redacciones
# de lo mismo dan distinto por mas que se normalicen.


class Periodicidad(str, Enum):
    """Cada cuanto se repite el monto de un respaldo."""

    MENSUAL = "MENSUAL"
    ANUAL = "ANUAL"
    UNICA = "UNICA"

    @property
    def factor_anual(self) -> int | None:
        """Cuantas veces entra en un anio.

        UNICA devuelve None y no 1 a proposito. La venta de un inmueble no es
        ingreso anual, y contarla como tal infla la capacidad documentada. Que
        peso se le da a un ingreso de unica vez es una regla por tipo de
        documento y se define en el item 3.1, no aca.
        """
        return {Periodicidad.MENSUAL: 12, Periodicidad.ANUAL: 1}.get(self)


# ---------------------------------------------------------------------------
# Normalizadores
# ---------------------------------------------------------------------------

def _texto(valor: Any) -> str:
    return normalizar(str(valor or ""))


def _pais(valor: Any) -> str:
    """Lleva el pais a su codigo ISO. "Iran", "IRAN" e "IR" son el mismo."""
    codigo = iso(str(valor or "").strip() or None)
    return codigo or _texto(valor)


def _fecha(valor: Any) -> str:
    """Se queda con la parte de la fecha. Una hora distinta no es otro dia."""
    if isinstance(valor, date):
        return valor.isoformat()
    return str(valor or "").strip()[:10]


def _codigo(valor: Any) -> str:
    """Codigo CLAE, solo digitos.

    ARCA lo escribe de varias formas para el mismo codigo: "620100",
    "620100 - Servicios de consultores", "62.01.00". Quedarse con los digitos
    hace que las tres sean el mismo codigo y evita una discrepancia falsa por
    como vino escrito el papel.
    """
    return "".join(c for c in str(valor or "") if c.isdigit())


def _booleano(valor: Any) -> str:
    if isinstance(valor, bool):
        return "SI" if valor else "NO"
    return "SI" if str(valor or "").strip().lower() in {"si", "sí", "true", "1", "s"} else "NO"


# Un normalizador por campo. Comparar es normalizar los dos lados y ver si dan
# lo mismo, asi que cambiar como se compara un campo se hace en una linea.
NORMALIZADORES: dict[Campo, Callable[[Any], str]] = {
    Campo.NOMBRE: _texto,
    Campo.TIPO: lambda v: str(v or "").strip().upper(),
    Campo.FECHA_NACIMIENTO: _fecha,
    Campo.NACIONALIDAD: _pais,
    Campo.PAIS_RESIDENCIA: _pais,
    # Hoy la actividad es texto libre y se compara normalizado. Cuando el
    # padron tenga el codigo CLAE de ARCA (item 3.4), este normalizador pasa a
    # devolver el codigo y el resto del modulo no se entera.
    # Texto libre. Se normaliza, pero dos redacciones distintas de la misma
    # actividad siguen dando distinto, asi que una diferencia aca no alcanza
    # para afirmar nada. Ver `_codigo`.
    Campo.ACTIVIDAD: _texto,
    Campo.OFERTA_PUBLICA: _booleano,
    Campo.ACTIVIDAD_CODIGO: _codigo,
    Campo.CONDICION_IVA: lambda v: str(v or "").strip().upper(),
}


def normalizar_campo(campo: Campo, valor: Any) -> str:
    return NORMALIZADORES[campo](valor)


# ---------------------------------------------------------------------------
# Registros
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Constatacion:
    """Un dato verificado contra una fuente, en una fecha.

    Van dos fechas y no una. `fecha_dato` es a cuando corresponde el dato y
    `fecha_consulta` es cuando se lo fue a buscar. Una situacion de marzo
    consultada hoy no es lo mismo que una consultada en marzo, y para el
    vencimiento del legajo importa la segunda.
    """

    cliente_id: str
    campo: Campo
    valor: str
    origen: Origen
    fecha_consulta: date
    fecha_dato: date | None = None
    referencia: str = ""        # numero de constancia, archivo, expediente

    @property
    def peso(self) -> int:
        return _PESO[self.origen]

    def resumen(self) -> str:
        cuando = self.fecha_consulta.isoformat()
        return f"{self.campo.value}={self.valor!r} por {self.origen.value} el {cuando}"


@dataclass(frozen=True)
class Cotejo:
    """Una constatacion ya comparada contra lo que el cliente declaro."""

    campo: Campo
    resultado: Resultado
    declarado: str
    hallado: str
    constatacion: Constatacion

    @property
    def es_hallazgo(self) -> bool:
        """Una diferencia que el programa puede afirmar.

        Hacen falta las dos cosas: que el resultado sea DISCREPA y que el campo
        sea de los que se comparan exacto. COMPLETA es informacion nueva y no
        contradice nada, y una diferencia de texto libre puede ser la misma
        actividad escrita de otra forma.
        """
        return (self.resultado is Resultado.DISCREPA
                and self.campo in CAMPOS_AFIRMABLES)

    @property
    def requiere_lectura(self) -> bool:
        """Difiere, pero en un campo de texto libre.

        No es un hallazgo ni es nada: es un par de valores que hay que leer.
        Meterlo entre los hallazgos ahogaria a los que si lo son, que fue
        exactamente lo que mostro la medicion contra ARCA.
        """
        return (self.resultado is Resultado.DISCREPA
                and self.campo not in CAMPOS_AFIRMABLES)


@dataclass(frozen=True)
class Respaldo:
    """Un documento del legajo que acredita capacidad economica.

    `monto` sin `periodicidad` no sirve: un recibo de sueldo de $900.000 y un
    balance con ventas por $900.000 no acreditan lo mismo.

    Van tres fechas y cada una contesta algo distinto:

        periodo_desde/hasta   a que periodo economico corresponde el monto
        emitido               cuando se produjo el papel
        vence                 hasta cuando se lo acepta en el legajo

    La que importa para la capacidad es el periodo, y por eso existe
    `fecha_dato`, que es el equivalente al de Constatacion. Un balance del
    ejercicio 2023 reimpreso la semana pasada tiene `emitido` de hace siete
    dias y acredita un hecho economico de hace tres anios. Medir la antiguedad
    por la emision lo haria pasar por actual, que es justamente la trampa.
    """

    cliente_id: str
    tipo: str                   # el catalogo por sujeto obligado es el item 1.4
    emitido: date
    monto: float = 0.0
    periodicidad: Periodicidad = Periodicidad.UNICA
    # Periodo economico que cubre. Un recibo de agosto va del 1 al 31 de
    # agosto, un balance cubre el ejercicio, y una escritura tiene desde y
    # hasta iguales porque la venta paso un dia.
    periodo_desde: date | None = None
    periodo_hasta: date | None = None
    vence: date | None = None
    referencia: str = ""

    @property
    def fecha_dato(self) -> date:
        """A cuando corresponde el hecho economico que acredita.

        Cae en la emision solo cuando no se cargo el periodo. Es una
        aproximacion y no lo mismo: para un documento reemitido, la emision
        miente sobre la antiguedad del hecho.
        """
        return self.periodo_hasta or self.emitido

    def antiguedad_en_dias(self, al: date | None = None) -> int:
        return ((al or date.today()) - self.fecha_dato).days

    def antiguedad_en_meses(self, al: date | None = None) -> float:
        return self.antiguedad_en_dias(al) / 30.44

    @property
    def periodo_cargado(self) -> bool:
        """Si se sabe a que periodo corresponde, o si hay que suponerlo."""
        return self.periodo_hasta is not None

    def vigente(self, al: date | None = None) -> bool:
        """Un documento sin vencimiento declarado se considera vigente.

        El vencimiento por tipo de documento lo fija el catalogo del item 1.4.
        Suponerlo aca seria adelantar una regla que todavia no esta escrita.
        """
        if self.vence is None:
            return True
        return self.vence >= (al or date.today())


# ---------------------------------------------------------------------------
# El legajo
# ---------------------------------------------------------------------------

@dataclass
class LegajoCliente:
    """Las constataciones y los respaldos de un cliente.

    Se llama LegajoCliente y no Legajo porque el paquete ya se llama legajo.

    Las constataciones solo crecen. No hay metodo para borrar ni modificar: una
    correccion es una constatacion nueva que tapa a la anterior por precedencia
    o por fecha.
    """

    cliente_id: str
    _constataciones: list[Constatacion] = field(default_factory=list)
    _respaldos: list[Respaldo] = field(default_factory=list)

    # --- alta ---

    def constatar(self, constatacion: Constatacion) -> Constatacion:
        if constatacion.cliente_id != self.cliente_id:
            raise ValueError(
                f"la constatacion es de {constatacion.cliente_id} y el legajo "
                f"de {self.cliente_id}"
            )
        self._constataciones.append(constatacion)
        return constatacion

    def agregar_respaldo(self, respaldo: Respaldo) -> Respaldo:
        if respaldo.cliente_id != self.cliente_id:
            raise ValueError(
                f"el respaldo es de {respaldo.cliente_id} y el legajo "
                f"de {self.cliente_id}"
            )
        self._respaldos.append(respaldo)
        return respaldo

    # --- lectura ---

    @property
    def constataciones(self) -> tuple[Constatacion, ...]:
        """Todas, en el orden en que se registraron. Copia inmutable."""
        return tuple(self._constataciones)

    @property
    def respaldos(self) -> tuple[Respaldo, ...]:
        return tuple(self._respaldos)

    def historial(self, campo: Campo) -> tuple[Constatacion, ...]:
        return tuple(c for c in self._constataciones if c.campo is campo)

    def vigente(self, campo: Campo) -> Constatacion | None:
        """La constatacion que manda para ese campo.

        Gana el origen mas fuerte. Entre dos del mismo origen gana la mas
        reciente, que es como una correccion tapa a la anterior sin borrarla.
        """
        candidatas = self.historial(campo)
        if not candidatas:
            return None
        return min(candidatas, key=lambda c: (c.peso, -c.fecha_consulta.toordinal()))

    def cotejar(self, cliente: Cliente, campo: Campo) -> Cotejo | None:
        """Compara lo constatado contra lo declarado para un campo."""
        constatacion = self.vigente(campo)
        if constatacion is None:
            return None

        declarado = normalizar_campo(campo, getattr(cliente, campo.value, None))
        hallado = normalizar_campo(campo, constatacion.valor)

        if not declarado and hallado:
            resultado = Resultado.COMPLETA
        elif declarado == hallado:
            resultado = Resultado.COINCIDE
        else:
            resultado = Resultado.DISCREPA

        return Cotejo(campo=campo, resultado=resultado, declarado=declarado,
                      hallado=hallado, constatacion=constatacion)

    def cotejos(self, cliente: Cliente) -> list[Cotejo]:
        """Todos los campos constatados, en el orden del enum."""
        salida = []
        for campo in Campo:
            cotejo = self.cotejar(cliente, campo)
            if cotejo is not None:
                salida.append(cotejo)
        return salida

    def discrepancias(self, cliente: Cliente) -> list[Cotejo]:
        """Todo lo que difiere, afirmable o no. Para el expediente."""
        return [c for c in self.cotejos(cliente) if c.resultado is Resultado.DISCREPA]

    def hallazgos(self, cliente: Cliente) -> list[Cotejo]:
        """Las diferencias que el programa puede afirmar."""
        return [c for c in self.cotejos(cliente) if c.es_hallazgo]

    def para_revisar(self, cliente: Cliente) -> list[Cotejo]:
        """Las diferencias de texto libre, que las lee una persona."""
        return [c for c in self.cotejos(cliente) if c.requiere_lectura]

    def completados(self, cliente: Cliente) -> list[Cotejo]:
        return [c for c in self.cotejos(cliente) if c.resultado is Resultado.COMPLETA]

    def respaldos_vigentes(self, al: date | None = None) -> tuple[Respaldo, ...]:
        return tuple(r for r in self._respaldos if r.vigente(al))

    def __len__(self) -> int:
        return len(self._constataciones)


class RegistroLegajos:
    """Los legajos de todos los clientes, indexados por cliente.

    Misma forma que RegistroPEP y que las demas tablas laterales del circuito.
    """

    def __init__(self, legajos: list[LegajoCliente] | None = None) -> None:
        self._por_cliente: dict[str, LegajoCliente] = {
            l.cliente_id: l for l in (legajos or [])
        }

    def de(self, cliente_id: str) -> LegajoCliente:
        """Devuelve el legajo, y si no existe lo crea vacio.

        Un cliente sin legajo no es un error: es un cliente al que todavia no
        se le constato nada. Devolver None obligaria a preguntar en cada punto
        del codigo.
        """
        if cliente_id not in self._por_cliente:
            self._por_cliente[cliente_id] = LegajoCliente(cliente_id)
        return self._por_cliente[cliente_id]

    def existentes(self) -> tuple[LegajoCliente, ...]:
        return tuple(self._por_cliente.values())

    def __len__(self) -> int:
        return len(self._por_cliente)
