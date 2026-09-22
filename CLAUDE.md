# legajo

Herramienta de análisis PLA/FT para el portfolio de Tiago, orientado a puestos
de Analista PLA/FT y Compliance en Argentina.

Las cinco etapas originales están terminadas. Ahora el proyecto se está
reorientando: el screening contra listas internacionales baja de protagonismo
y la pregunta central pasa a ser si la capacidad económica documentada del
cliente justifica lo que opera. El plan está en [ROADMAP.md](ROADMAP.md) y se
frena al terminar cada ítem para revisión.

El screening no se elimina. Sigue siendo obligatorio para todo cliente por la
Res. UIF 207/2025 art. 1.

---

## Antes de escribir código

Tres preguntas, en este orden:

1. **¿Es un problema real o inventado?** Nada de diseño preventivo.
2. **¿Hay una forma más simple?** Buscar la solución mínima.
3. **¿Va a romper algo?** Las pruebas existentes son el contrato.

Si una respuesta sale mal, decirlo y parar. No arrancar a codear igual.

---

## Cómo se trabaja acá

**Medí antes de optimizar.** Los dos hallazgos más valiosos del proyecto
salieron de correr benchmarks, no de leer código. El bug del matcher
unidireccional apareció construyendo el índice y preguntándome por qué los dos
no daban lo mismo.

**Los números van en el commit.** "Mejoré el matcher" no dice nada. "87 falsos
positivos bajaron a 30 conservando los 5 verdaderos positivos" sí.

**Si la medición contradice el diseño, gana la medición.** Ya pasó tres veces
y las tres el diseño estaba mal.

**Las pruebas se escriben como afirmaciones sobre el dominio**, no sobre la
implementación. `test_detectar_el_dia_89_deja_un_dia_de_plazo`, no
`test_vencimiento_returns_date`.

**Toda decisión no obvia va comentada con su porqué.** El código explica qué
hace, el comentario explica por qué así y no de otra forma. Varios comentarios
citan la resolución que obliga a hacerlo de esa manera.

---

## Cómo se escribe

Tiago dirige, prueba y reporta con datos reales. No escribe el código.

**Reglas duras para todo texto del repo** (README, commits, docstrings,
mensajes de la interfaz):

- **Nada de guiones largos.** Verificado en cero en todo el repo. Queda muy
  robot.
- **Nada de punto y coma en prosa.** Dos oraciones o una coma.
- Castellano rioplatense, directo, sin relleno.
- Evitar la estructura "X no es Y, es Z" repetida. Una o dos veces en todo un
  documento, no en cada párrafo.
- Evitar las tríadas paralelas y los párrafos que terminan siempre en aforismo.
- Los comentarios del código van sin tildes, por compatibilidad de encoding.
  La prosa del README sí las lleva.

**Propuestas:** concretas, con nombre, varias opciones y rating de impacto
para el CV. Funciona mejor eliminar de una lista que inventar desde cero.

---

## Decisiones que no se tocan sin discutir

Estas salieron de leer normativa o de medir. Cambiarlas rompe el sentido del
proyecto.

| Decisión | Por qué |
|---|---|
| El padrón es lo declarado, lo verificado va aparte | Una fila de padrón es una declaración. Así "actividad declarada contra inscripta" sale de comparar y no necesita regla propia |
| Las constataciones son append-only | Una corrección es una constatación nueva que tapa a la anterior, nunca un borrado. Sin eso no se puede mostrar qué se verificó y cuándo |
| `campo` de Constatación es enumeración cerrada | Hay una prueba que exige que cada valor exista en `Cliente`. Un renombre rompe la prueba y no el análisis en silencio |
| COMPLETA no se mezcla con DISCREPA | Un campo que el cliente nunca declaró no contradice nada. Juntarlos infla las discrepancias con ruido |
| Los identificadores del ejemplo van fuera del rango asignado | El repo es público. Un CUIT real en una demo de lavado asocia a una persona de verdad con una alerta. Hay una prueba que lo exige |
| Un documento no verificado contra la norma no es opcional | `SIN_VERIFICAR` manda al analista a leer la norma. `OPCIONAL` le diría que ya se miró, y nadie lo miró |
| La API del BCRA nunca se llama desde las pruebas | La descarga entra por parámetro y las pruebas inyectan fixtures. Una suite que depende de un tercero falla los días que el tercero está caído |
| Todo lo que se baja queda con su fecha de consulta | "Está en situación 3" no dice nada sin saber de cuándo es el dato |
| El expediente es append-only | Es el producto. Sin traza no hay nada que mostrarle a una inspección |
| Se calibra para recall, no precisión | Un falso negativo es incumplimiento del Cap. IV. Un falso positivo cuesta una hora |
| El umbral del 10% va a la suma de caminos | Arista por arista permite armar estructuras que lo esquivan |
| Capital y voto se acumulan por separado | La Res. 112/2021 dice capital **o** voto. Promediar esconde el control por voto |
| Las reglas de monitoreo son datos, no ramas | Un motor con cadena de if se pudre y nadie lo toca más |
| El plazo se deriva del régimen | Un campo cargado a mano es un campo que alguien carga mal |
| El sistema no emite ningún ROS | La conversión de inusual a sospechosa es criterio humano (Res. 56/2024) |
| El índice descarta trabajo, no coincidencias | Hay una prueba que corre las dos búsquedas y exige el mismo resultado |
| Un buque no se coteja contra un cliente persona | Un cliente es persona o sociedad, nunca un barco. Baja la falsa alerta de 81% a 61% sin mover el recall en tres semillas |
| El filtro por tipo estricto está descartado | Medido: se lleva un tercio del recall. Pierde unipersonales, tipos mal cargados y buques homónimos de su naviera |
| El visor solo lee, no calcula | Si tuviera lógica del dominio, el visor y la planilla divergen. La que ve una inspección es la planilla |
| `exportar` y `circuito` comparten `circuito.correr` | Dos copias del encadenado de etapas se despegan en la segunda corrección |
| El visor no tiene build ni CDN | Tiene que abrirse con doble clic y andar offline. Cytoscape va copiado en `visor/vendor/` |
| La demo y el export son archivos distintos | `demo.js` es ficticio y se publica. `datos.js` puede tener clientes reales y está ignorado |
| La interfaz es oscura y monoespaciada | Se mira varias horas seguidas. El contraste alto cansa menos que una planilla blanca |
| La interfaz llama a `cli.main` | Si duplicara lógica, las dos versiones divergen y nadie se entera |

---

## Comandos

```bash
python -m pytest tests/ -q          # 302 pruebas, tardan alrededor de un segundo

python -m legajo evaluar --listas <dir> --dificiles evaluacion/casos_dificiles.csv
                                   # recall y falsas alertas, ~1 min con 20 nucleos

python -m legajo circuito \
  --padron ejemplos/clientes.csv --listas ejemplos/listas \
  --societaria ejemplos/estructura.csv --peps ejemplos/peps.csv \
  --operaciones ejemplos/operaciones.csv --perfiles ejemplos/perfiles.csv \
  --salida /tmp/informe.xlsx

python -m legajo bcra --padron ejemplos/clientes_ar.csv --cache cache/bcra
                                   # Central de Deudores, ~2s por cliente

python -m legajo exportar --salida visor/datos.json  # + los mismos args que circuito
                                   # arma el JSON del visor, y abri visor/index.html

python legajo_gui.py               # interfaz de escritorio
build.bat                          # arma dist\legajo.exe (corre las pruebas antes)
```

Una sola dependencia: `openpyxl`. Si algo necesita otra, primero hay que
justificar por qué no alcanza con la biblioteca estándar.

---

## Estado y pendientes

**Terminado:** las cinco etapas, set de evaluación con recall y falsas alertas medidos, 302 pruebas, informe de diez hojas, visor web, interfaz
de escritorio y empaquetado.

**Probado en Windows 11 el 20/09/2026:**

- La ventana de tkinter corre. El layout tenía el `minsize` mal: a 780x640 los
  cuatro botones de acción quedaban abajo del borde. Corregido, y después
  rediseñada con aspecto de consola de análisis. El mínimo real es 820x760,
  medido widget por widget: ahí nada se corta y la consola conserva seis
  renglones. Hay captura en `docs/interfaz.png`.
- El `.exe` se arma con `build.bat` y arranca. Son 13,4 MB y PyInstaller lo
  hace en modo onefile, así que el proceso padre es el bootloader y la ventana
  la abre un proceso hijo con el mismo nombre. Buscar la ventana en el padre no
  la encuentra.

**En curso:** Fase 1 del roadmap. Terminados 1.1 (procedencia), 1.2 (sujeto
obligado), 1.3 (validación de CUIT) y 1.5 (padrón argentino de ejemplo, en
`ejemplos/clientes_ar.csv`). Sujeto obligado por defecto: BANCO, Res. UIF
14/2023.

Terminado también 2.1: Central de Deudores del BCRA, en
`legajo/fuentes/bcra.py`, con caché local y el subcomando `bcra`.

**Frenado por falta de datos normativos:** 1.4 necesita el texto vigente de la
Res. 78/2023 para ALYC, 3.3 las escalas de monotributo, 4.1 el Decreto
253/2018 y 4.2 el Anexo de la Res. 70/2011. No se completan de memoria. 2.2 ya
está investigado y espera decisión, 2.3 necesita saber qué formato tiene el
archivo que baja el analista.

**Pendientes del proyecto viejo, ordenados por valor:**

1. **El ruido que queda.** La falsa alerta está en 61%, y las que sobran son
   contra entidades (90% de las entidades argentinas limpias alertan). Bajar
   `PESO_COBERTURA_CORTA` de 0.60 a 0.45 la lleva a 50%, pero cuesta recall:
   pierde `entidad_sin_ultimo_token` en dos de tres semillas. Medido, no
   aplicado. Hay que discutirlo, porque toca la calibración.
2. **Publicar el visor en GitHub Pages.** Ya está hecho el visor y el juego
   de demostración (`visor/demo.js`). Falta prender Pages desde la raíz del
   repo, y queda en `milanechita.github.io/legajo/visor/`.
3. **Triangulación de fondos** entre cuentas vinculadas. Necesita el grafo de
   contrapartes.
4. **Reportes sistemáticos** RTE, RTI y SROM. Los datos ya están.
5. **Recalcular el riesgo** con el resultado del monitoreo. Hoy el borrador de
   ROS solo marca la inconsistencia.

**Referencias visuales:** `referencias/` tiene capturas de plataformas de
terceros usadas como referencia de diseño. Está en el `.gitignore` y no se
publica. El producto se llama legajo y no usa marcas ajenas en ningún lado.

**Lo que NO hay que hacer:** refactorizar `io_planilla.py` aunque esté
creciendo mal. Nadie lo ve y funciona.

---

## Datos que hay que mantener al día

Cada parámetro tiene su fecha escrita al lado en el código. Si la fecha está
vieja, los resultados están mal y el programa no avisa.

| Dato | Valor actual | Cadencia |
|---|---|---|
| SMVM | $383.800, septiembre 2026 | dos veces al año |
| Módulo sancionatorio | $54.140, Res. 95/2025 | por ejercicio presupuestario |
| Listas GAFI | plenario 19 junio 2026 | tres veces al año |
| ARCA no cooperantes | Decreto 398/2026 | por decreto |
| RePET | export de septiembre 2026 | manual, no hay API |
| Límite de tasa del BCRA | 10 pedidos seguidos, medido 22/09/2026 | si cambia, ajustar `PAUSA_ENTRE_PEDIDOS` |

Las listas reales no están en el repo. Se bajan con
`python -m legajo actualizar-listas --listas <dir>` y pesan unos 9 MB.
Las de `ejemplos/listas` son de juguete, sirven para las pruebas y no para medir.

---

## Contexto del repo

- GitHub: `github.com/Milanechita/legajo`, público, MIT
- 28 módulos, unas 5.800 líneas
- Python, sin frameworks
- Los commits son largos y explican el porqué, no el qué
