"""Estructura societaria: el grafo de titularidad.

Res. UIF 112/2021 define beneficiario final como la persona humana que posee
al menos el 10% del capital O de los derechos de voto, o que ejerce el control
final por otros medios.

Dos cosas que la definicion obliga a modelar y que se suelen omitir:

1. Capital y voto se acumulan por separado. Alguien con 5% de capital y 40%
   de los votos ES beneficiario final. Colapsar ambos en un solo numero
   pierde ese caso, que no es teorico: aparece cada vez que hay acciones
   preferidas sin voto.

2. El control por otros medios no tiene porcentaje. Un acuerdo de accionistas
   produce un beneficiario final igual que una tenencia del 80%.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Nodo:
    """Una persona humana o una estructura juridica.

    `jurisdiccion` y `oferta_publica` no son decorativos: la normativa cambia
    el umbral de beneficiario final segun esos dos datos. Ver beneficiario.py.
    """

    id: str
    nombre: str
    tipo: str = "PERSONA"  # PERSONA | ENTIDAD
    jurisdiccion: str = "AR"
    oferta_publica: bool = False

    @property
    def es_persona(self) -> bool:
        return self.tipo == "PERSONA"

    @property
    def del_exterior(self) -> bool:
        return self.jurisdiccion.strip().upper() not in {"AR", "ARGENTINA", ""}


@dataclass(frozen=True)
class Participacion:
    """Tenencia de `propietario` sobre `participada`. Fracciones en [0, 1]."""

    propietario: str
    participada: str
    capital: float
    voto: float | None = None  # None: los votos siguen al capital

    @property
    def votos(self) -> float:
        return self.capital if self.voto is None else self.voto


@dataclass(frozen=True)
class Control:
    """Control final por otros medios, sin porcentaje asociado.

    Acuerdos de accionistas, derecho a designar la mayoria del directorio,
    influencia dominante por via contractual.
    """

    persona: str
    entidad: str
    motivo: str


@dataclass(frozen=True)
class Administracion:
    """Quien dirige, administra o representa. Solo se usa como supletorio.

    La resolucion lo admite unicamente cuando fue imposible identificar al
    beneficiario final, y exige dejar constancia de la causa.
    """

    persona: str
    entidad: str
    cargo: str


@dataclass
class Estructura:
    """El grafo completo, con indices para recorrerlo hacia arriba."""

    nodos: dict[str, Nodo] = field(default_factory=dict)
    participaciones: list[Participacion] = field(default_factory=list)
    controles: list[Control] = field(default_factory=list)
    administraciones: list[Administracion] = field(default_factory=list)

    _por_participada: dict[str, list[Participacion]] = field(
        default_factory=dict, repr=False
    )

    def agregar_nodo(self, nodo: Nodo) -> None:
        self.nodos.setdefault(nodo.id, nodo)

    def agregar_participacion(self, p: Participacion) -> None:
        self.participaciones.append(p)
        self._por_participada.setdefault(p.participada, []).append(p)

    def agregar_control(self, c: Control) -> None:
        self.controles.append(c)

    def agregar_administracion(self, a: Administracion) -> None:
        self.administraciones.append(a)

    def socios_de(self, entidad_id: str) -> list[Participacion]:
        """Participaciones entrantes: quienes son titulares de esta entidad."""
        return self._por_participada.get(entidad_id, [])

    def controlantes_de(self, entidad_id: str) -> list[Control]:
        return [c for c in self.controles if c.entidad == entidad_id]

    def administradores_de(self, entidad_id: str) -> list[Administracion]:
        return [a for a in self.administraciones if a.entidad == entidad_id]

    def nombre(self, nodo_id: str) -> str:
        nodo = self.nodos.get(nodo_id)
        return nodo.nombre if nodo else nodo_id

    def nodo(self, nodo_id: str) -> Nodo | None:
        return self.nodos.get(nodo_id)

    def es_persona(self, nodo_id: str) -> bool:
        nodo = self.nodos.get(nodo_id)
        # Un id sin nodo declarado se trata como entidad opaca, no como
        # persona: asumir persona cerraria la cadena antes de tiempo y
        # daria por identificado un beneficiario que no lo esta.
        return bool(nodo and nodo.es_persona)

    def capital_declarado(self, entidad_id: str) -> float:
        """Suma del capital conocido de una entidad. Menos de 1.0 es opacidad."""
        return sum(p.capital for p in self.socios_de(entidad_id))
