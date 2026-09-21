"""Vuelca una corrida a JSON para el visor web.

Es una capa de presentacion y nada mas. No decide nada: lee lo que produjo
`circuito.correr` y lo acomoda. Si aca apareciera un umbral, un calculo de
riesgo o una regla de plazo, el visor y la planilla empezarian a discrepar, y
la que se le muestra a una inspeccion es la planilla.

Se usa `json` de la biblioteca estandar. El visor no necesita que el JSON sea
chico, necesita que sea completo: un analista que abre un caso quiere el
expediente entero, no un resumen.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any

from .circuito import Corrida
from .config import SMVM, SMVM_VIGENCIA
from .matriz import (
    JURISDICCIONES_ALTO_RIESGO, JURISDICCIONES_MONITOREO,
    JURISDICCIONES_NO_COOPERANTES, MESES_HASTA_REVISION,
)
from .paises import iso, nombre as nombre_pais

FORMATO = 1


# ---------------------------------------------------------------------------
# Serializacion
# ---------------------------------------------------------------------------

def _plano(valor: Any) -> Any:
    """Lleva cualquier valor del dominio a algo que json sepa escribir.

    El detalle de una evidencia es un diccionario libre: cada etapa mete lo
    que necesita justificar. Se recorre en profundidad en vez de enumerar
    campos, porque enumerarlos significa que una etapa nueva se exporta a
    medias y nadie se entera.
    """
    if isinstance(valor, Enum):
        return valor.value
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    if isinstance(valor, dict):
        return {str(k): _plano(v) for k, v in valor.items()}
    if isinstance(valor, (list, tuple, set, frozenset)):
        return [_plano(v) for v in valor]
    if isinstance(valor, float):
        return round(valor, 4)
    if isinstance(valor, (str, int, bool)) or valor is None:
        return valor
    return str(valor)


def _riesgo_pais(codigo: str | None) -> str:
    """Clasificacion de una jurisdiccion. Las listas viven en matriz.py."""
    if not codigo:
        return "SIN_DATO"
    if codigo in JURISDICCIONES_ALTO_RIESGO:
        return "ALTO_RIESGO"
    if codigo in JURISDICCIONES_MONITOREO:
        return "MONITOREO"
    if codigo in JURISDICCIONES_NO_COOPERANTES:
        return "NO_COOPERANTE"
    return "ORDINARIA"


# ---------------------------------------------------------------------------
# La nota
# ---------------------------------------------------------------------------

def _plural(n: int, singular: str, plural: str) -> str:
    return f"{n} {singular if n == 1 else plural}"


def nota_de(ficha: dict) -> str:
    """Redacta la nota del caso a partir de lo que ya se calculo.

    Describe, no concluye. El sistema no convierte una inusualidad en una
    sospecha: eso es criterio humano y lo dice la Res. 56/2024. Por eso la
    nota termina en lo que hay que decidir y nunca en una decision.

    Se arma aca y no en el visor porque el texto cita numeros y plazos que
    salen del dominio, y en JavaScript se volverian a redondear con otro
    criterio.
    """
    partes: list[str] = []

    tipo = "Persona humana" if ficha["tipo"] == "PERSONA" else "Persona juridica"
    riesgo = ficha["riesgo"]
    if riesgo["nivel"] == "SIN_SCORE":
        # Un caso escalado no tiene puntaje, y poner "riesgo SIN_SCORE, 0
        # puntos" haria leer como bajo riesgo lo mas grave que hay.
        partes.append(
            f"{tipo}. El caso esta escalado y no paso por scoring: una "
            "coincidencia en lista critica se escala sin ponderar, asi que no "
            "tiene puntaje ni regimen asignado."
        )
    else:
        partes.append(
            f"{tipo}. Riesgo {riesgo['nivel']} con {riesgo['puntaje']:g} puntos, "
            f"regimen {riesgo['regimen'].replace('_', ' ').lower()}, "
            f"revision cada {riesgo['revision_meses']} meses."
        )

    probables = [c for c in ficha["coincidencias"] if c["probable"]]
    if probables:
        c = probables[0]
        resto = (f" y {_plural(len(probables) - 1, 'coincidencia mas', 'coincidencias mas')}"
                 if len(probables) > 1 else "")
        partes.append(
            f"Coincidencia probable contra {c['designado']} en {c['lista']}, "
            f"score {c['score']:g} por {c['criterio'].lower()}{resto}."
        )
    elif ficha["coincidencias"]:
        partes.append(
            f"{_plural(len(ficha['coincidencias']), 'coincidencia', 'coincidencias')} "
            "por debajo del umbral de probable, para descarte manual."
        )

    if ficha["congelamiento"]:
        cong = ficha["congelamiento"]
        partes.append(
            f"Obligacion de congelamiento por regimen {cong['regimen']}, "
            f"{cong['norma']}. Se ejecuta sin demora y se reporta dentro de las "
            "24 horas. Prohibido informar al cliente."
        )

    bf = ficha["beneficiario"]
    if bf and not bf["exceptuada"]:
        if not bf["identificado"]:
            opaco = bf["opaco"]
            detalle = f", {opaco:.0%} de titularidad sin identificar" if opaco else ""
            partes.append(
                "No se pudo identificar al beneficiario final" + detalle +
                ". Es un impedimento para operar, no un dato pendiente."
            )
        else:
            cuantos = len(bf["beneficiarios"])
            nombres = ", ".join(b["nombre"] for b in bf["beneficiarios"][:3])
            resto = f" y {cuantos - 3} mas" if cuantos > 3 else ""
            verbo = "Se identifico al beneficiario final" if cuantos == 1 else \
                    f"Se identificaron {cuantos} beneficiarios finales"
            profundidad = (f", con {_plural(bf['profundidad'], 'nivel', 'niveles')} "
                           "de intermediacion" if bf["profundidad"] else "")
            partes.append(f"{verbo}{profundidad}: {nombres}{resto}.")

    if ficha["pep"]:
        pep = ficha["pep"]
        cola = " con declaracion vencida por el plazo de 2 anios" if pep["vencida"] else ""
        partes.append(f"Condicion PEP {pep['tipo'].lower()}{cola}.")

    alertas = ficha["alertas"]
    if alertas:
        vencidas = [a for a in alertas if a["vencida"]]
        monto = sum(a["monto"] for a in alertas)
        frase = (f"{_plural(len(alertas), 'alerta de monitoreo', 'alertas de monitoreo')} "
                 f"por ${monto:,.0f}")
        if vencidas:
            frase += (f", {len(vencidas)} con el plazo de reporte ya vencido. "
                      "El tope corre desde la operacion y no desde la deteccion")
        partes.append(frase + ".")

    if ficha["exposicion"]:
        partes.append(
            f"Exposicion sancionatoria estimada en ${ficha['exposicion']:,.0f}. "
            "Es una estimacion y no un calculo de multa: la fija la UIF en sumario."
        )

    pendiente = _pendiente(ficha)
    if pendiente:
        partes.append("Queda a criterio del analista: " + pendiente)

    return " ".join(partes)


def _pendiente(ficha: dict) -> str:
    """Que tiene que resolver una persona. Nunca lo resuelve el sistema."""
    faltantes: list[str] = []
    if ficha["congelamiento"]:
        faltantes.append("ejecutar el congelamiento y reportarlo")
    if any(c["probable"] for c in ficha["coincidencias"]):
        faltantes.append("confirmar o descartar la coincidencia contra la lista")
    elif ficha["coincidencias"]:
        faltantes.append("descartar las coincidencias por debajo del umbral")
    if ficha["alertas"]:
        faltantes.append("decidir si la inusualidad se convierte en sospecha")
    bf = ficha["beneficiario"]
    if bf and not bf["exceptuada"] and not bf["identificado"]:
        faltantes.append("completar la cadena de beneficiario final")
    if not faltantes:
        return ""
    return ", ".join(faltantes) + "."


# ---------------------------------------------------------------------------
# Fichas de cliente
# ---------------------------------------------------------------------------

def _ficha(corrida: Corrida, caso) -> dict:
    cliente = caso.cliente
    cid = cliente.cliente_id
    evaluacion = corrida.evaluaciones.get(cid)
    resolucion = corrida.resoluciones.get(cid)
    operatoria = corrida.operatorias.get(cid)
    perfil = corrida.perfiles.get(cid)
    congelamiento = next((c for c in corrida.congelamientos if c.cliente_id == cid), None)

    nivel = evaluacion.nivel if evaluacion else "SIN_SCORE"
    ficha: dict[str, Any] = {
        "id": cid,
        "caso_id": caso.caso_id,
        "nombre": cliente.nombre,
        "tipo": cliente.tipo,
        "documentos": [f"{d.tipo} {d.numero}" for d in cliente.documentos],
        "fecha_nacimiento": cliente.fecha_nacimiento,
        "nacionalidad": cliente.nacionalidad,
        "pais_residencia": cliente.pais_residencia,
        "pais_residencia_iso": iso(cliente.pais_residencia),
        "riesgo_pais": _riesgo_pais(iso(cliente.pais_residencia)),
        "actividad": cliente.actividad,
        "oferta_publica": cliente.oferta_publica,
        "estado": caso.estado.value,
        "escalado": caso.estado.value == "ESCALADO",
        "riesgo": {
            "puntaje": round(evaluacion.puntaje, 1) if evaluacion else 0.0,
            "nivel": nivel,
            "regimen": evaluacion.regimen if evaluacion else "",
            "revision_meses": MESES_HASTA_REVISION.get(nivel, 0),
            "factores": [
                {"codigo": f.codigo, "dimension": f.dimension,
                 "descripcion": f.descripcion, "puntos": f.puntos}
                for f in (evaluacion.factores if evaluacion else [])
            ],
            "elevadores": list(evaluacion.elevadores) if evaluacion else [],
        },
        "coincidencias": [
            {
                "lista": c.lista, "id_origen": c.id_origen,
                "designado": c.nombre_designado, "matcheado": c.nombre_matcheado,
                "score": c.score, "criterio": c.criterio,
                "probable": c.score >= corrida.politica.umbral_probable,
                "programas": list(c.programas), "atenuantes": list(c.atenuantes),
            }
            for c in corrida.coincidencias.get(cid, [])
        ],
        "congelamiento": None,
        "beneficiario": None,
        "pep": None,
        "alertas": [],
        "operatoria": None,
        "perfil": None,
        "exposicion": 0.0,
        "expediente": [
            {"momento": e.momento.isoformat(timespec="seconds"),
             "actor": e.actor, "accion": e.accion, "detalle": _plano(e.detalle)}
            for e in caso.evidencia
        ],
    }

    if congelamiento is not None:
        ficha["congelamiento"] = {
            "regimen": congelamiento.regimen.value,
            "lista": congelamiento.lista,
            "designado": congelamiento.designado,
            "score": congelamiento.score,
            "criterio": congelamiento.criterio,
            "norma": congelamiento.norma,
            "detectado": congelamiento.detectado.isoformat(),
            "pasos": [{"codigo": p.codigo, "descripcion": p.descripcion,
                       "cumplido": p.cumplido} for p in congelamiento.pasos],
        }

    if resolucion is not None:
        ficha["beneficiario"] = {
            "identificado": resolucion.identificado,
            "exceptuada": resolucion.exceptuada,
            "opaco": round(resolucion.titularidad_opaca, 4),
            "profundidad": resolucion.profundidad_maxima,
            "umbral": resolucion.umbral_aplicado,
            "beneficiarios": [
                {"id": b.persona_id, "nombre": b.nombre, "capital": round(b.capital, 4),
                 "voto": round(b.voto, 4), "via": b.via, "detalle": b.detalle}
                for b in resolucion.beneficiarios
            ],
            "menores": [
                {"id": b.persona_id, "nombre": b.nombre, "capital": round(b.capital, 4),
                 "voto": round(b.voto, 4), "via": b.via, "detalle": b.detalle}
                for b in resolucion.participes_menores
            ],
            "ciclos": [list(c) for c in resolucion.ciclos],
            "observaciones": list(resolucion.observaciones),
        }

    if corrida.registro_pep is not None:
        # `consultar` devuelve solo la condicion vigente, porque una vencida es
        # un no-PEP a los efectos del scoring. Para la ficha hacen falta las
        # dos: que una declaracion haya caducado es un dato del expediente.
        vigente = corrida.registro_pep.consultar(cid)
        caducada = next((p for p in corrida.registro_pep.vencidas()
                         if p.cliente_id == cid), None)
        declarado = vigente or caducada
        if declarado is not None:
            ficha["pep"] = {
                "tipo": declarado.tipo, "cargo": declarado.cargo,
                "por_parentesco": declarado.por_parentesco,
                "fecha_cese": declarado.fecha_cese.isoformat() if declarado.fecha_cese else None,
                "vencida": vigente is None,
            }

    for a in corrida.alertas.get(cid, []):
        ficha["alertas"].append({
            "id": a.identificador,
            "codigo": a.codigo,
            "severidad": a.severidad,
            "descripcion": a.descripcion,
            "metodologia": a.metodologia,
            "monto": round(a.monto_involucrado, 2),
            "regimen": a.regimen.value,
            "generada": a.generada.isoformat(),
            "vence": a.vence.isoformat(),
            "dias_restantes": a.dias_restantes,
            "vencida": a.vencida,
            "operaciones": [
                {"fecha": o.fecha.isoformat(), "monto": round(o.monto, 2),
                 "sentido": o.sentido, "instrumento": o.instrumento,
                 "canal": o.canal, "contraparte": o.contraparte,
                 "pais": o.pais_contraparte, "referencia": o.referencia}
                for o in a.operaciones
            ],
        })

    if operatoria is not None and operatoria.operaciones:
        ops = operatoria.operaciones
        efectivo = sum(o.monto for o in ops if o.instrumento == "EFECTIVO")
        total = sum(o.monto for o in ops)
        paises = sorted({iso(o.pais_contraparte) for o in ops if o.pais_contraparte} - {None})
        ficha["operatoria"] = {
            "cantidad": len(ops),
            "total": round(total, 2),
            "efectivo": round(efectivo, 2),
            "proporcion_efectivo": round(efectivo / total, 4) if total else 0.0,
            "desde": min(o.fecha for o in ops).isoformat(),
            "hasta": max(o.fecha for o in ops).isoformat(),
            "paises": paises,
            "contrapartes": sorted({o.contraparte for o in ops if o.contraparte}),
        }

    if perfil is not None:
        ficha["perfil"] = {
            "monto_mensual": perfil.monto_mensual,
            "operaciones_mensuales": perfil.operaciones_mensuales,
            "proporcion_efectivo": perfil.proporcion_efectivo,
            "paises": list(perfil.paises),
            "origen_fondos": perfil.origen_fondos,
            "proposito": perfil.proposito,
        }

    if corrida.exposicion is not None:
        # Solo se puede atribuir el cargo por ROS no emitido, que lleva el
        # nombre del cliente en el concepto. Los cargos por incumplimiento de
        # listados, monitoreo y beneficiario final se liquidan por materia y
        # no por cliente, asi que repartirlos aca seria inventar un numero.
        # El total sin repartir esta en la seccion de exposicion.
        ficha["exposicion"] = round(sum(
            c.monto for c in corrida.exposicion.cargos
            if c.concepto.endswith(", " + cliente.nombre)
        ), 2)

    ficha["nota"] = nota_de(ficha)
    return ficha


# ---------------------------------------------------------------------------
# Grafo
# ---------------------------------------------------------------------------

def _grafo(corrida: Corrida, fichas: list[dict]) -> dict:
    """Arma el grafo de vinculos. Solo une cosas que el circuito ya relaciono."""
    nodos: dict[str, dict] = {}
    aristas: list[dict] = []

    def nodo(nid: str, **datos) -> str:
        if nid not in nodos:
            nodos[nid] = {"id": nid, **datos}
        return nid

    def arista(origen: str, destino: str, tipo: str, etiqueta: str,
               peso: float = 1.0, **meta) -> None:
        aristas.append({
            "id": f"e{len(aristas):05d}", "origen": origen, "destino": destino,
            "tipo": tipo, "etiqueta": etiqueta, "peso": round(peso, 4), **meta,
        })

    por_id = {f["id"]: f for f in fichas}

    for f in fichas:
        nodo(f"cli:{f['id']}", tipo="CLIENTE", etiqueta=f["nombre"],
             subtipo=f["tipo"], nivel=f["riesgo"]["nivel"], escalado=f["escalado"],
             estado=f["estado"], congelado=bool(f["congelamiento"]),
             alertas=len(f["alertas"]), puntaje=f["riesgo"]["puntaje"])

        # Jurisdiccion del cliente, solo cuando no es ordinaria: un nodo por
        # cada pais comun llena el grafo de ruido que no aporta.
        if f["riesgo_pais"] not in ("ORDINARIA", "SIN_DATO"):
            pid = nodo(f"pais:{f['pais_residencia_iso']}", tipo="PAIS",
                       etiqueta=nombre_pais(f["pais_residencia_iso"]),
                       riesgo=f["riesgo_pais"])
            arista(f"cli:{f['id']}", pid, "JURISDICCION", f["riesgo_pais"].replace("_", " ").lower())

        for c in f["coincidencias"]:
            did = nodo(f"des:{c['lista']}:{c['id_origen']}", tipo="DESIGNADO",
                       etiqueta=c["designado"], lista=c["lista"],
                       programas=c["programas"])
            arista(f"cli:{f['id']}", did, "COINCIDENCIA",
                   f"{c['score']:g}", peso=c["score"] / 100,
                   score=c["score"], criterio=c["criterio"], probable=c["probable"],
                   lista=c["lista"])

        bf = f["beneficiario"]
        if bf:
            for b in bf["beneficiarios"]:
                bid = nodo(f"per:{b['id']}", tipo="BENEFICIARIO", etiqueta=b["nombre"])
                arista(bid, f"cli:{f['id']}", "BENEFICIARIO",
                       f"{b['capital']:.0%} cap", peso=b["capital"],
                       capital=b["capital"], voto=b["voto"], via=b["via"])

        op = f["operatoria"]
        if op:
            for nombre_cp in op["contrapartes"]:
                ops = [o for a in f["alertas"] for o in a["operaciones"]
                       if o["contraparte"] == nombre_cp]
                cid_cp = nodo(f"cp:{nombre_cp}", tipo="CONTRAPARTE", etiqueta=nombre_cp)
                monto = sum(o["monto"] for o in ops)
                arista(f"cli:{f['id']}", cid_cp, "OPERACION",
                       f"${monto:,.0f}" if monto else "operatoria",
                       peso=min(monto / 1e8, 1.0) if monto else 0.2,
                       monto=round(monto, 2), cantidad=len(ops))

    # Estructura societaria completa: los intermedios importan tanto como las
    # puntas, porque el 10% se mide sobre la suma de caminos.
    if corrida.estructura is not None:
        for n in corrida.estructura.nodos.values():
            if f"cli:{n.id}" in nodos:
                continue
            if f"per:{n.id}" in nodos:
                nodos[f"per:{n.id}"]["jurisdiccion"] = n.jurisdiccion
                continue
            nodo(f"soc:{n.id}", tipo="SOCIEDAD" if n.tipo != "PERSONA" else "PERSONA",
                 etiqueta=n.nombre, jurisdiccion=n.jurisdiccion,
                 oferta_publica=n.oferta_publica)

        def referencia(ident: str) -> str:
            for prefijo in ("cli", "per", "soc"):
                if f"{prefijo}:{ident}" in nodos:
                    return f"{prefijo}:{ident}"
            return nodo(f"soc:{ident}", tipo="SOCIEDAD", etiqueta=ident)

        for p in corrida.estructura.participaciones:
            voto = p.voto if p.voto is not None else p.capital
            arista(referencia(p.propietario), referencia(p.participada),
                   "PARTICIPACION", f"{p.capital:.0%}", peso=p.capital,
                   capital=p.capital, voto=voto)

        for c in corrida.estructura.controles:
            arista(referencia(c.persona), referencia(c.entidad), "CONTROL",
                   c.motivo, peso=1.0, motivo=c.motivo)

    return {"nodos": list(nodos.values()), "aristas": aristas}


# ---------------------------------------------------------------------------
# Armado
# ---------------------------------------------------------------------------

def a_diccionario(corrida: Corrida) -> dict:
    """La corrida entera, lista para escribir como JSON."""
    fichas = [_ficha(corrida, caso) for caso in corrida.casos]

    eventos = []
    for f in fichas:
        for e in f["expediente"]:
            eventos.append({
                "momento": e["momento"],
                "cliente_id": f["id"],
                "cliente": f["nombre"],
                "actor": e["actor"],
                "accion": e["accion"],
                "nivel": f["riesgo"]["nivel"],
                "severidad": str(e["detalle"].get("severidad", "")),
                "regimen": str(e["detalle"].get("regimen", "")),
                "detalle": e["detalle"],
            })
    eventos.sort(key=lambda e: e["momento"])

    operaciones = []
    for cid, operatoria in corrida.operatorias.items():
        for o in operatoria.operaciones:
            operaciones.append({
                "cliente_id": cid, "fecha": o.fecha.isoformat(),
                "monto": round(o.monto, 2), "sentido": o.sentido,
                "instrumento": o.instrumento, "canal": o.canal,
                "contraparte": o.contraparte, "pais": o.pais_contraparte,
                "referencia": o.referencia,
            })
    operaciones.sort(key=lambda o: o["fecha"])

    conteo = {"ALTO": 0, "MEDIO": 0, "BAJO": 0}
    for ev in corrida.evaluaciones.values():
        conteo[ev.nivel] = conteo.get(ev.nivel, 0) + 1

    alertas_todas = [a for f in fichas for a in f["alertas"]]
    exposicion = corrida.exposicion

    return {
        "formato": FORMATO,
        "meta": {
            "generado": datetime.now().isoformat(timespec="seconds"),
            "listas": list(corrida.padron.procedencia),
            "designados": len(corrida.padron),
            "clientes": len(corrida.clientes),
            "umbral_revision": corrida.politica.umbral_revision,
            "umbral_probable": corrida.politica.umbral_probable,
            "umbral_reporte": round(corrida.umbral_reporte, 2),
            "smvm": SMVM,
            "smvm_vigencia": SMVM_VIGENCIA.isoformat(),
        },
        "resumen": {
            "riesgo": conteo,
            "escalados": sum(1 for f in fichas if f["escalado"]),
            "coincidencias": sum(len(f["coincidencias"]) for f in fichas),
            "probables": sum(1 for f in fichas for c in f["coincidencias"] if c["probable"]),
            "alertas": len(alertas_todas),
            "alertas_vencidas": sum(1 for a in alertas_todas if a["vencida"]),
            "congelamientos": len(corrida.congelamientos),
            "operaciones": len(operaciones),
            "exposicion_total": round(exposicion.total, 2) if exposicion else 0.0,
        },
        "exposicion": {
            "total": round(exposicion.total, 2) if exposicion else 0.0,
            "por_falta_de_reporte": round(exposicion.por_falta_de_reporte, 2) if exposicion else 0.0,
            "por_incumplimientos": round(exposicion.por_incumplimientos, 2) if exposicion else 0.0,
            "modulo": exposicion.modulo_aplicado if exposicion else 0.0,
            "modulo_vigencia": exposicion.modulo_vigencia.isoformat() if exposicion else "",
            "cargos": [
                {"concepto": c.concepto, "materia": c.materia, "modulos": c.modulos,
                 "monto": round(c.monto, 2), "fundamento": c.fundamento}
                for c in (exposicion.cargos if exposicion else [])
            ],
        },
        "clientes": fichas,
        "grafo": _grafo(corrida, fichas),
        "eventos": eventos,
        "operaciones": operaciones,
    }


def escribir(corrida: Corrida, salida: str | Path,
             variable: str = "DATOS") -> tuple[Path, Path]:
    """Escribe el .json y, al lado, el .js con el mismo contenido.

    El .js existe por una razon practica: un navegador que abre index.html con
    doble clic esta en file:// y ahi fetch de un archivo local queda bloqueado
    por CORS. El .js asigna una variable global y se carga con una etiqueta
    script, que no tiene esa restriccion. Son el mismo contenido y se escriben
    juntos, asi que no pueden quedar desfasados.

    `variable` separa dos usos que no se pueden mezclar. El export de trabajo
    define DATOS y no se publica, porque puede tener clientes reales. El juego
    de demostracion define DEMO_DATOS, sale de `ejemplos/` y ese si se
    commitea. El visor prefiere DATOS y cae en DEMO_DATOS, asi que en GitHub
    Pages se ve la demo y en la maquina del analista se ve su corrida.
    """
    datos = a_diccionario(corrida)
    ruta = Path(salida)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    texto = json.dumps(datos, ensure_ascii=False, indent=1)
    ruta.write_text(texto, encoding="utf-8")

    gemelo = ruta.with_suffix(".js")
    gemelo.write_text(f"window.{variable} = " + texto + ";", encoding="utf-8")
    return ruta, gemelo
