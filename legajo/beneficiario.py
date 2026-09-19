"""Resolucion de beneficiario final.

El algoritmo recorre todos los caminos de titularidad desde la entidad hacia
arriba, multiplicando porcentajes, y recien al final aplica el umbral.

Ese orden no es un detalle de implementacion: es la diferencia entre resolver
bien y perder beneficiarios. Dos errores clasicos que este codigo evita:

1. Podar aristas por debajo del umbral durante el recorrido.
   Juan con 15% de A, A con 40% de X, mas 8% directo de Juan sobre X, suma
   14% y es beneficiario final. Si se descarta la arista del 8% por estar
   bajo el 10%, desaparece.

2. Usar un conjunto de visitados global para cortar ciclos.
   Juan con 50% de A y 50% de B, ambas con 30% de X, suma 30%. Con visitados
   global, Juan se cuenta una vez y da 15%. La deteccion de ciclos tiene que
   ser sobre el camino actual, no sobre el recorrido completo.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .societaria import Estructura

UMBRAL_BENEFICIARIO = 0.10  # Res. UIF 112/2021
PROFUNDIDAD_MAXIMA = 15


@dataclass(frozen=True)
class Beneficiario:
    """Una persona humana identificada como beneficiario final.

    Un unico tipo de salida para las tres vias de identificacion: cadena de
    participacion, control por otros medios, y supletorio. Aguas abajo nadie
    tiene que distinguir de cual vino.
    """

    persona_id: str
    nombre: str
    capital: float          # fraccion efectiva acumulada [0, 1]
    voto: float             # fraccion efectiva acumulada [0, 1]
    via: str                # PARTICIPACION | CONTROL | SUPLETORIO
    detalle: str = ""       # cadena descripta, o motivo del control

    @property
    def porcentaje_rector(self) -> float:
        """El mayor entre capital y voto: cualquiera de los dos califica."""
        return max(self.capital, self.voto)


@dataclass
class Resolucion:
    """Resultado del analisis de titularidad de una entidad."""

    entidad_id: str
    beneficiarios: list[Beneficiario] = field(default_factory=list)
    participes_menores: list[Beneficiario] = field(default_factory=list)
    ciclos: list[tuple[str, ...]] = field(default_factory=list)
    titularidad_opaca: float = 0.0
    profundidad_maxima: int = 0
    observaciones: list[str] = field(default_factory=list)

    @property
    def identificado(self) -> bool:
        return bool(self.beneficiarios)

    @property
    def niveles_de_capas(self) -> int:
        return self.profundidad_maxima


def _recorrer(
    estructura: Estructura,
    entidad_id: str,
    factor_capital: float,
    factor_voto: float,
    camino: tuple[str, ...],
    acumulado: dict[str, list[float]],
    cadenas: dict[str, list[str]],
    resolucion: Resolucion,
) -> None:
    """Recorre hacia arriba sumando la titularidad efectiva.

    `camino` es la rama actual, no el recorrido global: eso permite que una
    misma persona sea alcanzada por varias ramas y que sus tenencias sumen,
    y a la vez corta los ciclos.
    """
    profundidad = len(camino)
    resolucion.profundidad_maxima = max(resolucion.profundidad_maxima, profundidad)

    if profundidad >= PROFUNDIDAD_MAXIMA:
        resolucion.observaciones.append(
            f"cadena truncada en {PROFUNDIDAD_MAXIMA} niveles desde {entidad_id}"
        )
        return

    socios = estructura.socios_de(entidad_id)

    # Capital no declarado en este nivel: opacidad, ponderada por el peso
    # con que este nivel llega a la entidad raiz.
    faltante = 1.0 - sum(p.capital for p in socios)
    if faltante > 1e-9:
        resolucion.titularidad_opaca += faltante * factor_capital

    for p in socios:
        if p.propietario in camino or p.propietario == entidad_id:
            ciclo = camino[camino.index(p.propietario):] if p.propietario in camino else (entidad_id,)
            resolucion.ciclos.append(ciclo + (entidad_id,))
            # La titularidad que entra en un ciclo nunca alcanza una persona
            # humana. A efectos de cumplimiento eso es exactamente lo mismo
            # que capital no declarado: esa fraccion no tiene beneficiario
            # final identificable, y tiene que figurar como tal.
            resolucion.titularidad_opaca += factor_capital * p.capital
            continue

        nuevo_capital = factor_capital * p.capital
        nuevo_voto = factor_voto * p.votos

        if estructura.es_persona(p.propietario):
            registro = acumulado.setdefault(p.propietario, [0.0, 0.0])
            registro[0] += nuevo_capital
            registro[1] += nuevo_voto
            tramo = " -> ".join(
                estructura.nombre(n) for n in (*camino, entidad_id)
            )
            cadenas.setdefault(p.propietario, []).append(
                f"{nuevo_capital:.2%} via {tramo}" if camino else f"{nuevo_capital:.2%} directo"
            )
            continue

        _recorrer(
            estructura,
            p.propietario,
            nuevo_capital,
            nuevo_voto,
            (*camino, entidad_id),
            acumulado,
            cadenas,
            resolucion,
        )


def resolver(
    estructura: Estructura,
    entidad_id: str,
    umbral: float = UMBRAL_BENEFICIARIO,
) -> Resolucion:
    """Identifica los beneficiarios finales de una entidad.

    Orden de las tres vias, segun la resolucion:
      1. Participacion acumulada por encima del umbral.
      2. Control final por otros medios, sin importar porcentaje.
      3. Supletorio: quien administra o representa, solo si 1 y 2 no dieron
         resultado, y dejando constancia de la causa.
    """
    resolucion = Resolucion(entidad_id=entidad_id)

    if estructura.es_persona(entidad_id):
        resolucion.observaciones.append(
            "el titular es una persona humana: no corresponde cadena de titularidad"
        )
        return resolucion

    acumulado: dict[str, list[float]] = {}
    cadenas: dict[str, list[str]] = {}

    _recorrer(estructura, entidad_id, 1.0, 1.0, (), acumulado, cadenas, resolucion)

    # El umbral se aplica ahora, sobre la suma de todos los caminos.
    for persona_id, (capital, voto) in acumulado.items():
        beneficiario = Beneficiario(
            persona_id=persona_id,
            nombre=estructura.nombre(persona_id),
            capital=round(capital, 6),
            voto=round(voto, 6),
            via="PARTICIPACION",
            detalle=" | ".join(cadenas.get(persona_id, [])),
        )
        if max(capital, voto) >= umbral - 1e-9:
            resolucion.beneficiarios.append(beneficiario)
        else:
            resolucion.participes_menores.append(beneficiario)

    # Control por otros medios: califica sin porcentaje.
    ya_listados = {b.persona_id for b in resolucion.beneficiarios}
    for c in estructura.controlantes_de(entidad_id):
        if c.persona in ya_listados:
            continue
        previo = acumulado.get(c.persona, [0.0, 0.0])
        resolucion.beneficiarios.append(
            Beneficiario(
                persona_id=c.persona,
                nombre=estructura.nombre(c.persona),
                capital=round(previo[0], 6),
                voto=round(previo[1], 6),
                via="CONTROL",
                detalle=c.motivo,
            )
        )
        ya_listados.add(c.persona)

    # Supletorio: ultimo recurso, con la causa registrada.
    if not resolucion.beneficiarios:
        administradores = estructura.administradores_de(entidad_id)
        causa = (
            f"titularidad no identificada en {resolucion.titularidad_opaca:.2%} del capital"
            if resolucion.titularidad_opaca > 1e-9
            else "ningun titular alcanza el umbral y no hay control declarado"
        )
        for a in administradores:
            resolucion.beneficiarios.append(
                Beneficiario(
                    persona_id=a.persona,
                    nombre=estructura.nombre(a.persona),
                    capital=0.0,
                    voto=0.0,
                    via="SUPLETORIO",
                    detalle=f"{a.cargo}; causa: {causa}",
                )
            )
        if not administradores:
            resolucion.observaciones.append(
                "sin beneficiario final identificable y sin administrador declarado"
            )

    if resolucion.ciclos:
        resolucion.observaciones.append(
            f"{len(resolucion.ciclos)} participacion(es) circular(es) detectada(s)"
        )
    if resolucion.titularidad_opaca > 1e-9:
        resolucion.observaciones.append(
            f"titularidad no identificada: {resolucion.titularidad_opaca:.2%} del capital"
        )

    resolucion.beneficiarios.sort(key=lambda b: b.porcentaje_rector, reverse=True)
    resolucion.participes_menores.sort(key=lambda b: b.porcentaje_rector, reverse=True)
    return resolucion
