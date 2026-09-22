"""Capacidad economica documentada. Item 3.1.

Cuanto puede probar el cliente que gana o que tiene, a partir de los papeles
que hay en su legajo. Es la mitad de la pregunta central del proyecto, y la
otra mitad (compararla contra lo que opera) es el item 3.2.

LA CAPACIDAD NO ES UN NUMERO, SON DOS

    capacidad_anual     flujo recurrente documentado, en pesos por anio
    respaldo_puntual    disponibilidad documentada de una sola vez, total

Van separadas porque la comparacion contra lo operado es distinta para cada
una. El flujo anual explica un nivel sostenido de operatoria. La venta de un
inmueble explica el pico de un mes y no el nivel de todo el anio. Con una sola
cifra, esa venta o infla la capacidad anual para siempre o no explica nada.

NINGUN RESPALDO ENTRA SIN PASAR POR TRES PREGUNTAS

1. De quien es. Un balance acredita a la sociedad y no a la persona que la
   integra. Las ventas de una SAS no son ingreso de su socio: para eso hace
   falta el documento de distribucion de utilidades o de retiro.

2. Flujo o stock. Lo decide la periodicidad del respaldo. `factor_anual`
   devuelve None para los de unica vez, y esos van a `respaldo_puntual`.

3. Que acredita. Un estatuto prueba quien es la sociedad, no cuanto factura.
   El catalogo de documentos ya marca cuales acreditan capacidad.

NO HAY COEFICIENTES DE CONFIABILIDAD

Se penso en multiplicar cada monto por un coeficiente segun quien emite el
documento, y se descarto: esos numeros serian inventados. Ninguna norma dice
que una certificacion de contador valga 0,7. Ademas un coeficiente no arregla
el problema de titularidad, que es el grave: multiplicar el balance de la SAS
por 0,5 sigue dando plata que el socio no tiene.

En su lugar, la confiabilidad viaja con la cifra. `derivado_de_declarado` dice
cuanto del flujo se apoya en documentos que un tercero firma sobre lo que le
conto el cliente. Se muestra, no se multiplica.

NO SE CORTA POR ANTIGUEDAD

Se computa todo y cada respaldo expone su fecha. Cortar en, por ejemplo, doce
meses inventaria el umbral exacto que el proyecto viene evitando, y ademas
esconderia el problema: un cliente con capacidad apoyada entera en papeles de
hace tres anios no es lo mismo que uno sin documentacion, y con un corte los
dos quedan en cero. Asi el analista ve la diferencia.

=============================================================================
PREGUNTA ABIERTA, para el item 3.2

Cuando la regla compare `capacidad_anual` contra lo operado, hay que decidir
si un respaldo de 2019 pesa igual que uno de este mes para esa comparacion
puntual. Hoy pesan igual, porque este modulo no corta por antiguedad.

Si al escribir 3.2 hace falta ponderar o cortar, tiene que ser una politica
explicita y marcada, con el mismo criterio que se uso para el balance: nunca
un supuesto escondido adentro del calculo. `Capacidad` ya expone
`antiguedad_maxima_en_meses` y la fecha de cada computo para que esa regla
tenga con que decidir sin tener que recalcular nada.
=============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum

from . import documentos
from .documentos import TipoDocumento
from .modelo import Cliente
from .procedencia import LegajoCliente, Respaldo


class MotivoNoComputa(str, Enum):
    """Por que un respaldo del legajo no suma a la capacidad del cliente."""

    # Acredita a un tercero, tipicamente una sociedad que el cliente integra.
    DE_UN_TERCERO = "DE_UN_TERCERO"
    # Prueba algo real, pero no capacidad economica.
    NO_ACREDITA_CAPACIDAD = "NO_ACREDITA_CAPACIDAD"
    SIN_MONTO = "SIN_MONTO"
    # El tipo no esta en el catalogo, asi que no se sabe que acredita.
    FUERA_DEL_CATALOGO = "FUERA_DEL_CATALOGO"


@dataclass(frozen=True)
class Computo:
    """Un respaldo que si suma, con cuanto y de que forma."""

    respaldo: Respaldo
    aporte_anual: float = 0.0       # cero si es de unica vez
    aporte_puntual: float = 0.0     # cero si es flujo
    derivado_de_declarado: bool = False

    @property
    def es_flujo(self) -> bool:
        return self.aporte_anual > 0

    @property
    def fecha_dato(self) -> date:
        return self.respaldo.fecha_dato

    def antiguedad_en_meses(self, al: date | None = None) -> float:
        return self.respaldo.antiguedad_en_meses(al)


@dataclass(frozen=True)
class Descarte:
    """Un respaldo que no suma, con el motivo escrito para el analista.

    `mensaje` no dice solo que no computa. Cuando el documento acredita algo
    real, lo dice primero: un balance prueba que la sociedad existe y opero por
    ese monto, aunque no sirva para la capacidad de su socio. Descartar en
    silencio le haria creer al analista que el papel no vale nada.
    """

    respaldo: Respaldo
    motivo: MotivoNoComputa
    mensaje: str


@dataclass(frozen=True)
class Capacidad:
    """Lo que el cliente puede probar, en dos cifras."""

    cliente_id: str
    capacidad_anual: float = 0.0
    respaldo_puntual: float = 0.0
    computados: tuple[Computo, ...] = ()
    descartados: tuple[Descarte, ...] = ()

    @property
    def documentada(self) -> bool:
        return bool(self.computados)

    @property
    def derivado_de_declarado(self) -> float:
        """Cuanto del flujo anual sale de documentos que firma un tercero
        sobre lo que le conto el cliente."""
        return round(sum(c.aporte_anual for c in self.computados
                         if c.derivado_de_declarado), 2)

    @property
    def proporcion_derivada(self) -> float:
        """Fraccion del flujo anual apoyada en ese tipo de documento.

        Es el segundo hallazgo que puede dar el item 3.2: una cosa es exceder
        la capacidad documentada, y otra distinta es que esa capacidad se
        apoye casi entera en papeles que no se pueden cruzar contra un
        tercero.
        """
        if not self.capacidad_anual:
            return 0.0
        return round(self.derivado_de_declarado / self.capacidad_anual, 4)

    def antiguedad_maxima_en_meses(self, al: date | None = None) -> float | None:
        """La del computo mas viejo. None cuando no hay ninguno."""
        if not self.computados:
            return None
        return round(max(c.antiguedad_en_meses(al) for c in self.computados), 1)

    def composicion(self, al: date | None = None) -> list[dict]:
        """Cada computo con su fecha, para el informe y el visor.

        La antiguedad se expone en vez de aplicarse. Quien quiera cortar por
        fecha tiene el dato, y el corte queda a la vista en vez de estar
        metido adentro de la suma.
        """
        return [
            {
                "tipo": c.respaldo.tipo,
                "fecha_dato": c.fecha_dato.isoformat(),
                "periodo_cargado": c.respaldo.periodo_cargado,
                "antiguedad_meses": round(c.antiguedad_en_meses(al), 1),
                "aporte_anual": round(c.aporte_anual, 2),
                "aporte_puntual": round(c.aporte_puntual, 2),
                "derivado_de_declarado": c.derivado_de_declarado,
                "referencia": c.respaldo.referencia,
            }
            for c in sorted(self.computados, key=lambda c: c.fecha_dato, reverse=True)
        ]


# ---------------------------------------------------------------------------
# Mensajes
# ---------------------------------------------------------------------------

def _mensaje_de_tercero(respaldo: Respaldo, cliente: Cliente) -> str:
    """El mensaje de dos partes.

    Primero lo que el documento si acredita, porque es un dato verificado y
    descartarlo en silencio le haria creer al analista que el papel no sirve
    para nada. Despues por que no alcanza para lo que se esta midiendo.
    """
    quien = respaldo.referencia or "la sociedad"
    ficha = documentos.ficha(respaldo.tipo)
    que_es = ficha.descripcion.lower() if ficha else "el documento"

    acredita = (
        f"El documento acredita que {quien} existe y opero por "
        f"${respaldo.monto:,.0f}"
    )
    if respaldo.periodo_cargado:
        acredita += f" en el periodo cerrado el {respaldo.fecha_dato.isoformat()}"
    acredita += f". Es {que_es} y vale para la capacidad de esa sociedad."

    no_acredita = (
        "No acredita capacidad personal de este cliente: lo que factura una "
        "sociedad no es ingreso de quien la integra. Para computarlo hace "
        "falta el documento de distribucion de utilidades o de retiro."
    )
    return acredita + " " + no_acredita


# ---------------------------------------------------------------------------
# Calculo
# ---------------------------------------------------------------------------

def _es_de_un_tercero(tipo: TipoDocumento, cliente: Cliente) -> bool:
    """Si el documento acredita a alguien que no es este cliente.

    Se deduce del catalogo: un documento que solo aplica a personas juridicas,
    guardado en el legajo de una persona humana, es de una sociedad que el
    cliente integra. Y al reves.
    """
    ficha = documentos.ficha(tipo)
    if ficha is None or ficha.aplica_a == "AMBOS":
        return False
    del_cliente = "PERSONA" if cliente.tipo.strip().upper() == "PERSONA" else "ENTIDAD"
    return ficha.aplica_a != del_cliente


def _clasificar(respaldo: Respaldo, cliente: Cliente) -> Computo | Descarte:
    try:
        tipo = TipoDocumento(respaldo.tipo.strip().upper())
    except ValueError:
        return Descarte(
            respaldo, MotivoNoComputa.FUERA_DEL_CATALOGO,
            f"El tipo {respaldo.tipo!r} no esta en el catalogo de documentos, "
            f"asi que no se sabe que acredita. No computa hasta que se lo "
            f"agregue.",
        )

    ficha = documentos.ficha(tipo)

    if _es_de_un_tercero(tipo, cliente):
        return Descarte(respaldo, MotivoNoComputa.DE_UN_TERCERO,
                        _mensaje_de_tercero(respaldo, cliente))

    if not ficha.acredita_capacidad:
        return Descarte(
            respaldo, MotivoNoComputa.NO_ACREDITA_CAPACIDAD,
            f"{ficha.descripcion} acredita un dato del legajo, no capacidad "
            f"economica. No suma ni resta.",
        )

    if respaldo.monto <= 0:
        return Descarte(
            respaldo, MotivoNoComputa.SIN_MONTO,
            f"{ficha.descripcion} sin monto cargado. El documento puede estar "
            f"bien y faltar el dato: no computa, pero tampoco es un hallazgo.",
        )

    # El factor decide si es flujo o disponibilidad de una vez. Los de unica
    # vez devuelven None y no 1: la venta de un inmueble no es ingreso anual.
    factor = respaldo.periodicidad.factor_anual
    derivado = bool(ficha.derivado_de_declarado)

    if factor is None:
        return Computo(respaldo, aporte_puntual=respaldo.monto,
                       derivado_de_declarado=derivado)
    return Computo(respaldo, aporte_anual=respaldo.monto * factor,
                   derivado_de_declarado=derivado)


def calcular(cliente: Cliente, legajo: LegajoCliente | None) -> Capacidad:
    """Capacidad documentada de un cliente, a partir de su legajo.

    Se computa todo lo que hay, sin cortar por antiguedad. Cada computo lleva
    su fecha para que quien compare contra lo operado decida con el dato a la
    vista.
    """
    if legajo is None:
        return Capacidad(cliente_id=cliente.cliente_id)

    computados: list[Computo] = []
    descartados: list[Descarte] = []
    for respaldo in legajo.respaldos:
        resultado = _clasificar(respaldo, cliente)
        (computados if isinstance(resultado, Computo) else descartados).append(resultado)

    return Capacidad(
        cliente_id=cliente.cliente_id,
        capacidad_anual=round(sum(c.aporte_anual for c in computados), 2),
        respaldo_puntual=round(sum(c.aporte_puntual for c in computados), 2),
        computados=tuple(computados),
        descartados=tuple(descartados),
    )
