"""Del hallazgo al reporte.

Esta etapa no emite ningun ROS. Los reportes se cargan por el sistema SRO+ de
la UIF, y ademas hay una razon de fondo para que no se emitan solos.

La Res. UIF 56/2024 define operacion sospechosa como aquella que ocasiona
sospecha de que los bienes provienen de un ilicito, o que, habiendose
identificado previamente como inusual, luego del analisis y evaluacion
realizados por el sujeto obligado, no permite justificar la inusualidad.

La inusualidad la detecta el sistema. La conversion a sospecha requiere un
analisis humano que no la justifique. Automatizar ese salto seria fabricar una
conclusion que nadie saco, y es lo primero que desarma una inspeccion.

Lo que si arma el sistema es el borrador fundado: los datos que la norma exige
y la descripcion de las inusualidades con su metodologia. Queda en blanco,
marcado como faltante, exactamente lo que decide una persona.

La segunda salida es la que se suele olvidar. Las inusualidades que se
resuelven sin reportar tambien tienen que quedar registradas con su
justificacion documentada: es lo primero que pide un inspector cuando quiere
ver como funciona el sistema de monitoreo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum

from .alertas import Alerta
from .modelo import Cliente
from .operaciones import Perfil
from .regimen import Regimen


class Resolucion(str, Enum):
    PENDIENTE = "PENDIENTE"
    REPORTAR = "REPORTAR"
    JUSTIFICADA = "JUSTIFICADA"


@dataclass(frozen=True)
class Decision:
    """Lo que el analista resolvio sobre una inusualidad.

    Las dos partes de texto no son intercambiables. `medidas` es lo que se
    hizo para averiguar: pedir documentacion, entrevistar, cruzar con otras
    fuentes. `motivo` es la conclusion fundada. Un registro con medidas y sin
    motivo muestra actividad sin decision; uno con motivo y sin medidas
    muestra una decision sin analisis detras.
    """

    alerta_id: str
    cliente_id: str
    codigo_alerta: str
    resolucion: Resolucion
    medidas: str = ""
    motivo: str = ""
    fecha: date | None = None

    @property
    def fundada(self) -> bool:
        return bool(self.medidas.strip()) and bool(self.motivo.strip())

    def faltantes(self) -> list[str]:
        falta = []
        if self.resolucion is Resolucion.PENDIENTE:
            falta.append("resolucion sin definir")
        if not self.medidas.strip():
            falta.append("medidas adoptadas")
        if not self.motivo.strip():
            falta.append("decision final motivada")
        if self.fecha is None:
            falta.append("fecha de la decision")
        return falta


@dataclass
class BorradorROS:
    """Insumo para cargar un reporte en el SRO+.

    No es un reporte. Es todo lo que el sistema puede aportar para que una
    persona lo cargue sin tener que volver a juntar los datos.
    """

    cliente: Cliente
    regimen: Regimen
    nivel_riesgo: str
    alertas: list[Alerta]
    decision: Decision
    perfil: Perfil | None = None
    beneficiarios: list = field(default_factory=list)
    coincidencias: list = field(default_factory=list)

    # --- plazo ---

    @property
    def vence(self) -> date:
        return min(a.vence for a in self.alertas)

    @property
    def fuera_de_plazo(self) -> bool:
        return any(a.vencida for a in self.alertas)

    @property
    def monto(self) -> float:
        return max((a.monto_involucrado for a in self.alertas), default=0.0)

    # --- validacion ---

    @property
    def completo(self) -> bool:
        return not self.faltantes()

    def faltantes(self) -> list[str]:
        """Lo que impide presentar el reporte.

        El sistema no puede completarlo por su cuenta: son las partes que la
        norma pone en cabeza del sujeto obligado.
        """
        falta = list(self.decision.faltantes())

        if not self.cliente.documentos:
            falta.append("identificacion del cliente sin documento")
        if self.cliente.tipo != "PERSONA" and not self.beneficiarios:
            falta.append("beneficiario final no identificado")
        if not any(a.operaciones for a in self.alertas):
            falta.append("operaciones involucradas")

        return falta

    def observaciones(self) -> list[str]:
        """Inconsistencias que no impiden presentar pero conviene resolver antes.

        La primera es la que encuentra cualquier inspeccion: un cliente que se
        reporta por una operatoria millonaria y sigue clasificado como de
        riesgo bajo. La norma prevee que el monitoreo derive en la
        actualizacion del perfil y del nivel de riesgo; si el nivel quedo
        igual, el sistema de calificacion no esta funcionando.
        """
        obs = []
        if self.nivel_riesgo == "BAJO":
            obs.append(
                "se reporta un cliente clasificado como riesgo bajo: corresponde "
                "actualizar el nivel y el perfil tras el monitoreo"
            )
        if self.perfil is None or not self.perfil.declarado:
            obs.append("el cliente no tenia perfil transaccional declarado")
        return obs

    # --- fundamento ---

    def fundamento(self) -> str:
        """Descripcion de las razones por las que se reporta.

        Se arma con lo que consta, en el orden en que un tercero lo va a leer:
        que se detecto, contra que se comparo, que se hizo, y por que no se
        justifico. La ultima parte es del analista, y si falta el texto lo
        dice en vez de rellenarla.
        """
        partes: list[str] = []

        # 1. Que se detecto
        partes.append("INUSUALIDADES DETECTADAS")
        for a in self.alertas:
            partes.append(f"  - {a.codigo}: {a.descripcion}")
            partes.append(f"    Metodologia: {a.metodologia}")

        # 2. Contra que se comparo
        if self.perfil and self.perfil.declarado:
            partes.append("")
            partes.append("PERFIL TRANSACCIONAL DECLARADO")
            partes.append(
                f"  Monto mensual esperado ${self.perfil.monto_mensual:,.0f}, "
                f"{self.perfil.operaciones_mensuales} operacion(es) mensuales, "
                f"{self.perfil.proporcion_efectivo:.0%} en efectivo."
            )
            if self.perfil.origen_fondos:
                partes.append(f"  Origen de fondos declarado: {self.perfil.origen_fondos}")
            if self.perfil.proposito:
                partes.append(f"  Proposito de la relacion: {self.perfil.proposito}")
        else:
            partes.append("")
            partes.append("PERFIL TRANSACCIONAL")
            partes.append("  El cliente no tiene perfil transaccional declarado.")

        # 3. Antecedentes de control
        if self.coincidencias:
            partes.append("")
            partes.append("COINCIDENCIAS EN LISTAS DE CONTROL")
            for c in self.coincidencias:
                partes.append(
                    f"  - {c.lista}: {c.nombre_designado} "
                    f"(score {c.score}, por {c.criterio.lower()})"
                )

        if self.beneficiarios:
            partes.append("")
            partes.append("BENEFICIARIO FINAL")
            for b in self.beneficiarios:
                partes.append(
                    f"  - {b.nombre}, {b.porcentaje_rector:.2%} ({b.via.lower()})"
                )

        partes.append("")
        partes.append(f"NIVEL DE RIESGO ASIGNADO: {self.nivel_riesgo}")

        # 4. Analisis del sujeto obligado
        partes.append("")
        partes.append("MEDIDAS ADOPTADAS")
        partes.append(f"  {self.decision.medidas.strip()}" if self.decision.medidas.strip()
                      else "  [PENDIENTE: completar las medidas adoptadas]")

        partes.append("")
        partes.append("FUNDAMENTO DE LA SOSPECHA")
        partes.append(f"  {self.decision.motivo.strip()}" if self.decision.motivo.strip()
                      else "  [PENDIENTE: la inusualidad no se justifico por los "
                           "siguientes motivos...]")

        if self.fuera_de_plazo:
            partes.append("")
            partes.append("CONSTANCIA DE DEMORA")
            partes.append(
                f"  El plazo de reporte vencio el {self.vence.isoformat()}. "
                f"La demora debe explicarse en la presentacion."
            )

        return "\n".join(partes)


@dataclass
class InusualJustificada:
    """Inusualidad analizada que no derivo en reporte.

    Este registro es obligatorio. La norma exige llevar constancia de las
    operaciones inusuales que, luego del analisis documentado, no fueron
    determinadas como sospechosas. Sin el, el sistema de monitoreo no se puede
    auditar: no hay forma de distinguir una alerta bien resuelta de una alerta
    que nadie miro.
    """

    cliente_id: str
    cliente: str
    alerta: Alerta
    decision: Decision
    nivel_riesgo: str = ""

    @property
    def documentada(self) -> bool:
        return self.decision.fundada


@dataclass
class Resultado:
    borradores: list[BorradorROS] = field(default_factory=list)
    justificadas: list[InusualJustificada] = field(default_factory=list)
    pendientes: list[tuple[str, Alerta]] = field(default_factory=list)

    @property
    def presentables(self) -> list[BorradorROS]:
        return [b for b in self.borradores if b.completo]

    @property
    def incompletos(self) -> list[BorradorROS]:
        return [b for b in self.borradores if not b.completo]

    @property
    def sin_documentar(self) -> list[InusualJustificada]:
        """Justificadas sin analisis documentado. Es un hallazgo de auditoria."""
        return [j for j in self.justificadas if not j.documentada]


def armar(
    alertas_por_cliente: dict[str, list[Alerta]],
    decisiones: dict[str, Decision],
    clientes: dict[str, Cliente],
    evaluaciones: dict,
    perfiles: dict[str, Perfil],
    resoluciones: dict,
    coincidencias_por_cliente: dict,
) -> Resultado:
    """Separa las inusualidades segun lo que el analista resolvio.

    Las que se reportan se agrupan por cliente y regimen: un ROS cubre la
    operatoria del cliente bajo un regimen, no una alerta por reporte.
    """
    resultado = Resultado()
    agrupadas: dict[tuple[str, Regimen], list[Alerta]] = {}
    decision_del_grupo: dict[tuple[str, Regimen], Decision] = {}

    for cliente_id, alertas in alertas_por_cliente.items():
        for a in alertas:
            decision = decisiones.get(a.identificador)

            if decision is None or decision.resolucion is Resolucion.PENDIENTE:
                resultado.pendientes.append((cliente_id, a))
                continue

            if decision.resolucion is Resolucion.JUSTIFICADA:
                resultado.justificadas.append(InusualJustificada(
                    cliente_id=cliente_id,
                    cliente=clientes[cliente_id].nombre if cliente_id in clientes else "",
                    alerta=a,
                    decision=decision,
                    nivel_riesgo=(evaluaciones[cliente_id].nivel
                                  if cliente_id in evaluaciones else ""),
                ))
                continue

            clave = (cliente_id, a.regimen)
            agrupadas.setdefault(clave, []).append(a)
            # Se conserva la decision mas fundada del grupo.
            previa = decision_del_grupo.get(clave)
            if previa is None or (decision.fundada and not previa.fundada):
                decision_del_grupo[clave] = decision

    for (cliente_id, regimen), alertas in sorted(
        agrupadas.items(), key=lambda kv: (kv[0][0], kv[0][1].value)
    ):
        cliente = clientes.get(cliente_id)
        if cliente is None:
            continue
        evaluacion = evaluaciones.get(cliente_id)
        resolucion_bf = resoluciones.get(cliente_id)

        resultado.borradores.append(BorradorROS(
            cliente=cliente,
            regimen=regimen,
            nivel_riesgo=evaluacion.nivel if evaluacion else "",
            alertas=sorted(alertas, key=lambda a: -a.monto_involucrado),
            decision=decision_del_grupo[(cliente_id, regimen)],
            perfil=perfiles.get(cliente_id),
            beneficiarios=(resolucion_bf.beneficiarios if resolucion_bf else []),
            coincidencias=coincidencias_por_cliente.get(cliente_id, []),
        ))

    return resultado
