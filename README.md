# legajo

Automatización del circuito de análisis PLA/FT. Herramienta de escritorio para
equipos de cumplimiento que hoy resuelven el cotejo de listas en planillas.

**Estado: Etapa 1 de 5 — screening contra listas de control.**

---

## El problema

Un sujeto obligado tiene que cotejar su padrón de clientes contra listas de
sanciones, terrorismo y PEP, y dejar constancia auditable de qué buscó, contra
qué versión de lista, y qué decidió con cada coincidencia.

En la práctica esto se hace con `BUSCARV` sobre un Excel bajado hace tres meses.
Eso falla de tres formas: no detecta variantes de transliteración, no registra
contra qué versión de la lista se cotejó, y no deja rastro de las decisiones.

Las tres fallas son observables en una inspección.

---

## El circuito completo

```
ALTA ──▶ SCREENING ──▶ SCORING EBR ──▶ ANÁLISIS ──▶ ┬──▶ CERRADO
          (etapa 1)     (etapa 2)       (etapa 3)    └──▶ ESCALADO
```

| Etapa | Alcance | Estado |
|-------|---------|--------|
| 1 | Cotejo contra listas OFAC / ONU / PEP | ✅ implementada |
| 2 | Scoring EBR y beneficiario final | pendiente |
| 3 | Perfil declarado vs. operado real | pendiente |
| 4 | Motor de alertas y expediente | pendiente |
| 5 | Export e insumo de ROS | pendiente |

---

## Uso

```bash
pip install -r requirements.txt

python -m legajo screening \
  --padron  ejemplos/clientes.csv \
  --listas  ejemplos/listas \
  --salida  informe_screening.xlsx \
  --actor   "tiago/analista"
```

Salida:

```
Cargando listas...
  OFAC_SDN pub=s/d reg=5 sha256=1c1c5375071f
  ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=051bd50a4f04

Screening: 8 cliente(s) contra 7 designado(s)

  Coincidencias:        6
  Clientes alcanzados:  5
  Casos escalados:      5

Informe: informe_screening.xlsx
```

### Entrada

CSV o XLSX con estas columnas:

```
cliente_id, nombre, tipo, documento_tipo, documento_numero,
fecha_nacimiento, nacionalidad, pais_residencia, actividad
```

### Salida

XLSX de tres hojas: **Resumen**, **Coincidencias** (priorizadas y coloreadas)
y **Expediente** (traza completa de cada caso).

### Listas

Se descargan aparte y se colocan en el directorio indicado:

| Archivo | Fuente |
|---------|--------|
| `SDN.CSV` + `ALT.CSV` | [OFAC — Tesoro de EE.UU.](https://sanctionslist.ofac.treas.gov/) |
| `consolidated.xml` | [Lista Consolidada — Consejo de Seguridad ONU](https://scsanctions.un.org/resources/xml/en/consolidated.xml) |

El directorio `ejemplos/listas/` trae muestras sintéticas para probar sin
descargar nada.

---

## Decisiones de diseño

### El expediente es el producto, no un log

Una decisión sin trazabilidad no vale nada ante un supervisor. Por eso
`Caso.evidencia` es **append-only**: no se corrige un análisis previo, se agrega
una entrada nueva. El historial es inmutable por construcción, no por disciplina
de quien escribe el código.

### Se registra la versión de cada lista, con hash

"Screeneamos el 3 de marzo" no prueba nada si no consta contra qué versión de la
lista. Si OFAC publicó una actualización el 2 de marzo, el resultado es otro.
Cada corrida graba el SHA-256 del archivo usado.

### Las transiciones de estado son declarativas

Un caso no avanza si le falta la evidencia que el estado destino exige. No hay
que preguntar en cada punto del código si falta documentación: la transición se
rechaza sola. Y `estado` se modifica en un único lugar, así que no existe forma
de cambiarlo sin dejar rastro.

### Mecanismo separado de política

El matcher devuelve un puntaje y no decide nada. Los umbrales viven en
`config.py`. Recalibrar el apetito de riesgo no toca una línea del motor.

### Se calibra para recall, no para precisión

Criterio de dominio, no técnico: **un falso negativo es un incumplimiento con
sanción prevista en el Capítulo IV de la Ley 25.246; un falso positivo es una
hora de trabajo de un analista.** No son errores comparables, y el umbral lo
refleja.

Por el mismo motivo los atenuantes (fecha o nacionalidad discordante) **restan
puntaje pero nunca descartan solos**: las listas tienen campos secundarios
incompletos y contradictorios, y un descarte automático sería un falso negativo
introducido por el propio sistema.

### Entra y sale por Excel

El equipo de cumplimiento trabaja en Excel. Una herramienta que lo obligue a
abandonarlo es la solución teóricamente correcta e inútil en la práctica. La
automatización pasa por debajo; el analista no cambia de entorno.

### N parsers, un registro normalizado, un matcher

El motor de cotejo nunca sabe de qué lista vino un dato. Agregar una lista
nueva es agregar un archivo en `fuentes/`; el matcher no se toca.

---

## Arquitectura

```
                fuentes/ofac.py  ─┐
                fuentes/onu.py   ─┼─▶  Designado  ──▶  matcher.py  ──▶  Coincidencia
                fuentes/<nueva>  ─┘   (normalizado)    (Jaro-Winkler)         │
                                                                              ▼
   padrón (CSV/XLSX)  ──▶  Cliente  ──────────────▶  screening.py  ──▶  Caso.evidencia
                                                      (orquesta)        (append-only)
                                                                              │
                                                                              ▼
                                                                   informe.xlsx (3 hojas)
```

```
legajo/
├── modelo.py          Caso, Evidencia, máquina de estados
├── normalizar.py      canonicalización de nombres
├── matcher.py         Jaro-Winkler y cotejo por tokens
├── config.py          política: umbrales y atenuantes
├── screening.py       orquestador de la etapa 1
├── io_planilla.py     lectura CSV/XLSX y export a Excel
├── cli.py             interfaz de línea de comandos
└── fuentes/
    ├── base.py        Designado, VersionLista, contrato Parser
    ├── ofac.py        parser OFAC SDN
    └── onu.py         parser Lista Consolidada ONU
```

`Jaro-Winkler` está implementado a mano. Son cuarenta líneas, es un algoritmo
cerrado, y una dependencia externa para esto es una dependencia que hay que
auditar, versionar y justificar. La única dependencia del proyecto es `openpyxl`.

---

## Pruebas

```bash
python -m pytest tests/ -q
```

Están escritas como escenarios de dominio, no como pruebas de funciones sueltas.
Los casos que importan:

- Documento idéntico produce coincidencia aunque el nombre no se parezca
- Transliteración alternativa (`Khaled Shaikh Mohamed` ↔ `Khalid Sheikh Mohammed`) se detecta
- Nombres argentinos comunes no generan falsos positivos
- Orden apellido-nombre es irrelevante
- Un dato secundario ausente no penaliza
- Una transición de estado inválida se rechaza
- El expediente registra la procedencia de cada lista

---

## Marco normativo de referencia

- **Ley 25.246** y modificatorias — régimen de encubrimiento y lavado de activos
- **Res. UIF 112/2021** — identificación de beneficiario final (umbral 10%)
- **Res. UIF 3/2026** — financiamiento de la proliferación (FPADM); incorpora el
  ROS FPADM y el congelamiento administrativo sin demora, con las designaciones
  del Consejo de Seguridad de la ONU como fuente
- **Recomendaciones GAFI** — enfoque basado en riesgo

---

## Alcance y limitaciones

Herramienta de análisis, no de decisión. No reemplaza el criterio del oficial de
cumplimiento ni la debida diligencia documental.

Limitaciones conocidas:

- El parser de OFAC extrae identificadores de texto libre (`remarks`) por
  expresión regular; la cobertura no es total
- No resuelve nombres en alfabetos no latinos: opera sobre las transliteraciones
  que publican las listas
- Los umbrales por defecto son un punto de partida, no una calibración: cada
  sujeto obligado debe ajustarlos a su perfil de riesgo y medir el resultado

---

## Licencia

MIT
