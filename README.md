# legajo

Automatización del circuito de análisis PLA/FT. Herramienta de escritorio para
equipos de cumplimiento que hoy resuelven el cotejo de listas en planillas.

**Estado: etapas 1 y 2 de 5 — screening, beneficiario final y scoring EBR.**

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
| 2 | Beneficiario final y scoring EBR | ✅ implementada |
| 3 | Perfil declarado vs. operado real | pendiente |
| 4 | Motor de alertas y expediente | pendiente |
| 5 | Export e insumo de ROS | pendiente |

---

## Uso

```bash
pip install -r requirements.txt

# Etapa 1 sola
python -m legajo screening \
  --padron  ejemplos/clientes.csv \
  --listas  ejemplos/listas \
  --salida  informe_screening.xlsx

# Etapas 1 y 2 encadenadas
python -m legajo circuito \
  --padron      ejemplos/clientes.csv \
  --listas      ejemplos/listas \
  --societaria  ejemplos/estructura.csv \
  --peps        ejemplos/peps.txt \
  --salida      informe_circuito.xlsx
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

XLSX de cinco hojas: **Resumen**, **Coincidencias** (priorizadas y coloreadas),
**Expediente** (traza completa de cada caso), **Beneficiario final** y **Riesgo**
(coloreada por nivel).

### Estructura societaria (etapa 2)

Una sola tabla, con una columna `relacion` que despacha el tipo de vínculo:

```
relacion,origen_id,origen_nombre,origen_tipo,destino_id,capital,voto,detalle
PARTICIPACION,P-001,Roberto Iglesias,PERSONA,CL003,0.08,0.08,
PARTICIPACION,SOC-A,Inversora del Plata SA,ENTIDAD,CL003,0.55,0.55,
CONTROL,P-002,Silvia Marconi,PERSONA,CL003,,,acuerdo de accionistas
ADMINISTRACION,P-003,Hector Ledesma,PERSONA,CL003,,,presidente del directorio
```

Acepta `0.60`, `60` y `60%` como el mismo valor.

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

### El umbral del 10% va a la suma, no a cada arista

Éste es el error que hace perder beneficiarios en silencio:

```
Juan ─15%─▶ A ─40%─▶ X     =  6%
Juan ─ 8%─────────▶ X      =  8%
                             ────
                             14%  → ES beneficiario final
```

Podar la arista del 8% durante el recorrido por estar bajo el umbral hace
desaparecer a Juan. El recorrido acumula todos los caminos y el umbral se
aplica recién al final.

### La detección de ciclos es sobre el camino, no global

```
Juan ─50%─▶ A ─30%─▶ X
Juan ─50%─▶ B ─30%─▶ X     Juan = 15% + 15% = 30%
```

Con un conjunto de visitados global, Juan se cuenta una vez y da 15%. La
marca de visitado tiene que ser la rama actual, para que una misma persona
alcanzada por varias ramas sume.

### La titularidad se conserva

Invariante que las pruebas verifican: **beneficiarios + partícipes menores +
titularidad no identificada = 100%**. Si no cierra, hay titularidad perdida
en el recorrido.

Lo que entra en un ciclo se cuenta como no identificado: nunca alcanza una
persona humana, y a efectos de cumplimiento eso es lo mismo que capital no
declarado.

### Capital y voto se acumulan por separado

La Res. 112/2021 dice capital **o** derechos de voto. Alguien con 5% de
capital y 40% de los votos es beneficiario final. Colapsar ambos en un solo
número pierde el caso de las acciones preferidas sin voto, que no es teórico.

### Los elevadores fijan un piso, no suman puntos

"Pero si es PEP entonces siempre alto" termina como un `if` disperso en cinco
lugares del código. Como elevador, es una línea de configuración: ninguna
suma de factores bajos puede dejar en riesgo bajo a un cliente que la
normativa considera de riesgo alto por definición.

### Todo punto de riesgo queda desglosado

Un nivel que no se puede explicar factor por factor no sirve: hay que poder
justificar por qué un cliente quedó en diligencia reforzada. Cada factor
aplicado se registra con su código, su puntaje y su descripción.

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
├── config.py          política de screening: umbrales y atenuantes
├── screening.py       orquestador de la etapa 1
├── societaria.py      grafo de titularidad
├── beneficiario.py    resolución de beneficiario final
├── matriz.py          política de riesgo: factores y elevadores
├── riesgo.py          evaluador EBR
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
- El umbral del 10% se aplica a la suma de caminos, no a cada arista
- Un diamante societario suma las dos ramas
- El voto califica aunque el capital no alcance
- La titularidad se conserva: beneficiarios + menores + opaca = 100%
- Un ciclo no cuelga el recorrido y cuenta como titularidad no identificada
- Un elevador fija el nivel alto aunque el puntaje no alcance
- Cambiar la matriz cambia el resultado sin tocar el evaluador

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
- Las jurisdicciones de riesgo en `matriz.py` deben actualizarse contra la
  publicación vigente del GAFI en cada revisión de la matriz
- La condición de PEP se toma de un archivo declarativo; no hay cotejo
  automático contra un registro de PEP

---

## Licencia

MIT
