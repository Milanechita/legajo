window.DEMO_DATOS = {
 "formato": 1,
 "meta": {
  "generado": "2026-09-21T00:30:12",
  "listas": [
   "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
   "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
   "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
   "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
  ],
  "designados": 725,
  "clientes": 15,
  "umbral_revision": 78.0,
  "umbral_probable": 92.0,
  "umbral_reporte": 15352000.0,
  "smvm": 383800.0,
  "smvm_vigencia": "2026-09-01"
 },
 "resumen": {
  "riesgo": {
   "ALTO": 4,
   "MEDIO": 2,
   "BAJO": 4
  },
  "escalados": 5,
  "coincidencias": 23,
  "probables": 5,
  "alertas": 15,
  "alertas_vencidas": 5,
  "congelamientos": 5,
  "operaciones": 119,
  "exposicion_total": 197399033.6
 },
 "exposicion": {
  "total": 197399033.6,
  "por_falta_de_reporte": 185217533.6,
  "por_incumplimientos": 12181500.0,
  "modulo": 54140.0,
  "modulo_vigencia": "2025-06-19",
  "cargos": [
   {
    "concepto": "ROS no emitido, María González",
    "materia": "Reporte de Operaciones Sospechosas",
    "modulos": null,
    "monto": 72768480.0,
    "fundamento": "Res. UIF 129/2024 art. 35 inc. 1, Ley 25.246 art. 21 inc. b"
   },
   {
    "concepto": "ROS no emitido, Ana Beatriz Rodríguez",
    "materia": "Reporte de Operaciones Sospechosas",
    "modulos": null,
    "monto": 41726479.52,
    "fundamento": "Res. UIF 129/2024 art. 35 inc. 1, Ley 25.246 art. 21 inc. b"
   },
   {
    "concepto": "ROS no emitido, Fernanda Ortiz",
    "materia": "Reporte de Operaciones Sospechosas",
    "modulos": null,
    "monto": 13671014.67,
    "fundamento": "Res. UIF 129/2024 art. 35 inc. 1, Ley 25.246 art. 21 inc. b"
   },
   {
    "concepto": "ROS no emitido, Nadia Haddad",
    "materia": "Reporte de Operaciones Sospechosas",
    "modulos": null,
    "monto": 33914747.72,
    "fundamento": "Res. UIF 129/2024 art. 35 inc. 1, Ley 25.246 art. 21 inc. b"
   },
   {
    "concepto": "ROS no emitido, Sark Trust Services",
    "materia": "Reporte de Operaciones Sospechosas",
    "modulos": null,
    "monto": 23136811.69,
    "fundamento": "Res. UIF 129/2024 art. 35 inc. 1, Ley 25.246 art. 21 inc. b"
   },
   {
    "concepto": "Incumplimiento total en Listados de Terroristas",
    "materia": "Listados de Terroristas",
    "modulos": 30.0,
    "monto": 1624200.0,
    "fundamento": "Res. UIF 129/2024 art. 35 inc. 2"
   },
   {
    "concepto": "Incumplimiento total en Listados de Terroristas",
    "materia": "Listados de Terroristas",
    "modulos": 30.0,
    "monto": 1624200.0,
    "fundamento": "Res. UIF 129/2024 art. 35 inc. 2"
   },
   {
    "concepto": "Incumplimiento total en Listados de Terroristas",
    "materia": "Listados de Terroristas",
    "modulos": 30.0,
    "monto": 1624200.0,
    "fundamento": "Res. UIF 129/2024 art. 35 inc. 2"
   },
   {
    "concepto": "Incumplimiento total en Listados de Terroristas",
    "materia": "Listados de Terroristas",
    "modulos": 30.0,
    "monto": 1624200.0,
    "fundamento": "Res. UIF 129/2024 art. 35 inc. 2"
   },
   {
    "concepto": "Incumplimiento total en Listados de Terroristas",
    "materia": "Listados de Terroristas",
    "modulos": 30.0,
    "monto": 1624200.0,
    "fundamento": "Res. UIF 129/2024 art. 35 inc. 2"
   },
   {
    "concepto": "Incumplimiento parcial en Monitoreo",
    "materia": "Monitoreo",
    "modulos": 25.0,
    "monto": 1353500.0,
    "fundamento": "Res. UIF 129/2024 art. 35 inc. 3"
   },
   {
    "concepto": "Incumplimiento parcial en Beneficiario Final",
    "materia": "Beneficiario Final",
    "modulos": 25.0,
    "monto": 1353500.0,
    "fundamento": "Res. UIF 129/2024 art. 35 inc. 3"
   },
   {
    "concepto": "Incumplimiento parcial en Beneficiario Final",
    "materia": "Beneficiario Final",
    "modulos": 25.0,
    "monto": 1353500.0,
    "fundamento": "Res. UIF 129/2024 art. 35 inc. 3"
   }
  ]
 },
 "clientes": [
  {
   "id": "CL001",
   "caso_id": "C00001",
   "nombre": "Juan Pérez",
   "tipo": "PERSONA",
   "documentos": [
    "DNI 28456123"
   ],
   "fecha_nacimiento": "1980-05-12",
   "nacionalidad": "ARGENTINA",
   "pais_residencia": "ARGENTINA",
   "pais_residencia_iso": "AR",
   "riesgo_pais": "ORDINARIA",
   "actividad": "Comercio minorista",
   "oferta_publica": false,
   "estado": "CERRADO",
   "escalado": false,
   "riesgo": {
    "puntaje": 0,
    "nivel": "BAJO",
    "regimen": "DD_SIMPLIFICADA",
    "revision_meses": 60,
    "factores": [],
    "elevadores": []
   },
   "coincidencias": [],
   "congelamiento": null,
   "beneficiario": null,
   "pep": null,
   "alertas": [],
   "operatoria": {
    "cantidad": 24,
    "total": 6627605.13,
    "efectivo": 0,
    "proporcion_efectivo": 0.0,
    "desde": "2026-03-02",
    "hasta": "2026-08-10",
    "paises": [
     "AR"
    ],
    "contrapartes": [
     "Proveedor local"
    ]
   },
   "perfil": {
    "monto_mensual": 1500000.0,
    "operaciones_mensuales": 5,
    "proporcion_efectivo": 0.05,
    "paises": [
     "AR"
    ],
    "origen_fondos": "Actividad comercial",
    "proposito": "Cobros y pagos de proveedores"
   },
   "exposicion": 0,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SIN_COINCIDENCIAS",
     "detalle": {}
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "SCORING",
      "motivo": "sin coincidencias en listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "SCORING_EBR",
     "detalle": {
      "puntaje": 0,
      "nivel": "BAJO",
      "regimen": "DD_SIMPLIFICADA",
      "factores": [],
      "elevadores": [],
      "proxima_revision": "2031-09-21"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCORING",
      "destino": "CERRADO",
      "motivo": "riesgo bajo (0 pts), DD_SIMPLIFICADA"
     }
    }
   ],
   "nota": "Persona humana. Riesgo BAJO con 0 puntos, regimen dd simplificada, revision cada 60 meses."
  },
  {
   "id": "CL002",
   "caso_id": "C00002",
   "nombre": "Alireza Abbas",
   "tipo": "PERSONA",
   "documentos": [
    "PASAPORTE K1234567"
   ],
   "fecha_nacimiento": "1965-01-12",
   "nacionalidad": "IRAN",
   "pais_residencia": "IRAN",
   "pais_residencia_iso": "IR",
   "riesgo_pais": "ALTO_RIESGO",
   "actividad": "Importación",
   "oferta_publica": false,
   "estado": "ESCALADO",
   "escalado": true,
   "riesgo": {
    "puntaje": 0.0,
    "nivel": "SIN_SCORE",
    "regimen": "",
    "revision_meses": 0,
    "factores": [],
    "elevadores": []
   },
   "coincidencias": [
    {
     "lista": "OFAC_SDN",
     "id_origen": "36",
     "designado": "ABBAS, Ali Reza",
     "matcheado": "PASAPORTE:K1234567",
     "score": 100.0,
     "criterio": "DOCUMENTO",
     "probable": true,
     "programas": [
      "SDGT"
     ],
     "atenuantes": []
    },
    {
     "lista": "ONU_CONSOLIDADA",
     "id_origen": "6908001",
     "designado": "Ali Reza Abbas",
     "matcheado": "PASAPORTE:K1234567",
     "score": 100.0,
     "criterio": "DOCUMENTO",
     "probable": true,
     "programas": [
      "Iran"
     ],
     "atenuantes": []
    },
    {
     "lista": "REPET",
     "id_origen": "2975591",
     "designado": "ABDUL AZIZ ABBASIN",
     "matcheado": "ABDUL AZIZ ABBASIN",
     "score": 82.6,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "ONU",
      "Taliban",
      "TAi.155"
     ],
     "atenuantes": []
    },
    {
     "lista": "REPET",
     "id_origen": "119",
     "designado": "HAYTHAM ALL TABATABA `I",
     "matcheado": "Abu Ali Al-TABATABA `I; Abu Ali TABATABAI; Abu Ali TABTABAI",
     "score": 78.9,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "LOCAL",
      "SDN - EEUU"
     ],
     "atenuantes": []
    },
    {
     "lista": "REPET",
     "id_origen": "9",
     "designado": "Alí Akbar Velayati",
     "matcheado": "Alí Akbar Velayati",
     "score": 78.6,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "LOCAL",
      "UFI AMIA",
      "HArP.00009"
     ],
     "atenuantes": []
    },
    {
     "lista": "REPET",
     "id_origen": "29",
     "designado": "MOUSA HATEM BARAKAT",
     "matcheado": "ABU ALI BARAKAT",
     "score": 78.4,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "LOCAL",
      "U.I.F"
     ],
     "atenuantes": []
    },
    {
     "lista": "REPET",
     "id_origen": "69",
     "designado": "MOUSA HATEM BARAKAT",
     "matcheado": "ABU ALI BARAKAT",
     "score": 78.4,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "LOCAL",
      "Unidad de Información Financiera"
     ],
     "atenuantes": []
    }
   ],
   "congelamiento": {
    "regimen": "FPADM",
    "lista": "ONU_CONSOLIDADA",
    "designado": "Ali Reza Abbas",
    "score": 100.0,
    "criterio": "DOCUMENTO",
    "norma": "Res. UIF 3/2026, Ley 25.246 art. 14 inc. 12",
    "detectado": "2026-09-21",
    "pasos": [
     {
      "codigo": "COTEJAR_BASE",
      "descripcion": "cotejar la base de clientes e informar si hubo operaciones con la persona o entidad designada",
      "cumplido": false
     },
     {
      "codigo": "INMOVILIZAR",
      "descripcion": "inmovilizar los bienes u otros activos que sean propiedad o esten controlados, directa o indirectamente, por la designada, o cuyo destinatario o beneficiario sea",
      "cumplido": false
     },
     {
      "codigo": "INFORMAR_UIF",
      "descripcion": "informar inmediatamente a la UIF la aplicacion de la medida",
      "cumplido": false
     },
     {
      "codigo": "EMITIR_REPORTE",
      "descripcion": "emitir el reporte de operacion sospechosa sin demora alguna",
      "cumplido": false
     },
     {
      "codigo": "INFORMAR_RESULTADOS",
      "descripcion": "informar los resultados dentro de las 24 horas de notificada la resolucion, por el sistema Reporte Orden de Congelamiento",
      "cumplido": false
     },
     {
      "codigo": "MONITOREAR_POSTERIORES",
      "descripcion": "informar e inmovilizar las operaciones tentadas con posterioridad, mientras la medida siga vigente",
      "cumplido": false
     },
     {
      "codigo": "RESERVA",
      "descripcion": "abstenerse de informar al cliente o a terceros los antecedentes de la resolucion; solo puede indicarse que los bienes estan congelados en virtud del art. 6 de la Ley 26.734",
      "cumplido": false
     }
    ]
   },
   "beneficiario": null,
   "pep": null,
   "alertas": [],
   "operatoria": null,
   "perfil": null,
   "exposicion": 0,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "OFAC_SDN",
      "id_origen": "36",
      "designado": "ABBAS, Ali Reza",
      "matcheo_contra": "PASAPORTE:K1234567",
      "score": 100.0,
      "criterio": "DOCUMENTO",
      "atenuantes": [],
      "programas": [
       "SDGT"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "ONU_CONSOLIDADA",
      "id_origen": "6908001",
      "designado": "Ali Reza Abbas",
      "matcheo_contra": "PASAPORTE:K1234567",
      "score": 100.0,
      "criterio": "DOCUMENTO",
      "atenuantes": [],
      "programas": [
       "Iran"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "2975591",
      "designado": "ABDUL AZIZ ABBASIN",
      "matcheo_contra": "ABDUL AZIZ ABBASIN",
      "score": 82.6,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "ONU",
       "Taliban",
       "TAi.155"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "119",
      "designado": "HAYTHAM ALL TABATABA `I",
      "matcheo_contra": "Abu Ali Al-TABATABA `I; Abu Ali TABATABAI; Abu Ali TABTABAI",
      "score": 78.9,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "LOCAL",
       "SDN - EEUU"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "9",
      "designado": "Alí Akbar Velayati",
      "matcheo_contra": "Alí Akbar Velayati",
      "score": 78.6,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "LOCAL",
       "UFI AMIA",
       "HArP.00009"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "29",
      "designado": "MOUSA HATEM BARAKAT",
      "matcheo_contra": "ABU ALI BARAKAT",
      "score": 78.4,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "LOCAL",
       "U.I.F"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "69",
      "designado": "MOUSA HATEM BARAKAT",
      "matcheo_contra": "ABU ALI BARAKAT",
      "score": 78.4,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "LOCAL",
       "Unidad de Información Financiera"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "ESCALADO",
      "motivo": "coincidencia en lista critica (OFAC_SDN, score 100.0)"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "CONGELAMIENTO_REQUERIDO",
     "detalle": {
      "regimen": "FPADM",
      "lista": "ONU_CONSOLIDADA",
      "designado": "Ali Reza Abbas",
      "norma": "Res. UIF 3/2026, Ley 25.246 art. 14 inc. 12",
      "plazo": "24 horas",
      "reserva": "prohibido informar al cliente"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "CONGELAMIENTO_REQUERIDO",
     "detalle": {
      "regimen": "FT",
      "lista": "OFAC_SDN",
      "designado": "ABBAS, Ali Reza",
      "norma": "Res. UIF 207/2025, Decreto 918/2012, Ley 26.734 art. 6",
      "plazo": "24 horas",
      "reserva": "prohibido informar al cliente"
     }
    }
   ],
   "nota": "Persona humana. El caso esta escalado y no paso por scoring: una coincidencia en lista critica se escala sin ponderar, asi que no tiene puntaje ni regimen asignado. Coincidencia probable contra ABBAS, Ali Reza en OFAC_SDN, score 100 por documento y 1 coincidencia mas. Obligacion de congelamiento por regimen FPADM, Res. UIF 3/2026, Ley 25.246 art. 14 inc. 12. Se ejecuta sin demora y se reporta dentro de las 24 horas. Prohibido informar al cliente. Queda a criterio del analista: ejecutar el congelamiento y reportarlo, confirmar o descartar la coincidencia contra la lista."
  },
  {
   "id": "CL003",
   "caso_id": "C00003",
   "nombre": "Petroquímica del Sur S.A.",
   "tipo": "ENTIDAD",
   "documentos": [
    "CUIT 30-71234567-8"
   ],
   "fecha_nacimiento": null,
   "nacionalidad": null,
   "pais_residencia": "ARGENTINA",
   "pais_residencia_iso": "AR",
   "riesgo_pais": "ORDINARIA",
   "actividad": "Industria química",
   "oferta_publica": false,
   "estado": "ESCALADO",
   "escalado": true,
   "riesgo": {
    "puntaje": 0.0,
    "nivel": "SIN_SCORE",
    "regimen": "",
    "revision_meses": 0,
    "factores": [],
    "elevadores": []
   },
   "coincidencias": [
    {
     "lista": "OFAC_SDN",
     "id_origen": "1201",
     "designado": "PETROQUIMICA DEL SUR SA",
     "matcheado": "PETROQUIMICA DEL SUR SA",
     "score": 100.0,
     "criterio": "NOMBRE",
     "probable": true,
     "programas": [
      "NPWMD"
     ],
     "atenuantes": []
    }
   ],
   "congelamiento": {
    "regimen": "FPADM",
    "lista": "OFAC_SDN",
    "designado": "PETROQUIMICA DEL SUR SA",
    "score": 100.0,
    "criterio": "NOMBRE",
    "norma": "Res. UIF 3/2026, Ley 25.246 art. 14 inc. 12",
    "detectado": "2026-09-21",
    "pasos": [
     {
      "codigo": "COTEJAR_BASE",
      "descripcion": "cotejar la base de clientes e informar si hubo operaciones con la persona o entidad designada",
      "cumplido": false
     },
     {
      "codigo": "INMOVILIZAR",
      "descripcion": "inmovilizar los bienes u otros activos que sean propiedad o esten controlados, directa o indirectamente, por la designada, o cuyo destinatario o beneficiario sea",
      "cumplido": false
     },
     {
      "codigo": "INFORMAR_UIF",
      "descripcion": "informar inmediatamente a la UIF la aplicacion de la medida",
      "cumplido": false
     },
     {
      "codigo": "EMITIR_REPORTE",
      "descripcion": "emitir el reporte de operacion sospechosa sin demora alguna",
      "cumplido": false
     },
     {
      "codigo": "INFORMAR_RESULTADOS",
      "descripcion": "informar los resultados dentro de las 24 horas de notificada la resolucion, por el sistema Reporte Orden de Congelamiento",
      "cumplido": false
     },
     {
      "codigo": "MONITOREAR_POSTERIORES",
      "descripcion": "informar e inmovilizar las operaciones tentadas con posterioridad, mientras la medida siga vigente",
      "cumplido": false
     },
     {
      "codigo": "RESERVA",
      "descripcion": "abstenerse de informar al cliente o a terceros los antecedentes de la resolucion; solo puede indicarse que los bienes estan congelados en virtud del art. 6 de la Ley 26.734",
      "cumplido": false
     }
    ]
   },
   "beneficiario": {
    "identificado": true,
    "exceptuada": false,
    "opaco": 0.37,
    "profundidad": 1,
    "umbral": 0.1,
    "beneficiarios": [
     {
      "id": "P-002",
      "nombre": "Silvia Marconi",
      "capital": 0.33,
      "voto": 0.33,
      "via": "PARTICIPACION",
      "detalle": "33.00% via Petroquímica del Sur S.A. -> Inversora del Plata SA"
     },
     {
      "id": "P-001",
      "nombre": "Roberto Iglesias",
      "capital": 0.3,
      "voto": 0.3,
      "via": "PARTICIPACION",
      "detalle": "22.00% via Petroquímica del Sur S.A. -> Inversora del Plata SA | 8.00% directo"
     }
    ],
    "menores": [],
    "ciclos": [],
    "observaciones": [
     "titularidad no identificada: 37.00% del capital"
    ]
   },
   "pep": null,
   "alertas": [],
   "operatoria": null,
   "perfil": null,
   "exposicion": 0,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "OFAC_SDN",
      "id_origen": "1201",
      "designado": "PETROQUIMICA DEL SUR SA",
      "matcheo_contra": "PETROQUIMICA DEL SUR SA",
      "score": 100.0,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "NPWMD"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "ESCALADO",
      "motivo": "coincidencia en lista critica (OFAC_SDN, score 100.0)"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "CONGELAMIENTO_REQUERIDO",
     "detalle": {
      "regimen": "FPADM",
      "lista": "OFAC_SDN",
      "designado": "PETROQUIMICA DEL SUR SA",
      "norma": "Res. UIF 3/2026, Ley 25.246 art. 14 inc. 12",
      "plazo": "24 horas",
      "reserva": "prohibido informar al cliente"
     }
    }
   ],
   "nota": "Persona juridica. El caso esta escalado y no paso por scoring: una coincidencia en lista critica se escala sin ponderar, asi que no tiene puntaje ni regimen asignado. Coincidencia probable contra PETROQUIMICA DEL SUR SA en OFAC_SDN, score 100 por nombre. Obligacion de congelamiento por regimen FPADM, Res. UIF 3/2026, Ley 25.246 art. 14 inc. 12. Se ejecuta sin demora y se reporta dentro de las 24 horas. Prohibido informar al cliente. Se identificaron 2 beneficiarios finales, con 1 nivel de intermediacion: Silvia Marconi, Roberto Iglesias. Queda a criterio del analista: ejecutar el congelamiento y reportarlo, confirmar o descartar la coincidencia contra la lista."
  },
  {
   "id": "CL004",
   "caso_id": "C00004",
   "nombre": "Carlos A. Gomez Rivera",
   "tipo": "PERSONA",
   "documentos": [
    "DNI 30111222"
   ],
   "fecha_nacimiento": "1978-03-04",
   "nacionalidad": "ARGENTINA",
   "pais_residencia": "ARGENTINA",
   "pais_residencia_iso": "AR",
   "riesgo_pais": "ORDINARIA",
   "actividad": "Consultoría",
   "oferta_publica": false,
   "estado": "ESCALADO",
   "escalado": true,
   "riesgo": {
    "puntaje": 0.0,
    "nivel": "SIN_SCORE",
    "regimen": "",
    "revision_meses": 0,
    "factores": [],
    "elevadores": []
   },
   "coincidencias": [
    {
     "lista": "OFAC_SDN",
     "id_origen": "7788",
     "designado": "GOMEZ RIVERA, Carlos Alberto",
     "matcheado": "GOMEZ RIVERA, Carlos Alberto",
     "score": 87.6,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "SDNTK"
     ],
     "atenuantes": [
      "nacionalidad discordante (ARGENTINA vs COLOMBIA)"
     ]
    }
   ],
   "congelamiento": null,
   "beneficiario": null,
   "pep": null,
   "alertas": [],
   "operatoria": null,
   "perfil": null,
   "exposicion": 0,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "OFAC_SDN",
      "id_origen": "7788",
      "designado": "GOMEZ RIVERA, Carlos Alberto",
      "matcheo_contra": "GOMEZ RIVERA, Carlos Alberto",
      "score": 87.6,
      "criterio": "NOMBRE",
      "atenuantes": [
       "nacionalidad discordante (ARGENTINA vs COLOMBIA)"
      ],
      "programas": [
       "SDNTK"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "ESCALADO",
      "motivo": "coincidencia en lista critica (OFAC_SDN, score 87.6)"
     }
    }
   ],
   "nota": "Persona humana. El caso esta escalado y no paso por scoring: una coincidencia en lista critica se escala sin ponderar, asi que no tiene puntaje ni regimen asignado. 1 coincidencia por debajo del umbral de probable, para descarte manual. Queda a criterio del analista: descartar las coincidencias por debajo del umbral."
  },
  {
   "id": "CL005",
   "caso_id": "C00005",
   "nombre": "María González",
   "tipo": "PERSONA",
   "documentos": [
    "DNI 27998877"
   ],
   "fecha_nacimiento": "1991-11-30",
   "nacionalidad": "ARGENTINA",
   "pais_residencia": "ARGENTINA",
   "pais_residencia_iso": "AR",
   "riesgo_pais": "ORDINARIA",
   "actividad": "Servicios profesionales",
   "oferta_publica": false,
   "estado": "ANALISIS",
   "escalado": false,
   "riesgo": {
    "puntaje": 15.0,
    "nivel": "BAJO",
    "regimen": "DD_SIMPLIFICADA",
    "revision_meses": 60,
    "factores": [
     {
      "codigo": "COINCIDENCIA_REVISION",
      "dimension": "CONTROL",
      "descripcion": "1 coincidencia(s) pendiente(s) de revision (max 79.3)",
      "puntos": 15.0
     }
    ],
    "elevadores": []
   },
   "coincidencias": [
    {
     "lista": "REPET",
     "id_origen": "250",
     "designado": "Gerardo Gonzalez Valencia",
     "matcheado": "Gerardo Gonzalez Valencia",
     "score": 79.3,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "LOCAL",
      "Narcotics Rewards Program U.S. Department State"
     ],
     "atenuantes": []
    }
   ],
   "congelamiento": null,
   "beneficiario": null,
   "pep": null,
   "alertas": [
    {
     "id": "9a2fab5710c6",
     "codigo": "DESVIO_PERFIL",
     "severidad": "ALTA",
     "descripcion": "07/2026: opero $72,768,480 contra $900,000 declarados (80.9x)",
     "metodologia": "comparacion mensual contra perfil, tolerancia 25%",
     "monto": 72768480.0,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-09-22",
     "dias_restantes": 1,
     "vencida": false,
     "operaciones": [
      {
       "fecha": "2026-07-16",
       "monto": 15044960.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-13",
       "monto": 14891440.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-19",
       "monto": 14584400.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-14",
       "monto": 14277360.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-17",
       "monto": 13970320.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      }
     ]
    },
    {
     "id": "66449f7ac437",
     "codigo": "FRACCIONAMIENTO",
     "severidad": "ALTA",
     "descripcion": "5 operaciones en 7 dias por $72,768,480, todas bajo el umbral de reporte ($15,352,000); la mayor llego al 98%",
     "metodologia": "ventana deslizante de 7 dias, minimo 3 operaciones, piso 10% del umbral",
     "monto": 72768480.0,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-09-22",
     "dias_restantes": 1,
     "vencida": false,
     "operaciones": [
      {
       "fecha": "2026-07-13",
       "monto": 14891440.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-14",
       "monto": 14277360.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-16",
       "monto": 15044960.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-17",
       "monto": 13970320.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-19",
       "monto": 14584400.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      }
     ]
    },
    {
     "id": "0aa5f3a7826f",
     "codigo": "EFECTIVO_DESPROPORCIONADO",
     "severidad": "ALTA",
     "descripcion": "98% de la operatoria en efectivo ($72,768,480) contra 10% declarado",
     "metodologia": "proporcion de efectivo sobre el total operado",
     "monto": 72768480.0,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-09-22",
     "dias_restantes": 1,
     "vencida": false,
     "operaciones": [
      {
       "fecha": "2026-07-13",
       "monto": 14891440.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-14",
       "monto": 14277360.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-16",
       "monto": 15044960.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-17",
       "monto": 13970320.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-19",
       "monto": 14584400.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      }
     ]
    },
    {
     "id": "4b993a07fd7e",
     "codigo": "ACELERACION",
     "severidad": "MEDIA",
     "descripcion": "los ultimos 30 dias promedian $2,425,616 diarios contra $14,138 historicos (171.6x)",
     "metodologia": "promedio diario de los ultimos 30 dias contra el resto",
     "monto": 72768480.0,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-09-22",
     "dias_restantes": 1,
     "vencida": false,
     "operaciones": [
      {
       "fecha": "2026-07-13",
       "monto": 14891440.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-14",
       "monto": 14277360.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-16",
       "monto": 15044960.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-17",
       "monto": 13970320.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-07-19",
       "monto": 14584400.0,
       "sentido": "INGRESO",
       "instrumento": "EFECTIVO",
       "canal": "PRESENCIAL",
       "contraparte": "Deposito por ventanilla",
       "pais": "Argentina",
       "referencia": ""
      }
     ]
    }
   ],
   "operatoria": {
    "cantidad": 15,
    "total": 74309520.5,
    "efectivo": 72768480.0,
    "proporcion_efectivo": 0.9793,
    "desde": "2026-03-02",
    "hasta": "2026-07-19",
    "paises": [
     "AR"
    ],
    "contrapartes": [
     "Deposito por ventanilla",
     "Haberes"
    ]
   },
   "perfil": {
    "monto_mensual": 900000.0,
    "operaciones_mensuales": 4,
    "proporcion_efectivo": 0.1,
    "paises": [
     "AR"
    ],
    "origen_fondos": "Sueldo en relacion de dependencia",
    "proposito": "Caja de ahorro"
   },
   "exposicion": 72768480.0,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "250",
      "designado": "Gerardo Gonzalez Valencia",
      "matcheo_contra": "Gerardo Gonzalez Valencia",
      "score": 79.3,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "LOCAL",
       "Narcotics Rewards Program U.S. Department State"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "SCORING",
      "motivo": "1 coincidencia(s) para revision"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "SCORING_EBR",
     "detalle": {
      "puntaje": 15.0,
      "nivel": "BAJO",
      "regimen": "DD_SIMPLIFICADA",
      "factores": [
       "COINCIDENCIA_REVISION(+15): 1 coincidencia(s) pendiente(s) de revision (max 79.3)"
      ],
      "elevadores": [],
      "proxima_revision": "2031-09-21"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCORING",
      "destino": "CERRADO",
      "motivo": "riesgo bajo (15.0 pts), DD_SIMPLIFICADA"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "DESVIO_PERFIL",
      "severidad": "ALTA",
      "descripcion": "07/2026: opero $72,768,480 contra $900,000 declarados (80.9x)",
      "metodologia": "comparacion mensual contra perfil, tolerancia 25%",
      "monto": 72768480.0,
      "vence": "2026-09-22"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "FRACCIONAMIENTO",
      "severidad": "ALTA",
      "descripcion": "5 operaciones en 7 dias por $72,768,480, todas bajo el umbral de reporte ($15,352,000); la mayor llego al 98%",
      "metodologia": "ventana deslizante de 7 dias, minimo 3 operaciones, piso 10% del umbral",
      "monto": 72768480.0,
      "vence": "2026-09-22"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "EFECTIVO_DESPROPORCIONADO",
      "severidad": "ALTA",
      "descripcion": "98% de la operatoria en efectivo ($72,768,480) contra 10% declarado",
      "metodologia": "proporcion de efectivo sobre el total operado",
      "monto": 72768480.0,
      "vence": "2026-09-22"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "ACELERACION",
      "severidad": "MEDIA",
      "descripcion": "los ultimos 30 dias promedian $2,425,616 diarios contra $14,138 historicos (171.6x)",
      "metodologia": "promedio diario de los ultimos 30 dias contra el resto",
      "monto": 72768480.0,
      "vence": "2026-09-22"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "CERRADO",
      "destino": "ANALISIS",
      "motivo": "4 alerta(s) de monitoreo (reapertura del legajo)"
     }
    }
   ],
   "nota": "Persona humana. Riesgo BAJO con 15 puntos, regimen dd simplificada, revision cada 60 meses. 1 coincidencia por debajo del umbral de probable, para descarte manual. 4 alertas de monitoreo por $291,073,920. Exposicion sancionatoria estimada en $72,768,480. Es una estimacion y no un calculo de multa: la fija la UIF en sumario. Queda a criterio del analista: descartar las coincidencias por debajo del umbral, decidir si la inusualidad se convierte en sospecha."
  },
  {
   "id": "CL006",
   "caso_id": "C00006",
   "nombre": "Khaled Shaikh Mohamed",
   "tipo": "PERSONA",
   "documentos": [
    "PASAPORTE ZZ9988776"
   ],
   "fecha_nacimiento": "1964-03-01",
   "nacionalidad": "PAKISTAN",
   "pais_residencia": "EMIRATOS",
   "pais_residencia_iso": null,
   "riesgo_pais": "SIN_DATO",
   "actividad": "Comercio exterior",
   "oferta_publica": false,
   "estado": "ESCALADO",
   "escalado": true,
   "riesgo": {
    "puntaje": 0.0,
    "nivel": "SIN_SCORE",
    "regimen": "",
    "revision_meses": 0,
    "factores": [],
    "elevadores": []
   },
   "coincidencias": [
    {
     "lista": "OFAC_SDN",
     "id_origen": "4417",
     "designado": "MOHAMMED, Khalid Sheikh",
     "matcheado": "MOHAMED, Khalid Shaikh",
     "score": 97.8,
     "criterio": "NOMBRE",
     "probable": true,
     "programas": [
      "SDGT"
     ],
     "atenuantes": []
    },
    {
     "lista": "REPET",
     "id_origen": "3013137",
     "designado": "AHMED SHAH NOORZAI OBAIDULLAH",
     "matcheado": "Mullah Mohammed Shah",
     "score": 85.5,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "ONU",
      "Taliban",
      "TAi.166"
     ],
     "atenuantes": []
    },
    {
     "lista": "REPET",
     "id_origen": "2989740",
     "designado": "KHAIRULLAH BARAKZAI KHUDAI NAZAR",
     "matcheado": "Haji Khair Mohammad",
     "score": 82.0,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "ONU",
      "Taliban",
      "TAi.163"
     ],
     "atenuantes": []
    },
    {
     "lista": "REPET",
     "id_origen": "2813149",
     "designado": "PIO ABOGNE DE VERA",
     "matcheado": "Khalid",
     "score": 79.9,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "ONU",
      "Al-Qaida",
      "QDi.245"
     ],
     "atenuantes": [
      "nacionalidad discordante (PAKISTAN vs PHILIPPINES)"
     ]
    },
    {
     "lista": "REPET",
     "id_origen": "6908491",
     "designado": "TOREK AGHA",
     "matcheado": "Sayed Mohammed Hashan",
     "score": 79.4,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "ONU",
      "Taliban",
      "TAi.174"
     ],
     "atenuantes": []
    },
    {
     "lista": "REPET",
     "id_origen": "2833107",
     "designado": "HAFIZ MUHAMMAD SAEED",
     "matcheado": "Mohammad Sayed",
     "score": 78.5,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "ONU",
      "Al-Qaida",
      "QDi.263"
     ],
     "atenuantes": []
    },
    {
     "lista": "REPET",
     "id_origen": "111090",
     "designado": "AKHTAR MOHAMMAD MANSOUR SHAH MOHAMMED",
     "matcheado": "AKHTAR MOHAMMAD MANSOUR SHAH MOHAMMED",
     "score": 78.0,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "ONU",
      "Taliban",
      "TAi.011"
     ],
     "atenuantes": [
      "nacionalidad discordante (PAKISTAN vs AFGHANISTAN)"
     ]
    }
   ],
   "congelamiento": {
    "regimen": "FT",
    "lista": "OFAC_SDN",
    "designado": "MOHAMMED, Khalid Sheikh",
    "score": 97.8,
    "criterio": "NOMBRE",
    "norma": "Res. UIF 207/2025, Decreto 918/2012, Ley 26.734 art. 6",
    "detectado": "2026-09-21",
    "pasos": [
     {
      "codigo": "COTEJAR_BASE",
      "descripcion": "cotejar la base de clientes e informar si hubo operaciones con la persona o entidad designada",
      "cumplido": false
     },
     {
      "codigo": "INMOVILIZAR",
      "descripcion": "inmovilizar los bienes u otros activos que sean propiedad o esten controlados, directa o indirectamente, por la designada, o cuyo destinatario o beneficiario sea",
      "cumplido": false
     },
     {
      "codigo": "INFORMAR_UIF",
      "descripcion": "informar inmediatamente a la UIF la aplicacion de la medida",
      "cumplido": false
     },
     {
      "codigo": "EMITIR_REPORTE",
      "descripcion": "emitir el reporte de operacion sospechosa sin demora alguna",
      "cumplido": false
     },
     {
      "codigo": "INFORMAR_RESULTADOS",
      "descripcion": "informar los resultados dentro de las 24 horas de notificada la resolucion, por el sistema Reporte Orden de Congelamiento",
      "cumplido": false
     },
     {
      "codigo": "MONITOREAR_POSTERIORES",
      "descripcion": "informar e inmovilizar las operaciones tentadas con posterioridad, mientras la medida siga vigente",
      "cumplido": false
     },
     {
      "codigo": "RESERVA",
      "descripcion": "abstenerse de informar al cliente o a terceros los antecedentes de la resolucion; solo puede indicarse que los bienes estan congelados en virtud del art. 6 de la Ley 26.734",
      "cumplido": false
     }
    ]
   },
   "beneficiario": null,
   "pep": null,
   "alertas": [],
   "operatoria": null,
   "perfil": null,
   "exposicion": 0,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "OFAC_SDN",
      "id_origen": "4417",
      "designado": "MOHAMMED, Khalid Sheikh",
      "matcheo_contra": "MOHAMED, Khalid Shaikh",
      "score": 97.8,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "SDGT"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "3013137",
      "designado": "AHMED SHAH NOORZAI OBAIDULLAH",
      "matcheo_contra": "Mullah Mohammed Shah",
      "score": 85.5,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "ONU",
       "Taliban",
       "TAi.166"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "2989740",
      "designado": "KHAIRULLAH BARAKZAI KHUDAI NAZAR",
      "matcheo_contra": "Haji Khair Mohammad",
      "score": 82.0,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "ONU",
       "Taliban",
       "TAi.163"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "2813149",
      "designado": "PIO ABOGNE DE VERA",
      "matcheo_contra": "Khalid",
      "score": 79.9,
      "criterio": "NOMBRE",
      "atenuantes": [
       "nacionalidad discordante (PAKISTAN vs PHILIPPINES)"
      ],
      "programas": [
       "ONU",
       "Al-Qaida",
       "QDi.245"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "6908491",
      "designado": "TOREK AGHA",
      "matcheo_contra": "Sayed Mohammed Hashan",
      "score": 79.4,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "ONU",
       "Taliban",
       "TAi.174"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "2833107",
      "designado": "HAFIZ MUHAMMAD SAEED",
      "matcheo_contra": "Mohammad Sayed",
      "score": 78.5,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "ONU",
       "Al-Qaida",
       "QDi.263"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "111090",
      "designado": "AKHTAR MOHAMMAD MANSOUR SHAH MOHAMMED",
      "matcheo_contra": "AKHTAR MOHAMMAD MANSOUR SHAH MOHAMMED",
      "score": 78.0,
      "criterio": "NOMBRE",
      "atenuantes": [
       "nacionalidad discordante (PAKISTAN vs AFGHANISTAN)"
      ],
      "programas": [
       "ONU",
       "Taliban",
       "TAi.011"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "ESCALADO",
      "motivo": "coincidencia en lista critica (OFAC_SDN, score 97.8)"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "CONGELAMIENTO_REQUERIDO",
     "detalle": {
      "regimen": "FT",
      "lista": "OFAC_SDN",
      "designado": "MOHAMMED, Khalid Sheikh",
      "norma": "Res. UIF 207/2025, Decreto 918/2012, Ley 26.734 art. 6",
      "plazo": "24 horas",
      "reserva": "prohibido informar al cliente"
     }
    }
   ],
   "nota": "Persona humana. El caso esta escalado y no paso por scoring: una coincidencia en lista critica se escala sin ponderar, asi que no tiene puntaje ni regimen asignado. Coincidencia probable contra MOHAMMED, Khalid Sheikh en OFAC_SDN, score 97.8 por nombre. Obligacion de congelamiento por regimen FT, Res. UIF 207/2025, Decreto 918/2012, Ley 26.734 art. 6. Se ejecuta sin demora y se reporta dentro de las 24 horas. Prohibido informar al cliente. Queda a criterio del analista: ejecutar el congelamiento y reportarlo, confirmar o descartar la coincidencia contra la lista."
  },
  {
   "id": "CL007",
   "caso_id": "C00007",
   "nombre": "Eastern Trading Co",
   "tipo": "ENTIDAD",
   "documentos": [
    "TAX_ID 88991122"
   ],
   "fecha_nacimiento": null,
   "nacionalidad": null,
   "pais_residencia": "SINGAPUR",
   "pais_residencia_iso": "SG",
   "riesgo_pais": "ORDINARIA",
   "actividad": "Logística",
   "oferta_publica": false,
   "estado": "ESCALADO",
   "escalado": true,
   "riesgo": {
    "puntaje": 0.0,
    "nivel": "SIN_SCORE",
    "regimen": "",
    "revision_meses": 0,
    "factores": [],
    "elevadores": []
   },
   "coincidencias": [
    {
     "lista": "OFAC_SDN",
     "id_origen": "9001",
     "designado": "EASTERN TRADING LIMITED",
     "matcheado": "EASTERN TRADING LIMITED",
     "score": 100.0,
     "criterio": "NOMBRE",
     "probable": true,
     "programas": [
      "RES1718"
     ],
     "atenuantes": []
    },
    {
     "lista": "REPET",
     "id_origen": "2989573",
     "designado": "ROSHAN MONEY EXCHANGE",
     "matcheado": "Roshan Trading Company",
     "score": 79.0,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "ONU",
      "Taliban",
      "TAe.011"
     ],
     "atenuantes": []
    },
    {
     "lista": "REPET",
     "id_origen": "113356",
     "designado": "EASTERN TURKISTAN ISLAMIC MOVEMENT (ETIM)",
     "matcheado": "EASTERN TURKISTAN ISLAMIC MOVEMENT (ETIM)",
     "score": 78.9,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "ONU",
      "Al-Qaida",
      "QDe.088"
     ],
     "atenuantes": []
    },
    {
     "lista": "REPET",
     "id_origen": "3000510",
     "designado": "RAHAT LTD.",
     "matcheado": "Rahat Trading Company",
     "score": 78.1,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "ONU",
      "Taliban",
      "TAe.013"
     ],
     "atenuantes": []
    }
   ],
   "congelamiento": {
    "regimen": "FPADM",
    "lista": "OFAC_SDN",
    "designado": "EASTERN TRADING LIMITED",
    "score": 100.0,
    "criterio": "NOMBRE",
    "norma": "Res. UIF 3/2026, Ley 25.246 art. 14 inc. 12",
    "detectado": "2026-09-21",
    "pasos": [
     {
      "codigo": "COTEJAR_BASE",
      "descripcion": "cotejar la base de clientes e informar si hubo operaciones con la persona o entidad designada",
      "cumplido": false
     },
     {
      "codigo": "INMOVILIZAR",
      "descripcion": "inmovilizar los bienes u otros activos que sean propiedad o esten controlados, directa o indirectamente, por la designada, o cuyo destinatario o beneficiario sea",
      "cumplido": false
     },
     {
      "codigo": "INFORMAR_UIF",
      "descripcion": "informar inmediatamente a la UIF la aplicacion de la medida",
      "cumplido": false
     },
     {
      "codigo": "EMITIR_REPORTE",
      "descripcion": "emitir el reporte de operacion sospechosa sin demora alguna",
      "cumplido": false
     },
     {
      "codigo": "INFORMAR_RESULTADOS",
      "descripcion": "informar los resultados dentro de las 24 horas de notificada la resolucion, por el sistema Reporte Orden de Congelamiento",
      "cumplido": false
     },
     {
      "codigo": "MONITOREAR_POSTERIORES",
      "descripcion": "informar e inmovilizar las operaciones tentadas con posterioridad, mientras la medida siga vigente",
      "cumplido": false
     },
     {
      "codigo": "RESERVA",
      "descripcion": "abstenerse de informar al cliente o a terceros los antecedentes de la resolucion; solo puede indicarse que los bienes estan congelados en virtud del art. 6 de la Ley 26.734",
      "cumplido": false
     }
    ]
   },
   "beneficiario": {
    "identificado": true,
    "exceptuada": false,
    "opaco": 0.5,
    "profundidad": 2,
    "umbral": 0.0,
    "beneficiarios": [
     {
      "id": "P-004",
      "nombre": "Marcelo Duarte",
      "capital": 0.5,
      "voto": 0.5,
      "via": "PARTICIPACION",
      "detalle": "35.00% via Eastern Trading Co -> Andes Capital Ltd | 15.00% via Eastern Trading Co -> Pacific Holdings BV"
     }
    ],
    "menores": [],
    "ciclos": [
     [
      "SOC-C",
      "SOC-D"
     ]
    ],
    "observaciones": [
     "entidad del exterior sin oferta publica: no corresponde el umbral del 10%, se identifica a la totalidad de los beneficiarios",
     "1 participacion(es) circular(es) detectada(s)",
     "titularidad no identificada: 50.00% del capital"
    ]
   },
   "pep": null,
   "alertas": [],
   "operatoria": null,
   "perfil": null,
   "exposicion": 0,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "OFAC_SDN",
      "id_origen": "9001",
      "designado": "EASTERN TRADING LIMITED",
      "matcheo_contra": "EASTERN TRADING LIMITED",
      "score": 100.0,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "RES1718"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "2989573",
      "designado": "ROSHAN MONEY EXCHANGE",
      "matcheo_contra": "Roshan Trading Company",
      "score": 79.0,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "ONU",
       "Taliban",
       "TAe.011"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "113356",
      "designado": "EASTERN TURKISTAN ISLAMIC MOVEMENT (ETIM)",
      "matcheo_contra": "EASTERN TURKISTAN ISLAMIC MOVEMENT (ETIM)",
      "score": 78.9,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "ONU",
       "Al-Qaida",
       "QDe.088"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "3000510",
      "designado": "RAHAT LTD.",
      "matcheo_contra": "Rahat Trading Company",
      "score": 78.1,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "ONU",
       "Taliban",
       "TAe.013"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "ESCALADO",
      "motivo": "coincidencia en lista critica (OFAC_SDN, score 100.0)"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "CONGELAMIENTO_REQUERIDO",
     "detalle": {
      "regimen": "FPADM",
      "lista": "OFAC_SDN",
      "designado": "EASTERN TRADING LIMITED",
      "norma": "Res. UIF 3/2026, Ley 25.246 art. 14 inc. 12",
      "plazo": "24 horas",
      "reserva": "prohibido informar al cliente"
     }
    }
   ],
   "nota": "Persona juridica. El caso esta escalado y no paso por scoring: una coincidencia en lista critica se escala sin ponderar, asi que no tiene puntaje ni regimen asignado. Coincidencia probable contra EASTERN TRADING LIMITED en OFAC_SDN, score 100 por nombre. Obligacion de congelamiento por regimen FPADM, Res. UIF 3/2026, Ley 25.246 art. 14 inc. 12. Se ejecuta sin demora y se reporta dentro de las 24 horas. Prohibido informar al cliente. Se identifico al beneficiario final, con 2 niveles de intermediacion: Marcelo Duarte. Queda a criterio del analista: ejecutar el congelamiento y reportarlo, confirmar o descartar la coincidencia contra la lista."
  },
  {
   "id": "CL008",
   "caso_id": "C00008",
   "nombre": "Ana Beatriz Rodríguez",
   "tipo": "PERSONA",
   "documentos": [
    "DNI 33445566"
   ],
   "fecha_nacimiento": "1985-07-19",
   "nacionalidad": "ARGENTINA",
   "pais_residencia": "ARGENTINA",
   "pais_residencia_iso": "AR",
   "riesgo_pais": "ORDINARIA",
   "actividad": "Docencia",
   "oferta_publica": false,
   "estado": "ANALISIS",
   "escalado": false,
   "riesgo": {
    "puntaje": 0,
    "nivel": "BAJO",
    "regimen": "DD_SIMPLIFICADA",
    "revision_meses": 60,
    "factores": [],
    "elevadores": []
   },
   "coincidencias": [],
   "congelamiento": null,
   "beneficiario": null,
   "pep": null,
   "alertas": [
    {
     "id": "bb594060817a",
     "codigo": "DESVIO_PERFIL",
     "severidad": "ALTA",
     "descripcion": "06/2026: opero $41,618,770 contra $2,000,000 declarados (20.8x)",
     "metodologia": "comparacion mensual contra perfil, tolerancia 25%",
     "monto": 41618769.65,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-09-02",
     "dias_restantes": -19,
     "vencida": true,
     "operaciones": [
      {
       "fecha": "2026-06-22",
       "monto": 6476227.56,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-07",
       "monto": 6462853.67,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-19",
       "monto": 6302788.54,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-13",
       "monto": 5980133.58,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-04",
       "monto": 5852621.08,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-10",
       "monto": 5373572.16,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-16",
       "monto": 5170573.06,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      }
     ]
    },
    {
     "id": "64d197d32aab",
     "codigo": "ACELERACION",
     "severidad": "MEDIA",
     "descripcion": "los ultimos 30 dias promedian $1,390,883 diarios contra $34,639 historicos (40.2x)",
     "metodologia": "promedio diario de los ultimos 30 dias contra el resto",
     "monto": 41726479.52,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-08-24",
     "dias_restantes": -28,
     "vencida": true,
     "operaciones": [
      {
       "fecha": "2026-05-26",
       "monto": 107709.87,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Consultoria",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-04",
       "monto": 5852621.08,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-07",
       "monto": 6462853.67,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-10",
       "monto": 5373572.16,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-13",
       "monto": 5980133.58,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-16",
       "monto": 5170573.06,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-19",
       "monto": 6302788.54,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-22",
       "monto": 6476227.56,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      }
     ]
    },
    {
     "id": "d2f1e710df66",
     "codigo": "FRACCIONAMIENTO",
     "severidad": "MEDIA",
     "descripcion": "3 operaciones en 7 dias por $17,689,047, todas bajo el umbral de reporte ($15,352,000); la mayor llego al 42%",
     "metodologia": "ventana deslizante de 7 dias, minimo 3 operaciones, piso 10% del umbral",
     "monto": 17689046.91,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-09-02",
     "dias_restantes": -19,
     "vencida": true,
     "operaciones": [
      {
       "fecha": "2026-06-04",
       "monto": 5852621.08,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-07",
       "monto": 6462853.67,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-10",
       "monto": 5373572.16,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      }
     ]
    },
    {
     "id": "007e66aaa355",
     "codigo": "FRACCIONAMIENTO",
     "severidad": "MEDIA",
     "descripcion": "3 operaciones en 7 dias por $17,453,495, todas bajo el umbral de reporte ($15,352,000); la mayor llego al 41%",
     "metodologia": "ventana deslizante de 7 dias, minimo 3 operaciones, piso 10% del umbral",
     "monto": 17453495.18,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-09-11",
     "dias_restantes": -10,
     "vencida": true,
     "operaciones": [
      {
       "fecha": "2026-06-13",
       "monto": 5980133.58,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-16",
       "monto": 5170573.06,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-06-19",
       "monto": 6302788.54,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Transferencia recibida",
       "pais": "Argentina",
       "referencia": ""
      }
     ]
    }
   ],
   "operatoria": {
    "cantidad": 25,
    "total": 44566879.34,
    "efectivo": 0,
    "proporcion_efectivo": 0.0,
    "desde": "2026-03-02",
    "hasta": "2026-06-22",
    "paises": [
     "AR"
    ],
    "contrapartes": [
     "Consultoria",
     "Transferencia recibida"
    ]
   },
   "perfil": {
    "monto_mensual": 2000000.0,
    "operaciones_mensuales": 5,
    "proporcion_efectivo": 0.05,
    "paises": [
     "AR"
    ],
    "origen_fondos": "Honorarios profesionales",
    "proposito": "Cuenta operativa"
   },
   "exposicion": 41726479.52,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SIN_COINCIDENCIAS",
     "detalle": {}
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "SCORING",
      "motivo": "sin coincidencias en listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "SCORING_EBR",
     "detalle": {
      "puntaje": 0,
      "nivel": "BAJO",
      "regimen": "DD_SIMPLIFICADA",
      "factores": [],
      "elevadores": [],
      "proxima_revision": "2031-09-21"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCORING",
      "destino": "CERRADO",
      "motivo": "riesgo bajo (0 pts), DD_SIMPLIFICADA"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "DESVIO_PERFIL",
      "severidad": "ALTA",
      "descripcion": "06/2026: opero $41,618,770 contra $2,000,000 declarados (20.8x)",
      "metodologia": "comparacion mensual contra perfil, tolerancia 25%",
      "monto": 41618769.65,
      "vence": "2026-09-02"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "ACELERACION",
      "severidad": "MEDIA",
      "descripcion": "los ultimos 30 dias promedian $1,390,883 diarios contra $34,639 historicos (40.2x)",
      "metodologia": "promedio diario de los ultimos 30 dias contra el resto",
      "monto": 41726479.52,
      "vence": "2026-08-24"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "FRACCIONAMIENTO",
      "severidad": "MEDIA",
      "descripcion": "3 operaciones en 7 dias por $17,689,047, todas bajo el umbral de reporte ($15,352,000); la mayor llego al 42%",
      "metodologia": "ventana deslizante de 7 dias, minimo 3 operaciones, piso 10% del umbral",
      "monto": 17689046.91,
      "vence": "2026-09-02"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "FRACCIONAMIENTO",
      "severidad": "MEDIA",
      "descripcion": "3 operaciones en 7 dias por $17,453,495, todas bajo el umbral de reporte ($15,352,000); la mayor llego al 41%",
      "metodologia": "ventana deslizante de 7 dias, minimo 3 operaciones, piso 10% del umbral",
      "monto": 17453495.18,
      "vence": "2026-09-11"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "CERRADO",
      "destino": "ANALISIS",
      "motivo": "4 alerta(s) de monitoreo (reapertura del legajo)"
     }
    }
   ],
   "nota": "Persona humana. Riesgo BAJO con 0 puntos, regimen dd simplificada, revision cada 60 meses. 4 alertas de monitoreo por $118,487,791, 4 con el plazo de reporte ya vencido. El tope corre desde la operacion y no desde la deteccion. Exposicion sancionatoria estimada en $41,726,480. Es una estimacion y no un calculo de multa: la fija la UIF en sumario. Queda a criterio del analista: decidir si la inusualidad se convierte en sospecha."
  },
  {
   "id": "CL009",
   "caso_id": "C00009",
   "nombre": "Delta Servicios Financieros SA",
   "tipo": "ENTIDAD",
   "documentos": [
    "CUIT 30-99887766-1"
   ],
   "fecha_nacimiento": null,
   "nacionalidad": null,
   "pais_residencia": "ARGENTINA",
   "pais_residencia_iso": "AR",
   "riesgo_pais": "ORDINARIA",
   "actividad": "Casa de cambio",
   "oferta_publica": false,
   "estado": "ANALISIS",
   "escalado": false,
   "riesgo": {
    "puntaje": 55.0,
    "nivel": "ALTO",
    "regimen": "DD_REFORZADA",
    "revision_meses": 12,
    "factores": [
     {
      "codigo": "PERSONA_JURIDICA",
      "dimension": "CLIENTE",
      "descripcion": "cliente es persona juridica o estructura",
      "puntos": 8.0
     },
     {
      "codigo": "TITULARIDAD_OPACA",
      "dimension": "CLIENTE",
      "descripcion": "titularidad no identificada: 60.0%",
      "puntos": 12.0
     },
     {
      "codigo": "PEP_NACIONAL",
      "dimension": "CLIENTE",
      "descripcion": "PEP nacional (Legislador provincial)",
      "puntos": 20.0
     },
     {
      "codigo": "ACTIVIDAD_SENSIBLE",
      "dimension": "ACTIVIDAD",
      "descripcion": "actividad de exposicion elevada: CASA DE CAMBIO",
      "puntos": 15.0
     }
    ],
    "elevadores": []
   },
   "coincidencias": [],
   "congelamiento": null,
   "beneficiario": {
    "identificado": true,
    "exceptuada": false,
    "opaco": 0.6,
    "profundidad": 0,
    "umbral": 0.1,
    "beneficiarios": [
     {
      "id": "P-005",
      "nombre": "Laura Beltran",
      "capital": 0.05,
      "voto": 0.45,
      "via": "PARTICIPACION",
      "detalle": "5.00% directo"
     },
     {
      "id": "P-006",
      "nombre": "Diego Sanguinetti",
      "capital": 0.35,
      "voto": 0.05,
      "via": "PARTICIPACION",
      "detalle": "35.00% directo"
     }
    ],
    "menores": [],
    "ciclos": [],
    "observaciones": [
     "titularidad no identificada: 60.00% del capital"
    ]
   },
   "pep": {
    "tipo": "NACIONAL",
    "cargo": "Legislador provincial",
    "por_parentesco": false,
    "fecha_cese": null,
    "vencida": false
   },
   "alertas": [],
   "operatoria": null,
   "perfil": null,
   "exposicion": 0,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SIN_COINCIDENCIAS",
     "detalle": {}
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "SCORING",
      "motivo": "sin coincidencias en listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "BENEFICIARIO_FINAL",
     "detalle": {
      "identificados": [
       "Laura Beltran 45.00% (PARTICIPACION)",
       "Diego Sanguinetti 35.00% (PARTICIPACION)"
      ],
      "titularidad_opaca": "60.00%",
      "niveles": 0,
      "observaciones": [
       "titularidad no identificada: 60.00% del capital"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "SCORING_EBR",
     "detalle": {
      "puntaje": 55.0,
      "nivel": "ALTO",
      "regimen": "DD_REFORZADA",
      "factores": [
       "PERSONA_JURIDICA(+8): cliente es persona juridica o estructura",
       "TITULARIDAD_OPACA(+12): titularidad no identificada: 60.0%",
       "PEP_NACIONAL(+20): PEP nacional (Legislador provincial)",
       "ACTIVIDAD_SENSIBLE(+15): actividad de exposicion elevada: CASA DE CAMBIO"
      ],
      "elevadores": [],
      "proxima_revision": "2027-09-21"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCORING",
      "destino": "ANALISIS",
      "motivo": "riesgo alto (55.0 pts) requiere diligencia reforzada"
     }
    }
   ],
   "nota": "Persona juridica. Riesgo ALTO con 55 puntos, regimen dd reforzada, revision cada 12 meses. Se identificaron 2 beneficiarios finales: Laura Beltran, Diego Sanguinetti. Condicion PEP nacional."
  },
  {
   "id": "CL010",
   "caso_id": "C00010",
   "nombre": "Blue Harbour Trading Ltd",
   "tipo": "ENTIDAD",
   "documentos": [
    "TAX_ID 77001122"
   ],
   "fecha_nacimiento": null,
   "nacionalidad": null,
   "pais_residencia": "PANAMA",
   "pais_residencia_iso": "PA",
   "riesgo_pais": "ORDINARIA",
   "actividad": "Comercio exterior",
   "oferta_publica": false,
   "estado": "ANALISIS",
   "escalado": false,
   "riesgo": {
    "puntaje": 76.0,
    "nivel": "ALTO",
    "regimen": "DD_REFORZADA",
    "revision_meses": 12,
    "factores": [
     {
      "codigo": "PERSONA_JURIDICA",
      "dimension": "CLIENTE",
      "descripcion": "cliente es persona juridica o estructura",
      "puntos": 8.0
     },
     {
      "codigo": "TITULARIDAD_OPACA",
      "dimension": "CLIENTE",
      "descripcion": "titularidad no identificada: 90.0%",
      "puntos": 18.0
     },
     {
      "codigo": "PEP_EXTRANJERA",
      "dimension": "CLIENTE",
      "descripcion": "PEP extranjera (Ministro de Estado)",
      "puntos": 35.0
     },
     {
      "codigo": "ACTIVIDAD_SENSIBLE",
      "dimension": "ACTIVIDAD",
      "descripcion": "actividad de exposicion elevada: COMERCIO EXTERIOR",
      "puntos": 15.0
     }
    ],
    "elevadores": [
     "PEP_EXTRANJERA"
    ]
   },
   "coincidencias": [],
   "congelamiento": null,
   "beneficiario": {
    "identificado": true,
    "exceptuada": false,
    "opaco": 0.9,
    "profundidad": 0,
    "umbral": 0.0,
    "beneficiarios": [
     {
      "id": "P-008",
      "nombre": "Elena Ferrari",
      "capital": 0.06,
      "voto": 0.06,
      "via": "PARTICIPACION",
      "detalle": "6.00% directo"
     },
     {
      "id": "P-009",
      "nombre": "Tomas Rivas",
      "capital": 0.04,
      "voto": 0.04,
      "via": "PARTICIPACION",
      "detalle": "4.00% directo"
     }
    ],
    "menores": [],
    "ciclos": [],
    "observaciones": [
     "entidad del exterior sin oferta publica: no corresponde el umbral del 10%, se identifica a la totalidad de los beneficiarios",
     "titularidad no identificada: 90.00% del capital"
    ]
   },
   "pep": {
    "tipo": "EXTRANJERA",
    "cargo": "Ministro de Estado",
    "por_parentesco": false,
    "fecha_cese": null,
    "vencida": false
   },
   "alertas": [],
   "operatoria": null,
   "perfil": null,
   "exposicion": 0,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SIN_COINCIDENCIAS",
     "detalle": {}
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "SCORING",
      "motivo": "sin coincidencias en listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "BENEFICIARIO_FINAL",
     "detalle": {
      "identificados": [
       "Elena Ferrari 6.00% (PARTICIPACION)",
       "Tomas Rivas 4.00% (PARTICIPACION)"
      ],
      "titularidad_opaca": "90.00%",
      "niveles": 0,
      "observaciones": [
       "entidad del exterior sin oferta publica: no corresponde el umbral del 10%, se identifica a la totalidad de los beneficiarios",
       "titularidad no identificada: 90.00% del capital"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "SCORING_EBR",
     "detalle": {
      "puntaje": 76.0,
      "nivel": "ALTO",
      "regimen": "DD_REFORZADA",
      "factores": [
       "PERSONA_JURIDICA(+8): cliente es persona juridica o estructura",
       "TITULARIDAD_OPACA(+18): titularidad no identificada: 90.0%",
       "PEP_EXTRANJERA(+35): PEP extranjera (Ministro de Estado)",
       "ACTIVIDAD_SENSIBLE(+15): actividad de exposicion elevada: COMERCIO EXTERIOR"
      ],
      "elevadores": [
       "PEP_EXTRANJERA"
      ],
      "proxima_revision": "2027-09-21"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCORING",
      "destino": "ANALISIS",
      "motivo": "riesgo alto (76.0 pts) requiere diligencia reforzada"
     }
    }
   ],
   "nota": "Persona juridica. Riesgo ALTO con 76 puntos, regimen dd reforzada, revision cada 12 meses. Se identificaron 2 beneficiarios finales: Elena Ferrari, Tomas Rivas. Condicion PEP extranjera."
  },
  {
   "id": "CL011",
   "caso_id": "C00011",
   "nombre": "Grupo Cotizante SA",
   "tipo": "ENTIDAD",
   "documentos": [
    "CUIT 30-55443322-9"
   ],
   "fecha_nacimiento": null,
   "nacionalidad": null,
   "pais_residencia": "ARGENTINA",
   "pais_residencia_iso": "AR",
   "riesgo_pais": "ORDINARIA",
   "actividad": "Industria alimenticia",
   "oferta_publica": true,
   "estado": "CERRADO",
   "escalado": false,
   "riesgo": {
    "puntaje": 8.0,
    "nivel": "BAJO",
    "regimen": "DD_SIMPLIFICADA",
    "revision_meses": 60,
    "factores": [
     {
      "codigo": "PERSONA_JURIDICA",
      "dimension": "CLIENTE",
      "descripcion": "cliente es persona juridica o estructura",
      "puntos": 8.0
     }
    ],
    "elevadores": []
   },
   "coincidencias": [],
   "congelamiento": null,
   "beneficiario": {
    "identificado": true,
    "exceptuada": true,
    "opaco": 0.0,
    "profundidad": 0,
    "umbral": 0.1,
    "beneficiarios": [],
    "menores": [],
    "ciclos": [],
    "observaciones": [
     "sociedad con oferta publica de sus valores: exceptuada de identificar beneficiario final, sujeta a acreditar esa condicion"
    ]
   },
   "pep": {
    "tipo": "EXTRANJERA",
    "cargo": "Direccion de empresa estatal",
    "por_parentesco": false,
    "fecha_cese": "2019-03-31",
    "vencida": true
   },
   "alertas": [],
   "operatoria": null,
   "perfil": null,
   "exposicion": 0,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SIN_COINCIDENCIAS",
     "detalle": {}
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "SCORING",
      "motivo": "sin coincidencias en listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "BENEFICIARIO_FINAL",
     "detalle": {
      "identificados": [],
      "titularidad_opaca": "0.00%",
      "niveles": 0,
      "observaciones": [
       "sociedad con oferta publica de sus valores: exceptuada de identificar beneficiario final, sujeta a acreditar esa condicion"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "SCORING_EBR",
     "detalle": {
      "puntaje": 8.0,
      "nivel": "BAJO",
      "regimen": "DD_SIMPLIFICADA",
      "factores": [
       "PERSONA_JURIDICA(+8): cliente es persona juridica o estructura"
      ],
      "elevadores": [],
      "proxima_revision": "2031-09-21"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCORING",
      "destino": "CERRADO",
      "motivo": "riesgo bajo (8.0 pts), DD_SIMPLIFICADA"
     }
    }
   ],
   "nota": "Persona juridica. Riesgo BAJO con 8 puntos, regimen dd simplificada, revision cada 60 meses. Condicion PEP extranjera con declaracion vencida por el plazo de 2 anios."
  },
  {
   "id": "CL012",
   "caso_id": "C00012",
   "nombre": "Fernanda Ortiz",
   "tipo": "PERSONA",
   "documentos": [
    "DNI 31222333"
   ],
   "fecha_nacimiento": "1987-02-14",
   "nacionalidad": "ARGENTINA",
   "pais_residencia": "ARGENTINA",
   "pais_residencia_iso": "AR",
   "riesgo_pais": "ORDINARIA",
   "actividad": "Servicios profesionales",
   "oferta_publica": false,
   "estado": "ANALISIS",
   "escalado": false,
   "riesgo": {
    "puntaje": 30.0,
    "nivel": "MEDIO",
    "regimen": "DD_MEDIA",
    "revision_meses": 36,
    "factores": [
     {
      "codigo": "PEP_NACIONAL",
      "dimension": "CLIENTE",
      "descripcion": "PEP nacional por parentesco o cercania (Conyuge de intendente)",
      "puntos": 30.0
     }
    ],
    "elevadores": []
   },
   "coincidencias": [],
   "congelamiento": null,
   "beneficiario": null,
   "pep": {
    "tipo": "NACIONAL",
    "cargo": "Conyuge de intendente",
    "por_parentesco": true,
    "fecha_cese": null,
    "vencida": false
   },
   "alertas": [
    {
     "id": "7ed6f0ec8b9b",
     "codigo": "DESVIO_PERFIL",
     "severidad": "ALTA",
     "descripcion": "07/2026: opero $13,671,015 contra $2,500,000 declarados (5.5x)",
     "metodologia": "comparacion mensual contra perfil, tolerancia 25%",
     "monto": 13671014.67,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-09-22",
     "dias_restantes": 1,
     "vencida": false,
     "operaciones": [
      {
       "fecha": "2026-07-20",
       "monto": 4788953.5,
       "sentido": "EGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Panama Trade SA",
       "pais": "Islas Vírgenes Británicas",
       "referencia": ""
      },
      {
       "fecha": "2026-07-08",
       "monto": 4322387.23,
       "sentido": "EGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Panama Trade SA",
       "pais": "Islas Vírgenes Británicas",
       "referencia": ""
      },
      {
       "fecha": "2026-07-14",
       "monto": 4235406.17,
       "sentido": "EGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Panama Trade SA",
       "pais": "Islas Vírgenes Británicas",
       "referencia": ""
      },
      {
       "fecha": "2026-07-01",
       "monto": 324267.77,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Cliente",
       "pais": "Uruguay",
       "referencia": ""
      }
     ]
    },
    {
     "id": "517cc196a0a9",
     "codigo": "JURISDICCION_NO_DECLARADA",
     "severidad": "ALTA",
     "descripcion": "3 operacion(es) por $13,346,747 con contraparte en Islas Virgenes Britanicas, jurisdiccion en lista de riesgo",
     "metodologia": "paises de contraparte normalizados a ISO, contra el perfil y las listas",
     "monto": 13346746.9,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-09-22",
     "dias_restantes": 1,
     "vencida": false,
     "operaciones": [
      {
       "fecha": "2026-07-08",
       "monto": 4322387.23,
       "sentido": "EGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Panama Trade SA",
       "pais": "Islas Vírgenes Británicas",
       "referencia": ""
      },
      {
       "fecha": "2026-07-14",
       "monto": 4235406.17,
       "sentido": "EGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Panama Trade SA",
       "pais": "Islas Vírgenes Británicas",
       "referencia": ""
      },
      {
       "fecha": "2026-07-20",
       "monto": 4788953.5,
       "sentido": "EGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Panama Trade SA",
       "pais": "Islas Vírgenes Británicas",
       "referencia": ""
      }
     ]
    },
    {
     "id": "7f3a295e74f3",
     "codigo": "ACELERACION",
     "severidad": "MEDIA",
     "descripcion": "los ultimos 30 dias promedian $455,700 diarios contra $55,494 historicos (8.2x)",
     "metodologia": "promedio diario de los ultimos 30 dias contra el resto",
     "monto": 13671014.67,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-09-22",
     "dias_restantes": 1,
     "vencida": false,
     "operaciones": [
      {
       "fecha": "2026-07-01",
       "monto": 324267.77,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Cliente",
       "pais": "Uruguay",
       "referencia": ""
      },
      {
       "fecha": "2026-07-08",
       "monto": 4322387.23,
       "sentido": "EGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Panama Trade SA",
       "pais": "Islas Vírgenes Británicas",
       "referencia": ""
      },
      {
       "fecha": "2026-07-14",
       "monto": 4235406.17,
       "sentido": "EGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Panama Trade SA",
       "pais": "Islas Vírgenes Británicas",
       "referencia": ""
      },
      {
       "fecha": "2026-07-20",
       "monto": 4788953.5,
       "sentido": "EGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Panama Trade SA",
       "pais": "Islas Vírgenes Británicas",
       "referencia": ""
      }
     ]
    }
   ],
   "operatoria": {
    "cantidad": 15,
    "total": 19775381.25,
    "efectivo": 0,
    "proporcion_efectivo": 0.0,
    "desde": "2026-03-02",
    "hasta": "2026-07-20",
    "paises": [
     "UY",
     "VG"
    ],
    "contrapartes": [
     "Cliente",
     "Panama Trade SA"
    ]
   },
   "perfil": {
    "monto_mensual": 2500000.0,
    "operaciones_mensuales": 4,
    "proporcion_efectivo": 0.0,
    "paises": [
     "AR",
     "UY"
    ],
    "origen_fondos": "Servicios profesionales",
    "proposito": "Cobros del exterior"
   },
   "exposicion": 13671014.67,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SIN_COINCIDENCIAS",
     "detalle": {}
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "SCORING",
      "motivo": "sin coincidencias en listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "SCORING_EBR",
     "detalle": {
      "puntaje": 30.0,
      "nivel": "MEDIO",
      "regimen": "DD_MEDIA",
      "factores": [
       "PEP_NACIONAL(+30): PEP nacional por parentesco o cercania (Conyuge de intendente)"
      ],
      "elevadores": [],
      "proxima_revision": "2029-09-21"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCORING",
      "destino": "CERRADO",
      "motivo": "riesgo medio (30.0 pts), DD_MEDIA"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "DESVIO_PERFIL",
      "severidad": "ALTA",
      "descripcion": "07/2026: opero $13,671,015 contra $2,500,000 declarados (5.5x)",
      "metodologia": "comparacion mensual contra perfil, tolerancia 25%",
      "monto": 13671014.67,
      "vence": "2026-09-22"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "JURISDICCION_NO_DECLARADA",
      "severidad": "ALTA",
      "descripcion": "3 operacion(es) por $13,346,747 con contraparte en Islas Virgenes Britanicas, jurisdiccion en lista de riesgo",
      "metodologia": "paises de contraparte normalizados a ISO, contra el perfil y las listas",
      "monto": 13346746.9,
      "vence": "2026-09-22"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "ACELERACION",
      "severidad": "MEDIA",
      "descripcion": "los ultimos 30 dias promedian $455,700 diarios contra $55,494 historicos (8.2x)",
      "metodologia": "promedio diario de los ultimos 30 dias contra el resto",
      "monto": 13671014.67,
      "vence": "2026-09-22"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "CERRADO",
      "destino": "ANALISIS",
      "motivo": "3 alerta(s) de monitoreo (reapertura del legajo)"
     }
    }
   ],
   "nota": "Persona humana. Riesgo MEDIO con 30 puntos, regimen dd media, revision cada 36 meses. Condicion PEP nacional. 3 alertas de monitoreo por $40,688,776. Exposicion sancionatoria estimada en $13,671,015. Es una estimacion y no un calculo de multa: la fija la UIF en sumario. Queda a criterio del analista: decidir si la inusualidad se convierte en sospecha."
  },
  {
   "id": "CL013",
   "caso_id": "C00013",
   "nombre": "Sark Trust Services",
   "tipo": "ENTIDAD",
   "documentos": [
    "TAX_ID 55009911"
   ],
   "fecha_nacimiento": null,
   "nacionalidad": null,
   "pais_residencia": "Isla de Sark",
   "pais_residencia_iso": "GG",
   "riesgo_pais": "NO_COOPERANTE",
   "actividad": "Fideicomisos",
   "oferta_publica": false,
   "estado": "ANALISIS",
   "escalado": false,
   "riesgo": {
    "puntaje": 80.0,
    "nivel": "ALTO",
    "regimen": "DD_REFORZADA",
    "revision_meses": 12,
    "factores": [
     {
      "codigo": "PERSONA_JURIDICA",
      "dimension": "CLIENTE",
      "descripcion": "cliente es persona juridica o estructura",
      "puntos": 8.0
     },
     {
      "codigo": "BENEFICIARIO_NO_IDENTIFICADO",
      "dimension": "CLIENTE",
      "descripcion": "no se identifico beneficiario final",
      "puntos": 25.0
     },
     {
      "codigo": "TITULARIDAD_OPACA",
      "dimension": "CLIENTE",
      "descripcion": "titularidad no identificada: 100.0%",
      "puntos": 20.0
     },
     {
      "codigo": "JURISDICCION_NO_COOPERANTE",
      "dimension": "GEOGRAFICO",
      "descripcion": "jurisdiccion no cooperante a fines fiscales: Guernsey",
      "puntos": 12.0
     },
     {
      "codigo": "COINCIDENCIA_REVISION",
      "dimension": "CONTROL",
      "descripcion": "1 coincidencia(s) pendiente(s) de revision (max 78.4)",
      "puntos": 15.0
     }
    ],
    "elevadores": [
     "BENEFICIARIO_NO_IDENTIFICADO"
    ]
   },
   "coincidencias": [
    {
     "lista": "REPET",
     "id_origen": "6908490",
     "designado": "TARKHAN ISMAILOVICH GAZIEV",
     "matcheado": "Sever",
     "score": 78.4,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "ONU",
      "Al-Qaida",
      "QDi.366"
     ],
     "atenuantes": []
    }
   ],
   "congelamiento": null,
   "beneficiario": {
    "identificado": false,
    "exceptuada": false,
    "opaco": 1.0,
    "profundidad": 0,
    "umbral": 0.0,
    "beneficiarios": [],
    "menores": [],
    "ciclos": [],
    "observaciones": [
     "entidad del exterior sin oferta publica: no corresponde el umbral del 10%, se identifica a la totalidad de los beneficiarios",
     "sin beneficiario final identificable y sin administrador declarado",
     "titularidad no identificada: 100.00% del capital"
    ]
   },
   "pep": null,
   "alertas": [
    {
     "id": "525b44ddf3f8",
     "codigo": "JURISDICCION_NO_DECLARADA",
     "severidad": "ALTA",
     "descripcion": "6 operacion(es) por $23,136,812 con contraparte en Guernsey, jurisdiccion en lista de riesgo",
     "metodologia": "paises de contraparte normalizados a ISO, contra el perfil y las listas",
     "monto": 23136811.69,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-05-31",
     "dias_restantes": -113,
     "vencida": true,
     "operaciones": [
      {
       "fecha": "2026-03-02",
       "monto": 3107760.72,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Fideicomiso",
       "pais": "Isla de Sark",
       "referencia": ""
      },
      {
       "fecha": "2026-03-22",
       "monto": 3699023.67,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Fideicomiso",
       "pais": "Isla de Sark",
       "referencia": ""
      },
      {
       "fecha": "2026-04-11",
       "monto": 4859293.78,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Fideicomiso",
       "pais": "Isla de Sark",
       "referencia": ""
      },
      {
       "fecha": "2026-05-01",
       "monto": 4071480.97,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Fideicomiso",
       "pais": "Isla de Sark",
       "referencia": ""
      },
      {
       "fecha": "2026-05-21",
       "monto": 3546474.3,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Fideicomiso",
       "pais": "Isla de Sark",
       "referencia": ""
      },
      {
       "fecha": "2026-06-10",
       "monto": 3852778.25,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Fideicomiso",
       "pais": "Isla de Sark",
       "referencia": ""
      }
     ]
    },
    {
     "id": "61316a385132",
     "codigo": "SIN_PERFIL",
     "severidad": "MEDIA",
     "descripcion": "opero 6 vez/veces por $23,136,812 sin perfil transaccional declarado",
     "metodologia": "ausencia de perfil declarado con operatoria registrada",
     "monto": 23136811.69,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-09-22",
     "dias_restantes": 1,
     "vencida": false,
     "operaciones": []
    }
   ],
   "operatoria": {
    "cantidad": 6,
    "total": 23136811.69,
    "efectivo": 0,
    "proporcion_efectivo": 0.0,
    "desde": "2026-03-02",
    "hasta": "2026-06-10",
    "paises": [
     "GG"
    ],
    "contrapartes": [
     "Fideicomiso"
    ]
   },
   "perfil": null,
   "exposicion": 23136811.69,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "6908490",
      "designado": "TARKHAN ISMAILOVICH GAZIEV",
      "matcheo_contra": "Sever",
      "score": 78.4,
      "criterio": "NOMBRE",
      "atenuantes": [],
      "programas": [
       "ONU",
       "Al-Qaida",
       "QDi.366"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "SCORING",
      "motivo": "1 coincidencia(s) para revision"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "BENEFICIARIO_FINAL",
     "detalle": {
      "identificados": [],
      "titularidad_opaca": "100.00%",
      "niveles": 0,
      "observaciones": [
       "entidad del exterior sin oferta publica: no corresponde el umbral del 10%, se identifica a la totalidad de los beneficiarios",
       "sin beneficiario final identificable y sin administrador declarado",
       "titularidad no identificada: 100.00% del capital"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "SCORING_EBR",
     "detalle": {
      "puntaje": 80.0,
      "nivel": "ALTO",
      "regimen": "DD_REFORZADA",
      "factores": [
       "PERSONA_JURIDICA(+8): cliente es persona juridica o estructura",
       "BENEFICIARIO_NO_IDENTIFICADO(+25): no se identifico beneficiario final",
       "TITULARIDAD_OPACA(+20): titularidad no identificada: 100.0%",
       "JURISDICCION_NO_COOPERANTE(+12): jurisdiccion no cooperante a fines fiscales: Guernsey",
       "COINCIDENCIA_REVISION(+15): 1 coincidencia(s) pendiente(s) de revision (max 78.4)"
      ],
      "elevadores": [
       "BENEFICIARIO_NO_IDENTIFICADO"
      ],
      "proxima_revision": "2027-09-21"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCORING",
      "destino": "ANALISIS",
      "motivo": "riesgo alto (80.0 pts) requiere diligencia reforzada"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "JURISDICCION_NO_DECLARADA",
      "severidad": "ALTA",
      "descripcion": "6 operacion(es) por $23,136,812 con contraparte en Guernsey, jurisdiccion en lista de riesgo",
      "metodologia": "paises de contraparte normalizados a ISO, contra el perfil y las listas",
      "monto": 23136811.69,
      "vence": "2026-05-31"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "SIN_PERFIL",
      "severidad": "MEDIA",
      "descripcion": "opero 6 vez/veces por $23,136,812 sin perfil transaccional declarado",
      "metodologia": "ausencia de perfil declarado con operatoria registrada",
      "monto": 23136811.69,
      "vence": "2026-09-22"
     }
    }
   ],
   "nota": "Persona juridica. Riesgo ALTO con 80 puntos, regimen dd reforzada, revision cada 12 meses. 1 coincidencia por debajo del umbral de probable, para descarte manual. No se pudo identificar al beneficiario final, 100% de titularidad sin identificar. Es un impedimento para operar, no un dato pendiente. 2 alertas de monitoreo por $46,273,623, 1 con el plazo de reporte ya vencido. El tope corre desde la operacion y no desde la deteccion. Exposicion sancionatoria estimada en $23,136,812. Es una estimacion y no un calculo de multa: la fija la UIF en sumario. Queda a criterio del analista: descartar las coincidencias por debajo del umbral, decidir si la inusualidad se convierte en sospecha, completar la cadena de beneficiario final."
  },
  {
   "id": "CL014",
   "caso_id": "C00014",
   "nombre": "Nadia Haddad",
   "tipo": "PERSONA",
   "documentos": [
    "PASAPORTE LB884422"
   ],
   "fecha_nacimiento": "1982-09-03",
   "nacionalidad": "Líbano",
   "pais_residencia": "Argentina",
   "pais_residencia_iso": "AR",
   "riesgo_pais": "ORDINARIA",
   "actividad": "Comercio",
   "oferta_publica": false,
   "estado": "ANALISIS",
   "escalado": false,
   "riesgo": {
    "puntaje": 38.0,
    "nivel": "MEDIO",
    "regimen": "DD_MEDIA",
    "revision_meses": 36,
    "factores": [
     {
      "codigo": "JURISDICCION_MONITOREO",
      "dimension": "GEOGRAFICO",
      "descripcion": "jurisdiccion GAFI bajo monitoreo intensificado: Libano",
      "puntos": 18.0
     },
     {
      "codigo": "RESIDENCIA_DISTINTA",
      "dimension": "GEOGRAFICO",
      "descripcion": "reside en Argentina con nacionalidad Libano",
      "puntos": 5.0
     },
     {
      "codigo": "COINCIDENCIA_REVISION",
      "dimension": "CONTROL",
      "descripcion": "1 coincidencia(s) pendiente(s) de revision (max 80.5)",
      "puntos": 15.0
     }
    ],
    "elevadores": []
   },
   "coincidencias": [
    {
     "lista": "REPET",
     "id_origen": "111922",
     "designado": "IMED BEN MEKKI ZARKAOUI",
     "matcheado": "Nadra",
     "score": 80.5,
     "criterio": "NOMBRE",
     "probable": false,
     "programas": [
      "ONU",
      "Al-Qaida",
      "QDi.139"
     ],
     "atenuantes": [
      "nacionalidad discordante (LÍBANO vs TUNISIA)"
     ]
    }
   ],
   "congelamiento": null,
   "beneficiario": null,
   "pep": null,
   "alertas": [
    {
     "id": "93d693fc9910",
     "codigo": "DESVIO_PERFIL",
     "severidad": "ALTA",
     "descripcion": "09/2026: opero $18,242,214 contra $1,400,000 declarados (13.0x)",
     "metodologia": "comparacion mensual contra perfil, tolerancia 25%",
     "monto": 18242213.83,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-09-22",
     "dias_restantes": 1,
     "vencida": false,
     "operaciones": [
      {
       "fecha": "2026-09-09",
       "monto": 2742597.61,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-09-07",
       "monto": 2575940.37,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-09-15",
       "monto": 2470314.4,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-09-11",
       "monto": 2220394.59,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-09-05",
       "monto": 2173337.73,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-09-03",
       "monto": 2171130.99,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-09-01",
       "monto": 2081948.37,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-09-13",
       "monto": 1806549.77,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      }
     ]
    },
    {
     "id": "bde31162bcea",
     "codigo": "ACELERACION",
     "severidad": "MEDIA",
     "descripcion": "los ultimos 30 dias promedian $1,130,492 diarios contra $24,118 historicos (46.9x)",
     "metodologia": "promedio diario de los ultimos 30 dias contra el resto",
     "monto": 33914747.72,
     "regimen": "LA",
     "generada": "2026-09-21",
     "vence": "2026-09-22",
     "dias_restantes": 1,
     "vencida": false,
     "operaciones": [
      {
       "fecha": "2026-08-20",
       "monto": 2245473.7,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-08-22",
       "monto": 2464474.43,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-08-24",
       "monto": 2374033.86,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-08-26",
       "monto": 3214708.52,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-08-28",
       "monto": 3332369.93,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-08-30",
       "monto": 2041473.45,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-09-01",
       "monto": 2081948.37,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-09-03",
       "monto": 2171130.99,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-09-05",
       "monto": 2173337.73,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      },
      {
       "fecha": "2026-09-07",
       "monto": 2575940.37,
       "sentido": "INGRESO",
       "instrumento": "TRANSFERENCIA",
       "canal": "ELECTRONICO",
       "contraparte": "Comercio",
       "pais": "Argentina",
       "referencia": ""
      }
     ]
    }
   ],
   "operatoria": {
    "cantidad": 34,
    "total": 37942440.52,
    "efectivo": 0,
    "proporcion_efectivo": 0.0,
    "desde": "2026-03-02",
    "hasta": "2026-09-15",
    "paises": [
     "AR"
    ],
    "contrapartes": [
     "Comercio"
    ]
   },
   "perfil": {
    "monto_mensual": 1400000.0,
    "operaciones_mensuales": 4,
    "proporcion_efectivo": 0.05,
    "paises": [
     "AR"
    ],
    "origen_fondos": "Comercio minorista",
    "proposito": "Cuenta comercial"
   },
   "exposicion": 33914747.72,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "COINCIDENCIA",
     "detalle": {
      "lista": "REPET",
      "id_origen": "111922",
      "designado": "IMED BEN MEKKI ZARKAOUI",
      "matcheo_contra": "Nadra",
      "score": 80.5,
      "criterio": "NOMBRE",
      "atenuantes": [
       "nacionalidad discordante (LÍBANO vs TUNISIA)"
      ],
      "programas": [
       "ONU",
       "Al-Qaida",
       "QDi.139"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "SCORING",
      "motivo": "1 coincidencia(s) para revision"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "SCORING_EBR",
     "detalle": {
      "puntaje": 38.0,
      "nivel": "MEDIO",
      "regimen": "DD_MEDIA",
      "factores": [
       "JURISDICCION_MONITOREO(+18): jurisdiccion GAFI bajo monitoreo intensificado: Libano",
       "RESIDENCIA_DISTINTA(+5): reside en Argentina con nacionalidad Libano",
       "COINCIDENCIA_REVISION(+15): 1 coincidencia(s) pendiente(s) de revision (max 80.5)"
      ],
      "elevadores": [],
      "proxima_revision": "2029-09-21"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCORING",
      "destino": "CERRADO",
      "motivo": "riesgo medio (38.0 pts), DD_MEDIA"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "DESVIO_PERFIL",
      "severidad": "ALTA",
      "descripcion": "09/2026: opero $18,242,214 contra $1,400,000 declarados (13.0x)",
      "metodologia": "comparacion mensual contra perfil, tolerancia 25%",
      "monto": 18242213.83,
      "vence": "2026-09-22"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "ALERTA_MONITOREO",
     "detalle": {
      "tipo": "ACELERACION",
      "severidad": "MEDIA",
      "descripcion": "los ultimos 30 dias promedian $1,130,492 diarios contra $24,118 historicos (46.9x)",
      "metodologia": "promedio diario de los ultimos 30 dias contra el resto",
      "monto": 33914747.72,
      "vence": "2026-09-22"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "CERRADO",
      "destino": "ANALISIS",
      "motivo": "2 alerta(s) de monitoreo (reapertura del legajo)"
     }
    }
   ],
   "nota": "Persona humana. Riesgo MEDIO con 38 puntos, regimen dd media, revision cada 36 meses. 1 coincidencia por debajo del umbral de probable, para descarte manual. 2 alertas de monitoreo por $52,156,962. Exposicion sancionatoria estimada en $33,914,748. Es una estimacion y no un calculo de multa: la fija la UIF en sumario. Queda a criterio del analista: descartar las coincidencias por debajo del umbral, decidir si la inusualidad se convierte en sospecha."
  },
  {
   "id": "CL015",
   "caso_id": "C00015",
   "nombre": "Pyongyang Trading Co",
   "tipo": "ENTIDAD",
   "documentos": [
    "TAX_ID 11223344"
   ],
   "fecha_nacimiento": null,
   "nacionalidad": null,
   "pais_residencia": "República Popular Democrática de Corea",
   "pais_residencia_iso": "KP",
   "riesgo_pais": "ALTO_RIESGO",
   "actividad": "Comercio exterior",
   "oferta_publica": false,
   "estado": "ANALISIS",
   "escalado": false,
   "riesgo": {
    "puntaje": 125.0,
    "nivel": "ALTO",
    "regimen": "DD_REFORZADA",
    "revision_meses": 12,
    "factores": [
     {
      "codigo": "PERSONA_JURIDICA",
      "dimension": "CLIENTE",
      "descripcion": "cliente es persona juridica o estructura",
      "puntos": 8.0
     },
     {
      "codigo": "BENEFICIARIO_NO_IDENTIFICADO",
      "dimension": "CLIENTE",
      "descripcion": "no se identifico beneficiario final",
      "puntos": 25.0
     },
     {
      "codigo": "TITULARIDAD_OPACA",
      "dimension": "CLIENTE",
      "descripcion": "titularidad no identificada: 100.0%",
      "puntos": 20.0
     },
     {
      "codigo": "JURISDICCION_CONTRAMEDIDAS",
      "dimension": "GEOGRAFICO",
      "descripcion": "jurisdiccion GAFI sujeta a contramedidas: Corea del Norte",
      "puntos": 45.0
     },
     {
      "codigo": "JURISDICCION_NO_COOPERANTE",
      "dimension": "GEOGRAFICO",
      "descripcion": "jurisdiccion no cooperante a fines fiscales: Corea del Norte",
      "puntos": 12.0
     },
     {
      "codigo": "ACTIVIDAD_SENSIBLE",
      "dimension": "ACTIVIDAD",
      "descripcion": "actividad de exposicion elevada: COMERCIO EXTERIOR",
      "puntos": 15.0
     }
    ],
    "elevadores": [
     "BENEFICIARIO_NO_IDENTIFICADO",
     "JURISDICCION_ALTO_RIESGO"
    ]
   },
   "coincidencias": [],
   "congelamiento": null,
   "beneficiario": {
    "identificado": false,
    "exceptuada": false,
    "opaco": 1.0,
    "profundidad": 0,
    "umbral": 0.0,
    "beneficiarios": [],
    "menores": [],
    "ciclos": [],
    "observaciones": [
     "entidad del exterior sin oferta publica: no corresponde el umbral del 10%, se identifica a la totalidad de los beneficiarios",
     "sin beneficiario final identificable y sin administrador declarado",
     "titularidad no identificada: 100.00% del capital"
    ]
   },
   "pep": null,
   "alertas": [],
   "operatoria": null,
   "perfil": null,
   "exposicion": 0,
   "expediente": [
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "ALTA",
      "destino": "SCREENING",
      "motivo": "inicio de cotejo contra listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:11+00:00",
     "actor": "sistema/legajo",
     "accion": "SCREENING_EJECUTADO",
     "detalle": {
      "listas": [
       "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
       "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
       "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
       "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
      ],
      "umbral_revision": 78.0,
      "umbral_probable": 92.0,
      "designados_evaluados": 725
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "SIN_COINCIDENCIAS",
     "detalle": {}
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCREENING",
      "destino": "SCORING",
      "motivo": "sin coincidencias en listas"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "BENEFICIARIO_FINAL",
     "detalle": {
      "identificados": [],
      "titularidad_opaca": "100.00%",
      "niveles": 0,
      "observaciones": [
       "entidad del exterior sin oferta publica: no corresponde el umbral del 10%, se identifica a la totalidad de los beneficiarios",
       "sin beneficiario final identificable y sin administrador declarado",
       "titularidad no identificada: 100.00% del capital"
      ]
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "SCORING_EBR",
     "detalle": {
      "puntaje": 125.0,
      "nivel": "ALTO",
      "regimen": "DD_REFORZADA",
      "factores": [
       "PERSONA_JURIDICA(+8): cliente es persona juridica o estructura",
       "BENEFICIARIO_NO_IDENTIFICADO(+25): no se identifico beneficiario final",
       "TITULARIDAD_OPACA(+20): titularidad no identificada: 100.0%",
       "JURISDICCION_CONTRAMEDIDAS(+45): jurisdiccion GAFI sujeta a contramedidas: Corea del Norte",
       "JURISDICCION_NO_COOPERANTE(+12): jurisdiccion no cooperante a fines fiscales: Corea del Norte",
       "ACTIVIDAD_SENSIBLE(+15): actividad de exposicion elevada: COMERCIO EXTERIOR"
      ],
      "elevadores": [
       "BENEFICIARIO_NO_IDENTIFICADO",
       "JURISDICCION_ALTO_RIESGO"
      ],
      "proxima_revision": "2027-09-21"
     }
    },
    {
     "momento": "2026-09-21T03:30:12+00:00",
     "actor": "sistema/legajo",
     "accion": "TRANSICION",
     "detalle": {
      "origen": "SCORING",
      "destino": "ANALISIS",
      "motivo": "riesgo alto (125.0 pts) requiere diligencia reforzada"
     }
    }
   ],
   "nota": "Persona juridica. Riesgo ALTO con 125 puntos, regimen dd reforzada, revision cada 12 meses. No se pudo identificar al beneficiario final, 100% de titularidad sin identificar. Es un impedimento para operar, no un dato pendiente. Queda a criterio del analista: completar la cadena de beneficiario final."
  }
 ],
 "grafo": {
  "nodos": [
   {
    "id": "cli:CL001",
    "tipo": "CLIENTE",
    "etiqueta": "Juan Pérez",
    "subtipo": "PERSONA",
    "nivel": "BAJO",
    "escalado": false,
    "estado": "CERRADO",
    "congelado": false,
    "alertas": 0,
    "puntaje": 0
   },
   {
    "id": "cp:Proveedor local",
    "tipo": "CONTRAPARTE",
    "etiqueta": "Proveedor local"
   },
   {
    "id": "cli:CL002",
    "tipo": "CLIENTE",
    "etiqueta": "Alireza Abbas",
    "subtipo": "PERSONA",
    "nivel": "SIN_SCORE",
    "escalado": true,
    "estado": "ESCALADO",
    "congelado": true,
    "alertas": 0,
    "puntaje": 0.0
   },
   {
    "id": "pais:IR",
    "tipo": "PAIS",
    "etiqueta": "Iran",
    "riesgo": "ALTO_RIESGO"
   },
   {
    "id": "des:OFAC_SDN:36",
    "tipo": "DESIGNADO",
    "etiqueta": "ABBAS, Ali Reza",
    "lista": "OFAC_SDN",
    "programas": [
     "SDGT"
    ]
   },
   {
    "id": "des:ONU_CONSOLIDADA:6908001",
    "tipo": "DESIGNADO",
    "etiqueta": "Ali Reza Abbas",
    "lista": "ONU_CONSOLIDADA",
    "programas": [
     "Iran"
    ]
   },
   {
    "id": "des:REPET:2975591",
    "tipo": "DESIGNADO",
    "etiqueta": "ABDUL AZIZ ABBASIN",
    "lista": "REPET",
    "programas": [
     "ONU",
     "Taliban",
     "TAi.155"
    ]
   },
   {
    "id": "des:REPET:119",
    "tipo": "DESIGNADO",
    "etiqueta": "HAYTHAM ALL TABATABA `I",
    "lista": "REPET",
    "programas": [
     "LOCAL",
     "SDN - EEUU"
    ]
   },
   {
    "id": "des:REPET:9",
    "tipo": "DESIGNADO",
    "etiqueta": "Alí Akbar Velayati",
    "lista": "REPET",
    "programas": [
     "LOCAL",
     "UFI AMIA",
     "HArP.00009"
    ]
   },
   {
    "id": "des:REPET:29",
    "tipo": "DESIGNADO",
    "etiqueta": "MOUSA HATEM BARAKAT",
    "lista": "REPET",
    "programas": [
     "LOCAL",
     "U.I.F"
    ]
   },
   {
    "id": "des:REPET:69",
    "tipo": "DESIGNADO",
    "etiqueta": "MOUSA HATEM BARAKAT",
    "lista": "REPET",
    "programas": [
     "LOCAL",
     "Unidad de Información Financiera"
    ]
   },
   {
    "id": "cli:CL003",
    "tipo": "CLIENTE",
    "etiqueta": "Petroquímica del Sur S.A.",
    "subtipo": "ENTIDAD",
    "nivel": "SIN_SCORE",
    "escalado": true,
    "estado": "ESCALADO",
    "congelado": true,
    "alertas": 0,
    "puntaje": 0.0
   },
   {
    "id": "des:OFAC_SDN:1201",
    "tipo": "DESIGNADO",
    "etiqueta": "PETROQUIMICA DEL SUR SA",
    "lista": "OFAC_SDN",
    "programas": [
     "NPWMD"
    ]
   },
   {
    "id": "per:P-002",
    "tipo": "BENEFICIARIO",
    "etiqueta": "Silvia Marconi",
    "jurisdiccion": "AR"
   },
   {
    "id": "per:P-001",
    "tipo": "BENEFICIARIO",
    "etiqueta": "Roberto Iglesias",
    "jurisdiccion": "AR"
   },
   {
    "id": "cli:CL004",
    "tipo": "CLIENTE",
    "etiqueta": "Carlos A. Gomez Rivera",
    "subtipo": "PERSONA",
    "nivel": "SIN_SCORE",
    "escalado": true,
    "estado": "ESCALADO",
    "congelado": false,
    "alertas": 0,
    "puntaje": 0.0
   },
   {
    "id": "des:OFAC_SDN:7788",
    "tipo": "DESIGNADO",
    "etiqueta": "GOMEZ RIVERA, Carlos Alberto",
    "lista": "OFAC_SDN",
    "programas": [
     "SDNTK"
    ]
   },
   {
    "id": "cli:CL005",
    "tipo": "CLIENTE",
    "etiqueta": "María González",
    "subtipo": "PERSONA",
    "nivel": "BAJO",
    "escalado": false,
    "estado": "ANALISIS",
    "congelado": false,
    "alertas": 4,
    "puntaje": 15.0
   },
   {
    "id": "des:REPET:250",
    "tipo": "DESIGNADO",
    "etiqueta": "Gerardo Gonzalez Valencia",
    "lista": "REPET",
    "programas": [
     "LOCAL",
     "Narcotics Rewards Program U.S. Department State"
    ]
   },
   {
    "id": "cp:Deposito por ventanilla",
    "tipo": "CONTRAPARTE",
    "etiqueta": "Deposito por ventanilla"
   },
   {
    "id": "cp:Haberes",
    "tipo": "CONTRAPARTE",
    "etiqueta": "Haberes"
   },
   {
    "id": "cli:CL006",
    "tipo": "CLIENTE",
    "etiqueta": "Khaled Shaikh Mohamed",
    "subtipo": "PERSONA",
    "nivel": "SIN_SCORE",
    "escalado": true,
    "estado": "ESCALADO",
    "congelado": true,
    "alertas": 0,
    "puntaje": 0.0
   },
   {
    "id": "des:OFAC_SDN:4417",
    "tipo": "DESIGNADO",
    "etiqueta": "MOHAMMED, Khalid Sheikh",
    "lista": "OFAC_SDN",
    "programas": [
     "SDGT"
    ]
   },
   {
    "id": "des:REPET:3013137",
    "tipo": "DESIGNADO",
    "etiqueta": "AHMED SHAH NOORZAI OBAIDULLAH",
    "lista": "REPET",
    "programas": [
     "ONU",
     "Taliban",
     "TAi.166"
    ]
   },
   {
    "id": "des:REPET:2989740",
    "tipo": "DESIGNADO",
    "etiqueta": "KHAIRULLAH BARAKZAI KHUDAI NAZAR",
    "lista": "REPET",
    "programas": [
     "ONU",
     "Taliban",
     "TAi.163"
    ]
   },
   {
    "id": "des:REPET:2813149",
    "tipo": "DESIGNADO",
    "etiqueta": "PIO ABOGNE DE VERA",
    "lista": "REPET",
    "programas": [
     "ONU",
     "Al-Qaida",
     "QDi.245"
    ]
   },
   {
    "id": "des:REPET:6908491",
    "tipo": "DESIGNADO",
    "etiqueta": "TOREK AGHA",
    "lista": "REPET",
    "programas": [
     "ONU",
     "Taliban",
     "TAi.174"
    ]
   },
   {
    "id": "des:REPET:2833107",
    "tipo": "DESIGNADO",
    "etiqueta": "HAFIZ MUHAMMAD SAEED",
    "lista": "REPET",
    "programas": [
     "ONU",
     "Al-Qaida",
     "QDi.263"
    ]
   },
   {
    "id": "des:REPET:111090",
    "tipo": "DESIGNADO",
    "etiqueta": "AKHTAR MOHAMMAD MANSOUR SHAH MOHAMMED",
    "lista": "REPET",
    "programas": [
     "ONU",
     "Taliban",
     "TAi.011"
    ]
   },
   {
    "id": "cli:CL007",
    "tipo": "CLIENTE",
    "etiqueta": "Eastern Trading Co",
    "subtipo": "ENTIDAD",
    "nivel": "SIN_SCORE",
    "escalado": true,
    "estado": "ESCALADO",
    "congelado": true,
    "alertas": 0,
    "puntaje": 0.0
   },
   {
    "id": "des:OFAC_SDN:9001",
    "tipo": "DESIGNADO",
    "etiqueta": "EASTERN TRADING LIMITED",
    "lista": "OFAC_SDN",
    "programas": [
     "RES1718"
    ]
   },
   {
    "id": "des:REPET:2989573",
    "tipo": "DESIGNADO",
    "etiqueta": "ROSHAN MONEY EXCHANGE",
    "lista": "REPET",
    "programas": [
     "ONU",
     "Taliban",
     "TAe.011"
    ]
   },
   {
    "id": "des:REPET:113356",
    "tipo": "DESIGNADO",
    "etiqueta": "EASTERN TURKISTAN ISLAMIC MOVEMENT (ETIM)",
    "lista": "REPET",
    "programas": [
     "ONU",
     "Al-Qaida",
     "QDe.088"
    ]
   },
   {
    "id": "des:REPET:3000510",
    "tipo": "DESIGNADO",
    "etiqueta": "RAHAT LTD.",
    "lista": "REPET",
    "programas": [
     "ONU",
     "Taliban",
     "TAe.013"
    ]
   },
   {
    "id": "per:P-004",
    "tipo": "BENEFICIARIO",
    "etiqueta": "Marcelo Duarte",
    "jurisdiccion": "AR"
   },
   {
    "id": "cli:CL008",
    "tipo": "CLIENTE",
    "etiqueta": "Ana Beatriz Rodríguez",
    "subtipo": "PERSONA",
    "nivel": "BAJO",
    "escalado": false,
    "estado": "ANALISIS",
    "congelado": false,
    "alertas": 4,
    "puntaje": 0
   },
   {
    "id": "cp:Consultoria",
    "tipo": "CONTRAPARTE",
    "etiqueta": "Consultoria"
   },
   {
    "id": "cp:Transferencia recibida",
    "tipo": "CONTRAPARTE",
    "etiqueta": "Transferencia recibida"
   },
   {
    "id": "cli:CL009",
    "tipo": "CLIENTE",
    "etiqueta": "Delta Servicios Financieros SA",
    "subtipo": "ENTIDAD",
    "nivel": "ALTO",
    "escalado": false,
    "estado": "ANALISIS",
    "congelado": false,
    "alertas": 0,
    "puntaje": 55.0
   },
   {
    "id": "per:P-005",
    "tipo": "BENEFICIARIO",
    "etiqueta": "Laura Beltran",
    "jurisdiccion": "AR"
   },
   {
    "id": "per:P-006",
    "tipo": "BENEFICIARIO",
    "etiqueta": "Diego Sanguinetti",
    "jurisdiccion": "AR"
   },
   {
    "id": "cli:CL010",
    "tipo": "CLIENTE",
    "etiqueta": "Blue Harbour Trading Ltd",
    "subtipo": "ENTIDAD",
    "nivel": "ALTO",
    "escalado": false,
    "estado": "ANALISIS",
    "congelado": false,
    "alertas": 0,
    "puntaje": 76.0
   },
   {
    "id": "per:P-008",
    "tipo": "BENEFICIARIO",
    "etiqueta": "Elena Ferrari",
    "jurisdiccion": "ES"
   },
   {
    "id": "per:P-009",
    "tipo": "BENEFICIARIO",
    "etiqueta": "Tomas Rivas",
    "jurisdiccion": "ES"
   },
   {
    "id": "cli:CL011",
    "tipo": "CLIENTE",
    "etiqueta": "Grupo Cotizante SA",
    "subtipo": "ENTIDAD",
    "nivel": "BAJO",
    "escalado": false,
    "estado": "CERRADO",
    "congelado": false,
    "alertas": 0,
    "puntaje": 8.0
   },
   {
    "id": "cli:CL012",
    "tipo": "CLIENTE",
    "etiqueta": "Fernanda Ortiz",
    "subtipo": "PERSONA",
    "nivel": "MEDIO",
    "escalado": false,
    "estado": "ANALISIS",
    "congelado": false,
    "alertas": 3,
    "puntaje": 30.0
   },
   {
    "id": "cp:Cliente",
    "tipo": "CONTRAPARTE",
    "etiqueta": "Cliente"
   },
   {
    "id": "cp:Panama Trade SA",
    "tipo": "CONTRAPARTE",
    "etiqueta": "Panama Trade SA"
   },
   {
    "id": "cli:CL013",
    "tipo": "CLIENTE",
    "etiqueta": "Sark Trust Services",
    "subtipo": "ENTIDAD",
    "nivel": "ALTO",
    "escalado": false,
    "estado": "ANALISIS",
    "congelado": false,
    "alertas": 2,
    "puntaje": 80.0
   },
   {
    "id": "pais:GG",
    "tipo": "PAIS",
    "etiqueta": "Guernsey",
    "riesgo": "NO_COOPERANTE"
   },
   {
    "id": "des:REPET:6908490",
    "tipo": "DESIGNADO",
    "etiqueta": "TARKHAN ISMAILOVICH GAZIEV",
    "lista": "REPET",
    "programas": [
     "ONU",
     "Al-Qaida",
     "QDi.366"
    ]
   },
   {
    "id": "cp:Fideicomiso",
    "tipo": "CONTRAPARTE",
    "etiqueta": "Fideicomiso"
   },
   {
    "id": "cli:CL014",
    "tipo": "CLIENTE",
    "etiqueta": "Nadia Haddad",
    "subtipo": "PERSONA",
    "nivel": "MEDIO",
    "escalado": false,
    "estado": "ANALISIS",
    "congelado": false,
    "alertas": 2,
    "puntaje": 38.0
   },
   {
    "id": "des:REPET:111922",
    "tipo": "DESIGNADO",
    "etiqueta": "IMED BEN MEKKI ZARKAOUI",
    "lista": "REPET",
    "programas": [
     "ONU",
     "Al-Qaida",
     "QDi.139"
    ]
   },
   {
    "id": "cp:Comercio",
    "tipo": "CONTRAPARTE",
    "etiqueta": "Comercio"
   },
   {
    "id": "cli:CL015",
    "tipo": "CLIENTE",
    "etiqueta": "Pyongyang Trading Co",
    "subtipo": "ENTIDAD",
    "nivel": "ALTO",
    "escalado": false,
    "estado": "ANALISIS",
    "congelado": false,
    "alertas": 0,
    "puntaje": 125.0
   },
   {
    "id": "pais:KP",
    "tipo": "PAIS",
    "etiqueta": "Corea del Norte",
    "riesgo": "ALTO_RIESGO"
   },
   {
    "id": "soc:SOC-A",
    "tipo": "SOCIEDAD",
    "etiqueta": "Inversora del Plata SA",
    "jurisdiccion": "AR",
    "oferta_publica": false
   },
   {
    "id": "soc:P-003",
    "tipo": "PERSONA",
    "etiqueta": "Hector Ledesma",
    "jurisdiccion": "AR",
    "oferta_publica": false
   },
   {
    "id": "soc:SOC-B",
    "tipo": "SOCIEDAD",
    "etiqueta": "Andes Capital Ltd",
    "jurisdiccion": "KY",
    "oferta_publica": false
   },
   {
    "id": "soc:SOC-C",
    "tipo": "SOCIEDAD",
    "etiqueta": "Pacific Holdings BV",
    "jurisdiccion": "NL",
    "oferta_publica": false
   },
   {
    "id": "soc:SOC-D",
    "tipo": "SOCIEDAD",
    "etiqueta": "Offshore Nominees Inc",
    "jurisdiccion": "VG",
    "oferta_publica": false
   },
   {
    "id": "soc:P-007",
    "tipo": "PERSONA",
    "etiqueta": "Nora Vidal",
    "jurisdiccion": "AR",
    "oferta_publica": false
   },
   {
    "id": "soc:P-010",
    "tipo": "PERSONA",
    "etiqueta": "Gustavo Peralta",
    "jurisdiccion": "AR",
    "oferta_publica": false
   }
  ],
  "aristas": [
   {
    "id": "e00000",
    "origen": "cli:CL001",
    "destino": "cp:Proveedor local",
    "tipo": "OPERACION",
    "etiqueta": "operatoria",
    "peso": 0.2,
    "monto": 0,
    "cantidad": 0
   },
   {
    "id": "e00001",
    "origen": "cli:CL002",
    "destino": "pais:IR",
    "tipo": "JURISDICCION",
    "etiqueta": "alto riesgo",
    "peso": 1.0
   },
   {
    "id": "e00002",
    "origen": "cli:CL002",
    "destino": "des:OFAC_SDN:36",
    "tipo": "COINCIDENCIA",
    "etiqueta": "100",
    "peso": 1.0,
    "score": 100.0,
    "criterio": "DOCUMENTO",
    "probable": true,
    "lista": "OFAC_SDN"
   },
   {
    "id": "e00003",
    "origen": "cli:CL002",
    "destino": "des:ONU_CONSOLIDADA:6908001",
    "tipo": "COINCIDENCIA",
    "etiqueta": "100",
    "peso": 1.0,
    "score": 100.0,
    "criterio": "DOCUMENTO",
    "probable": true,
    "lista": "ONU_CONSOLIDADA"
   },
   {
    "id": "e00004",
    "origen": "cli:CL002",
    "destino": "des:REPET:2975591",
    "tipo": "COINCIDENCIA",
    "etiqueta": "82.6",
    "peso": 0.826,
    "score": 82.6,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00005",
    "origen": "cli:CL002",
    "destino": "des:REPET:119",
    "tipo": "COINCIDENCIA",
    "etiqueta": "78.9",
    "peso": 0.789,
    "score": 78.9,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00006",
    "origen": "cli:CL002",
    "destino": "des:REPET:9",
    "tipo": "COINCIDENCIA",
    "etiqueta": "78.6",
    "peso": 0.786,
    "score": 78.6,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00007",
    "origen": "cli:CL002",
    "destino": "des:REPET:29",
    "tipo": "COINCIDENCIA",
    "etiqueta": "78.4",
    "peso": 0.784,
    "score": 78.4,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00008",
    "origen": "cli:CL002",
    "destino": "des:REPET:69",
    "tipo": "COINCIDENCIA",
    "etiqueta": "78.4",
    "peso": 0.784,
    "score": 78.4,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00009",
    "origen": "cli:CL003",
    "destino": "des:OFAC_SDN:1201",
    "tipo": "COINCIDENCIA",
    "etiqueta": "100",
    "peso": 1.0,
    "score": 100.0,
    "criterio": "NOMBRE",
    "probable": true,
    "lista": "OFAC_SDN"
   },
   {
    "id": "e00010",
    "origen": "per:P-002",
    "destino": "cli:CL003",
    "tipo": "BENEFICIARIO",
    "etiqueta": "33% cap",
    "peso": 0.33,
    "capital": 0.33,
    "voto": 0.33,
    "via": "PARTICIPACION"
   },
   {
    "id": "e00011",
    "origen": "per:P-001",
    "destino": "cli:CL003",
    "tipo": "BENEFICIARIO",
    "etiqueta": "30% cap",
    "peso": 0.3,
    "capital": 0.3,
    "voto": 0.3,
    "via": "PARTICIPACION"
   },
   {
    "id": "e00012",
    "origen": "cli:CL004",
    "destino": "des:OFAC_SDN:7788",
    "tipo": "COINCIDENCIA",
    "etiqueta": "87.6",
    "peso": 0.876,
    "score": 87.6,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "OFAC_SDN"
   },
   {
    "id": "e00013",
    "origen": "cli:CL005",
    "destino": "des:REPET:250",
    "tipo": "COINCIDENCIA",
    "etiqueta": "79.3",
    "peso": 0.793,
    "score": 79.3,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00014",
    "origen": "cli:CL005",
    "destino": "cp:Deposito por ventanilla",
    "tipo": "OPERACION",
    "etiqueta": "$291,073,920",
    "peso": 1.0,
    "monto": 291073920.0,
    "cantidad": 20
   },
   {
    "id": "e00015",
    "origen": "cli:CL005",
    "destino": "cp:Haberes",
    "tipo": "OPERACION",
    "etiqueta": "operatoria",
    "peso": 0.2,
    "monto": 0,
    "cantidad": 0
   },
   {
    "id": "e00016",
    "origen": "cli:CL006",
    "destino": "des:OFAC_SDN:4417",
    "tipo": "COINCIDENCIA",
    "etiqueta": "97.8",
    "peso": 0.978,
    "score": 97.8,
    "criterio": "NOMBRE",
    "probable": true,
    "lista": "OFAC_SDN"
   },
   {
    "id": "e00017",
    "origen": "cli:CL006",
    "destino": "des:REPET:3013137",
    "tipo": "COINCIDENCIA",
    "etiqueta": "85.5",
    "peso": 0.855,
    "score": 85.5,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00018",
    "origen": "cli:CL006",
    "destino": "des:REPET:2989740",
    "tipo": "COINCIDENCIA",
    "etiqueta": "82",
    "peso": 0.82,
    "score": 82.0,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00019",
    "origen": "cli:CL006",
    "destino": "des:REPET:2813149",
    "tipo": "COINCIDENCIA",
    "etiqueta": "79.9",
    "peso": 0.799,
    "score": 79.9,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00020",
    "origen": "cli:CL006",
    "destino": "des:REPET:6908491",
    "tipo": "COINCIDENCIA",
    "etiqueta": "79.4",
    "peso": 0.794,
    "score": 79.4,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00021",
    "origen": "cli:CL006",
    "destino": "des:REPET:2833107",
    "tipo": "COINCIDENCIA",
    "etiqueta": "78.5",
    "peso": 0.785,
    "score": 78.5,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00022",
    "origen": "cli:CL006",
    "destino": "des:REPET:111090",
    "tipo": "COINCIDENCIA",
    "etiqueta": "78",
    "peso": 0.78,
    "score": 78.0,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00023",
    "origen": "cli:CL007",
    "destino": "des:OFAC_SDN:9001",
    "tipo": "COINCIDENCIA",
    "etiqueta": "100",
    "peso": 1.0,
    "score": 100.0,
    "criterio": "NOMBRE",
    "probable": true,
    "lista": "OFAC_SDN"
   },
   {
    "id": "e00024",
    "origen": "cli:CL007",
    "destino": "des:REPET:2989573",
    "tipo": "COINCIDENCIA",
    "etiqueta": "79",
    "peso": 0.79,
    "score": 79.0,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00025",
    "origen": "cli:CL007",
    "destino": "des:REPET:113356",
    "tipo": "COINCIDENCIA",
    "etiqueta": "78.9",
    "peso": 0.789,
    "score": 78.9,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00026",
    "origen": "cli:CL007",
    "destino": "des:REPET:3000510",
    "tipo": "COINCIDENCIA",
    "etiqueta": "78.1",
    "peso": 0.781,
    "score": 78.1,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00027",
    "origen": "per:P-004",
    "destino": "cli:CL007",
    "tipo": "BENEFICIARIO",
    "etiqueta": "50% cap",
    "peso": 0.5,
    "capital": 0.5,
    "voto": 0.5,
    "via": "PARTICIPACION"
   },
   {
    "id": "e00028",
    "origen": "cli:CL008",
    "destino": "cp:Consultoria",
    "tipo": "OPERACION",
    "etiqueta": "$107,710",
    "peso": 0.0011,
    "monto": 107709.87,
    "cantidad": 1
   },
   {
    "id": "e00029",
    "origen": "cli:CL008",
    "destino": "cp:Transferencia recibida",
    "tipo": "OPERACION",
    "etiqueta": "$118,380,081",
    "peso": 1.0,
    "monto": 118380081.39,
    "cantidad": 20
   },
   {
    "id": "e00030",
    "origen": "per:P-005",
    "destino": "cli:CL009",
    "tipo": "BENEFICIARIO",
    "etiqueta": "5% cap",
    "peso": 0.05,
    "capital": 0.05,
    "voto": 0.45,
    "via": "PARTICIPACION"
   },
   {
    "id": "e00031",
    "origen": "per:P-006",
    "destino": "cli:CL009",
    "tipo": "BENEFICIARIO",
    "etiqueta": "35% cap",
    "peso": 0.35,
    "capital": 0.35,
    "voto": 0.05,
    "via": "PARTICIPACION"
   },
   {
    "id": "e00032",
    "origen": "per:P-008",
    "destino": "cli:CL010",
    "tipo": "BENEFICIARIO",
    "etiqueta": "6% cap",
    "peso": 0.06,
    "capital": 0.06,
    "voto": 0.06,
    "via": "PARTICIPACION"
   },
   {
    "id": "e00033",
    "origen": "per:P-009",
    "destino": "cli:CL010",
    "tipo": "BENEFICIARIO",
    "etiqueta": "4% cap",
    "peso": 0.04,
    "capital": 0.04,
    "voto": 0.04,
    "via": "PARTICIPACION"
   },
   {
    "id": "e00034",
    "origen": "cli:CL012",
    "destino": "cp:Cliente",
    "tipo": "OPERACION",
    "etiqueta": "$648,536",
    "peso": 0.0065,
    "monto": 648535.54,
    "cantidad": 2
   },
   {
    "id": "e00035",
    "origen": "cli:CL012",
    "destino": "cp:Panama Trade SA",
    "tipo": "OPERACION",
    "etiqueta": "$40,040,241",
    "peso": 0.4004,
    "monto": 40040240.7,
    "cantidad": 9
   },
   {
    "id": "e00036",
    "origen": "cli:CL013",
    "destino": "pais:GG",
    "tipo": "JURISDICCION",
    "etiqueta": "no cooperante",
    "peso": 1.0
   },
   {
    "id": "e00037",
    "origen": "cli:CL013",
    "destino": "des:REPET:6908490",
    "tipo": "COINCIDENCIA",
    "etiqueta": "78.4",
    "peso": 0.784,
    "score": 78.4,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00038",
    "origen": "cli:CL013",
    "destino": "cp:Fideicomiso",
    "tipo": "OPERACION",
    "etiqueta": "$23,136,812",
    "peso": 0.2314,
    "monto": 23136811.69,
    "cantidad": 6
   },
   {
    "id": "e00039",
    "origen": "cli:CL014",
    "destino": "des:REPET:111922",
    "tipo": "COINCIDENCIA",
    "etiqueta": "80.5",
    "peso": 0.805,
    "score": 80.5,
    "criterio": "NOMBRE",
    "probable": false,
    "lista": "REPET"
   },
   {
    "id": "e00040",
    "origen": "cli:CL014",
    "destino": "cp:Comercio",
    "tipo": "OPERACION",
    "etiqueta": "$42,917,105",
    "peso": 0.4292,
    "monto": 42917105.18,
    "cantidad": 18
   },
   {
    "id": "e00041",
    "origen": "cli:CL015",
    "destino": "pais:KP",
    "tipo": "JURISDICCION",
    "etiqueta": "alto riesgo",
    "peso": 1.0
   },
   {
    "id": "e00042",
    "origen": "soc:SOC-A",
    "destino": "cli:CL003",
    "tipo": "PARTICIPACION",
    "etiqueta": "55%",
    "peso": 0.55,
    "capital": 0.55,
    "voto": 0.55
   },
   {
    "id": "e00043",
    "origen": "per:P-001",
    "destino": "cli:CL003",
    "tipo": "PARTICIPACION",
    "etiqueta": "8%",
    "peso": 0.08,
    "capital": 0.08,
    "voto": 0.08
   },
   {
    "id": "e00044",
    "origen": "per:P-001",
    "destino": "soc:SOC-A",
    "tipo": "PARTICIPACION",
    "etiqueta": "40%",
    "peso": 0.4,
    "capital": 0.4,
    "voto": 0.4
   },
   {
    "id": "e00045",
    "origen": "per:P-002",
    "destino": "soc:SOC-A",
    "tipo": "PARTICIPACION",
    "etiqueta": "60%",
    "peso": 0.6,
    "capital": 0.6,
    "voto": 0.6
   },
   {
    "id": "e00046",
    "origen": "soc:SOC-B",
    "destino": "cli:CL007",
    "tipo": "PARTICIPACION",
    "etiqueta": "50%",
    "peso": 0.5,
    "capital": 0.5,
    "voto": 0.5
   },
   {
    "id": "e00047",
    "origen": "soc:SOC-C",
    "destino": "cli:CL007",
    "tipo": "PARTICIPACION",
    "etiqueta": "50%",
    "peso": 0.5,
    "capital": 0.5,
    "voto": 0.5
   },
   {
    "id": "e00048",
    "origen": "per:P-004",
    "destino": "soc:SOC-B",
    "tipo": "PARTICIPACION",
    "etiqueta": "70%",
    "peso": 0.7,
    "capital": 0.7,
    "voto": 0.7
   },
   {
    "id": "e00049",
    "origen": "per:P-004",
    "destino": "soc:SOC-C",
    "tipo": "PARTICIPACION",
    "etiqueta": "30%",
    "peso": 0.3,
    "capital": 0.3,
    "voto": 0.3
   },
   {
    "id": "e00050",
    "origen": "soc:SOC-D",
    "destino": "soc:SOC-C",
    "tipo": "PARTICIPACION",
    "etiqueta": "70%",
    "peso": 0.7,
    "capital": 0.7,
    "voto": 0.7
   },
   {
    "id": "e00051",
    "origen": "soc:SOC-C",
    "destino": "soc:SOC-D",
    "tipo": "PARTICIPACION",
    "etiqueta": "100%",
    "peso": 1.0,
    "capital": 1.0,
    "voto": 1.0
   },
   {
    "id": "e00052",
    "origen": "per:P-005",
    "destino": "cli:CL009",
    "tipo": "PARTICIPACION",
    "etiqueta": "5%",
    "peso": 0.05,
    "capital": 0.05,
    "voto": 0.45
   },
   {
    "id": "e00053",
    "origen": "per:P-006",
    "destino": "cli:CL009",
    "tipo": "PARTICIPACION",
    "etiqueta": "35%",
    "peso": 0.35,
    "capital": 0.35,
    "voto": 0.05
   },
   {
    "id": "e00054",
    "origen": "per:P-008",
    "destino": "cli:CL010",
    "tipo": "PARTICIPACION",
    "etiqueta": "6%",
    "peso": 0.06,
    "capital": 0.06,
    "voto": 0.06
   },
   {
    "id": "e00055",
    "origen": "per:P-009",
    "destino": "cli:CL010",
    "tipo": "PARTICIPACION",
    "etiqueta": "4%",
    "peso": 0.04,
    "capital": 0.04,
    "voto": 0.04
   },
   {
    "id": "e00056",
    "origen": "soc:P-010",
    "destino": "cli:CL011",
    "tipo": "PARTICIPACION",
    "etiqueta": "30%",
    "peso": 0.3,
    "capital": 0.3,
    "voto": 0.3
   }
  ]
 },
 "eventos": [
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL001",
   "cliente": "Juan Pérez",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL001",
   "cliente": "Juan Pérez",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL001",
   "cliente": "Juan Pérez",
   "actor": "sistema/legajo",
   "accion": "SIN_COINCIDENCIAS",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {}
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL001",
   "cliente": "Juan Pérez",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "SCORING",
    "motivo": "sin coincidencias en listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL002",
   "cliente": "Alireza Abbas",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL002",
   "cliente": "Alireza Abbas",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL002",
   "cliente": "Alireza Abbas",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "OFAC_SDN",
    "id_origen": "36",
    "designado": "ABBAS, Ali Reza",
    "matcheo_contra": "PASAPORTE:K1234567",
    "score": 100.0,
    "criterio": "DOCUMENTO",
    "atenuantes": [],
    "programas": [
     "SDGT"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL002",
   "cliente": "Alireza Abbas",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "ONU_CONSOLIDADA",
    "id_origen": "6908001",
    "designado": "Ali Reza Abbas",
    "matcheo_contra": "PASAPORTE:K1234567",
    "score": 100.0,
    "criterio": "DOCUMENTO",
    "atenuantes": [],
    "programas": [
     "Iran"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL002",
   "cliente": "Alireza Abbas",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "2975591",
    "designado": "ABDUL AZIZ ABBASIN",
    "matcheo_contra": "ABDUL AZIZ ABBASIN",
    "score": 82.6,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "ONU",
     "Taliban",
     "TAi.155"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL002",
   "cliente": "Alireza Abbas",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "119",
    "designado": "HAYTHAM ALL TABATABA `I",
    "matcheo_contra": "Abu Ali Al-TABATABA `I; Abu Ali TABATABAI; Abu Ali TABTABAI",
    "score": 78.9,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "LOCAL",
     "SDN - EEUU"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL002",
   "cliente": "Alireza Abbas",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "9",
    "designado": "Alí Akbar Velayati",
    "matcheo_contra": "Alí Akbar Velayati",
    "score": 78.6,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "LOCAL",
     "UFI AMIA",
     "HArP.00009"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL002",
   "cliente": "Alireza Abbas",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "29",
    "designado": "MOUSA HATEM BARAKAT",
    "matcheo_contra": "ABU ALI BARAKAT",
    "score": 78.4,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "LOCAL",
     "U.I.F"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL002",
   "cliente": "Alireza Abbas",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "69",
    "designado": "MOUSA HATEM BARAKAT",
    "matcheo_contra": "ABU ALI BARAKAT",
    "score": 78.4,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "LOCAL",
     "Unidad de Información Financiera"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL002",
   "cliente": "Alireza Abbas",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "ESCALADO",
    "motivo": "coincidencia en lista critica (OFAC_SDN, score 100.0)"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL003",
   "cliente": "Petroquímica del Sur S.A.",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL003",
   "cliente": "Petroquímica del Sur S.A.",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL003",
   "cliente": "Petroquímica del Sur S.A.",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "OFAC_SDN",
    "id_origen": "1201",
    "designado": "PETROQUIMICA DEL SUR SA",
    "matcheo_contra": "PETROQUIMICA DEL SUR SA",
    "score": 100.0,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "NPWMD"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL003",
   "cliente": "Petroquímica del Sur S.A.",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "ESCALADO",
    "motivo": "coincidencia en lista critica (OFAC_SDN, score 100.0)"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL004",
   "cliente": "Carlos A. Gomez Rivera",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL004",
   "cliente": "Carlos A. Gomez Rivera",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL004",
   "cliente": "Carlos A. Gomez Rivera",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "OFAC_SDN",
    "id_origen": "7788",
    "designado": "GOMEZ RIVERA, Carlos Alberto",
    "matcheo_contra": "GOMEZ RIVERA, Carlos Alberto",
    "score": 87.6,
    "criterio": "NOMBRE",
    "atenuantes": [
     "nacionalidad discordante (ARGENTINA vs COLOMBIA)"
    ],
    "programas": [
     "SDNTK"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL004",
   "cliente": "Carlos A. Gomez Rivera",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "ESCALADO",
    "motivo": "coincidencia en lista critica (OFAC_SDN, score 87.6)"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL005",
   "cliente": "María González",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL005",
   "cliente": "María González",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL005",
   "cliente": "María González",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "250",
    "designado": "Gerardo Gonzalez Valencia",
    "matcheo_contra": "Gerardo Gonzalez Valencia",
    "score": 79.3,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "LOCAL",
     "Narcotics Rewards Program U.S. Department State"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL005",
   "cliente": "María González",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "SCORING",
    "motivo": "1 coincidencia(s) para revision"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL006",
   "cliente": "Khaled Shaikh Mohamed",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL006",
   "cliente": "Khaled Shaikh Mohamed",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL006",
   "cliente": "Khaled Shaikh Mohamed",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "OFAC_SDN",
    "id_origen": "4417",
    "designado": "MOHAMMED, Khalid Sheikh",
    "matcheo_contra": "MOHAMED, Khalid Shaikh",
    "score": 97.8,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "SDGT"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL006",
   "cliente": "Khaled Shaikh Mohamed",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "3013137",
    "designado": "AHMED SHAH NOORZAI OBAIDULLAH",
    "matcheo_contra": "Mullah Mohammed Shah",
    "score": 85.5,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "ONU",
     "Taliban",
     "TAi.166"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL006",
   "cliente": "Khaled Shaikh Mohamed",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "2989740",
    "designado": "KHAIRULLAH BARAKZAI KHUDAI NAZAR",
    "matcheo_contra": "Haji Khair Mohammad",
    "score": 82.0,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "ONU",
     "Taliban",
     "TAi.163"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL006",
   "cliente": "Khaled Shaikh Mohamed",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "2813149",
    "designado": "PIO ABOGNE DE VERA",
    "matcheo_contra": "Khalid",
    "score": 79.9,
    "criterio": "NOMBRE",
    "atenuantes": [
     "nacionalidad discordante (PAKISTAN vs PHILIPPINES)"
    ],
    "programas": [
     "ONU",
     "Al-Qaida",
     "QDi.245"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL006",
   "cliente": "Khaled Shaikh Mohamed",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "6908491",
    "designado": "TOREK AGHA",
    "matcheo_contra": "Sayed Mohammed Hashan",
    "score": 79.4,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "ONU",
     "Taliban",
     "TAi.174"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL006",
   "cliente": "Khaled Shaikh Mohamed",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "2833107",
    "designado": "HAFIZ MUHAMMAD SAEED",
    "matcheo_contra": "Mohammad Sayed",
    "score": 78.5,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "ONU",
     "Al-Qaida",
     "QDi.263"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL006",
   "cliente": "Khaled Shaikh Mohamed",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "111090",
    "designado": "AKHTAR MOHAMMAD MANSOUR SHAH MOHAMMED",
    "matcheo_contra": "AKHTAR MOHAMMAD MANSOUR SHAH MOHAMMED",
    "score": 78.0,
    "criterio": "NOMBRE",
    "atenuantes": [
     "nacionalidad discordante (PAKISTAN vs AFGHANISTAN)"
    ],
    "programas": [
     "ONU",
     "Taliban",
     "TAi.011"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL006",
   "cliente": "Khaled Shaikh Mohamed",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "ESCALADO",
    "motivo": "coincidencia en lista critica (OFAC_SDN, score 97.8)"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL007",
   "cliente": "Eastern Trading Co",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL007",
   "cliente": "Eastern Trading Co",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL007",
   "cliente": "Eastern Trading Co",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "OFAC_SDN",
    "id_origen": "9001",
    "designado": "EASTERN TRADING LIMITED",
    "matcheo_contra": "EASTERN TRADING LIMITED",
    "score": 100.0,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "RES1718"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL007",
   "cliente": "Eastern Trading Co",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "2989573",
    "designado": "ROSHAN MONEY EXCHANGE",
    "matcheo_contra": "Roshan Trading Company",
    "score": 79.0,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "ONU",
     "Taliban",
     "TAe.011"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL007",
   "cliente": "Eastern Trading Co",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "113356",
    "designado": "EASTERN TURKISTAN ISLAMIC MOVEMENT (ETIM)",
    "matcheo_contra": "EASTERN TURKISTAN ISLAMIC MOVEMENT (ETIM)",
    "score": 78.9,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "ONU",
     "Al-Qaida",
     "QDe.088"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL007",
   "cliente": "Eastern Trading Co",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "3000510",
    "designado": "RAHAT LTD.",
    "matcheo_contra": "Rahat Trading Company",
    "score": 78.1,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "ONU",
     "Taliban",
     "TAe.013"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL007",
   "cliente": "Eastern Trading Co",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "ESCALADO",
    "motivo": "coincidencia en lista critica (OFAC_SDN, score 100.0)"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL008",
   "cliente": "Ana Beatriz Rodríguez",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL008",
   "cliente": "Ana Beatriz Rodríguez",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL008",
   "cliente": "Ana Beatriz Rodríguez",
   "actor": "sistema/legajo",
   "accion": "SIN_COINCIDENCIAS",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {}
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL008",
   "cliente": "Ana Beatriz Rodríguez",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "SCORING",
    "motivo": "sin coincidencias en listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL009",
   "cliente": "Delta Servicios Financieros SA",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL009",
   "cliente": "Delta Servicios Financieros SA",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL009",
   "cliente": "Delta Servicios Financieros SA",
   "actor": "sistema/legajo",
   "accion": "SIN_COINCIDENCIAS",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {}
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL009",
   "cliente": "Delta Servicios Financieros SA",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "SCORING",
    "motivo": "sin coincidencias en listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL010",
   "cliente": "Blue Harbour Trading Ltd",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL010",
   "cliente": "Blue Harbour Trading Ltd",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL010",
   "cliente": "Blue Harbour Trading Ltd",
   "actor": "sistema/legajo",
   "accion": "SIN_COINCIDENCIAS",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {}
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL010",
   "cliente": "Blue Harbour Trading Ltd",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "SCORING",
    "motivo": "sin coincidencias en listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL011",
   "cliente": "Grupo Cotizante SA",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL011",
   "cliente": "Grupo Cotizante SA",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL011",
   "cliente": "Grupo Cotizante SA",
   "actor": "sistema/legajo",
   "accion": "SIN_COINCIDENCIAS",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {}
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL011",
   "cliente": "Grupo Cotizante SA",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "SCORING",
    "motivo": "sin coincidencias en listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL012",
   "cliente": "Fernanda Ortiz",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "MEDIO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL012",
   "cliente": "Fernanda Ortiz",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "MEDIO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL012",
   "cliente": "Fernanda Ortiz",
   "actor": "sistema/legajo",
   "accion": "SIN_COINCIDENCIAS",
   "nivel": "MEDIO",
   "severidad": "",
   "regimen": "",
   "detalle": {}
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL012",
   "cliente": "Fernanda Ortiz",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "MEDIO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "SCORING",
    "motivo": "sin coincidencias en listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL013",
   "cliente": "Sark Trust Services",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL013",
   "cliente": "Sark Trust Services",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL013",
   "cliente": "Sark Trust Services",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "6908490",
    "designado": "TARKHAN ISMAILOVICH GAZIEV",
    "matcheo_contra": "Sever",
    "score": 78.4,
    "criterio": "NOMBRE",
    "atenuantes": [],
    "programas": [
     "ONU",
     "Al-Qaida",
     "QDi.366"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL013",
   "cliente": "Sark Trust Services",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "SCORING",
    "motivo": "1 coincidencia(s) para revision"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL014",
   "cliente": "Nadia Haddad",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "MEDIO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL014",
   "cliente": "Nadia Haddad",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "MEDIO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL014",
   "cliente": "Nadia Haddad",
   "actor": "sistema/legajo",
   "accion": "COINCIDENCIA",
   "nivel": "MEDIO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "lista": "REPET",
    "id_origen": "111922",
    "designado": "IMED BEN MEKKI ZARKAOUI",
    "matcheo_contra": "Nadra",
    "score": 80.5,
    "criterio": "NOMBRE",
    "atenuantes": [
     "nacionalidad discordante (LÍBANO vs TUNISIA)"
    ],
    "programas": [
     "ONU",
     "Al-Qaida",
     "QDi.139"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL014",
   "cliente": "Nadia Haddad",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "MEDIO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "SCORING",
    "motivo": "1 coincidencia(s) para revision"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL015",
   "cliente": "Pyongyang Trading Co",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "ALTA",
    "destino": "SCREENING",
    "motivo": "inicio de cotejo contra listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:11+00:00",
   "cliente_id": "CL015",
   "cliente": "Pyongyang Trading Co",
   "actor": "sistema/legajo",
   "accion": "SCREENING_EJECUTADO",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "listas": [
     "OFAC_SDN pub=s/d reg=5 sha256=150ff08b396e",
     "ONU_CONSOLIDADA pub=2026-09-01 reg=2 sha256=402d3096e839",
     "REPET pub=2026-09-17 reg=607 sha256=639db1eced28",
     "REPET pub=2026-08-11 reg=111 sha256=82ea41f44007"
    ],
    "umbral_revision": 78.0,
    "umbral_probable": 92.0,
    "designados_evaluados": 725
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL001",
   "cliente": "Juan Pérez",
   "actor": "sistema/legajo",
   "accion": "SCORING_EBR",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "DD_SIMPLIFICADA",
   "detalle": {
    "puntaje": 0,
    "nivel": "BAJO",
    "regimen": "DD_SIMPLIFICADA",
    "factores": [],
    "elevadores": [],
    "proxima_revision": "2031-09-21"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL001",
   "cliente": "Juan Pérez",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCORING",
    "destino": "CERRADO",
    "motivo": "riesgo bajo (0 pts), DD_SIMPLIFICADA"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL002",
   "cliente": "Alireza Abbas",
   "actor": "sistema/legajo",
   "accion": "CONGELAMIENTO_REQUERIDO",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "FPADM",
   "detalle": {
    "regimen": "FPADM",
    "lista": "ONU_CONSOLIDADA",
    "designado": "Ali Reza Abbas",
    "norma": "Res. UIF 3/2026, Ley 25.246 art. 14 inc. 12",
    "plazo": "24 horas",
    "reserva": "prohibido informar al cliente"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL002",
   "cliente": "Alireza Abbas",
   "actor": "sistema/legajo",
   "accion": "CONGELAMIENTO_REQUERIDO",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "FT",
   "detalle": {
    "regimen": "FT",
    "lista": "OFAC_SDN",
    "designado": "ABBAS, Ali Reza",
    "norma": "Res. UIF 207/2025, Decreto 918/2012, Ley 26.734 art. 6",
    "plazo": "24 horas",
    "reserva": "prohibido informar al cliente"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL003",
   "cliente": "Petroquímica del Sur S.A.",
   "actor": "sistema/legajo",
   "accion": "CONGELAMIENTO_REQUERIDO",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "FPADM",
   "detalle": {
    "regimen": "FPADM",
    "lista": "OFAC_SDN",
    "designado": "PETROQUIMICA DEL SUR SA",
    "norma": "Res. UIF 3/2026, Ley 25.246 art. 14 inc. 12",
    "plazo": "24 horas",
    "reserva": "prohibido informar al cliente"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL005",
   "cliente": "María González",
   "actor": "sistema/legajo",
   "accion": "SCORING_EBR",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "DD_SIMPLIFICADA",
   "detalle": {
    "puntaje": 15.0,
    "nivel": "BAJO",
    "regimen": "DD_SIMPLIFICADA",
    "factores": [
     "COINCIDENCIA_REVISION(+15): 1 coincidencia(s) pendiente(s) de revision (max 79.3)"
    ],
    "elevadores": [],
    "proxima_revision": "2031-09-21"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL005",
   "cliente": "María González",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCORING",
    "destino": "CERRADO",
    "motivo": "riesgo bajo (15.0 pts), DD_SIMPLIFICADA"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL005",
   "cliente": "María González",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "BAJO",
   "severidad": "ALTA",
   "regimen": "",
   "detalle": {
    "tipo": "DESVIO_PERFIL",
    "severidad": "ALTA",
    "descripcion": "07/2026: opero $72,768,480 contra $900,000 declarados (80.9x)",
    "metodologia": "comparacion mensual contra perfil, tolerancia 25%",
    "monto": 72768480.0,
    "vence": "2026-09-22"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL005",
   "cliente": "María González",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "BAJO",
   "severidad": "ALTA",
   "regimen": "",
   "detalle": {
    "tipo": "FRACCIONAMIENTO",
    "severidad": "ALTA",
    "descripcion": "5 operaciones en 7 dias por $72,768,480, todas bajo el umbral de reporte ($15,352,000); la mayor llego al 98%",
    "metodologia": "ventana deslizante de 7 dias, minimo 3 operaciones, piso 10% del umbral",
    "monto": 72768480.0,
    "vence": "2026-09-22"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL005",
   "cliente": "María González",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "BAJO",
   "severidad": "ALTA",
   "regimen": "",
   "detalle": {
    "tipo": "EFECTIVO_DESPROPORCIONADO",
    "severidad": "ALTA",
    "descripcion": "98% de la operatoria en efectivo ($72,768,480) contra 10% declarado",
    "metodologia": "proporcion de efectivo sobre el total operado",
    "monto": 72768480.0,
    "vence": "2026-09-22"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL005",
   "cliente": "María González",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "BAJO",
   "severidad": "MEDIA",
   "regimen": "",
   "detalle": {
    "tipo": "ACELERACION",
    "severidad": "MEDIA",
    "descripcion": "los ultimos 30 dias promedian $2,425,616 diarios contra $14,138 historicos (171.6x)",
    "metodologia": "promedio diario de los ultimos 30 dias contra el resto",
    "monto": 72768480.0,
    "vence": "2026-09-22"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL005",
   "cliente": "María González",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "CERRADO",
    "destino": "ANALISIS",
    "motivo": "4 alerta(s) de monitoreo (reapertura del legajo)"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL006",
   "cliente": "Khaled Shaikh Mohamed",
   "actor": "sistema/legajo",
   "accion": "CONGELAMIENTO_REQUERIDO",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "FT",
   "detalle": {
    "regimen": "FT",
    "lista": "OFAC_SDN",
    "designado": "MOHAMMED, Khalid Sheikh",
    "norma": "Res. UIF 207/2025, Decreto 918/2012, Ley 26.734 art. 6",
    "plazo": "24 horas",
    "reserva": "prohibido informar al cliente"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL007",
   "cliente": "Eastern Trading Co",
   "actor": "sistema/legajo",
   "accion": "CONGELAMIENTO_REQUERIDO",
   "nivel": "SIN_SCORE",
   "severidad": "",
   "regimen": "FPADM",
   "detalle": {
    "regimen": "FPADM",
    "lista": "OFAC_SDN",
    "designado": "EASTERN TRADING LIMITED",
    "norma": "Res. UIF 3/2026, Ley 25.246 art. 14 inc. 12",
    "plazo": "24 horas",
    "reserva": "prohibido informar al cliente"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL008",
   "cliente": "Ana Beatriz Rodríguez",
   "actor": "sistema/legajo",
   "accion": "SCORING_EBR",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "DD_SIMPLIFICADA",
   "detalle": {
    "puntaje": 0,
    "nivel": "BAJO",
    "regimen": "DD_SIMPLIFICADA",
    "factores": [],
    "elevadores": [],
    "proxima_revision": "2031-09-21"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL008",
   "cliente": "Ana Beatriz Rodríguez",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCORING",
    "destino": "CERRADO",
    "motivo": "riesgo bajo (0 pts), DD_SIMPLIFICADA"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL008",
   "cliente": "Ana Beatriz Rodríguez",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "BAJO",
   "severidad": "ALTA",
   "regimen": "",
   "detalle": {
    "tipo": "DESVIO_PERFIL",
    "severidad": "ALTA",
    "descripcion": "06/2026: opero $41,618,770 contra $2,000,000 declarados (20.8x)",
    "metodologia": "comparacion mensual contra perfil, tolerancia 25%",
    "monto": 41618769.65,
    "vence": "2026-09-02"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL008",
   "cliente": "Ana Beatriz Rodríguez",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "BAJO",
   "severidad": "MEDIA",
   "regimen": "",
   "detalle": {
    "tipo": "ACELERACION",
    "severidad": "MEDIA",
    "descripcion": "los ultimos 30 dias promedian $1,390,883 diarios contra $34,639 historicos (40.2x)",
    "metodologia": "promedio diario de los ultimos 30 dias contra el resto",
    "monto": 41726479.52,
    "vence": "2026-08-24"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL008",
   "cliente": "Ana Beatriz Rodríguez",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "BAJO",
   "severidad": "MEDIA",
   "regimen": "",
   "detalle": {
    "tipo": "FRACCIONAMIENTO",
    "severidad": "MEDIA",
    "descripcion": "3 operaciones en 7 dias por $17,689,047, todas bajo el umbral de reporte ($15,352,000); la mayor llego al 42%",
    "metodologia": "ventana deslizante de 7 dias, minimo 3 operaciones, piso 10% del umbral",
    "monto": 17689046.91,
    "vence": "2026-09-02"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL008",
   "cliente": "Ana Beatriz Rodríguez",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "BAJO",
   "severidad": "MEDIA",
   "regimen": "",
   "detalle": {
    "tipo": "FRACCIONAMIENTO",
    "severidad": "MEDIA",
    "descripcion": "3 operaciones en 7 dias por $17,453,495, todas bajo el umbral de reporte ($15,352,000); la mayor llego al 41%",
    "metodologia": "ventana deslizante de 7 dias, minimo 3 operaciones, piso 10% del umbral",
    "monto": 17453495.18,
    "vence": "2026-09-11"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL008",
   "cliente": "Ana Beatriz Rodríguez",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "CERRADO",
    "destino": "ANALISIS",
    "motivo": "4 alerta(s) de monitoreo (reapertura del legajo)"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL009",
   "cliente": "Delta Servicios Financieros SA",
   "actor": "sistema/legajo",
   "accion": "BENEFICIARIO_FINAL",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "identificados": [
     "Laura Beltran 45.00% (PARTICIPACION)",
     "Diego Sanguinetti 35.00% (PARTICIPACION)"
    ],
    "titularidad_opaca": "60.00%",
    "niveles": 0,
    "observaciones": [
     "titularidad no identificada: 60.00% del capital"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL009",
   "cliente": "Delta Servicios Financieros SA",
   "actor": "sistema/legajo",
   "accion": "SCORING_EBR",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "DD_REFORZADA",
   "detalle": {
    "puntaje": 55.0,
    "nivel": "ALTO",
    "regimen": "DD_REFORZADA",
    "factores": [
     "PERSONA_JURIDICA(+8): cliente es persona juridica o estructura",
     "TITULARIDAD_OPACA(+12): titularidad no identificada: 60.0%",
     "PEP_NACIONAL(+20): PEP nacional (Legislador provincial)",
     "ACTIVIDAD_SENSIBLE(+15): actividad de exposicion elevada: CASA DE CAMBIO"
    ],
    "elevadores": [],
    "proxima_revision": "2027-09-21"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL009",
   "cliente": "Delta Servicios Financieros SA",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCORING",
    "destino": "ANALISIS",
    "motivo": "riesgo alto (55.0 pts) requiere diligencia reforzada"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL010",
   "cliente": "Blue Harbour Trading Ltd",
   "actor": "sistema/legajo",
   "accion": "BENEFICIARIO_FINAL",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "identificados": [
     "Elena Ferrari 6.00% (PARTICIPACION)",
     "Tomas Rivas 4.00% (PARTICIPACION)"
    ],
    "titularidad_opaca": "90.00%",
    "niveles": 0,
    "observaciones": [
     "entidad del exterior sin oferta publica: no corresponde el umbral del 10%, se identifica a la totalidad de los beneficiarios",
     "titularidad no identificada: 90.00% del capital"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL010",
   "cliente": "Blue Harbour Trading Ltd",
   "actor": "sistema/legajo",
   "accion": "SCORING_EBR",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "DD_REFORZADA",
   "detalle": {
    "puntaje": 76.0,
    "nivel": "ALTO",
    "regimen": "DD_REFORZADA",
    "factores": [
     "PERSONA_JURIDICA(+8): cliente es persona juridica o estructura",
     "TITULARIDAD_OPACA(+18): titularidad no identificada: 90.0%",
     "PEP_EXTRANJERA(+35): PEP extranjera (Ministro de Estado)",
     "ACTIVIDAD_SENSIBLE(+15): actividad de exposicion elevada: COMERCIO EXTERIOR"
    ],
    "elevadores": [
     "PEP_EXTRANJERA"
    ],
    "proxima_revision": "2027-09-21"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL010",
   "cliente": "Blue Harbour Trading Ltd",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCORING",
    "destino": "ANALISIS",
    "motivo": "riesgo alto (76.0 pts) requiere diligencia reforzada"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL011",
   "cliente": "Grupo Cotizante SA",
   "actor": "sistema/legajo",
   "accion": "BENEFICIARIO_FINAL",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "identificados": [],
    "titularidad_opaca": "0.00%",
    "niveles": 0,
    "observaciones": [
     "sociedad con oferta publica de sus valores: exceptuada de identificar beneficiario final, sujeta a acreditar esa condicion"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL011",
   "cliente": "Grupo Cotizante SA",
   "actor": "sistema/legajo",
   "accion": "SCORING_EBR",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "DD_SIMPLIFICADA",
   "detalle": {
    "puntaje": 8.0,
    "nivel": "BAJO",
    "regimen": "DD_SIMPLIFICADA",
    "factores": [
     "PERSONA_JURIDICA(+8): cliente es persona juridica o estructura"
    ],
    "elevadores": [],
    "proxima_revision": "2031-09-21"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL011",
   "cliente": "Grupo Cotizante SA",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "BAJO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCORING",
    "destino": "CERRADO",
    "motivo": "riesgo bajo (8.0 pts), DD_SIMPLIFICADA"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL012",
   "cliente": "Fernanda Ortiz",
   "actor": "sistema/legajo",
   "accion": "SCORING_EBR",
   "nivel": "MEDIO",
   "severidad": "",
   "regimen": "DD_MEDIA",
   "detalle": {
    "puntaje": 30.0,
    "nivel": "MEDIO",
    "regimen": "DD_MEDIA",
    "factores": [
     "PEP_NACIONAL(+30): PEP nacional por parentesco o cercania (Conyuge de intendente)"
    ],
    "elevadores": [],
    "proxima_revision": "2029-09-21"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL012",
   "cliente": "Fernanda Ortiz",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "MEDIO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCORING",
    "destino": "CERRADO",
    "motivo": "riesgo medio (30.0 pts), DD_MEDIA"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL012",
   "cliente": "Fernanda Ortiz",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "MEDIO",
   "severidad": "ALTA",
   "regimen": "",
   "detalle": {
    "tipo": "DESVIO_PERFIL",
    "severidad": "ALTA",
    "descripcion": "07/2026: opero $13,671,015 contra $2,500,000 declarados (5.5x)",
    "metodologia": "comparacion mensual contra perfil, tolerancia 25%",
    "monto": 13671014.67,
    "vence": "2026-09-22"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL012",
   "cliente": "Fernanda Ortiz",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "MEDIO",
   "severidad": "ALTA",
   "regimen": "",
   "detalle": {
    "tipo": "JURISDICCION_NO_DECLARADA",
    "severidad": "ALTA",
    "descripcion": "3 operacion(es) por $13,346,747 con contraparte en Islas Virgenes Britanicas, jurisdiccion en lista de riesgo",
    "metodologia": "paises de contraparte normalizados a ISO, contra el perfil y las listas",
    "monto": 13346746.9,
    "vence": "2026-09-22"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL012",
   "cliente": "Fernanda Ortiz",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "MEDIO",
   "severidad": "MEDIA",
   "regimen": "",
   "detalle": {
    "tipo": "ACELERACION",
    "severidad": "MEDIA",
    "descripcion": "los ultimos 30 dias promedian $455,700 diarios contra $55,494 historicos (8.2x)",
    "metodologia": "promedio diario de los ultimos 30 dias contra el resto",
    "monto": 13671014.67,
    "vence": "2026-09-22"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL012",
   "cliente": "Fernanda Ortiz",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "MEDIO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "CERRADO",
    "destino": "ANALISIS",
    "motivo": "3 alerta(s) de monitoreo (reapertura del legajo)"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL013",
   "cliente": "Sark Trust Services",
   "actor": "sistema/legajo",
   "accion": "BENEFICIARIO_FINAL",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "identificados": [],
    "titularidad_opaca": "100.00%",
    "niveles": 0,
    "observaciones": [
     "entidad del exterior sin oferta publica: no corresponde el umbral del 10%, se identifica a la totalidad de los beneficiarios",
     "sin beneficiario final identificable y sin administrador declarado",
     "titularidad no identificada: 100.00% del capital"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL013",
   "cliente": "Sark Trust Services",
   "actor": "sistema/legajo",
   "accion": "SCORING_EBR",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "DD_REFORZADA",
   "detalle": {
    "puntaje": 80.0,
    "nivel": "ALTO",
    "regimen": "DD_REFORZADA",
    "factores": [
     "PERSONA_JURIDICA(+8): cliente es persona juridica o estructura",
     "BENEFICIARIO_NO_IDENTIFICADO(+25): no se identifico beneficiario final",
     "TITULARIDAD_OPACA(+20): titularidad no identificada: 100.0%",
     "JURISDICCION_NO_COOPERANTE(+12): jurisdiccion no cooperante a fines fiscales: Guernsey",
     "COINCIDENCIA_REVISION(+15): 1 coincidencia(s) pendiente(s) de revision (max 78.4)"
    ],
    "elevadores": [
     "BENEFICIARIO_NO_IDENTIFICADO"
    ],
    "proxima_revision": "2027-09-21"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL013",
   "cliente": "Sark Trust Services",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCORING",
    "destino": "ANALISIS",
    "motivo": "riesgo alto (80.0 pts) requiere diligencia reforzada"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL013",
   "cliente": "Sark Trust Services",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "ALTO",
   "severidad": "ALTA",
   "regimen": "",
   "detalle": {
    "tipo": "JURISDICCION_NO_DECLARADA",
    "severidad": "ALTA",
    "descripcion": "6 operacion(es) por $23,136,812 con contraparte en Guernsey, jurisdiccion en lista de riesgo",
    "metodologia": "paises de contraparte normalizados a ISO, contra el perfil y las listas",
    "monto": 23136811.69,
    "vence": "2026-05-31"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL013",
   "cliente": "Sark Trust Services",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "ALTO",
   "severidad": "MEDIA",
   "regimen": "",
   "detalle": {
    "tipo": "SIN_PERFIL",
    "severidad": "MEDIA",
    "descripcion": "opero 6 vez/veces por $23,136,812 sin perfil transaccional declarado",
    "metodologia": "ausencia de perfil declarado con operatoria registrada",
    "monto": 23136811.69,
    "vence": "2026-09-22"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL014",
   "cliente": "Nadia Haddad",
   "actor": "sistema/legajo",
   "accion": "SCORING_EBR",
   "nivel": "MEDIO",
   "severidad": "",
   "regimen": "DD_MEDIA",
   "detalle": {
    "puntaje": 38.0,
    "nivel": "MEDIO",
    "regimen": "DD_MEDIA",
    "factores": [
     "JURISDICCION_MONITOREO(+18): jurisdiccion GAFI bajo monitoreo intensificado: Libano",
     "RESIDENCIA_DISTINTA(+5): reside en Argentina con nacionalidad Libano",
     "COINCIDENCIA_REVISION(+15): 1 coincidencia(s) pendiente(s) de revision (max 80.5)"
    ],
    "elevadores": [],
    "proxima_revision": "2029-09-21"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL014",
   "cliente": "Nadia Haddad",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "MEDIO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCORING",
    "destino": "CERRADO",
    "motivo": "riesgo medio (38.0 pts), DD_MEDIA"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL014",
   "cliente": "Nadia Haddad",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "MEDIO",
   "severidad": "ALTA",
   "regimen": "",
   "detalle": {
    "tipo": "DESVIO_PERFIL",
    "severidad": "ALTA",
    "descripcion": "09/2026: opero $18,242,214 contra $1,400,000 declarados (13.0x)",
    "metodologia": "comparacion mensual contra perfil, tolerancia 25%",
    "monto": 18242213.83,
    "vence": "2026-09-22"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL014",
   "cliente": "Nadia Haddad",
   "actor": "sistema/legajo",
   "accion": "ALERTA_MONITOREO",
   "nivel": "MEDIO",
   "severidad": "MEDIA",
   "regimen": "",
   "detalle": {
    "tipo": "ACELERACION",
    "severidad": "MEDIA",
    "descripcion": "los ultimos 30 dias promedian $1,130,492 diarios contra $24,118 historicos (46.9x)",
    "metodologia": "promedio diario de los ultimos 30 dias contra el resto",
    "monto": 33914747.72,
    "vence": "2026-09-22"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL014",
   "cliente": "Nadia Haddad",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "MEDIO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "CERRADO",
    "destino": "ANALISIS",
    "motivo": "2 alerta(s) de monitoreo (reapertura del legajo)"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL015",
   "cliente": "Pyongyang Trading Co",
   "actor": "sistema/legajo",
   "accion": "SIN_COINCIDENCIAS",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {}
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL015",
   "cliente": "Pyongyang Trading Co",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCREENING",
    "destino": "SCORING",
    "motivo": "sin coincidencias en listas"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL015",
   "cliente": "Pyongyang Trading Co",
   "actor": "sistema/legajo",
   "accion": "BENEFICIARIO_FINAL",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "identificados": [],
    "titularidad_opaca": "100.00%",
    "niveles": 0,
    "observaciones": [
     "entidad del exterior sin oferta publica: no corresponde el umbral del 10%, se identifica a la totalidad de los beneficiarios",
     "sin beneficiario final identificable y sin administrador declarado",
     "titularidad no identificada: 100.00% del capital"
    ]
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL015",
   "cliente": "Pyongyang Trading Co",
   "actor": "sistema/legajo",
   "accion": "SCORING_EBR",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "DD_REFORZADA",
   "detalle": {
    "puntaje": 125.0,
    "nivel": "ALTO",
    "regimen": "DD_REFORZADA",
    "factores": [
     "PERSONA_JURIDICA(+8): cliente es persona juridica o estructura",
     "BENEFICIARIO_NO_IDENTIFICADO(+25): no se identifico beneficiario final",
     "TITULARIDAD_OPACA(+20): titularidad no identificada: 100.0%",
     "JURISDICCION_CONTRAMEDIDAS(+45): jurisdiccion GAFI sujeta a contramedidas: Corea del Norte",
     "JURISDICCION_NO_COOPERANTE(+12): jurisdiccion no cooperante a fines fiscales: Corea del Norte",
     "ACTIVIDAD_SENSIBLE(+15): actividad de exposicion elevada: COMERCIO EXTERIOR"
    ],
    "elevadores": [
     "BENEFICIARIO_NO_IDENTIFICADO",
     "JURISDICCION_ALTO_RIESGO"
    ],
    "proxima_revision": "2027-09-21"
   }
  },
  {
   "momento": "2026-09-21T03:30:12+00:00",
   "cliente_id": "CL015",
   "cliente": "Pyongyang Trading Co",
   "actor": "sistema/legajo",
   "accion": "TRANSICION",
   "nivel": "ALTO",
   "severidad": "",
   "regimen": "",
   "detalle": {
    "origen": "SCORING",
    "destino": "ANALISIS",
    "motivo": "riesgo alto (125.0 pts) requiere diligencia reforzada"
   }
  }
 ],
 "operaciones": [
  {
   "cliente_id": "CL001",
   "fecha": "2026-03-02",
   "monto": 257719.86,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-03-02",
   "monto": 114523.36,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Haberes",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-03-02",
   "monto": 98940.18,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-03-02",
   "monto": 529210.38,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Cliente",
   "pais": "Uruguay",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-03-02",
   "monto": 267946.46,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL013",
   "fecha": "2026-03-02",
   "monto": 3107760.72,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Fideicomiso",
   "pais": "Isla de Sark",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-03-07",
   "monto": 120893.81,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-03-08",
   "monto": 171227.2,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-03-09",
   "monto": 216203.8,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-03-11",
   "monto": 110024.68,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Haberes",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-03-12",
   "monto": 192060.0,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-03-13",
   "monto": 650191.12,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Cliente",
   "pais": "Uruguay",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-03-14",
   "monto": 189442.46,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-03-16",
   "monto": 336224.27,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-03-17",
   "monto": 154138.85,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-03-20",
   "monto": 142441.91,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Haberes",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-03-20",
   "monto": 240357.49,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-03-22",
   "monto": 137122.08,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL013",
   "fecha": "2026-03-22",
   "monto": 3699023.67,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Fideicomiso",
   "pais": "Isla de Sark",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-03-23",
   "monto": 197384.71,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-03-24",
   "monto": 425499.01,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Cliente",
   "pais": "Uruguay",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-03-26",
   "monto": 124061.33,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-03-27",
   "monto": 177834.28,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-03-29",
   "monto": 228741.48,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Haberes",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-03-30",
   "monto": 308611.68,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-04-01",
   "monto": 157977.66,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-04-01",
   "monto": 203105.15,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-04-04",
   "monto": 578118.15,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Cliente",
   "pais": "Uruguay",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-04-06",
   "monto": 267765.34,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-04-06",
   "monto": 134965.05,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-04-07",
   "monto": 120723.48,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Haberes",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-04-07",
   "monto": 150248.71,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-04-11",
   "monto": 209156.92,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL013",
   "fecha": "2026-04-11",
   "monto": 4859293.78,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Fideicomiso",
   "pais": "Isla de Sark",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-04-13",
   "monto": 193919.74,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-04-13",
   "monto": 141077.24,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-04-15",
   "monto": 537747.95,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Cliente",
   "pais": "Uruguay",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-04-16",
   "monto": 188872.03,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Haberes",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-04-16",
   "monto": 194849.17,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-04-19",
   "monto": 130611.8,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-04-20",
   "monto": 301784.58,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-04-21",
   "monto": 126614.48,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-04-25",
   "monto": 198615.29,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Haberes",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-04-25",
   "monto": 258281.94,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-04-26",
   "monto": 176163.56,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-04-26",
   "monto": 531958.08,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Cliente",
   "pais": "Uruguay",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-04-27",
   "monto": 188998.96,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-05-01",
   "monto": 168779.48,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-05-01",
   "monto": 143281.24,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL013",
   "fecha": "2026-05-01",
   "monto": 4071480.97,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Fideicomiso",
   "pais": "Isla de Sark",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-05-04",
   "monto": 284074.96,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-05-04",
   "monto": 153307.58,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Haberes",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-05-06",
   "monto": 221270.62,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-05-07",
   "monto": 482482.13,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Cliente",
   "pais": "Uruguay",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-05-07",
   "monto": 164570.67,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-05-11",
   "monto": 196765.3,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-05-11",
   "monto": 199416.79,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-05-13",
   "monto": 183116.56,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Haberes",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-05-13",
   "monto": 190370.95,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-05-16",
   "monto": 133190.66,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-05-18",
   "monto": 201771.12,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-05-18",
   "monto": 635987.11,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Cliente",
   "pais": "Uruguay",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-05-19",
   "monto": 276855.96,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-05-21",
   "monto": 237026.23,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL013",
   "fecha": "2026-05-21",
   "monto": 3546474.3,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Fideicomiso",
   "pais": "Isla de Sark",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-05-22",
   "monto": 100674.13,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Haberes",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-05-25",
   "monto": 281884.61,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-05-25",
   "monto": 134504.63,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-05-26",
   "monto": 107709.87,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Consultoria",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-05-29",
   "monto": 677872.44,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Cliente",
   "pais": "Uruguay",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-05-31",
   "monto": 200853.73,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-06-01",
   "monto": 378444.51,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-06-04",
   "monto": 5852621.08,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Transferencia recibida",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-06-06",
   "monto": 218899.18,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-06-07",
   "monto": 6462853.67,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Transferencia recibida",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-06-08",
   "monto": 209712.47,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-06-09",
   "monto": 489639.33,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Cliente",
   "pais": "Uruguay",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-06-10",
   "monto": 5373572.16,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Transferencia recibida",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL013",
   "fecha": "2026-06-10",
   "monto": 3852778.25,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Fideicomiso",
   "pais": "Isla de Sark",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-06-12",
   "monto": 279009.09,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-06-13",
   "monto": 5980133.58,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Transferencia recibida",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-06-15",
   "monto": 233577.35,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-06-16",
   "monto": 5170573.06,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Transferencia recibida",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-06-18",
   "monto": 267470.37,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-06-19",
   "monto": 6302788.54,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Transferencia recibida",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-06-20",
   "monto": 565660.88,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Cliente",
   "pais": "Uruguay",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-06-22",
   "monto": 330583.97,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL008",
   "fecha": "2026-06-22",
   "monto": 6476227.56,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Transferencia recibida",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-06-24",
   "monto": 275517.2,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-06-29",
   "monto": 407450.15,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-07-01",
   "monto": 324267.77,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Cliente",
   "pais": "Uruguay",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-07-06",
   "monto": 318504.71,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-07-08",
   "monto": 4322387.23,
   "sentido": "EGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Panama Trade SA",
   "pais": "Islas Vírgenes Británicas",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-07-13",
   "monto": 275203.31,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-07-13",
   "monto": 14891440.0,
   "sentido": "INGRESO",
   "instrumento": "EFECTIVO",
   "canal": "PRESENCIAL",
   "contraparte": "Deposito por ventanilla",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-07-14",
   "monto": 14277360.0,
   "sentido": "INGRESO",
   "instrumento": "EFECTIVO",
   "canal": "PRESENCIAL",
   "contraparte": "Deposito por ventanilla",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-07-14",
   "monto": 4235406.17,
   "sentido": "EGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Panama Trade SA",
   "pais": "Islas Vírgenes Británicas",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-07-16",
   "monto": 15044960.0,
   "sentido": "INGRESO",
   "instrumento": "EFECTIVO",
   "canal": "PRESENCIAL",
   "contraparte": "Deposito por ventanilla",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-07-17",
   "monto": 13970320.0,
   "sentido": "INGRESO",
   "instrumento": "EFECTIVO",
   "canal": "PRESENCIAL",
   "contraparte": "Deposito por ventanilla",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL005",
   "fecha": "2026-07-19",
   "monto": 14584400.0,
   "sentido": "INGRESO",
   "instrumento": "EFECTIVO",
   "canal": "PRESENCIAL",
   "contraparte": "Deposito por ventanilla",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-07-20",
   "monto": 414301.23,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL012",
   "fecha": "2026-07-20",
   "monto": 4788953.5,
   "sentido": "EGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Panama Trade SA",
   "pais": "Islas Vírgenes Británicas",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-07-27",
   "monto": 191179.84,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-08-03",
   "monto": 386032.43,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL001",
   "fecha": "2026-08-10",
   "monto": 249506.23,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Proveedor local",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-08-20",
   "monto": 2245473.7,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-08-22",
   "monto": 2464474.43,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-08-24",
   "monto": 2374033.86,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-08-26",
   "monto": 3214708.52,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-08-28",
   "monto": 3332369.93,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-08-30",
   "monto": 2041473.45,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-09-01",
   "monto": 2081948.37,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-09-03",
   "monto": 2171130.99,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-09-05",
   "monto": 2173337.73,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-09-07",
   "monto": 2575940.37,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-09-09",
   "monto": 2742597.61,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-09-11",
   "monto": 2220394.59,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-09-13",
   "monto": 1806549.77,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  },
  {
   "cliente_id": "CL014",
   "fecha": "2026-09-15",
   "monto": 2470314.4,
   "sentido": "INGRESO",
   "instrumento": "TRANSFERENCIA",
   "canal": "ELECTRONICO",
   "contraparte": "Comercio",
   "pais": "Argentina",
   "referencia": ""
  }
 ]
};