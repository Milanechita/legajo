/* Visor de legajo.
 *
 * Lee y muestra. No calcula riesgo, no aplica umbrales y no deriva plazos:
 * todo eso ya vino resuelto en datos.js. Es la misma regla por la que la
 * interfaz de escritorio llama a cli.main en vez de rearmar los comandos. Si
 * aca apareciera una regla del dominio, el visor y la planilla empezarian a
 * discrepar, y la que se le muestra a una inspeccion es la planilla.
 */

"use strict";

const ES_DEMO = !window.DATOS && !!window.DEMO_DATOS;
const D = window.DATOS || window.DEMO_DATOS || null;

/* ====================== utilidades ====================== */

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

function el(tag, clase, texto) {
  const n = document.createElement(tag);
  if (clase) n.className = clase;
  if (texto !== undefined) n.textContent = texto;
  return n;
}

function pesos(n) {
  if (!n) return "$0";
  return "$" + Math.round(n).toLocaleString("es-AR");
}

function porciento(f) {
  return (f * 100).toFixed(f < 0.1 && f > 0 ? 1 : 0) + "%";
}

function fecha(iso) {
  return (iso || "").slice(0, 10).split("-").reverse().join("/");
}

function momento(iso) {
  return fecha(iso) + " " + (iso || "").slice(11, 16);
}

const COLOR_NIVEL = { ALTO: "alto", MEDIO: "medio", BAJO: "bajo", SIN_SCORE: "escalado" };

/* Paleta del grafo. Se define aca y no en el CSS porque Cytoscape pinta sobre
   canvas y no lee variables de hoja de estilo. */
const TINTES = {
  CLIENTE: "#4a9eff",
  DESIGNADO: "#e5484d",
  BENEFICIARIO: "#a371f7",
  SOCIEDAD: "#39c5cf",
  PERSONA: "#7d8896",
  CONTRAPARTE: "#8b96a3",
  PAIS: "#e0a33e",
};

/* ====================== estado ====================== */

const estado = {
  filtros: {},          // {campo: Set(valores)} para el grafo
  facetas: {},          // {campo: Set(valores)} para eventos
  clienteActivo: null,
  soloCriticos: false,
  orden: { campo: "momento", asc: true },
  ventana: null,        // [desdeISO, hastaISO] elegida en la linea de tiempo
};

let cy = null;

/* ====================== arranque ====================== */

function arrancar() {
  pintarCifras();
  pintarLeyenda();
  armarGrafo();
  pintarHistogramas();
  pintarLineaTiempo();
  pintarListaClientes();
  pintarFacetas();
  pintarHistogramaEventos();
  pintarTablaEventos();
  conectarNavegacion();

  if (D.clientes.length) seleccionarCliente(clientesOrdenados()[0].id);
}

function mostrarVista(nombre) {
  const boton = $(`#vistas .vista[data-vista="${nombre}"]`);
  if (!boton) return;
  $$("#vistas .vista").forEach((x) => x.classList.remove("activa"));
  $$(".pantalla").forEach((x) => x.classList.remove("activa"));
  boton.classList.add("activa");
  $("#pantalla-" + nombre).classList.add("activa");
  // Cytoscape mide el contenedor al crearse. Si la pestana estaba oculta el
  // contenedor medía cero, asi que hay que reencuadrar al volver.
  if (nombre === "vinculos" && cy) { cy.resize(); cy.fit(undefined, 40); }
}

function conectarNavegacion() {
  $$("#vistas .vista").forEach((b) => {
    // El hash permite mandarle a alguien el enlace de una vista concreta, que
    // en una herramienta que se mira de a dos es lo primero que se pide.
    b.onclick = () => { location.hash = b.dataset.vista; };
  });
  window.addEventListener("hashchange", () => {
    mostrarVista(location.hash.slice(1) || "vinculos");
  });
  mostrarVista(location.hash.slice(1) || "vinculos");

  $$("#disposiciones .chip").forEach((b) => {
    b.onclick = () => {
      $$("#disposiciones .chip").forEach((x) => x.classList.remove("activo"));
      b.classList.add("activo");
      correrDisposicion(b.dataset.layout);
    };
  });

  $("#reencuadrar").onclick = () => cy && cy.fit(undefined, 40);

  $("#solo-criticos").onchange = (e) => {
    estado.soloCriticos = e.target.checked;
    aplicarFiltrosGrafo();
  };

  $("#buscar-nodo").oninput = (e) => {
    const q = e.target.value.trim().toLowerCase();
    if (!cy) return;
    cy.nodes().forEach((n) => {
      const coincide = !q || n.data("etiqueta").toLowerCase().includes(q);
      n.toggleClass("apagado", !coincide && !!q);
    });
  };

  $("#limpiar-filtros").onclick = () => {
    estado.filtros = {};
    estado.ventana = null;
    $("#solo-criticos").checked = false;
    estado.soloCriticos = false;
    aplicarFiltrosGrafo();
    pintarHistogramas();
    pintarLineaTiempo();
  };

  $("#limpiar-facetas").onclick = () => {
    estado.facetas = {};
    pintarFacetas();
    pintarHistogramaEventos();
    pintarTablaEventos();
  };

  $("#buscar-cliente").oninput = pintarListaClientes;
  $$("#filtro-nivel .chip").forEach((b) => {
    b.onclick = () => {
      $$("#filtro-nivel .chip").forEach((x) => x.classList.remove("activo"));
      b.classList.add("activo");
      pintarListaClientes();
    };
  });

  $$("#tabla-eventos th[data-orden]").forEach((th) => {
    th.onclick = () => {
      const campo = th.dataset.orden;
      estado.orden = {
        campo,
        asc: estado.orden.campo === campo ? !estado.orden.asc : true,
      };
      $$("#tabla-eventos th").forEach((x) =>
        x.classList.remove("orden-asc", "orden-desc"));
      th.classList.add(estado.orden.asc ? "orden-asc" : "orden-desc");
      pintarTablaEventos();
    };
  });
}

/* ====================== cabecera ====================== */

function pintarCifras() {
  const r = D.resumen;
  const cifras = [
    ["clientes", D.meta.clientes, ""],
    ["designados", D.meta.designados.toLocaleString("es-AR"), ""],
    ["riesgo alto", r.riesgo.ALTO || 0, r.riesgo.ALTO ? "aviso" : ""],
    ["escalados", r.escalados, r.escalados ? "critica" : ""],
    ["congelamientos", r.congelamientos, r.congelamientos ? "critica" : ""],
    ["plazos vencidos", r.alertas_vencidas, r.alertas_vencidas ? "critica" : ""],
    ["exposición", pesos(r.exposicion_total), ""],
  ];
  const cont = $("#cifras");
  cont.innerHTML = "";

  if (ES_DEMO) {
    const aviso = el("div", "cifra");
    aviso.appendChild(el("b", null, "DEMO"));
    aviso.appendChild(el("span", null, "datos de ejemplo"));
    aviso.title = "Padron ficticio de ejemplos/. No son clientes reales.";
    aviso.style.cssText = "align-items:flex-start;color:var(--ambar)";
    cont.appendChild(aviso);
  }
  cifras.forEach(([et, val, clase]) => {
    const d = el("div", "cifra " + clase);
    d.appendChild(el("b", null, String(val)));
    d.appendChild(el("span", null, et));
    cont.appendChild(d);
  });
}

function pintarLeyenda() {
  const items = [
    ["CLIENTE", "Cliente", "redondo"],
    ["DESIGNADO", "Designado en lista", "rombo"],
    ["BENEFICIARIO", "Beneficiario final", "redondo"],
    ["SOCIEDAD", "Sociedad intermedia", ""],
    ["CONTRAPARTE", "Contraparte", ""],
    ["PAIS", "Jurisdicción de riesgo", "rombo"],
  ];
  const cont = $("#leyenda");
  cont.innerHTML = "";
  items.forEach(([tipo, texto, forma]) => {
    const s = el("span");
    const i = el("i", forma);
    i.style.background = TINTES[tipo];
    s.appendChild(i);
    s.appendChild(document.createTextNode(texto));
    cont.appendChild(s);
  });
}

/* ====================== grafo ====================== */

function armarGrafo() {
  const elementos = [];
  D.grafo.nodos.forEach((n) => {
    elementos.push({
      data: {
        id: n.id, etiqueta: n.etiqueta, tipo: n.tipo,
        nivel: n.nivel || "", lista: n.lista || "",
        escalado: !!n.escalado, congelado: !!n.congelado,
        grado: 1, info: n,
      },
    });
  });
  D.grafo.aristas.forEach((a) => {
    elementos.push({
      data: {
        id: a.id, source: a.origen, target: a.destino,
        tipo: a.tipo, etiqueta: a.etiqueta, peso: a.peso, info: a,
      },
    });
  });

  cy = cytoscape({
    container: $("#grafo"),
    elements: elementos,
    minZoom: 0.15,
    maxZoom: 3,
    wheelSensitivity: 0.25,
    style: [
      {
        selector: "node",
        style: {
          "background-color": (n) => TINTES[n.data("tipo")] || "#7d8896",
          "label": "data(etiqueta)",
          "color": "#c8d3e0",
          "font-size": 9,
          "font-family": "Segoe UI, sans-serif",
          "text-valign": "bottom",
          "text-margin-y": 4,
          "text-max-width": 110,
          "text-wrap": "ellipsis",
          "width": 16, "height": 16,
          "border-width": 1,
          "border-color": "#0d1117",
          "transition-property": "opacity, border-width",
          "transition-duration": 120,
        },
      },
      { selector: 'node[tipo = "CLIENTE"]', style: { width: 24, height: 24, "font-size": 10 } },
      {
        selector: 'node[tipo = "DESIGNADO"]',
        style: { shape: "diamond", width: 22, height: 22 },
      },
      { selector: 'node[tipo = "PAIS"]', style: { shape: "diamond", width: 18, height: 18 } },
      { selector: 'node[tipo = "SOCIEDAD"]', style: { shape: "round-rectangle", width: 20, height: 14 } },
      { selector: 'node[tipo = "CONTRAPARTE"]', style: { shape: "round-rectangle", width: 14, height: 11 } },
      // Lo que no admite demora se ve sin buscarlo: aro rojo grueso.
      {
        selector: "node[?escalado], node[?congelado]",
        style: { "border-width": 3, "border-color": "#e5484d" },
      },
      { selector: 'node[nivel = "ALTO"]', style: { "border-width": 2, "border-color": "#e0a33e" } },
      {
        selector: "edge",
        style: {
          "width": (e) => 0.8 + e.data("peso") * 2.2,
          "line-color": "#2b3947",
          "target-arrow-color": "#2b3947",
          "target-arrow-shape": "triangle",
          "arrow-scale": 0.7,
          "curve-style": "bezier",
          "font-size": 8,
          "color": "#78838f",
          "text-rotation": "autorotate",
          "transition-property": "opacity",
          "transition-duration": 120,
        },
      },
      { selector: 'edge[tipo = "COINCIDENCIA"]', style: { "line-color": "#7d3033", "target-arrow-color": "#7d3033", "line-style": "dashed" } },
      { selector: 'edge[tipo = "BENEFICIARIO"]', style: { "line-color": "#5a3f86", "target-arrow-color": "#5a3f86" } },
      { selector: 'edge[tipo = "PARTICIPACION"]', style: { "line-color": "#2d5566", "target-arrow-color": "#2d5566", "label": "data(etiqueta)" } },
      { selector: 'edge[tipo = "JURISDICCION"]', style: { "line-color": "#6b5424", "target-arrow-color": "#6b5424", "line-style": "dotted" } },
      { selector: "node.apagado", style: { opacity: 0.12 } },
      { selector: "edge.apagado", style: { opacity: 0.05 } },
      { selector: "node.oculto, edge.oculto", style: { display: "none" } },
      {
        selector: "node:selected",
        style: { "border-width": 3, "border-color": "#4a9eff" },
      },
      { selector: "node.vecino", style: { "border-width": 2, "border-color": "#4a9eff" } },
      { selector: "edge.vecino", style: { "line-color": "#4a9eff", "target-arrow-color": "#4a9eff", opacity: 1 } },
    ],
    layout: disposicion("cose"),
  });

  cy.on("tap", "node", (e) => mostrarPropiedades(e.target));
  cy.on("tap", "edge", (e) => mostrarPropiedadesArista(e.target));
  cy.on("dbltap", "node", (e) => expandirVecinos(e.target));
  cy.on("tap", (e) => {
    if (e.target === cy) {
      cy.elements().removeClass("vecino");
      limpiarPropiedades();
    }
  });

  actualizarContador();
}

function disposicion(nombre) {
  const base = { name: nombre, animate: false, fit: true, padding: 40 };
  if (nombre === "cose") {
    return Object.assign(base, {
      nodeRepulsion: 9000, idealEdgeLength: 90, edgeElasticity: 110,
      gravity: 42, numIter: 1200, nodeDimensionsIncludeLabels: true,
      randomize: false,
    });
  }
  if (nombre === "concentric") {
    return Object.assign(base, {
      // Lo mas grave al centro: un escalado o un congelamiento primero, y
      // despues los clientes por puntaje.
      concentric: (n) => {
        if (n.data("escalado") || n.data("congelado")) return 100;
        if (n.data("tipo") === "CLIENTE") return 50 + (n.data("info").puntaje || 0) / 10;
        if (n.data("tipo") === "DESIGNADO") return 40;
        return 10;
      },
      levelWidth: () => 18, minNodeSpacing: 26,
    });
  }
  return Object.assign(base, { directed: true, spacingFactor: 1.2 });
}

function correrDisposicion(nombre) {
  cy.layout(disposicion(nombre)).run();
}

function expandirVecinos(nodo) {
  // "Expandir" no trae datos nuevos: el grafo ya esta completo. Lo que hace es
  // resaltar el entorno directo, que es lo que un analista mira cuando abre
  // una entidad.
  cy.elements().removeClass("vecino");
  const entorno = nodo.closedNeighborhood();
  entorno.addClass("vecino");
  cy.animate({ fit: { eles: entorno, padding: 70 }, duration: 240 });
}

function aplicarFiltrosGrafo() {
  const activos = Object.entries(estado.filtros).filter(([, v]) => v.size);

  cy.nodes().forEach((n) => {
    let visible = true;

    if (estado.soloCriticos) {
      const info = n.data("info");
      visible = n.data("escalado") || n.data("congelado") ||
                n.data("nivel") === "ALTO" || n.data("tipo") === "DESIGNADO" ||
                (info && info.riesgo && info.riesgo !== "ORDINARIA");
    }

    if (visible) {
      for (const [campo, valores] of activos) {
        const propio = valorDeFiltro(n, campo);
        // Un nodo que no tiene ese campo no se esconde: el filtro "lista OFAC"
        // habla de designados, y esconder por eso a las sociedades dejaria el
        // grafo sin contexto.
        if (propio !== null && !valores.has(propio)) { visible = false; break; }
      }
    }
    n.toggleClass("oculto", !visible);
  });

  cy.edges().forEach((e) => {
    e.toggleClass("oculto", e.source().hasClass("oculto") || e.target().hasClass("oculto"));
  });

  if (estado.ventana) marcarVentanaEnGrafo();
  actualizarContador();
}

function valorDeFiltro(nodo, campo) {
  if (campo === "tipo") return nodo.data("tipo");
  if (campo === "nivel") return nodo.data("tipo") === "CLIENTE" ? (nodo.data("nivel") || "SIN_SCORE") : null;
  if (campo === "lista") return nodo.data("tipo") === "DESIGNADO" ? nodo.data("lista") : null;
  return null;
}

function marcarVentanaEnGrafo() {
  const [desde, hasta] = estado.ventana;
  const conActividad = new Set();
  D.operaciones.forEach((o) => {
    if (o.fecha >= desde && o.fecha <= hasta) conActividad.add("cli:" + o.cliente_id);
  });
  D.clientes.forEach((c) => {
    c.alertas.forEach((a) => {
      if (a.generada >= desde && a.generada <= hasta) conActividad.add("cli:" + c.id);
    });
  });
  cy.nodes('[tipo = "CLIENTE"]').forEach((n) => {
    n.toggleClass("apagado", !conActividad.has(n.id()));
  });
}

function actualizarContador() {
  const nv = cy.nodes().filter((n) => !n.hasClass("oculto")).length;
  const av = cy.edges().filter((e) => !e.hasClass("oculto")).length;
  $("#contador-grafo").textContent =
    `${nv}/${cy.nodes().length} entidades · ${av}/${cy.edges().length} vínculos`;
}

/* ====================== panel de selección ====================== */

function limpiarPropiedades() {
  $("#seleccion").innerHTML =
    '<div class="titulo-seccion"><span>Selección</span></div>' +
    '<div class="vacio">Hacé clic en una entidad del grafo para ver sus ' +
    "propiedades. Doble clic expande sus vínculos.</div>";
}

function mostrarPropiedades(nodo) {
  const info = nodo.data("info");
  const caja = $("#seleccion");
  caja.innerHTML = "";
  caja.appendChild(tituloSeccion("Selección"));

  const props = el("div", "props");
  props.appendChild(el("div", "nombre", info.etiqueta));
  props.appendChild(el("div", "clase", etiquetaTipo(info.tipo)));

  const filas = [];
  if (info.tipo === "CLIENTE") {
    const c = D.clientes.find((x) => x.id === info.id.slice(4));
    if (c) {
      filas.push(["ID", c.id], ["Tipo", c.tipo], ["Estado", c.estado],
                 ["Riesgo", `${c.riesgo.nivel} (${c.riesgo.puntaje} pts)`],
                 ["Régimen", c.riesgo.regimen || "sin asignar"],
                 ["Residencia", c.pais_residencia || "s/d"],
                 ["Actividad", c.actividad || "s/d"],
                 ["Coincidencias", c.coincidencias.length],
                 ["Alertas", c.alertas.length]);
      if (c.congelamiento) filas.push(["Congelamiento", c.congelamiento.regimen]);
    }
  } else if (info.tipo === "DESIGNADO") {
    filas.push(["Lista", info.lista], ["ID origen", info.id.split(":").pop()]);
    if (info.programas && info.programas.length) filas.push(["Programas", info.programas.join(", ")]);
  } else if (info.tipo === "PAIS") {
    filas.push(["Clasificación", (info.riesgo || "").replace(/_/g, " ").toLowerCase()]);
  } else if (info.tipo === "SOCIEDAD" || info.tipo === "PERSONA") {
    if (info.jurisdiccion) filas.push(["Jurisdicción", info.jurisdiccion]);
    if (info.oferta_publica) filas.push(["Oferta pública", "sí"]);
  }

  filas.push(["Vínculos", nodo.degree()]);

  const dl = el("dl");
  filas.forEach(([k, v]) => {
    const fila = el("div", "prop");
    fila.appendChild(el("dt", null, k));
    fila.appendChild(el("dd", null, String(v)));
    dl.appendChild(fila);
  });
  props.appendChild(dl);

  if (info.tipo === "CLIENTE") {
    const cid = info.id.slice(4);
    const boton = el("button", "chip", "Abrir ficha completa");
    boton.style.marginTop = "12px";
    boton.onclick = () => {
      seleccionarCliente(cid);
      location.hash = "ficha";
    };
    props.appendChild(boton);
  }

  caja.appendChild(props);
  expandirVecinos(nodo);
}

function mostrarPropiedadesArista(arista) {
  const a = arista.data("info");
  const caja = $("#seleccion");
  caja.innerHTML = "";
  caja.appendChild(tituloSeccion("Vínculo"));

  const props = el("div", "props");
  props.appendChild(el("div", "nombre",
    arista.source().data("etiqueta") + "  →  " + arista.target().data("etiqueta")));
  props.appendChild(el("div", "clase", etiquetaTipo(a.tipo)));

  const filas = [];
  if (a.tipo === "COINCIDENCIA") {
    filas.push(["Score", a.score], ["Criterio", a.criterio],
               ["Probable", a.probable ? "sí" : "no"], ["Lista", a.lista]);
  } else if (a.tipo === "PARTICIPACION") {
    filas.push(["Capital", porciento(a.capital)], ["Voto", porciento(a.voto)]);
  } else if (a.tipo === "BENEFICIARIO") {
    filas.push(["Capital efectivo", porciento(a.capital)],
               ["Voto efectivo", porciento(a.voto)], ["Vía", a.via]);
  } else if (a.tipo === "OPERACION") {
    filas.push(["Monto", pesos(a.monto)], ["Operaciones", a.cantidad]);
  } else if (a.tipo === "CONTROL") {
    filas.push(["Motivo", a.motivo]);
  }

  const dl = el("dl");
  filas.forEach(([k, v]) => {
    const fila = el("div", "prop");
    fila.appendChild(el("dt", null, k));
    fila.appendChild(el("dd", null, String(v)));
    dl.appendChild(fila);
  });
  props.appendChild(dl);
  caja.appendChild(props);
}

function tituloSeccion(texto) {
  const t = el("div", "titulo-seccion");
  t.appendChild(el("span", null, texto));
  return t;
}

function etiquetaTipo(t) {
  return ({
    CLIENTE: "Cliente", DESIGNADO: "Designado en lista",
    BENEFICIARIO: "Beneficiario final", SOCIEDAD: "Sociedad",
    PERSONA: "Persona", CONTRAPARTE: "Contraparte", PAIS: "Jurisdicción",
    COINCIDENCIA: "Coincidencia en lista", PARTICIPACION: "Participación societaria",
    OPERACION: "Operatoria", JURISDICCION: "Jurisdicción", CONTROL: "Control",
  })[t] || t;
}

/* ====================== histogramas ====================== */

function pintarHistogramas() {
  const cont = $("#histogramas");
  cont.innerHTML = "";

  const porTipo = contar(D.grafo.nodos, (n) => n.tipo);
  const porNivel = contar(D.clientes, (c) => c.riesgo.nivel);
  const porLista = contar(
    D.grafo.nodos.filter((n) => n.tipo === "DESIGNADO"), (n) => n.lista);

  cont.appendChild(histograma("Tipo de entidad", porTipo, "tipo",
    (k) => etiquetaTipo(k), () => null));
  cont.appendChild(histograma("Nivel de riesgo", porNivel, "nivel",
    (k) => k === "SIN_SCORE" ? "Escalado" : k.charAt(0) + k.slice(1).toLowerCase(),
    (k) => ({ ALTO: "rojo", MEDIO: "ambar", BAJO: "verde", SIN_SCORE: "rojo" })[k]));
  if (Object.keys(porLista).length) {
    cont.appendChild(histograma("Lista de control", porLista, "lista",
      (k) => k, () => "rojo"));
  }
}

function contar(items, clave) {
  const m = {};
  items.forEach((i) => {
    const k = clave(i);
    if (k === null || k === undefined || k === "") return;
    m[k] = (m[k] || 0) + 1;
  });
  return m;
}

function histograma(titulo, mapa, campo, etiquetar, colorear) {
  const caja = el("div", "histo");
  caja.appendChild(el("h4", null, titulo));
  const entradas = Object.entries(mapa).sort((a, b) => b[1] - a[1]);
  const tope = Math.max(...entradas.map((e) => e[1]), 1);

  entradas.forEach(([clave, valor]) => {
    const activo = estado.filtros[campo] && estado.filtros[campo].has(clave);
    const fila = el("div", "barra-fila" + (activo ? " activo" : ""));
    const color = colorear(clave);
    if (color) fila.dataset.color = color;

    const et = el("div", "barra-etiqueta");
    const relleno = el("div", "barra-relleno");
    relleno.style.width = (valor / tope * 100) + "%";
    et.appendChild(relleno);
    et.appendChild(el("span", null, etiquetar(clave)));
    fila.appendChild(et);
    fila.appendChild(el("div", "barra-valor", String(valor)));

    fila.onclick = () => {
      if (!estado.filtros[campo]) estado.filtros[campo] = new Set();
      const s = estado.filtros[campo];
      s.has(clave) ? s.delete(clave) : s.add(clave);
      aplicarFiltrosGrafo();
      pintarHistogramas();
    };
    caja.appendChild(fila);
  });
  return caja;
}

/* ====================== línea de tiempo ====================== */

function pintarLineaTiempo() {
  const cont = $("#tiempo");
  cont.innerHTML = "";

  // Se apilan operaciones y alertas por mes. El mes es la unidad util: el
  // plazo de reporte se cuenta en dias, pero la operatoria de un cliente se
  // lee por periodo.
  const meses = {};
  const mesDe = (iso) => (iso || "").slice(0, 7);

  D.operaciones.forEach((o) => {
    const m = mesDe(o.fecha);
    if (!m) return;
    meses[m] = meses[m] || { operacion: 0, alerta: 0, vencida: 0 };
    meses[m].operacion++;
  });
  D.clientes.forEach((c) => c.alertas.forEach((a) => {
    const m = mesDe(a.generada);
    if (!m) return;
    meses[m] = meses[m] || { operacion: 0, alerta: 0, vencida: 0 };
    a.vencida ? meses[m].vencida++ : meses[m].alerta++;
  }));

  const claves = Object.keys(meses).sort();
  if (!claves.length) {
    cont.appendChild(el("div", "vacio", "Sin operaciones ni alertas para ubicar en el tiempo."));
    return;
  }

  $("#rango-tiempo").textContent = claves[0] + "  a  " + claves[claves.length - 1];

  const tope = Math.max(...claves.map((k) => {
    const v = meses[k];
    return v.operacion + v.alerta + v.vencida;
  }), 1);

  const pilas = el("div", "pilas");
  claves.forEach((k) => {
    const v = meses[k];
    const total = v.operacion + v.alerta + v.vencida;
    const pila = el("div", "pila");
    pila.title = `${k}\n${v.operacion} operación(es)\n${v.alerta} alerta(s)` +
                 `\n${v.vencida} con plazo vencido`;

    [["vencida", "#e5484d"], ["alerta", "#e0a33e"], ["operacion", "#2d4a63"]]
      .forEach(([campo, color]) => {
        if (!v[campo]) return;
        const t = el("div", "tramo");
        t.style.height = (v[campo] / tope * 74) + "px";
        t.style.background = color;
        pila.appendChild(t);
      });

    if (!total) pila.style.minHeight = "1px";

    const activo = estado.ventana && estado.ventana[0].slice(0, 7) === k;
    if (estado.ventana && !activo) pila.classList.add("fuera");

    pila.onclick = () => {
      if (activo) {
        estado.ventana = null;
        cy.nodes().removeClass("apagado");
      } else {
        estado.ventana = [k + "-01", k + "-31"];
      }
      aplicarFiltrosGrafo();
      pintarLineaTiempo();
    };
    pilas.appendChild(pila);
  });

  cont.appendChild(pilas);
  const ejes = el("div", "ejes");
  ejes.appendChild(el("span", null, claves[0]));
  ejes.appendChild(el("span", null, claves[claves.length - 1]));
  cont.appendChild(ejes);
}

/* ====================== ficha del cliente ====================== */

function clientesOrdenados() {
  const peso = { SIN_SCORE: 4, ALTO: 3, MEDIO: 2, BAJO: 1 };
  return D.clientes.slice().sort((a, b) => {
    const d = (peso[b.riesgo.nivel] || 0) - (peso[a.riesgo.nivel] || 0);
    return d !== 0 ? d : b.riesgo.puntaje - a.riesgo.puntaje;
  });
}

function pintarListaClientes() {
  const q = ($("#buscar-cliente").value || "").trim().toLowerCase();
  const nivel = ($("#filtro-nivel .chip.activo") || {}).dataset
    ? $("#filtro-nivel .chip.activo").dataset.nivel : "";

  const cont = $("#lista-clientes");
  cont.innerHTML = "";

  clientesOrdenados()
    .filter((c) => !nivel || c.riesgo.nivel === nivel)
    .filter((c) => !q || c.nombre.toLowerCase().includes(q) ||
                   c.id.toLowerCase().includes(q))
    .forEach((c) => {
      const item = el("div", "item-cliente" + (c.id === estado.clienteActivo ? " activo" : ""));
      item.appendChild(el("span", "id", c.id));

      const marcas = el("div", "marcas");
      if (c.escalado) marcas.appendChild(insignia("ESCALADO", "escalado"));
      else marcas.appendChild(insignia(c.riesgo.nivel, COLOR_NIVEL[c.riesgo.nivel] || "neutro"));
      if (c.congelamiento) marcas.appendChild(insignia("CONGELA", "critico"));
      if (c.alertas.some((a) => a.vencida)) marcas.appendChild(insignia("VENCIDO", "critico"));
      item.appendChild(marcas);

      item.appendChild(el("div", "nom", c.nombre));
      item.onclick = () => seleccionarCliente(c.id);
      cont.appendChild(item);
    });
}

function insignia(texto, clase) {
  return el("span", "insignia " + (clase || "neutro"), texto);
}

function seleccionarCliente(id) {
  estado.clienteActivo = id;
  pintarListaClientes();
  pintarFicha(D.clientes.find((c) => c.id === id));
}

function pintarFicha(c) {
  const cont = $("#detalle-cliente");
  cont.innerHTML = "";
  if (!c) return;

  // --- encabezado ---
  const cab = el("div", "encabezado-ficha");
  const tit = el("div", "titulo");
  tit.appendChild(el("h2", null, c.nombre));
  const sub = [c.id, c.caso_id, ...(c.documentos || [])].join("  ·  ");
  tit.appendChild(el("div", "sub", sub));

  const marcas = el("div", "marcas-ficha");
  if (c.escalado) marcas.appendChild(insignia("CASO ESCALADO", "escalado"));
  marcas.appendChild(insignia("ESTADO " + c.estado, "neutro"));
  if (!c.escalado) marcas.appendChild(insignia("RIESGO " + c.riesgo.nivel, COLOR_NIVEL[c.riesgo.nivel]));
  if (c.pep) marcas.appendChild(insignia("PEP " + c.pep.tipo + (c.pep.vencida ? " VENCIDA" : ""), "info"));
  if (c.congelamiento) marcas.appendChild(insignia("CONGELAMIENTO " + c.congelamiento.regimen, "critico"));
  if (c.oferta_publica) marcas.appendChild(insignia("OFERTA PÚBLICA", "neutro"));
  tit.appendChild(marcas);
  cab.appendChild(tit);
  cont.appendChild(cab);

  // --- nota ---
  const tNota = tarjeta("Nota del caso");
  const nota = el("div", "nota", c.nota);
  tNota.querySelector(".cuerpo").appendChild(nota);
  cont.appendChild(tNota);

  // --- identificación ---
  const tId = tarjeta("Identificación");
  const rej = el("div", "rejilla");
  [["Tipo", c.tipo === "PERSONA" ? "Persona humana" : "Persona jurídica"],
   ["Nacionalidad", c.nacionalidad || "s/d"],
   ["Residencia", c.pais_residencia || "s/d"],
   ["Jurisdicción", (c.riesgo_pais || "").replace(/_/g, " ").toLowerCase()],
   ["Actividad", c.actividad || "s/d"],
   ["Nacimiento", c.fecha_nacimiento ? fecha(c.fecha_nacimiento) : "s/d"],
  ].forEach(([k, v]) => rej.appendChild(celda(k, v, true)));
  tId.querySelector(".cuerpo").style.padding = "0";
  tId.querySelector(".cuerpo").appendChild(rej);
  cont.appendChild(tId);

  // --- riesgo ---
  if (!c.escalado || c.riesgo.factores.length) {
    const tR = tarjeta("Puntaje de riesgo");
    const cuerpo = tR.querySelector(".cuerpo");

    const res = el("div", "rejilla");
    res.style.marginBottom = "14px";
    res.appendChild(celda("Puntaje", String(c.riesgo.puntaje)));
    res.appendChild(celda("Nivel", c.riesgo.nivel));
    res.appendChild(celda("Régimen", (c.riesgo.regimen || "sin asignar").replace(/_/g, " "), true));
    res.appendChild(celda("Revisión", c.riesgo.revision_meses ? c.riesgo.revision_meses + " meses" : "s/d", true));
    cuerpo.style.padding = "0";
    cuerpo.appendChild(res);

    const lista = el("div");
    lista.style.padding = "0 14px 14px";
    if (c.riesgo.factores.length) {
      c.riesgo.factores.forEach((f) => {
        const fila = el("div", "factor");
        const izq = el("div");
        izq.appendChild(el("div", null, f.descripcion));
        izq.appendChild(el("div", "dim", f.dimension + " · " + f.codigo));
        fila.appendChild(izq);
        fila.appendChild(el("div", "pts", "+" + f.puntos));
        lista.appendChild(fila);
      });
    } else {
      lista.appendChild(el("div", "vacio", "Sin factores: el caso se escaló antes del scoring."));
    }
    cuerpo.appendChild(lista);
    cont.appendChild(tR);
  }

  // --- coincidencias ---
  if (c.coincidencias.length) {
    const t = tarjeta(`Coincidencias en listas (${c.coincidencias.length})`);
    const cuerpo = t.querySelector(".cuerpo");
    cuerpo.style.padding = "0";
    cuerpo.appendChild(tablita(
      ["Lista", "Designado", "Matcheó contra", "Score", "Criterio"],
      c.coincidencias.map((x) => [
        x.lista, x.designado, x.matcheado, String(x.score), x.criterio,
      ]),
      c.coincidencias.map((x) => x.probable)));
    cont.appendChild(t);
  }

  // --- congelamiento ---
  if (c.congelamiento) {
    const cg = c.congelamiento;
    const t = tarjeta("Congelamiento administrativo");
    const cuerpo = t.querySelector(".cuerpo");
    const rej2 = el("div", "rejilla");
    rej2.appendChild(celda("Régimen", cg.regimen));
    rej2.appendChild(celda("Norma", cg.norma, true));
    rej2.appendChild(celda("Detectado", fecha(cg.detectado), true));
    rej2.appendChild(celda("Plazo de reporte", "24 horas", true));
    cuerpo.style.padding = "0";
    cuerpo.appendChild(rej2);

    const pasos = el("div");
    pasos.style.padding = "12px 14px 14px";
    cg.pasos.forEach((p) => {
      const fila = el("div", "factor");
      fila.appendChild(el("div", null, p.descripcion));
      fila.appendChild(el("div", "pts", p.cumplido ? "hecho" : "pendiente"));
      pasos.appendChild(fila);
    });
    cuerpo.appendChild(pasos);
    cont.appendChild(t);
  }

  // --- beneficiario final ---
  if (c.beneficiario) {
    const bf = c.beneficiario;
    const t = tarjeta("Beneficiario final");
    const cuerpo = t.querySelector(".cuerpo");

    if (bf.exceptuada) {
      cuerpo.appendChild(el("div", "vacio",
        "Exceptuada de identificar beneficiario final por hacer oferta pública."));
    } else if (!bf.beneficiarios.length) {
      cuerpo.appendChild(el("div", "vacio",
        `No identificado. ${porciento(bf.opaco)} de la titularidad quedó sin resolver.`));
    } else {
      const cadena = el("div", "cadena");
      bf.beneficiarios.forEach((b) => {
        const e = el("div", "eslabon");
        const izq = el("div");
        izq.appendChild(el("div", null, b.nombre));
        izq.appendChild(el("div", "via", b.via + (b.detalle ? " · " + b.detalle : "")));
        e.appendChild(izq);
        e.appendChild(el("div", "pct", porciento(b.capital) + " cap · " + porciento(b.voto) + " voto"));
        cadena.appendChild(e);
      });
      cuerpo.appendChild(cadena);
    }

    if (bf.observaciones && bf.observaciones.length) {
      const obs = el("div");
      obs.style.marginTop = "12px";
      bf.observaciones.forEach((o) => {
        const li = el("div", "dim");
        li.style.cssText = "font-size:11px;color:var(--tenue);padding:2px 0";
        li.textContent = "· " + o;
        obs.appendChild(li);
      });
      cuerpo.appendChild(obs);
    }
    cont.appendChild(t);
  }

  // --- alertas ---
  if (c.alertas.length) {
    const vencidas = c.alertas.filter((a) => a.vencida).length;
    const t = tarjeta(`Alertas de monitoreo (${c.alertas.length}` +
      (vencidas ? `, ${vencidas} con plazo vencido` : "") + ")");
    const cuerpo = t.querySelector(".cuerpo");
    cuerpo.style.padding = "0";
    cuerpo.appendChild(tablita(
      ["Tipo", "Severidad", "Régimen", "Monto", "Vence", "Plazo"],
      c.alertas.map((a) => [
        a.codigo, a.severidad, a.regimen, pesos(a.monto), fecha(a.vence),
        a.vencida ? "VENCIDO" : a.dias_restantes + " días",
      ]),
      c.alertas.map((a) => a.vencida)));

    const pie = el("div");
    pie.style.cssText = "padding:10px 14px;font-size:11px;color:var(--tenue);line-height:1.6";
    pie.textContent = "El tope corre desde la operación y no desde la detección. " +
      "Una alerta con el plazo vencido no deja de tener que reportarse.";
    cuerpo.appendChild(pie);
    cont.appendChild(t);
  }

  // --- operatoria ---
  if (c.operatoria) {
    const o = c.operatoria;
    const t = tarjeta("Operatoria");
    const cuerpo = t.querySelector(".cuerpo");
    cuerpo.style.padding = "0";
    const rej3 = el("div", "rejilla");
    rej3.appendChild(celda("Operaciones", String(o.cantidad)));
    rej3.appendChild(celda("Monto total", pesos(o.total)));
    rej3.appendChild(celda("En efectivo", pesos(o.efectivo) + " (" + porciento(o.proporcion_efectivo) + ")", true));
    rej3.appendChild(celda("Período", fecha(o.desde) + " a " + fecha(o.hasta), true));
    if (o.paises.length) rej3.appendChild(celda("Jurisdicciones", o.paises.join(", "), true));
    if (c.perfil) {
      rej3.appendChild(celda("Perfil declarado", pesos(c.perfil.monto_mensual) + "/mes", true));
    } else {
      rej3.appendChild(celda("Perfil declarado", "sin perfil", true));
    }
    cuerpo.appendChild(rej3);
    cont.appendChild(t);
  }

  // --- exposición ---
  if (c.exposicion) {
    const t = tarjeta("Exposición sancionatoria atribuible");
    const cuerpo = t.querySelector(".cuerpo");
    cuerpo.appendChild(el("div", "celda")).innerHTML =
      `<div class="va" style="font-size:20px;color:var(--ambar)">${pesos(c.exposicion)}</div>`;
    const nota2 = el("div");
    nota2.style.cssText = "font-size:11px;color:var(--tenue);margin-top:8px;line-height:1.6";
    nota2.textContent = "Solo el cargo por ROS no emitido se puede atribuir a un " +
      "cliente. Los cargos por incumplimiento de listados, monitoreo y beneficiario " +
      "final se liquidan por materia. Es una estimación, no un cálculo de multa.";
    cuerpo.appendChild(nota2);
    cont.appendChild(t);
  }

  // --- expediente ---
  const tExp = tarjeta(`Expediente (${c.expediente.length} entradas)`);
  const cuerpo = tExp.querySelector(".cuerpo");
  const crono = el("div", "cronologia");
  c.expediente.forEach((e) => {
    const grave = /CONGELAMIENTO|ESCALADO/.test(e.accion) ||
                  String(e.detalle.severidad || "") === "ALTA";
    const medio = /ALERTA|COINCIDENCIA/.test(e.accion);
    const hito = el("div", "hito" + (grave ? " rojo" : medio ? " ambar" : ""));
    const cabh = el("div", "cab");
    cabh.appendChild(el("span", "acc", e.accion.replace(/_/g, " ")));
    cabh.appendChild(el("span", "mom", momento(e.momento)));
    cabh.appendChild(el("span", "act", e.actor));
    hito.appendChild(cabh);
    const det = detalleLegible(e.detalle);
    if (det) hito.appendChild(el("div", "det", det));
    crono.appendChild(hito);
  });
  cuerpo.appendChild(crono);
  cont.appendChild(tExp);

  cont.scrollTop = 0;
}

function tarjeta(titulo) {
  const t = el("div", "tarjeta");
  t.appendChild(el("h3", null, titulo));
  t.appendChild(el("div", "cuerpo"));
  return t;
}

function celda(etiqueta, valor, chico) {
  const c = el("div", "celda");
  c.appendChild(el("div", "et", etiqueta));
  c.appendChild(el("div", "va" + (chico ? " chico" : ""), String(valor)));
  return c;
}

function tablita(cabeceras, filas, criticas) {
  const tabla = el("table", "densa");
  const thead = el("thead");
  const tr = el("tr");
  cabeceras.forEach((h) => {
    const th = el("th", null, h);
    th.style.cursor = "default";
    tr.appendChild(th);
  });
  thead.appendChild(tr);
  tabla.appendChild(thead);

  const tbody = el("tbody");
  filas.forEach((f, i) => {
    const fila = el("tr", criticas && criticas[i] ? "fila-critica" : "");
    f.forEach((v, j) => fila.appendChild(el("td", j > 1 ? "mono" : "", v)));
    tbody.appendChild(fila);
  });
  tabla.appendChild(tbody);
  return tabla;
}

function detalleLegible(detalle) {
  if (!detalle) return "";
  return Object.entries(detalle)
    .filter(([, v]) => v !== null && v !== "" && !(Array.isArray(v) && !v.length))
    .map(([k, v]) => {
      let texto = Array.isArray(v) ? v.join(", ") : String(v);
      if (texto.length > 160) texto = texto.slice(0, 157) + "...";
      return k.replace(/_/g, " ") + ": " + texto;
    })
    .join("   ·   ");
}

/* ====================== eventos ====================== */

function eventosFiltrados() {
  return D.eventos.filter((e) => {
    for (const [campo, valores] of Object.entries(estado.facetas)) {
      if (!valores.size) continue;
      if (!valores.has(String(e[campo] || "(sin dato)"))) return false;
    }
    return true;
  });
}

function pintarFacetas() {
  const cont = $("#facetas");
  cont.innerHTML = "";

  const definiciones = [
    ["accion", "Tipo de evento", (k) => k.replace(/_/g, " ")],
    ["severidad", "Severidad", (k) => k],
    ["regimen", "Régimen", (k) => k],
    ["nivel", "Nivel de riesgo", (k) => k === "SIN_SCORE" ? "Escalado" : k],
    ["cliente", "Cliente", (k) => k],
  ];

  definiciones.forEach(([campo, titulo, etiquetar]) => {
    // El conteo se calcula sobre los eventos que pasan las OTRAS facetas, no
    // sobre el total. Si se contara sobre el total, un valor podria mostrar
    // "12" y al tildarlo devolver cero filas.
    const otras = {};
    Object.entries(estado.facetas).forEach(([c, v]) => { if (c !== campo) otras[c] = v; });
    const base = D.eventos.filter((e) => {
      for (const [c, valores] of Object.entries(otras)) {
        if (!valores.size) continue;
        if (!valores.has(String(e[c] || "(sin dato)"))) return false;
      }
      return true;
    });

    const mapa = contar(base, (e) => String(e[campo] || ""));
    if (!Object.keys(mapa).length) return;

    const caja = el("div", "histo");
    caja.appendChild(el("h4", null, titulo));
    const entradas = Object.entries(mapa).sort((a, b) => b[1] - a[1]).slice(0, 12);
    const tope = Math.max(...entradas.map((e) => e[1]), 1);

    entradas.forEach(([clave, valor]) => {
      const activo = estado.facetas[campo] && estado.facetas[campo].has(clave);
      const fila = el("div", "barra-fila" + (activo ? " activo" : ""));
      if (clave === "ALTA" || clave === "SIN_SCORE") fila.dataset.color = "rojo";
      else if (clave === "MEDIA" || clave === "ALTO") fila.dataset.color = "ambar";

      const et = el("div", "barra-etiqueta");
      const relleno = el("div", "barra-relleno");
      relleno.style.width = (valor / tope * 100) + "%";
      et.appendChild(relleno);
      et.appendChild(el("span", null, etiquetar(clave)));
      fila.appendChild(et);
      fila.appendChild(el("div", "barra-valor", String(valor)));

      fila.onclick = () => {
        if (!estado.facetas[campo]) estado.facetas[campo] = new Set();
        const s = estado.facetas[campo];
        s.has(clave) ? s.delete(clave) : s.add(clave);
        pintarFacetas();
        pintarHistogramaEventos();
        pintarTablaEventos();
      };
      caja.appendChild(fila);
    });
    cont.appendChild(caja);
  });
}

function pintarHistogramaEventos() {
  const cont = $("#histograma-eventos");
  cont.innerHTML = "";
  const eventos = eventosFiltrados();

  const porDia = {};
  eventos.forEach((e) => {
    const d = e.momento.slice(0, 10);
    porDia[d] = porDia[d] || { alta: 0, otras: 0 };
    (String(e.severidad) === "ALTA" ? porDia[d].alta++ : porDia[d].otras++);
  });

  const claves = Object.keys(porDia).sort();
  if (!claves.length) {
    cont.appendChild(el("div", "vacio", "Ningún evento con los filtros puestos."));
    return;
  }

  // El expediente se escribe entero durante la corrida, asi que si el circuito
  // se corrio una sola vez todos los eventos caen el mismo dia y el eje
  // temporal queda en una barra sola. Ahi no sirve de nada, y conviene decir
  // por que en vez de dibujar una barra muda: se muestra el reparto por
  // cliente, que es lo que si tiene forma.
  if (claves.length === 1) {
    cont.appendChild(histogramaPorCliente(eventos, claves[0]));
    return;
  }

  const tope = Math.max(...claves.map((k) => porDia[k].alta + porDia[k].otras), 1);

  const pilas = el("div", "pilas");
  claves.forEach((k) => {
    const v = porDia[k];
    const pila = el("div", "pila");
    pila.title = `${fecha(k)}\n${v.alta + v.otras} evento(s)` +
                 (v.alta ? `\n${v.alta} de severidad alta` : "");
    [["alta", "#e5484d"], ["otras", "#2d4a63"]].forEach(([campo, color]) => {
      if (!v[campo]) return;
      const t = el("div", "tramo");
      t.style.height = (v[campo] / tope * 74) + "px";
      t.style.background = color;
      pila.appendChild(t);
    });
    pilas.appendChild(pila);
  });
  cont.appendChild(pilas);

  const ejes = el("div", "ejes");
  ejes.appendChild(el("span", null, fecha(claves[0])));
  ejes.appendChild(el("span", null, fecha(claves[claves.length - 1])));
  cont.appendChild(ejes);
}

function histogramaPorCliente(eventos, dia) {
  const caja = document.createElement("div");

  const aviso = el("div");
  aviso.style.cssText = "font-size:11px;color:var(--tenue);line-height:1.6;margin-bottom:12px";
  aviso.textContent = "Todos los eventos son del " + fecha(dia) + ": el expediente se " +
    "escribe durante la corrida, asi que el eje temporal no separa nada. " +
    "Abajo va el reparto por cliente.";
  caja.appendChild(aviso);

  const porCliente = {};
  eventos.forEach((e) => {
    porCliente[e.cliente] = porCliente[e.cliente] || { alta: 0, otras: 0 };
    (String(e.severidad) === "ALTA" ? porCliente[e.cliente].alta++
                                    : porCliente[e.cliente].otras++);
  });

  const entradas = Object.entries(porCliente)
    .sort((a, b) => (b[1].alta + b[1].otras) - (a[1].alta + a[1].otras));
  const tope = Math.max(...entradas.map(([, v]) => v.alta + v.otras), 1);

  const pilas = el("div", "pilas");
  entradas.forEach(([nombre, v]) => {
    const pila = el("div", "pila");
    pila.title = nombre + "\n" + (v.alta + v.otras) + " evento(s)" +
                 (v.alta ? "\n" + v.alta + " de severidad alta" : "");
    [["alta", "#e5484d"], ["otras", "#2d4a63"]].forEach(([campo, color]) => {
      if (!v[campo]) return;
      const t = el("div", "tramo");
      t.style.height = (v[campo] / tope * 74) + "px";
      t.style.background = color;
      pila.appendChild(t);
    });
    pila.onclick = () => {
      const cliente = eventos.find((e) => e.cliente === nombre);
      if (!cliente) return;
      seleccionarCliente(cliente.cliente_id);
      location.hash = "ficha";
    };
    pilas.appendChild(pila);
  });
  caja.appendChild(pilas);

  const ejes = el("div", "ejes");
  ejes.appendChild(el("span", null, entradas.length + " cliente(s) con eventos"));
  ejes.appendChild(el("span", null, "rojo: severidad alta"));
  caja.appendChild(ejes);
  return caja;
}


function pintarTablaEventos() {
  const cuerpo = $("#tabla-eventos tbody");
  cuerpo.innerHTML = "";

  const eventos = eventosFiltrados().slice().sort((a, b) => {
    const { campo, asc } = estado.orden;
    const x = String(a[campo] || ""), y = String(b[campo] || "");
    return (x < y ? -1 : x > y ? 1 : 0) * (asc ? 1 : -1);
  });

  $("#conteo-eventos").textContent =
    eventos.length === D.eventos.length
      ? `${eventos.length} eventos`
      : `${eventos.length} de ${D.eventos.length} eventos`;

  eventos.forEach((e) => {
    const critico = String(e.severidad) === "ALTA" ||
                    /CONGELAMIENTO|ESCALADO/.test(e.accion);
    const fila = el("tr", critico ? "fila-critica" : "");
    fila.appendChild(el("td", "mono", momento(e.momento)));

    const tdCliente = el("td");
    const enlace = el("span", null, e.cliente);
    enlace.style.cssText = "cursor:pointer;color:var(--acento)";
    enlace.onclick = () => {
      seleccionarCliente(e.cliente_id);
      location.hash = "ficha";
    };
    tdCliente.appendChild(enlace);
    fila.appendChild(tdCliente);

    fila.appendChild(el("td", null, e.accion.replace(/_/g, " ")));

    const tdNivel = el("td");
    tdNivel.appendChild(insignia(
      e.nivel === "SIN_SCORE" ? "ESCALADO" : e.nivel,
      COLOR_NIVEL[e.nivel] || "neutro"));
    fila.appendChild(tdNivel);

    fila.appendChild(el("td", "detalle", detalleLegible(e.detalle)));
    cuerpo.appendChild(fila);
  });
}

/* ====================== punto de entrada ======================
 * Va al final a proposito. Las utilidades se declaran con const, y una const
 * no existe hasta que se ejecuta su linea: llamar a arrancar() desde arriba
 * rompe con "Cannot access before initialization". */

if (!D) {
  document.getElementById("sin-datos").hidden = false;
} else {
  arrancar();
}
