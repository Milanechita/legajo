# Roadmap

El proyecto nació orientado al screening contra listas internacionales. En una
ALYC o un banco argentino eso es una parte chica del trabajo. La pregunta
central del analista es otra:

> ¿La capacidad económica documentada del cliente justifica lo que opera?

Este roadmap reorienta el programa al análisis del perfil del cliente
argentino con toda la información disponible.

Se frena al terminar cada ítem para revisión.

---

## Reglas que no cambian

- **El screening sigue siendo obligatorio.** RePET y ONU se cotejan para todo
  cliente (Res. UIF 207/2025 art. 1). Baja de protagonismo en la interfaz, no
  se elimina.
- **Nada de datos inventados.** Escalas de monotributo, umbrales y cualquier
  valor normativo van como parámetro con fecha y norma, igual que el SMVM. Si
  no están a mano, se piden. No se completan de memoria.
- **Nosis y Veraz no se integran por API.** Se importa el archivo que baja el
  analista.
- **Los CUIT ficticios de la demo van en rango no asignado.** DNI desde
  99.000.000 para personas humanas, con dígito verificador válido. El repo es
  público y no se puede asociar por accidente el CUIT de una persona real a
  una alerta de lavado.
- **DDJJ impositivas.** La Res. UIF 78/2025 prohíbe requerirlas a entidades
  financieras (sustituyó el art. 37 de la Res. 14/2023). Para ALYC rige la
  Res. 78/2023, hay que verificar su texto vigente antes de decidir. El
  sistema nunca marca como faltante un documento que la norma no permite
  pedir.
- **La API del BCRA nunca se llama desde las pruebas.** Fixtures locales y
  caché con fecha de consulta.

---

## Fase 1 · Fundaciones

| | Ítem |
|---|---|
| 1.1 | Procedencia de cada dato: fuente, fecha, declarado o verificado |
| 1.2 | Tipo de sujeto obligado como parámetro (banco, ALYC): resolución aplicable, umbrales y documentos exigibles |
| 1.3 | Validación de CUIT/CUIL: dígito verificador y prefijo contra tipo de persona |
| 1.4 | Catálogo de documentos: exigible, prohibido y vencimiento de cada uno, por tipo de sujeto obligado |
| 1.5 | Padrón de ejemplo argentino: 30 a 40 clientes típicos (monotributistas, RI, empleados, jubilados, SAS, SRL, SA), con dos o tres hits en listas para que el screening siga visible |

## Fase 2 · Fuentes

| | Ítem |
|---|---|
| 2.1 | BCRA Central de Deudores (api.bcra.gob.ar, sin autenticación): deudas, históricas y cheques rechazados. Caché local |
| 2.2 | Condición tributaria ARCA. Antes de implementar, averiguar qué fuente pública existe hoy y reportarlo |
| 2.3 | Importador de informes comerciales desde archivo |

## Fase 3 · Perfil económico

| | Ítem |
|---|---|
| 3.1 | Capacidad económica documentada: monto anual justificado por documento, con reglas por tipo de documento |
| 3.2 | Regla nueva: capacidad documentada vs operado |
| 3.3 | Monotributo: categoría vs volumen anualizado |
| 3.4 | Actividad declarada vs actividad inscripta en ARCA |
| 3.5 | Personas jurídicas: ventas del balance vs operado, y antigüedad |
| 3.6 | Recalcular el riesgo con el resultado del monitoreo y las fuentes |

## Fase 4 · Señales argentinas

| | Ítem |
|---|---|
| 4.1 | Domicilio en zona de frontera. **Aproximación por provincia**, ver nota |
| 4.2 | Cliente sujeto obligado sin constancia de inscripción UIF (Anexo Res. 70/2011) |
| 4.3 | Domicilio, teléfono o email compartido entre clientes |
| 4.4 | Persona que integra cinco o más sociedades (Res. 70/2011 art. 11) |
| 4.5 | Situación BCRA 3 o peor operando montos altos |

**Nota sobre 4.1.** El Decreto 253/2018 no trae una lista de partidos: define
la zona por descripción cartográfica (ríos, rutas, coordenadas), con un anexo
distinto por provincia. Sacar de ahí una lista de partidos confiable exige
transcribir el PDF oficial, que es un trabajo aparte.

Se acordó una aproximación explícita a nivel provincia, con las dieciséis que
limitan con otro país: Misiones, Corrientes, Entre Ríos, Chaco, Formosa,
Salta, Jujuy, Catamarca, La Rioja, San Juan, Mendoza, Neuquén, Río Negro,
Chubut, Santa Cruz y Tierra del Fuego.

La señal se llama `ZONA_FRONTERA_PROVINCIA`. La precisión va en el nombre y no
en una constante aparte, para que el código se explique solo si alguien lo
lista sin mirar comentarios. Nunca se muestra como si fuera el dato exacto del
decreto. La precisión a nivel partido queda pendiente hasta transcribir el
anexo oficial.

## Fase 5 · Legajo

| | Ítem |
|---|---|
| 5.1 | Checklist de legajo por tipo de cliente |
| 5.2 | Vencimientos de documentos y de actualización del legajo |

## Fase 6 · Visor

| | Ítem |
|---|---|
| 6.1 | Ficha con "capacidad vs operado" como gráfico principal, semáforo de documentación y situación BCRA |
| 6.2 | Filtros: provincia, condición IVA, categoría, situación BCRA, sujeto obligado, legajo incompleto |
| 6.3 | Cifras de la barra superior: perfil excedido, legajo incompleto, BCRA 3+, riesgo alto, plazos vencidos, exposición |
| 6.4 | Grafo: domicilios y personas compartidas como nodos |

## Fase 7 · Calibración

| | Ítem |
|---|---|
| 7.1 | Set de casos etiquetados con métricas de precisión y recall |

**Casos que le faltan al set.** Los tres monotributistas de
`ejemplos/operaciones_ar.csv` son todos "excede sistemático", que es el caso
fácil. Faltan dos:

- **Caso límite:** justo 1,05 veces el tope. Sirve para ver si el corte de
  severidad y el mínimo de meses se comportan en el borde.
- **Exceso puntual y explicable:** la venta de un bien, una sola vez, que
  levanta el anualizado sin que haya actividad sostenida. Es el caso que el
  modelo de capacidad tiene que saber distinguir de un exceso recurrente.

También se calibra acá el `factor_monotributo_grave`, hoy marcado
**SIN CALIBRAR: revisar antes de usar en producción**.
