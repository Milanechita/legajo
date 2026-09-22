# Decisiones de diseño de legajo

Cada una salió de leer normativa o de medir, y el porqué está al lado.

El [README](../README.md) desarrolla en prosa las nueve que más cambian el
resultado. Esta es la tabla completa, para consulta.

---

## Decisiones de diseño y su fundamento

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
| La regla documental depende del sujeto obligado | Las DDJJ impositivas están **prohibidas** en banco (Res. 78/2025, sustituyó art. 37 de la 14/2023) y son **exigibles** en ALYC (Res. 78/2023 art. 33). Misma pregunta, respuesta opuesta |
| La exigibilidad se declara por materia cuando la norma habla de materias | El art. 33 nombra economía, patrimonio, finanzas y tributos, no documentos. Enumerar documento por documento sería inventar una lista que la norma no escribe |
| Una escala incompleta no responde como si estuviera completa | Devolver cero o False se leería como "el cliente está en regla", que es lo contrario de lo que pasa |
| Las reglas reciben el cliente, no solo la operatoria | Hay reglas que comparan contra lo declarado en el alta. Un segundo motor de reglas al lado del primero se despega en la tercera corrección |
| La alerta de monotributo describe, no acusa | El volumen que ve el banco incluye transferencias entre cuentas propias y préstamos. No es facturación, así que el programa marca la inconsistencia y la conclusión la saca el analista |
| Una ventana corta no se anualiza | Proyectar dos meses por seis da un número que no significa nada, y una alerta que no significa nada entrena al analista a ignorarlas |
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
| `io_planilla.py` no se refactoriza por ahora | Funciona y no es superficie visible. Crece mal, pero reescribir lo que no rompe nada tiene costo y no tiene beneficio |

El screening contra listas no se elimina aunque baje de protagonismo: sigue
siendo obligatorio para todo cliente por la Res. UIF 207/2025 art. 1.

---

## Convenciones del código

Las pruebas se escriben como afirmaciones sobre el dominio y no sobre la
implementación. Toda decisión no obvia lleva un comentario con su porqué, y
varios citan la resolución que la obliga.

---

## Cortes sin calibrar

**SIN CALIBRAR: revisar antes de usar en producción.**

| Parámetro | Dónde | Qué decide |
|---|---|---|
| `factor_monotributo_grave` = 2.0 | `config.py` | Si `MONOTRIBUTO_EXCEDIDO` sale MEDIA o ALTA. Sale de razonar, no de medir. Nadie lo comparó contra operatoria real. Es la severidad que el analista mira primero: si está mal, entierra casos graves entre los medios o llena de ALTA lo que no lo es |

El aviso va en el código, en el parámetro y en el lugar donde se usa.

---

## Parámetros normativos y su vigencia

Cada uno tiene su fecha escrita al lado en el código. Si la fecha está vieja,
los resultados están mal y el programa no avisa.

| Dato | Valor | Cadencia |
|---|---|---|
| SMVM | $383.800, septiembre 2026 | dos veces al año |
| Módulo sancionatorio | $54.140, Res. 95/2025 | por ejercicio presupuestario |
| Listas GAFI | plenario 19 junio 2026 | tres veces al año |
| ARCA no cooperantes | Decreto 398/2026 | por decreto |
| RePET | export de septiembre 2026 | manual, no hay API |
| Escalas de monotributo | A a K, vigencia 1/08/2026 | próxima actualización febrero 2027 |
| Límite de tasa del BCRA | 10 pedidos seguidos, medido 22/09/2026 | si cambia, ajustar `PAUSA_ENTRE_PEDIDOS` |

Las listas reales no están en el repo. Se bajan con
`python -m legajo actualizar-listas --listas <dir>` y pesan unos 9 MB. Las de
`ejemplos/listas` son de juguete, sirven para las pruebas y no para medir.

---

## Límites conocidos de la Res. UIF 78/2023

El sujeto obligado por defecto es banco, con la Res. UIF 14/2023. ALYC existe
como parámetro y tiene dos diferencias que todavía no están implementadas.

**Plazos de reporte, art. 36.** `regimen.py` hoy solo calcula los de banco:
lavado 24 horas desde la conclusión con tope de 90 días, terrorismo 24 horas
sin tope. Para ALYC son otros: lavado 15 días desde que se concluye con tope
de 150 días desde la operación, terrorismo 48 horas desde la operación. Si se
activa ALYC como sujeto obligado, `regimen.py` necesita sus propios plazos
antes de que el cálculo de vencimientos sirva para algo.

**SAS de mayor riesgo, art. 26 inc. g).** Para ALYC las SAS son de mayor
riesgo por definición normativa. Todavía no pondera en el scoring.

**Art. 30, verificado.** El legajo se actualiza cada 1 año en riesgo alto, 3
en medio y 5 en bajo. Coincide con `matriz.MESES_HASTA_REVISION`, que ya
calculaba eso para banco. Hay una prueba que exige que las dos sigan
coincidiendo.

---

## Probado en Windows 11

**La ventana de tkinter.** El layout tenía el `minsize` mal: a 780x640 los
cuatro botones de acción quedaban abajo del borde. El mínimo real es 820x760,
medido widget por widget. Ahí nada se corta y la consola conserva seis
renglones.

**El ejecutable.** Se arma con `build.bat` y arranca. Son 13,4 MB y
PyInstaller lo hace en modo onefile, así que el proceso padre es el bootloader
y la ventana la abre un proceso hijo con el mismo nombre. Buscar la ventana en
el proceso padre no la encuentra.

---

## Lo que falta

1. **El ruido que queda.** La falsa alerta está en 61%, y las que sobran son
   contra entidades: el 90% de las entidades argentinas limpias alerta. Bajar
   `PESO_COBERTURA_CORTA` de 0.60 a 0.45 la lleva a 50%, pero cuesta recall:
   pierde `entidad_sin_ultimo_token` en dos de tres semillas. Medido y no
   aplicado, porque toca la calibración.
2. **Triangulación de fondos** entre cuentas vinculadas. Necesita el grafo de
   contrapartes.
3. **Reportes sistemáticos** RTE, RTI y SROM. Los datos ya están.
4. **Recalcular el riesgo** con el resultado del monitoreo. Hoy el borrador de
   ROS solo marca la inconsistencia.

---

## Material de referencia

`referencias/` guarda capturas de plataformas de terceros usadas como
referencia de diseño. Está en el `.gitignore` y no se publica. El producto se
llama legajo y no usa marcas ajenas en ninguna parte de la interfaz.
