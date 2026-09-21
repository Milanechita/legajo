"""Tipo de sujeto obligado, como parametro.

El mismo circuito corre para un banco y para una ALYC, pero no les aplica la
misma resolucion, ni los mismos umbrales, ni los mismos documentos. Poner eso
como parametro evita la cadena de `if` que se pudre y que despues nadie toca.

Lo que esta escrito aca es lo que se pudo verificar. Lo que no, figura como
pendiente y el programa lo dice en voz alta en vez de suponerlo. Un catalogo
de documentos a medias que se comporta como completo es peor que no tener
catalogo: marca faltante lo que nadie tenia que pedir, y deja pasar lo que si.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum

from .config import UMBRALES, UmbralesSMVM


class TipoSujetoObligado(str, Enum):
    BANCO = "BANCO"
    ALYC = "ALYC"


class Exigibilidad(str, Enum):
    """Que puede hacer el sujeto obligado con un documento."""

    EXIGIBLE = "EXIGIBLE"
    OPCIONAL = "OPCIONAL"
    # Prohibido requerirlo. No es lo mismo que no exigirlo: un documento
    # prohibido nunca puede figurar como faltante en el legajo, y pedirlo es
    # el incumplimiento.
    PROHIBIDO = "PROHIBIDO"
    # Todavia no se verifico contra la norma. El programa no afirma nada.
    SIN_VERIFICAR = "SIN_VERIFICAR"


@dataclass(frozen=True)
class SujetoObligado:
    """Marco normativo bajo el que corre el analisis."""

    tipo: TipoSujetoObligado
    resolucion: str
    vigencia_consultada: date
    umbrales: UmbralesSMVM = UMBRALES
    # El catalogo completo es el item 1.4. Aca solo van las reglas de
    # documentos que ya estan verificadas contra la norma.
    documentos: dict[str, Exigibilidad] = field(default_factory=dict)
    catalogo_completo: bool = False
    nota: str = ""

    def exigibilidad(self, documento: str) -> Exigibilidad:
        """Que se puede hacer con ese documento.

        Un documento que no esta en el catalogo devuelve SIN_VERIFICAR, no
        OPCIONAL. La diferencia importa: SIN_VERIFICAR le dice al analista que
        vaya a la norma, y OPCIONAL le diria que ya se miro y no hace falta.
        """
        return self.documentos.get(documento.strip().upper(),
                                   Exigibilidad.SIN_VERIFICAR)

    def puede_requerir(self, documento: str) -> bool:
        """Falso solo cuando la norma lo prohibe expresamente."""
        return self.exigibilidad(documento) is not Exigibilidad.PROHIBIDO

    def prohibidos(self) -> tuple[str, ...]:
        return tuple(sorted(d for d, e in self.documentos.items()
                            if e is Exigibilidad.PROHIBIDO))

    def exigibles(self) -> tuple[str, ...]:
        return tuple(sorted(d for d, e in self.documentos.items()
                            if e is Exigibilidad.EXIGIBLE))


# ---------------------------------------------------------------------------
# Los sujetos obligados que el programa conoce.
#
# Cada entrada lleva la fecha en que se consulto la norma. Si esa fecha esta
# vieja, los umbrales y los documentos pueden estar mal y el programa no avisa.
# ---------------------------------------------------------------------------

BANCO = SujetoObligado(
    tipo=TipoSujetoObligado.BANCO,
    resolucion="Res. UIF 14/2023",
    vigencia_consultada=date(2026, 9, 21),
    umbrales=UMBRALES,
    documentos={
        # La Res. UIF 78/2025 sustituyo el art. 37 de la Res. 14/2023 y
        # prohibio requerir declaraciones juradas impositivas a las entidades
        # financieras. Nunca puede figurar como documentacion faltante.
        "DDJJ_IMPOSITIVA": Exigibilidad.PROHIBIDO,
    },
    catalogo_completo=False,
    nota="Catalogo parcial. Solo esta cargada la prohibicion del art. 37 "
         "segun Res. 78/2025. El resto es el item 1.4.",
)

ALYC = SujetoObligado(
    tipo=TipoSujetoObligado.ALYC,
    resolucion="Res. UIF 78/2023",
    vigencia_consultada=date(2026, 9, 21),
    umbrales=UMBRALES,
    documentos={},
    catalogo_completo=False,
    nota="Sin catalogo. El texto vigente de la Res. 78/2023 sobre DDJJ "
         "impositivas todavia no se verifico, asi que el programa no afirma "
         "que un documento sea exigible ni prohibido para una ALYC.",
)

POR_TIPO: dict[TipoSujetoObligado, SujetoObligado] = {
    TipoSujetoObligado.BANCO: BANCO,
    TipoSujetoObligado.ALYC: ALYC,
}

# Por defecto se analiza como banco. Es el caso principal del proyecto y el
# unico con umbrales verificados contra su resolucion.
POR_DEFECTO = BANCO


def de(tipo: str | TipoSujetoObligado) -> SujetoObligado:
    """Devuelve el sujeto obligado por nombre, o falla con los validos.

    No cae en un valor por defecto en silencio: correr un analisis de ALYC
    bajo los umbrales de un banco da resultados que parecen correctos y no lo
    son.
    """
    if isinstance(tipo, SujetoObligado):
        return tipo
    clave = str(getattr(tipo, "value", tipo)).strip().upper()
    try:
        return POR_TIPO[TipoSujetoObligado(clave)]
    except (KeyError, ValueError):
        validos = ", ".join(t.value for t in TipoSujetoObligado)
        raise ValueError(f"sujeto obligado desconocido: {tipo!r}. Validos: {validos}")
