"""Congelamiento administrativo.

Cuando hay coincidencia con una persona o entidad designada, lo que sigue no
es una alerta. Es otro proceso, con otros pasos, otro reloj y una obligacion
de silencio.

    congelar sin demora e inaudita parte
    informar inmediatamente a la UIF
    reportar dentro de 24 horas
    cotejar el resto de la base de clientes
    inmovilizar lo que ingrese despues, mientras la medida siga vigente
    no informarle al cliente

Modelar esto como "una alerta mas en la cola" seria un error de fondo. Una
alerta de monitoreo se analiza, se justifica o no, y puede cerrarse sin
reportar. Un congelamiento no admite analisis previo: primero se inmoviliza y
despues se explica. "Sin demora" esta definido en la norma como ejecucion
inmediata para prevenir la fuga o disipacion de los bienes.

La obligacion de reserva tampoco es un detalle. El sujeto obligado debe
abstenerse de informar a sus clientes o a terceros los antecedentes de la
resolucion, y solo puede decir que los bienes estan congelados en virtud del
articulo 6 de la Ley 26.734. Un sistema que imprima esto en algo que el
cliente pueda ver convierte un cumplimiento en un delito de aviso.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from .regimen import Regimen

# Res. UIF 207/2025 art. 4 y Res. UIF 3/2026 art. 8.
PASOS: tuple[tuple[str, str], ...] = (
    ("COTEJAR_BASE",
     "cotejar la base de clientes e informar si hubo operaciones con la persona "
     "o entidad designada"),
    ("INMOVILIZAR",
     "inmovilizar los bienes u otros activos que sean propiedad o esten "
     "controlados, directa o indirectamente, por la designada, o cuyo "
     "destinatario o beneficiario sea"),
    ("INFORMAR_UIF",
     "informar inmediatamente a la UIF la aplicacion de la medida"),
    ("EMITIR_REPORTE",
     "emitir el reporte de operacion sospechosa sin demora alguna"),
    ("INFORMAR_RESULTADOS",
     "informar los resultados dentro de las 24 horas de notificada la "
     "resolucion, por el sistema Reporte Orden de Congelamiento"),
    ("MONITOREAR_POSTERIORES",
     "informar e inmovilizar las operaciones tentadas con posterioridad, "
     "mientras la medida siga vigente"),
    ("RESERVA",
     "abstenerse de informar al cliente o a terceros los antecedentes de la "
     "resolucion; solo puede indicarse que los bienes estan congelados en "
     "virtud del art. 6 de la Ley 26.734"),
)

NORMA_POR_REGIMEN = {
    Regimen.FT: "Res. UIF 207/2025, Decreto 918/2012, Ley 26.734 art. 6",
    Regimen.FPADM: "Res. UIF 3/2026, Ley 25.246 art. 14 inc. 12",
}


@dataclass(frozen=True)
class Paso:
    codigo: str
    descripcion: str
    cumplido: bool = False


@dataclass
class Congelamiento:
    """Obligacion de congelamiento sobre un cliente.

    Los pasos salen sin cumplir. Esta herramienta no congela nada: identifica
    la obligacion, la fecha en que nacio y que hay que hacer. Marcarlos como
    cumplidos de oficio seria documentar un cumplimiento que no ocurrio.
    """

    cliente_id: str
    cliente: str
    regimen: Regimen
    lista: str
    designado: str
    id_origen: str
    score: float
    criterio: str
    detectado: date = field(default_factory=date.today)
    pasos: tuple[Paso, ...] = field(default_factory=lambda: tuple(
        Paso(codigo, descripcion) for codigo, descripcion in PASOS
    ))

    @property
    def norma(self) -> str:
        return NORMA_POR_REGIMEN.get(self.regimen, "")

    @property
    def confidencial(self) -> bool:
        """Todo congelamiento lo es. Existe como propiedad para que el codigo
        que exporta no tenga que acordarse."""
        return True

    def resumen(self) -> str:
        return (f"{self.regimen.value} / {self.lista}: {self.designado} "
                f"(score {self.score}, {self.criterio})")


def obligaciones(
    coincidencias,
    nombres: dict[str, str],
    umbral_confirmacion: float,
    detectado: date | None = None,
) -> list[Congelamiento]:
    """Deriva las obligaciones de congelamiento de las coincidencias.

    Solo las coincidencias por encima del umbral de confirmacion generan
    obligacion. Una coincidencia debil pendiente de revision no habilita a
    inmovilizar los bienes de nadie: el congelamiento inaudita parte sobre un
    homonimo es un dano que despues hay que explicar.
    """
    from .regimen import regimen_de_coincidencia

    # La obligacion es una por cliente y por regimen, no una por asiento de
    # lista. Una persona designada en tres listas bajo el mismo comite genera
    # un congelamiento, no tres: se inmoviliza una vez y se reporta una vez.
    # Lo que si son distintos son los regimenes, porque el tipo de reporte
    # cambia: no es lo mismo un ROS de terrorismo que uno de proliferacion.
    mejores: dict[tuple[str, Regimen], Congelamiento] = {}

    for c in coincidencias:
        if c.score < umbral_confirmacion:
            continue
        reg = regimen_de_coincidencia(c.lista, c.programas)
        if reg is Regimen.LA:
            # Sin designacion de terrorismo ni proliferacion no hay
            # congelamiento administrativo, aunque la coincidencia sea firme.
            continue

        clave = (c.cliente_id, reg)
        previo = mejores.get(clave)
        if previo is not None and previo.score >= c.score:
            continue

        mejores[clave] = Congelamiento(
            cliente_id=c.cliente_id,
            cliente=nombres.get(c.cliente_id, ""),
            regimen=reg,
            lista=c.lista,
            designado=c.nombre_designado,
            id_origen=c.id_origen,
            score=c.score,
            criterio=c.criterio,
            detectado=detectado or date.today(),
        )

    return sorted(mejores.values(), key=lambda x: (x.cliente_id, x.regimen.value))
