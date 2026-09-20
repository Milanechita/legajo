# legajo

Circuito de análisis PLA/FT en Python. Cotejo contra listas de sanciones,
beneficiario final sobre la cadena societaria, scoring de riesgo, monitoreo
transaccional y armado de ROS.

Todo con expediente auditable y una sola dependencia externa.

```
        padrón                    listas de control
     clientes.csv            OFAC · ONU Consolidada · RePET
           │                             │
           └──────────────┬──────────────┘
                          ▼
              ╔═══════════════════════╗
              ║  1   SCREENING        ║   cotejo por nombre y documento
              ╚═══════════╤═══════════╝
                          ▼
              ╔═══════════════════════╗
              ║  2   BENEFICIARIO     ║   cadena societaria al 10%
              ║      FINAL Y RIESGO   ║   scoring EBR + PEP
              ╚═══════════╤═══════════╝
                          ▼
              ╔═══════════════════════╗
              ║  3   MONITOREO        ║   perfil declarado vs operado
              ╚═══════════╤═══════════╝
                          ▼
              ╔═══════════════════════╗
              ║  4   PLAZOS Y         ║   LA / FT / FPADM
              ║      CONGELAMIENTO    ║   exposición sancionatoria
              ╚═══════════╤═══════════╝
                          ▼
              ╔═══════════════════════╗
              ║  5   ROS              ║   borradores + inusuales
              ╚═══════════╤═══════════╝
                          ▼
                   informe.xlsx
                     10 hojas
```

---

## Por qué existe

Los avisos de Analista PLA/FT en Argentina piden siempre lo mismo. Cotejar
clientes contra listas de sanciones, identificar al beneficiario final,
scorear el riesgo, monitorear las operaciones y preparar el ROS.

Casi todos esos pasos se resuelven con un Excel a mano o con un software caro
que nadie termina de entender. Este proyecto los codifica de punta a punta y
deja documentado por qué cada decisión está donde está.

Lo que **no** hace: emitir reportes. Eso se carga en el SRO+ de la UIF y
necesita la conclusión de una persona. Más abajo está el detalle.

---

## Cómo se usa

```bash
pip install openpyxl
```

**Bajar las listas** (OFAC y ONU tienen fuente oficial, RePET va a mano)

```bash
python -m legajo actualizar-listas --listas listas/
```

**Correr el circuito**

```bash
python -m legajo circuito \
  --padron       ejemplos/clientes.csv \
  --listas       ejemplos/listas \
  --societaria   ejemplos/estructura.csv \
  --peps         ejemplos/peps.csv \
  --operaciones  ejemplos/operaciones.csv \
  --perfiles     ejemplos/perfiles.csv \
  --salida       informe.xlsx
```

**Armar los ROS**, después de que el analista complete las decisiones en Excel

```bash
python -m legajo ros --informe informe.xlsx \
  --padron ejemplos/clientes.csv --listas ejemplos/listas \
  --operaciones ejemplos/operaciones.csv --perfiles ejemplos/perfiles.csv
```

Sale así:

```
[1/4] Screening: 15 cliente(s) contra 725 designado(s)
      23 coincidencia(s), 5 escalado(s)

[2/4] Beneficiario final y scoring EBR
      7 estructura(s) analizada(s)
      4 declaracion(es) de PEP, 1 vencida(s) por el plazo de 2 anios

[3/4] Monitoreo transaccional
      119 operacion(es) de 6 cliente(s), 5 perfil(es) declarado(s)
      umbral de reporte: $15.352.000 (40 SMVM, Res. 78/2025)

[4/4] Congelamiento administrativo
      5 obligacion(es), reporte dentro de 24hs

  Alertas de monitoreo: 15 sobre 5 cliente(s), 8 de severidad alta
  ATENCION: 5 alerta(s) con el plazo de reporte ya vencido

  Exposicion sancionatoria estimada: $262.266.267
```

---

## Interfaz de escritorio

Para quien no quiere tocar la terminal hay una ventana con selectores de
archivo, la consola embebida y un botón para abrir el informe cuando termina.

```
  ┌────────────────────────────────────────────────────────────┐
  │  legajo                                                    │
  │  Screening, beneficiario final, riesgo, monitoreo y ROS    │
  │                                                            │
  │  ┌─ Archivos de entrada ──────────────────────────────┐   │
  │  │  Padrón de clientes  *  [ clientes.csv    ] Examinar│   │
  │  │  Carpeta de listas   *  [ listas/         ] Examinar│   │
  │  │  Estructura societaria  [ estructura.csv  ] Examinar│   │
  │  │  Operatoria             [ operaciones.csv ] Examinar│   │
  │  └────────────────────────────────────────────────────┘   │
  │                                                            │
  │  [ Correr circuito ] [ Armar ROS ]      [ Abrir informe ]  │
  │                                                            │
  │  ┌─ Salida ───────────────────────────────────────────┐   │
  │  │ [1/4] Screening: 15 cliente(s) contra 725           │   │
  │  │ [4/4] Congelamiento administrativo                  │   │
  │  │ ATENCION: 5 alerta(s) con el plazo vencido          │   │
  │  └────────────────────────────────────────────────────┘   │
  └────────────────────────────────────────────────────────────┘
```

La interfaz no reimplementa nada. Arma la línea de comandos y llama al mismo
`cli.main` que usa la terminal, capturando lo que imprime.

Si la lógica viviera duplicada ahí adentro, en la segunda corrección las dos
versiones empezarían a dar resultados distintos y nadie se enteraría hasta que
un informe salga mal.

**Correrla desde el código**

```bash
python legajo_gui.py
```

**Armar el ejecutable**

```bash
build.bat      # Windows  ->  dist\legajo.exe
./build.sh     # Linux o macOS
```

El script corre las pruebas antes de empaquetar y aborta si alguna falla. Un
ejecutable que sale de código roto es peor que no tenerlo.

Queda un solo archivo que anda sin Python instalado. Usa tkinter, que viene
con Python, así que no arrastra ninguna dependencia gráfica.

---

## Entrada y salida

Entra CSV o XLSX. Sale un XLSX de diez hojas.

| Hoja | Qué tiene |
|------|-----------|
| Resumen | una fila por cliente con su estado |
| Coincidencias | cada hit con score, criterio y atenuantes |
| Expediente | la traza completa, append-only |
| Beneficiario final | quién controla cada estructura |
| Riesgo | puntaje desglosado factor por factor |
| Alertas | registro de operaciones inusuales |
| Congelamiento | obligaciones y checklist, con aviso de reserva |
| Exposición | cuánto cuesta no reportar |
| Borradores ROS | insumo para cargar en el SRO+ |
| Inusuales justificadas | las que se decidió no reportar |

<details>
<summary><b>Formato de los archivos de entrada</b></summary>

**Padrón de clientes**

```
cliente_id,nombre,tipo,doc_tipo,doc_numero,fecha_nacimiento,nacionalidad,pais_residencia,actividad,pep
CL001,Juan Perez,PERSONA,DNI,28456123,1981-04-12,Argentina,Argentina,Comercio,no
CL003,Petroquímica del Sur S.A.,ENTIDAD,CUIT,30712345678,,,Argentina,Industria,no
```

**Estructura societaria**, una fila por participación

```
entidad_id,participe_id,participe_nombre,participe_tipo,capital,voto,documento
CL003,H01,Holding Andes SA,ENTIDAD,0.60,0.60,CUIT:30999888777
H01,P01,Ricardo Salas,PERSONA,0.50,0.50,DNI:20111222
```

**Declaraciones juradas de PEP**

```
cliente_id,tipo,cargo,fecha_cese,por_parentesco
CL010,EXTRANJERA,Ministro de Estado,,no
CL011,EXTRANJERA,Direccion de empresa estatal,2019-03-31,no
```

**Operatoria**, una fila por operación

```
cliente_id,fecha,monto,sentido,instrumento,canal,contraparte,pais_contraparte
CL005,2026-07-13,14891440,INGRESO,EFECTIVO,PRESENCIAL,Deposito por ventanilla,Argentina
```

**Perfiles transaccionales**, lo que el cliente declaró al alta

```
cliente_id,monto_mensual,operaciones_mensuales,proporcion_efectivo,paises,origen_fondos,proposito
CL005,900000,4,0.10,Argentina,Sueldo en relacion de dependencia,Caja de ahorro
```

Los montos aceptan `1234.56`, `1.234,56` y `$ 1.234,56`.

</details>

---

## De dónde salen las listas

| Lista | Fuente | Cómo se obtiene |
|-------|--------|-----------------|
| OFAC SDN + alias | Tesoro de EE.UU. | descarga automática |
| ONU Consolidada | Consejo de Seguridad | descarga automática |
| UK Sanctions List | FCDO | descarga automática |
| RePET | Registro argentino | export manual |

RePET es la excepción. Es la lista que la normativa argentina nombra por su
nombre y no publica ningún endpoint, solo tiene buscador web. Hay que
exportarla y cargarla.

Se suele suponer que RePET copia el listado de la ONU y que por lo tanto no
aporta nada. Los datos dicen otra cosa. Sobre el export de septiembre de 2026,
de 718 registros:

```
ONU (Al-Qaida y Talibán)  ████████████████████████░░░░░░░░░  469
Origen local              ████████████░░░░░░░░░░░░░░░░░░░░░  249
```

Ese resto son congelamientos de la UIF, Notificaciones Rojas de INTERPOL, la
causa AMIA y actuaciones de PROCELAC. Un tercio del registro que no está en
ninguna otra lista del mundo.

---

## Las decisiones que importan

Hay muchas decisiones chicas comentadas en el código. Estas son las que
cambian el resultado.

### El expediente es el producto

El output no es "el cliente coincidió". Es el legajo entero: cuándo se cotejó,
contra qué versión de qué lista, con qué umbral, quién lo revisó y qué
resolvió.

Cuando viene una inspección, la pregunta no es si detectaste. Es si podés
demostrar cómo detectaste. La evidencia es append-only y no se puede editar
después.

Cada corrida graba el SHA-256 de la lista que usó. Sin eso, "el cliente no
figuraba en marzo" es una afirmación sin respaldo.

### Se calibra para recall, no para precisión

Un falso negativo es un designado que pasó el filtro. Eso es incumplimiento
del Capítulo IV de la Ley 25.246 y puede terminar en sanción.

Un falso positivo le cuesta una hora a un analista.

Los dos errores no valen lo mismo, así que el sistema prefiere equivocarse
hacia el ruido. Umbrales bajos y atenuantes que bajan la prioridad en vez de
descartar.

### El 10% va a la suma de caminos, no a cada arista

Si alguien tiene 6% por una sociedad y 5% por otra, tiene 11% y es
beneficiario final. Evaluar arista por arista permite armar estructuras que
esquivan el umbral quedándose justo abajo en cada rama.

```
        Juan
       ╱     ╲
    6%╱       ╲5%
     ╱         ╲
  Holding A  Holding B
     ╲         ╱
      ╲       ╱
       ╲     ╱
       Cliente        ←  Juan tiene 11%, no dos participaciones chicas
```

La detección de ciclos va sobre el camino actual, no global. Un diamante
societario no es un ciclo, son dos caminos distintos al mismo nodo, y los dos
suman.

### El 10% no siempre es 10%

Para entidades del exterior sin oferta pública el umbral es 0%. Hay que
identificar a todos los beneficiarios, no a los que superen un piso.

Y si la entidad hace oferta pública en un mercado autorizado, queda exceptuada
del requisito. Que el umbral sea función de la entidad y no una constante es
lo que hace que esto no se pueda hardcodear.

### Capital y voto se acumulan por separado

La Res. 112/2021 dice capital **o** derechos de voto. Promediar los dos
esconde justamente la estructura que interesa, que es participación chica con
control de voto.

### Las reglas de monitoreo son datos

Los motores de reglas se pudren siempre igual. Una función por tipología, cada
una recorriendo las operaciones a su manera, y a los seis meses nadie sabe qué
dispara qué. El equipo deja de tocarlo y las tipologías nuevas no entran más.

Acá una regla es una entrada del catálogo con forma uniforme. El motor recorre
el catálogo y no sabe qué hace ninguna. Agregar una tipología es agregar una
línea.

### Una regla puede estar apagada, y hay que decir por qué

`MONTOS_REDONDOS` es una tipología real. La operatoria genuina deja decimales,
la armada usa cifras redondas.

En Argentina dispara sobre operatoria normal, porque por el orden de magnitud
nominal los importes redondos son comunes. Queda en el catálogo, apagada, con
el motivo escrito al lado.

Una regla ruidosa entrena al analista a cerrar alertas sin leerlas. A partir
de ahí el sistema entero deja de servir, no solo esa regla.

### Detectar tarde no regala plazo

Tres regímenes, tres plazos distintos.

| Régimen | Plazo |
|---------|-------|
| Lavado de activos | 24hs desde que se concluye, tope de 90 días desde la operación |
| Financiación del terrorismo | 24hs desde la operación |
| Financiamiento de la proliferación | 24hs desde la operación |

El tope de 90 días corre desde que la operación fue realizada. Un análisis que
empieza el día 89 tiene un día, no noventa.

Eso salió al correr el motor sobre los fixtures. Operaciones de marzo
detectadas en septiembre ya tienen el plazo vencido, así que el sistema las
marca en rojo en vez de mostrar noventa días por delante.

### Un congelamiento no se analiza, se ejecuta

Cuando hay coincidencia firme con una persona designada, lo que sigue no es
una alerta más en la cola:

```
  1.  congelar sin demora e inaudita parte
  2.  informar inmediatamente a la UIF
  3.  reportar dentro de 24 horas
  4.  cotejar el resto de la base de clientes
  5.  inmovilizar lo que ingrese después
  6.  NO informarle al cliente
```

El paso 6 no es un detalle. La hoja sale con advertencia de reserva en la
primera fila, porque un informe que circule sin esa marca es un aviso
esperando ocurrir.

Los pasos salen sin cumplir. Marcarlos de oficio sería documentar un
cumplimiento que no ocurrió.

### Una alerta sin su costo es un pendiente más

La Res. 129/2024 art. 35 liquida la falta de ROS por **una vez el valor total
de la operación**. No es multa fija ni porcentaje.

```
no reportar un ROS .......  1 × el monto de la operación
incumplimiento total .....  30 módulos  =  $1.624.200
incumplimiento parcial ...  25 módulos  =  $1.353.500
```

Calcular eso convierte cada alerta en un número. Es la diferencia entre
"tenemos 15 alertas pendientes" y "tenemos $262 millones de exposición", y es
lo que consigue que cumplimiento tenga presupuesto.

### El sistema no emite ningún ROS

Los reportes se cargan por el SRO+ de la UIF. Pero hay una razón más de fondo
que la operativa.

La Res. 56/2024 define operación sospechosa como la que ocasiona sospecha de
origen ilícito, o que **habiéndose identificado previamente como inusual,
luego del análisis del sujeto obligado, no permite justificar la
inusualidad**.

La inusualidad la detecta el sistema. El salto a sospecha necesita un análisis
humano que no la justifique. Automatizar eso sería fabricar una conclusión que
nadie sacó.

Entonces el fundamento sale así:

```
FUNDAMENTO DE LA SOSPECHA
  [PENDIENTE: la inusualidad no se justificó por los siguientes motivos...]
```

Marcado, no rellenado con una frase plausible.

### El informe va y vuelve

```
   sistema  ──▶  informe.xlsx con las columnas de decisión vacías
                              │
                              ▼
                     el analista resuelve en Excel
                              │
                              ▼
   sistema  ◀──  borradores de ROS + registro de inusuales
```

El equipo de cumplimiento trabaja en Excel y ahí se queda. Obligarlo a cargar
las conclusiones en otra herramienta es la solución prolija que nadie usa.

Las inusualidades que **no** se reportan también van a registro, con su
análisis. Sin eso el monitoreo no se puede auditar, porque no hay forma de
distinguir una alerta bien resuelta de una que nadie miró.

---

## Lo que encontré midiendo

Las dos cosas de abajo no aparecieron leyendo el código. Aparecieron corriendo
benchmarks y preguntándome por qué los números no cerraban.

### El matcher medía media evidencia

El puntaje promediaba sobre el conjunto de tokens más corto, o sea medía
cuánto del nombre corto quedaba explicado por el largo. Con eso, un designado
de una sola palabra matcheaba contra casi cualquier nombre:

```
79.2   "Ana Rodriguez Diaz"  vs  "Ajnad"    ← cruzaba el umbral de 78
49.2   "Juan Perez Gomez"    vs  "Khalid Sheikh Mohammed"
```

"Ajnad" queda bien explicado por "Ana". Pero "Ana Rodriguez Diaz" queda
explicado en un tercio, y esa mitad de la evidencia no se puede ignorar.

El padrón tiene **216 designados de un solo token**, muchos de ellos
organizaciones. El defecto era sistemático.

Midiendo las dos coberturas, sobre 250 nombres argentinos comunes:

```
falsos positivos      87  ──▶  30
verdaderos positivos  5/5 ──▶  5/5
```

Y la corrección salió gratis. Medir las dos direcciones duplicaba las llamadas
a Jaro-Winkler, hasta que vi que las dos coberturas salen de la misma matriz.
Máximos por fila para una, máximos por columna para la otra.

### El índice descarta trabajo, no coincidencias

El screening es cuadrático. Cada cliente contra cada nombre y alias del
padrón, que proyectado a 50.000 clientes son unas dos horas.

El índice tiene dos caminos porque el matcher tiene dos caminos.

```
documento  ──▶  diccionario exacto, O(1)
nombre     ──▶  trigramas de cada token
```

Mezclarlos perdería coincidencias. Un cliente que coincide por pasaporte con
un designado de nombre completamente distinto es un hit válido, y un índice
construido sobre nombres lo descartaría sin dejar rastro.

Probé exigir dos trigramas compartidos, tres y más. Todos filtran mejor y
pierden coincidencias:

| mínimo | selectividad | recall |
|--------|--------------|--------|
| 2 | 42% | 99.6% ← pierde |
| 1 | 56% | **100%** |

Pares como `RAHMAN` contra `EMRAAN` comparten un solo trigrama y aun así
puntúan arriba del umbral. Jaro-Winkler y el solapamiento de trigramas miden
cosas distintas, y no hay umbral que los haga equivalentes.

Entre filtrar mejor y no perder nada, en screening gana no perder nada.

### Y el error que cometí

Me fui derecho al índice porque era el problema interesante. El profile decía
otra cosa:

```
jaro          43%   ← 3.194.640 llamadas para 60 clientes
normalizar    15%   ← los mismos 2.681 nombres, una vez por cliente
```

Estaba normalizando el padrón entero de nuevo para cada cliente. Trabajo
repetido que no cambia nunca.

```
antes     118 min   proyectado a 50.000 clientes
después    64 min   con recall del 100%
```

### Cuánto ruido cuesta el recall

Decir que el sistema está calibrado para recall era una afirmación. Ahora hay
un comando que la mide, `python -m legajo evaluar`, contra las listas reales
(20.404 designados de OFAC y ONU al 19 de septiembre de 2026).

Hay dos conjuntos y se reportan separados. El sintético se genera desde la
lista real con semilla fija: designados con el orden cambiado, sin el nombre
del medio, con iniciales, con un error de tipeo o por alias, más clientes
argentinos comunes y homónimos parciales como negativos. El difícil son 26
casos escritos a mano en `evaluacion/casos_dificiles.csv`, con
transliteraciones como `Khaled Sheikh Mohamed` o `Hizbullah`.

```
umbral   recall   precisión   falsa alerta
    78    99,2%      64,5%          81,9%   <- revisión
    85    97,1%      82,9%          30,0%
    92    82,5%      98,0%           2,5%   <- probable
```

El recall aguanta. Los 18 casos difíciles positivos salen detectados, y en el
sintético solo se pierden 2 de 240, ambos del tipo "sin nombre del medio".

El costo está del otro lado. Con el umbral de revisión en 78, el 82% de los
clientes limpios genera al menos una alerta, unas 7,5 en promedio. Los
nombres argentinos comunes chocan con designados de una sola palabra
(`ROMINA`, `CAROL`, `ARIA`) y con nombres de buques. De las 985 alertas sobre
clientes limpios, 386 son contra buques y 558 contra entidades.
Solo 41 son contra personas.

Cómo leer estos números: el recall es contra el modelo de error que armé yo,
no contra el mundo. Las perturbaciones las elegí yo y un padrón real puede
fallar de maneras que no imaginé. Y los negativos no son una muestra de un
padrón de clientes real. Sirven para comparar cambios entre sí, no para
prometer una tasa de alertas.

---

## Arquitectura

```
legajo/
├── modelo.py          Cliente, Caso, Evidencia, máquina de estados
├── normalizar.py      limpieza de nombres y documentos
├── matcher.py         Jaro-Winkler y puntaje bidireccional por tokens
├── indice.py          índice invertido: documentos y trigramas de token
├── screening.py       motor de cotejo y atenuantes
├── beneficiario.py    recorrido de la cadena societaria
├── matriz.py          política de riesgo: factores y elevadores
├── riesgo.py          evaluador EBR
├── paises.py          normalización a código ISO
├── pep.py             tipificación y vigencia de la condición PEP
├── operaciones.py     operatoria, perfil y ventanas deslizantes
├── alertas.py         catálogo de tipologías y motor de monitoreo
├── regimen.py         LA, FT y FPADM: plazos y derivación
├── congelamiento.py   obligaciones de congelamiento administrativo
├── sanciones.py       módulo, liquidación y exposición estimada
├── ros.py             borradores de reporte y registro de inusuales
├── config.py          política, SMVM y umbrales normativos
├── io_planilla.py     lectura y escritura de planillas
├── cli.py             comandos
└── fuentes/           un parser por lista

legajo_gui.py          interfaz de escritorio
legajo.spec            receta de empaquetado
build.bat / build.sh   armado del ejecutable
```

Una sola dependencia, `openpyxl`, para leer y escribir Excel. El resto es
biblioteca estándar, incluido Jaro-Winkler.

---

## Pruebas

```bash
python -m pytest tests/ -q
```

Son 200 y están escritas como afirmaciones sobre el dominio, no sobre la
implementación. Algunas de las que más valor tienen:

- Un cliente y un designado con distinto nombre pero mismo documento coinciden
- Cambiar la matriz de riesgo cambia el resultado sin tocar el evaluador
- Una tilde o un apóstrofo no rompen el cotejo geográfico
- Un designado de una sola palabra no matchea contra cualquier nombre
- El índice devuelve exactamente lo mismo que la búsqueda exhaustiva
- Cinco depósitos bajo el umbral en una semana se detectan como fraccionamiento
- Cuatrocientos depósitos chicos no lo son
- Una ventana corrida un día no genera una alerta nueva
- Operar dentro del perfil declarado no genera ninguna alerta
- Detectar el día 89 deja un día de plazo, no noventa
- Tres coincidencias del mismo régimen son una sola obligación de congelamiento
- Una coincidencia débil no congela los bienes de nadie
- Sin la conclusión del analista el borrador queda incompleto y lo dice
- Una justificada sin análisis documentado se marca como hallazgo

---

## Marco normativo

- **Ley 25.246** y modificatorias, en particular la **Ley 27.739**
- **Res. UIF 112/2021**, beneficiario final
- **Res. UIF 35/2023** y **192/2024**, personas expuestas políticamente
- **Res. UIF 56/2024**, plazos de reporte y operaciones inusuales
- **Res. UIF 78/2025**, umbrales de reporte en efectivo
- **Res. UIF 84/2023**, el SMVM como parámetro de actualización
- **Res. UIF 95/2025**, valor del módulo
- **Res. UIF 129/2024**, liquidación del procedimiento abreviado
- **Res. UIF 207/2025** y **3/2026**, congelamiento por FT y FPADM
- **Decreto 918/2012** y **Ley 26.734 art. 6**
- **Decreto 862/2019** según **Decreto 398/2026**, jurisdicciones no cooperantes
- **Recomendaciones GAFI**, enfoque basado en riesgo

---

## Lo que no hace

Esto es una herramienta de análisis, no un sistema de cumplimiento
certificado. Las decisiones las toma una persona.

- **No emite reportes.** Prepara el insumo, la carga va por el SRO+ de la UIF
- **No congela nada.** Identifica la obligación y arma el checklist
- **No se conecta a ningún core bancario.** La extracción de la operatoria es
  responsabilidad de quien lo use
- **Las listas hay que actualizarlas.** GAFI publica tres veces al año, el
  SMVM se fija dos veces, el módulo por ejercicio presupuestario. Cada
  parámetro tiene su fecha escrita al lado en el código
- **RePET depende de un export manual**, porque no hay fuente en formato
  máquina
- **No recalcula el riesgo** con el resultado del monitoreo. Marca la
  inconsistencia y ahí queda
- **No hay set de casos etiquetados**, así que "calibrado para recall" sigue
  siendo una afirmación sin métrica de precisión y recall detrás. Es el
  agujero más grande que le queda

---

## Licencia

MIT.
