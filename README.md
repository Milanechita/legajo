# legajo

Herramienta para automatizar el circuito de análisis PLA/FT. Está pensada para
equipos de cumplimiento que hoy resuelven el cotejo de listas y el armado del
legajo con planillas y búsquedas manuales.

**Estado actual: etapas 1 y 2 de 5.** Screening contra listas, resolución de
beneficiario final y scoring de riesgo.

---

## Por qué existe

Un sujeto obligado tiene que cotejar su padrón de clientes contra las listas de
sanciones, terrorismo y PEP. Tiene que identificar quién controla realmente a
sus clientes personas jurídicas. Y tiene que poder demostrarle a un supervisor
qué controló, contra qué versión de cada lista, y por qué decidió lo que
decidió.

En la práctica eso se hace con `BUSCARV` sobre un Excel que alguien bajó hace
tres meses. Falla de tres maneras, y las tres se notan en una inspección: no
detecta variantes de transliteración, no deja constancia de contra qué versión
de la lista se cotejó, y no guarda el razonamiento detrás de cada decisión.

---

## El circuito completo

```
ALTA ──▶ SCREENING ──▶ SCORING EBR ──▶ ANÁLISIS ──▶ ┬──▶ CERRADO
          (etapa 1)     (etapa 2)       (etapa 3)    └──▶ ESCALADO
```

| Etapa | Alcance | Estado |
|-------|---------|--------|
| 1 | Cotejo contra listas OFAC, ONU y RePET | ✅ implementada |
| 2 | Beneficiario final y scoring EBR | ✅ implementada |
| 3 | Perfil declarado contra operado real | pendiente |
| 4 | Motor de alertas y expediente consolidado | pendiente |
| 5 | Export e insumo de ROS | pendiente |

---

## Uso

```bash
pip install -r requirements.txt

# Bajar las listas desde las fuentes oficiales
python -m legajo actualizar-listas --listas listas/

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
  --peps        ejemplos/peps.csv \
  --salida      informe_circuito.xlsx
```

Salida típica:

```
[1/2] Screening: 12 cliente(s) contra 7 designado(s)
      6 coincidencia(s), 5 escalado(s)

[2/2] Beneficiario final y scoring EBR
      5 estructura(s) analizada(s)
      4 declaracion(es) de PEP, 1 vencida(s) por el plazo de 2 anios

  Distribucion de riesgo
    ALTO       2
    MEDIO      1
    BAJO       4
    escalado   5   (no scoreados: coincidencia en lista critica)
```

---

## De dónde salen las listas

Las que importan para un sujeto obligado argentino son públicas y no piden
credenciales. No hay que registrarse ni pedir API key.

| Lista | Fuente | Acceso |
|-------|--------|--------|
| OFAC SDN más alias | Sanctions List Service del Tesoro de EE.UU. | libre |
| ONU Consolidada | Consejo de Seguridad, XML público | libre |
| UK Sanctions List | FCDO, opcional para Argentina | libre |

El comando `actualizar-listas` las baja, calcula el SHA-256 de cada archivo y
lo deja registrado. Si una descarga falla, el archivo anterior queda intacto.
Screenear con una lista vieja es malo, pero screenear con una lista a medias es
peor.

**RePET es la excepción y conviene decirlo claro.** Es la lista que la
normativa argentina nombra por su nombre, y no publica ningún endpoint de
datos: solo tiene buscador web en `repet.jus.gob.ar`. Para cotejar un padrón
entero hay que exportarla desde un redistribuidor (OpenSanctions publica el
dataset `ar_repet` actualizado a diario) o cargarla a mano. El parser acepta
los dos formatos.

Hay algo más que vale aclarar sobre RePET. Incorpora el listado consolidado de
la ONU, así que en la práctica se superpone casi por completo con lo que ya
estamos cotejando. Lo que agrega son las designaciones de origen local, que son
las personas con resolución judicial o del Ministerio Público Fiscal y aquellas
sobre las que la UIF ordenó congelamiento administrativo. Esas no figuran en
ninguna otra lista, y por eso el cotejo sigue siendo obligatorio.

---

## Entrada y salida

Entra CSV o XLSX, sale un XLSX de cinco hojas: Resumen, Coincidencias,
Expediente, Beneficiario final y Riesgo.

### Padrón de clientes

```
cliente_id, nombre, tipo, documento_tipo, documento_numero,
fecha_nacimiento, nacionalidad, pais_residencia, actividad, oferta_publica
```

### Estructura societaria

Una sola tabla con una columna `relacion` que despacha el tipo de vínculo:

```
relacion,origen_id,origen_nombre,origen_tipo,origen_jurisdiccion,origen_oferta_publica,destino_id,capital,voto,detalle
PARTICIPACION,P-001,Roberto Iglesias,PERSONA,AR,no,CL003,0.08,0.08,
PARTICIPACION,SOC-A,Inversora del Plata SA,ENTIDAD,AR,no,CL003,0.55,0.55,
CONTROL,P-002,Silvia Marconi,PERSONA,AR,no,CL003,,,acuerdo de accionistas
ADMINISTRACION,P-003,Hector Ledesma,PERSONA,AR,no,CL003,,,presidente del directorio
```

Acepta `0.60`, `60` y `60%` como el mismo valor.

### Declaraciones juradas de PEP

```
cliente_id,tipo,cargo,fecha_cese,por_parentesco
CL009,NACIONAL,Legislador provincial,,no
CL010,EXTRANJERA,Ministro de Estado,,no
CL011,EXTRANJERA,Direccion de empresa estatal,2019-03-31,no
CL012,NACIONAL,Conyuge de intendente,,si
```

---

## Decisiones de diseño

### El expediente es el producto, no un registro secundario

Una decisión sin trazabilidad no le sirve a nadie cuando llega una supervisión.
Por eso `Caso.evidencia` solo crece: no se corrige un análisis previo, se
agrega una entrada nueva. El historial queda inmutable por construcción y no
por disciplina de quien escribe el código.

### Se guarda el hash de cada lista

"Screeneamos el 3 de marzo" no prueba nada si no consta contra qué versión de
la lista. Si OFAC publicó una actualización el 2 de marzo, el resultado es
otro. Cada corrida graba el SHA-256 del archivo que usó.

### Las transiciones de estado son declarativas

Un caso no avanza si le falta la evidencia que el estado destino exige. No hay
que preguntar en cada punto del código si falta documentación, porque la
transición se rechaza sola. Y como `estado` se modifica en un único lugar, no
existe forma de cambiarlo sin dejar rastro.

### Los umbrales son configuración, no código

El matcher devuelve un puntaje y no decide nada. Los umbrales viven en
`config.py` y la matriz de riesgo en `matriz.py`. Recalibrar el apetito de
riesgo de un sujeto obligado no toca una línea del motor.

### Se calibra para recall, no para precisión

Esto es criterio de dominio antes que técnico. Un falso negativo es un
incumplimiento con sanción prevista en el Capítulo IV de la Ley 25.246. Un
falso positivo es una hora de trabajo de un analista. No son errores
comparables y el umbral lo refleja.

Por el mismo motivo los atenuantes (fecha o nacionalidad discordante) restan
puntaje pero nunca descartan solos. Las listas tienen campos secundarios
incompletos y contradictorios, así que un descarte automático sería un falso
negativo que introduce el propio sistema.

### El umbral del 10% va a la suma, no a cada arista

Este es el error que hace perder beneficiarios en silencio:

```
Juan ─15%─▶ A ─40%─▶ X     =  6%
Juan ─ 8%─────────▶ X      =  8%
                             ────
                             14%  → ES beneficiario final
```

Podar la arista del 8% durante el recorrido, por estar debajo del umbral, hace
desaparecer a Juan. El recorrido acumula todos los caminos y el umbral se
aplica recién al final.

### La detección de ciclos es sobre el camino, no global

```
Juan ─50%─▶ A ─30%─▶ X
Juan ─50%─▶ B ─30%─▶ X     Juan = 15% + 15% = 30%
```

Con un conjunto de visitados global, Juan se cuenta una sola vez y da 15%. La
marca de visitado tiene que ser la rama actual, para que una misma persona
alcanzada por varias ramas sume.

### El 10% no siempre es 10%

La regla general tiene dos excepciones escritas en la normativa que una
implementación con constante se saltea.

Para entidades constituidas o radicadas en el exterior que no hacen oferta
pública de sus títulos, el umbral no corresponde y hay que identificar a la
totalidad de los beneficiarios. Una sociedad que sí hace oferta pública queda
exceptuada del requisito, porque ya está sujeta a un régimen propio de
transparencia.

La consecuencia práctica se ve mejor con un ejemplo. La misma estructura, con
un tenedor del 6%, da distinto según dónde esté constituida la entidad: en una
sociedad argentina es partícipe menor, en una offshore es beneficiario final.

Por eso el umbral es una función de la entidad y no una constante. Se calcula
una vez al entrar y el recorrido no cambia ni una línea.

### La titularidad se conserva

Invariante que verifican las pruebas: beneficiarios más partícipes menores más
titularidad no identificada siempre da 100%. Si no cierra, hay titularidad
perdida en el recorrido.

Lo que entra en un ciclo se cuenta como no identificado, porque nunca alcanza
una persona humana. A efectos de cumplimiento eso es lo mismo que capital no
declarado.

### Capital y voto se acumulan por separado

La normativa dice capital **o** derechos de voto. Alguien con 5% de capital y
40% de los votos es beneficiario final. Si se colapsan los dos en un solo
número se pierde el caso de las acciones preferidas sin voto, que no es
hipotético.

### PEP extranjera y PEP nacional no son lo mismo

Una PEP extranjera es cliente de alto riesgo por definición normativa. Una PEP
nacional se evalúa según su riesgo concreto, igual que cualquier otro cliente.

Tratarlas igual produce dos errores en direcciones opuestas: deja pasar a una
PEP extranjera que sumó pocos puntos, y manda a diligencia reforzada a un
concejal municipal que no tiene ningún otro factor de riesgo.

La condición además vence. Se mantiene mientras se ejerce el cargo y hasta dos
años después del cese. Un ex funcionario que cesó en 2019 hoy no es PEP, y
seguir tratándolo como tal es ruido que le cuesta horas al analista. El dato
igual no se borra del archivo, porque sirve para el expediente.

### Los elevadores fijan un piso en lugar de sumar puntos

"Pero si es PEP extranjera entonces siempre alto" termina como un `if` disperso
en cinco lugares del código. Como elevador es una línea de configuración, y
garantiza que ninguna suma de factores bajos deje en riesgo bajo a un cliente
que la normativa considera de riesgo alto.

### Todo punto de riesgo queda desglosado

Un nivel que no se puede explicar factor por factor no sirve, porque hay que
poder justificar por qué un cliente quedó en diligencia reforzada. Cada factor
aplicado se registra con su código, su puntaje y su descripción.

### La periodicidad de revisión sale del nivel de riesgo

Riesgo alto se revisa cada 12 meses, medio cada 36, bajo cada 60. Calcular la
fecha a partir del nivel, y no desde una agenda separada, evita que el plazo y
el riesgo se desincronicen.

### Entra y sale por Excel

El equipo de cumplimiento trabaja en Excel. Una herramienta que lo obligue a
abandonarlo es la solución teóricamente correcta e inútil en la práctica. La
automatización pasa por debajo y el analista no cambia de entorno.

### N parsers, un registro normalizado, un matcher

El motor de cotejo nunca sabe de qué lista vino un dato. Agregar una lista
nueva es agregar un archivo en `fuentes/`, sin tocar el matcher.

---

## Arquitectura

```
   fuentes/ofac.py   ─┐
   fuentes/onu.py    ─┼──▶  Designado  ──▶  matcher.py
   fuentes/repet.py  ─┤    (normalizado)   (Jaro-Winkler)
   fuentes/<nueva>   ─┘                          │
                                                 ▼
   padrón            ──▶  Cliente   ─┬──▶  screening.py      Caso.evidencia
   estructura        ──▶  Grafo     ─┼──▶  beneficiario.py   (append-only)
   declaraciones PEP ──▶  PEP       ─┴──▶  riesgo.py                │
                                                                    ▼
                                                        informe.xlsx (5 hojas)
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
├── pep.py             tipificación y vigencia de la condición PEP
├── matriz.py          política de riesgo: factores, elevadores, periodicidad
├── riesgo.py          evaluador EBR
├── io_planilla.py     lectura CSV/XLSX y export a Excel
├── cli.py             interfaz de línea de comandos
└── fuentes/
    ├── base.py        Designado, VersionLista, contrato Parser
    ├── descarga.py    bajada desde las fuentes oficiales
    ├── ofac.py        parser OFAC SDN
    ├── onu.py         parser Lista Consolidada ONU
    └── repet.py       parser RePET
```

Jaro-Winkler está implementado a mano. Son cuarenta líneas de un algoritmo
cerrado, y una dependencia externa para eso es una dependencia que después hay
que auditar, versionar y justificar. La única dependencia del proyecto es
`openpyxl`.

---

## Pruebas

```bash
python -m pytest tests/ -q
```

Son 61 y están escritas como escenarios de dominio, no como pruebas de
funciones sueltas. Las que importan:

- El umbral del 10% se aplica a la suma de caminos y no a cada arista
- Un diamante societario suma las dos ramas en lugar de contar una sola vez
- El voto califica aunque el capital no alcance
- La titularidad se conserva: beneficiarios más menores más opaca da 100%
- Un ciclo no cuelga el recorrido y cuenta como titularidad no identificada
- El mismo 6% es partícipe menor en una sociedad local y beneficiario final en
  una del exterior
- Una sociedad con oferta pública queda exceptuada
- Una PEP extranjera eleva a alto riesgo y una nacional no
- Una PEP que cesó hace más de dos años deja de aplicarse
- Las transliteraciones alternativas se detectan y los nombres comunes no
  generan falsos positivos
- El expediente registra la procedencia de cada lista
- Cambiar la matriz cambia el resultado sin tocar el evaluador

---

## Marco normativo de referencia

- **Ley 25.246** y modificatorias, régimen de encubrimiento y lavado de activos
- **Res. UIF 112/2021**, identificación de beneficiario final y umbral del 10%
- **Res. UIF 192/2024**, nómina de personas expuestas políticamente
- **Res. UIF 207/2025**, listas antiterroristas y congelamiento administrativo
- **Res. UIF 3/2026**, financiamiento de la proliferación de armas de
  destrucción masiva, con el ROS FPADM
- **Decreto 918/2012 y 489/2019**, creación del RePET
- **Recomendaciones GAFI**, enfoque basado en riesgo

---

## Alcance y limitaciones

Es una herramienta de análisis, no de decisión. No reemplaza el criterio del
oficial de cumplimiento ni la debida diligencia documental.

Lo que conviene saber antes de usarla:

- El parser de OFAC extrae identificadores desde texto libre con expresiones
  regulares, así que la cobertura no es total
- No resuelve nombres en alfabetos no latinos y opera sobre las
  transliteraciones que publican las listas
- RePET depende de una exportación manual o de un redistribuidor, porque no
  hay fuente oficial en formato máquina
- Los umbrales por defecto son un punto de partida y no una calibración. Cada
  sujeto obligado tiene que ajustarlos a su perfil de riesgo y medir el
  resultado
- Las jurisdicciones de riesgo en `matriz.py` hay que actualizarlas contra la
  publicación vigente del GAFI en cada revisión de la matriz
- La condición de PEP se toma de declaraciones juradas. No hay cotejo
  automático contra un registro de PEP porque en Argentina no existe uno
  público consolidado

---

## Licencia

MIT
