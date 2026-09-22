"""Tipo de sujeto obligado, como parametro.

El mismo circuito corre para un banco y para una ALYC, pero no les aplica la
misma resolucion, ni los mismos umbrales, ni los mismos documentos. Poner eso
como parametro evita la cadena de `if` que se pudre y que despues nadie toca.

El caso que obliga a separarlos de verdad son las declaraciones juradas
impositivas. Para un banco estan PROHIBIDAS: la Res. UIF 78/2025 sustituyo el
art. 37 de la Res. 14/2023 y no permite requerirlas. Para una ALYC son
EXIGIBLES: el art. 33 de la Res. UIF 78/2023 arma el perfil transaccional con
documentacion de la situacion economica, patrimonial, financiera y tributaria.

Son respuestas opuestas para el mismo documento. Asumir la regla del banco
para los dos casos deja a la ALYC sin pedir documentacion que la norma le
manda pedir, y aplicar la de la ALYC al banco lo hace incumplir. Hay una
prueba que exige que las dos respuestas sigan siendo opuestas.

Lo que no se verifico figura como SIN_VERIFICAR y el programa lo dice en voz
alta en vez de suponerlo. Un catalogo a medias que se comporta como completo
es peor que no tener catalogo: marca faltante lo que nadie tenia que pedir, y
deja pasar lo que si.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum

from .config import UMBRALES, UmbralesSMVM
from .documentos import CATALOGO, Materia, TipoDocumento, materia_de


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
class Regla:
    """Una regla documental con la norma que la respalda.

    La norma va pegada a la regla y no en un comentario suelto: cuando alguien
    discuta por que el programa pide o no pide un documento, la respuesta
    tiene que salir del mismo lugar que la decision.
    """

    exigibilidad: Exigibilidad
    norma: str
    nota: str = ""


@dataclass(frozen=True)
class SujetoObligado:
    """Marco normativo bajo el que corre el analisis."""

    tipo: TipoSujetoObligado
    resolucion: str
    vigencia_consultada: date
    umbrales: UmbralesSMVM = UMBRALES
    # La exigibilidad se declara por materia cuando la norma habla de materias,
    # y por documento cuando habla de documentos puntuales. La regla del
    # documento le gana a la de su materia.
    por_materia: dict[Materia, Regla] = field(default_factory=dict)
    por_documento: dict[TipoDocumento, Regla] = field(default_factory=dict)
    catalogo_completo: bool = False
    nota: str = ""

    # --- consulta ---

    def regla(self, documento: TipoDocumento | str) -> Regla:
        """La regla que aplica a un documento, con su norma.

        Un documento que no esta en ningun lado devuelve SIN_VERIFICAR, no
        OPCIONAL. La diferencia importa: SIN_VERIFICAR le dice al analista que
        vaya a la norma, y OPCIONAL le diria que ya se miro y no hace falta.
        """
        try:
            tipo = TipoDocumento(str(getattr(documento, "value", documento)))
        except ValueError:
            return Regla(Exigibilidad.SIN_VERIFICAR, "",
                         "documento que no esta en el catalogo")

        if tipo in self.por_documento:
            return self.por_documento[tipo]

        materia = materia_de(tipo)
        if materia is not None and materia in self.por_materia:
            return self.por_materia[materia]

        return Regla(Exigibilidad.SIN_VERIFICAR, "",
                     f"{self.resolucion} no se verifico para este documento")

    def exigibilidad(self, documento: TipoDocumento | str) -> Exigibilidad:
        return self.regla(documento).exigibilidad

    def puede_requerir(self, documento: TipoDocumento | str) -> bool:
        """Falso solo cuando la norma lo prohibe expresamente."""
        return self.exigibilidad(documento) is not Exigibilidad.PROHIBIDO

    def _con(self, exigibilidad: Exigibilidad,
             tipo_persona: str | None = None) -> tuple[TipoDocumento, ...]:
        from .documentos import para
        candidatos = para(tipo_persona) if tipo_persona else tuple(CATALOGO)
        return tuple(sorted(
            (t for t in candidatos if self.exigibilidad(t) is exigibilidad),
            key=lambda t: t.value,
        ))

    def exigibles(self, tipo_persona: str | None = None) -> tuple[TipoDocumento, ...]:
        return self._con(Exigibilidad.EXIGIBLE, tipo_persona)

    def prohibidos(self, tipo_persona: str | None = None) -> tuple[TipoDocumento, ...]:
        return self._con(Exigibilidad.PROHIBIDO, tipo_persona)

    def sin_verificar(self, tipo_persona: str | None = None) -> tuple[TipoDocumento, ...]:
        return self._con(Exigibilidad.SIN_VERIFICAR, tipo_persona)


# ---------------------------------------------------------------------------
# Los sujetos obligados que el programa conoce.
#
# Cada entrada lleva la fecha en que se consulto la norma. Si esa fecha esta
# vieja, los umbrales y los documentos pueden estar mal y el programa no avisa.
# ---------------------------------------------------------------------------

_CONSULTADA = date(2026, 9, 22)

_DDJJ_IMPOSITIVAS = (
    TipoDocumento.DDJJ_GANANCIAS,
    TipoDocumento.DDJJ_BIENES_PERSONALES,
    TipoDocumento.DDJJ_IVA,
)

_PROHIBIDA_EN_BANCO = Regla(
    Exigibilidad.PROHIBIDO,
    "Res. UIF 78/2025, que sustituyo el art. 37 de la Res. UIF 14/2023",
    "No se pueden requerir declaraciones juradas impositivas a entidades "
    "financieras. Nunca puede figurar como documentacion faltante.",
)

BANCO = SujetoObligado(
    tipo=TipoSujetoObligado.BANCO,
    resolucion="Res. UIF 14/2023",
    vigencia_consultada=_CONSULTADA,
    umbrales=UMBRALES,
    # La prohibicion alcanza a las declaraciones juradas y no a toda la materia
    # tributaria. Una constancia de inscripcion no es una declaracion jurada,
    # asi que queda sin verificar en vez de prohibida.
    por_documento={d: _PROHIBIDA_EN_BANCO for d in _DDJJ_IMPOSITIVAS},
    catalogo_completo=False,
    nota="Catalogo parcial. Esta cargada la prohibicion de las DDJJ "
         "impositivas. El resto de los documentos queda sin verificar.",
)

_EXIGIBLE_EN_ALYC = Regla(
    Exigibilidad.EXIGIBLE,
    "Res. UIF 78/2023 art. 33",
    "El perfil transaccional se arma con documentacion de la situacion "
    "economica, patrimonial, financiera y tributaria.",
)

ALYC = SujetoObligado(
    tipo=TipoSujetoObligado.ALYC,
    resolucion="Res. UIF 78/2023",
    vigencia_consultada=_CONSULTADA,
    umbrales=UMBRALES,
    # El art. 33 nombra materias y no documentos, asi que la exigibilidad se
    # declara por materia. Enumerar documento por documento seria inventar una
    # lista que la norma no escribe.
    por_materia={
        Materia.ECONOMICA: _EXIGIBLE_EN_ALYC,
        Materia.PATRIMONIAL: _EXIGIBLE_EN_ALYC,
        Materia.FINANCIERA: _EXIGIBLE_EN_ALYC,
        Materia.TRIBUTARIA: _EXIGIBLE_EN_ALYC,
    },
    catalogo_completo=False,
    nota="Cargado el art. 33. Identidad y societaria quedan sin verificar.",
)

POR_TIPO: dict[TipoSujetoObligado, SujetoObligado] = {
    TipoSujetoObligado.BANCO: BANCO,
    TipoSujetoObligado.ALYC: ALYC,
}

# Por defecto se analiza como banco. Es el caso principal del proyecto y el
# unico con umbrales y plazos verificados contra su resolucion.
POR_DEFECTO = BANCO


# ---------------------------------------------------------------------------
# Actualizacion del legajo.
#
# El art. 30 de la Res. UIF 78/2023 fija 1 anio en riesgo alto, 3 en medio y 5
# en bajo. Coincide con lo que el programa ya calcula para banco en
# matriz.MESES_HASTA_REVISION, asi que por ahora no hace falta separarlo por
# sujeto obligado. La prueba de abajo lo fija: si alguna de las dos cambia sin
# la otra, se entera.
# ---------------------------------------------------------------------------

MESES_ACTUALIZACION_LEGAJO = {"ALTO": 12, "MEDIO": 36, "BAJO": 60}


def de(tipo: str | TipoSujetoObligado | SujetoObligado) -> SujetoObligado:
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
