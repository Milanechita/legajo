"""Indice invertido sobre el padron de designados.

Sin esto el screening es cuadratico: cada cliente se compara contra cada
nombre y alias del padron. Con las listas completas eso es del orden de mil
millones de comparaciones Jaro-Winkler para un padron de cincuenta mil
clientes, y no corre.

El indice tiene dos caminos, porque el matcher tiene dos caminos y mezclarlos
perderia coincidencias:

    documento  ->  diccionario exacto, O(1)
    nombre     ->  trigramas con umbral de conteo

El camino del documento no puede pasar por el indice de nombres. Un cliente
que coincide por numero de pasaporte con un designado de nombre completamente
distinto es una coincidencia valida, y un indice construido sobre nombres la
descartaria sin dejar rastro.

El filtro de nombres no es "comparte algun trigrama", que trae media lista,
sino "comparte al menos N trigramas". Dos nombres que puntuan por encima del
umbral de revision comparten muchos mas que uno; el minimo esta calibrado
contra el padron real verificando que no se pierda ninguna coincidencia que
la busqueda exhaustiva encuentre.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field

from .fuentes.base import Designado, Padron
from .modelo import Cliente
from .normalizar import normalizar

# Minimo de trigramas compartidos entre un token del cliente y un token del
# designado para considerarlo candidato.
#
# Es uno, y el numero salio de medir, no de elegirlo. Con dos el indice filtra
# mas pero pierde coincidencias que la busqueda exhaustiva encuentra: pares
# como RAHMAN contra EMRAAN comparten un solo trigrama y aun asi puntuan por
# encima del umbral, porque Jaro-Winkler y el solapamiento de trigramas miden
# cosas distintas y no hay umbral que los haga equivalentes.
#
# Entre filtrar mejor y no perder nada, en screening gana no perder nada.
MINIMO_TRIGRAMAS = 1


def minimo_trigramas(token: str) -> int:
    return MINIMO_TRIGRAMAS


def trigramas(texto: str) -> set[str]:
    """Trigramas de un nombre normalizado, con relleno en los bordes.

    El relleno hace que el principio y el final del nombre generen sus
    propios trigramas, que es donde esta la informacion mas discriminante.
    """
    if not texto:
        return set()
    acolchado = f"  {texto} "
    return {acolchado[i:i + 3] for i in range(len(acolchado) - 2)}


@dataclass
class Indice:
    """Indice invertido de un padron.

    Se construye una vez y se consulta por cliente. El costo de construccion
    es lineal sobre el padron, y se amortiza en la primera decena de
    clientes.
    """

    padron: Padron
    _por_trigrama: dict[str, list[int]] = field(default_factory=lambda: defaultdict(list),
                                                repr=False)
    _por_documento: dict[str, list[int]] = field(default_factory=lambda: defaultdict(list),
                                                 repr=False)

    def __post_init__(self) -> None:
        for posicion, designado in enumerate(self.padron.designados):
            for documento in designado.documentos:
                self._por_documento[documento].append(posicion)

            # Se indexa por trigramas DE CADA TOKEN, no de la cadena entera.
            #
            # El matcher compara token contra token con Jaro-Winkler. Un
            # indice sobre la cadena completa mide otra cosa, y en el margen
            # los dos discrepan: hay pares que puntuan por encima del umbral
            # compartiendo un solo trigrama de cadena, porque el parecido
            # esta concentrado dentro de un token y no repartido.
            #
            # Para que el indice descarte trabajo y no coincidencias, tiene
            # que reflejar la estructura del matcher.
            propios: set[str] = set()
            for nombre in designado.todos_los_nombres:
                for token in normalizar(nombre, es_entidad=designado.es_entidad).split():
                    propios |= trigramas(token)
            for g in propios:
                self._por_trigrama[g].append(posicion)

    # --- consulta ----------------------------------------------------------

    def candidatos(self, cliente: Cliente) -> list[Designado]:
        """Designados que vale la pena comparar contra este cliente.

        La union de los dos caminos. El del documento entra siempre, sin
        importar el parecido del nombre.

        Para el camino de nombres alcanza con que UN token del cliente se
        parezca a algun token del designado. Exigir que se parezcan varios
        perderia el caso habitual del nombre incompleto, que es justamente el
        que el matcher esta calibrado para encontrar.
        """
        posiciones: set[int] = set()

        for documento in cliente.documentos:
            posiciones.update(self._por_documento.get(documento.clave(), ()))

        es_entidad = cliente.tipo != "PERSONA"
        for token in normalizar(cliente.nombre, es_entidad=es_entidad).split():
            minimo = minimo_trigramas(token)
            conteo: Counter[int] = Counter()
            for g in trigramas(token):
                conteo.update(self._por_trigrama.get(g, ()))
            posiciones.update(p for p, n in conteo.items() if n >= minimo)

        return [self.padron.designados[p] for p in posiciones]

    # --- diagnostico -------------------------------------------------------

    @property
    def trigramas_indexados(self) -> int:
        return len(self._por_trigrama)

    @property
    def documentos_indexados(self) -> int:
        return len(self._por_documento)

    def selectividad(self, cliente: Cliente) -> float:
        """Fraccion del padron que hay que comparar para este cliente.

        Sirve para saber si el indice esta trabajando. Cerca de 1 significa
        que no filtra nada y conviene subir el minimo de trigramas; cerca de
        0 significa que filtra bien, pero hay que verificar que no este
        filtrando de mas.
        """
        if not self.padron.designados:
            return 0.0
        return len(self.candidatos(cliente)) / len(self.padron.designados)
