"""Interfaz de escritorio para legajo.

No reimplementa nada. Arma la linea de comandos y llama al mismo `cli.main`
que usa la terminal, capturando lo que imprime.

Esa es toda la gracia del diseño: si la logica viviera duplicada aca, en la
segunda correccion las dos versiones empezarian a dar resultados distintos y
nadie se enteraria hasta que un informe salga mal.

Corre con tkinter, que viene con Python, asi que el ejecutable no arrastra
ninguna dependencia grafica.

La apariencia es de consola de analisis: fondo oscuro, monoespaciada y densa.
La version anterior era gris claro con el argumento de que esto lo abre
alguien de cumplimiento y no de diseno. El argumento no se sostiene: un
analista mira esta pantalla varias horas seguidas, y el contraste alto sobre
fondo oscuro cansa menos que una planilla blanca. Todo lo que se ve aca sale
de tkinter puro, sin imagenes ni tipografias de afuera, porque el ejecutable
tiene que seguir siendo un solo archivo.
"""

from __future__ import annotations

import json
import queue
import sys
import threading
import time
import tkinter as tk
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from legajo.cli import main as cli_main

TITULO = "legajo  ·  circuito PLA/FT"
CONFIG = Path.home() / ".legajo_gui.json"

# Paleta de consola. El fondo no es negro puro sino azulado: el negro absoluto
# contra texto claro produce halo en pantallas LCD y cansa la vista.
FONDO = "#0B0E14"
PANEL = "#111620"
BORDE = "#1E2732"
BORDE_VIVO = "#2E3B4A"
TINTA = "#C9D4E0"
GRIS = "#5D6976"
ACENTO = "#4FD1C5"
AMBAR = "#E0A33E"
ROJO = "#E5484D"
VERDE = "#3FB950"

MONO = "Consolas"
CAMPO_FONDO = "#0E131B"


def espaciado(texto: str) -> str:
    """Separa las letras de un rotulo.

    Tk no tiene letter-spacing, y los encabezados en versalita separada son
    la mitad del caracter de una consola de analisis. Meter los espacios a
    mano es feo pero es lo unico que hay.
    """
    return " ".join(texto.upper())


def _columnas(grilla) -> None:
    """Fija el reparto de columnas de una grilla de campos.

    El minsize es lo que mide el rotulo mas largo. Sin el, cada seccion
    calcula su propio ancho y las cajas de texto de "Fuentes de datos" y las
    de "Parametros" arrancan en x distintos, que en una pantalla asi se nota.
    """
    grilla.columnconfigure(0, minsize=186)
    grilla.columnconfigure(1, minsize=16)
    grilla.columnconfigure(2, weight=1)


class Campo:
    """Una fila de la grilla: rotulo, caja de texto y boton de examinar."""

    def __init__(self, padre, fila, etiqueta, ayuda, modo="archivo",
                 requerido=False, tipos=None):
        self.modo = modo
        self.tipos = tipos or [("CSV o Excel", "*.csv *.xlsx"), ("Todos", "*.*")]
        self.valor = tk.StringVar()

        # Cuatro columnas: rotulo, marca de obligatorio, caja y boton. El
        # asterisco va en columna propia y no pegado al rotulo, porque si no
        # los nombres largos lo empujan contra la caja y los cortos lo dejan
        # flotando lejos.
        ttk.Label(padre, text=etiqueta.upper(), style="Campo.TLabel").grid(
            row=fila, column=0, sticky="w", pady=(6, 0))

        if requerido:
            ttk.Label(padre, text="*", style="Requerido.TLabel").grid(
                row=fila, column=1, sticky="w", padx=(6, 10), pady=(6, 0))

        entrada = ttk.Entry(padre, textvariable=self.valor, width=52,
                            font=(MONO, 9), style="Consola.TEntry")
        entrada.grid(row=fila, column=2, sticky="ew", pady=(6, 0))

        ttk.Button(padre, text="EXAMINAR", width=11, style="Chico.TButton",
                   command=self._elegir).grid(
            row=fila, column=3, padx=(8, 0), pady=(6, 0))

        ttk.Label(padre, text=ayuda, style="Ayuda.TLabel").grid(
            row=fila + 1, column=2, sticky="w", pady=(1, 0))

    def _elegir(self):
        if self.modo == "carpeta":
            elegido = filedialog.askdirectory(title="Elegir carpeta")
        elif self.modo == "guardar":
            elegido = filedialog.asksaveasfilename(
                title="Guardar informe como", defaultextension=".xlsx",
                filetypes=[("Excel", "*.xlsx")])
        else:
            elegido = filedialog.askopenfilename(title="Elegir archivo",
                                                 filetypes=self.tipos)
        if elegido:
            self.valor.set(elegido)

    def get(self) -> str:
        return self.valor.get().strip()

    def set(self, texto: str) -> None:
        self.valor.set(texto or "")


class Aplicacion(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title(TITULO)
        self.geometry("980x820")
        # Medido widget por widget, achicando la ventana de a 40 px. Abajo de
        # 680 de alto los botones de accion se van afuera del borde, y entre
        # 680 y 760 la consola queda en tres renglones, que no alcanza para
        # ver una corrida. 760 deja seis renglones y entra en una pantalla de
        # notebook. El ancho que pide el formulario son 745, asi que 820 sobra.
        self.minsize(820, 760)
        self.configure(bg=FONDO)

        self.cola: queue.Queue[str] = queue.Queue()
        self.corriendo = False
        self.ultimo_informe: Path | None = None
        self.visor_pendiente: Path | None = None
        self.inicio: float | None = None
        self.duracion: int | None = None
        self.lineas = 0

        self._estilos()
        self._armar()
        self._barra_oscura()
        self._cargar_config()
        self.after(80, self._drenar_cola)
        self.after(200, self._latido)
        self.protocol("WM_DELETE_WINDOW", self._cerrar)

    # --- apariencia --------------------------------------------------------

    def _barra_oscura(self):
        """Pide a Windows que pinte la barra de titulo en oscuro.

        Tk no la dibuja, la dibuja el sistema operativo, asi que sin esto
        queda una franja blanca arriba de una ventana negra. Es una llamada a
        dwmapi por ctypes, sin dependencias nuevas. Si el Windows es viejo o
        la funcion no esta, no pasa nada y la barra queda como estaba.
        """
        if not sys.platform.startswith("win"):
            return
        try:
            import ctypes

            self.update_idletasks()
            ventana = ctypes.windll.user32.GetParent(self.winfo_id())
            prendido = ctypes.c_int(1)
            # 20 es DWMWA_USE_IMMERSIVE_DARK_MODE desde Windows 10 20H1, y 19
            # en las builds anteriores. Se corta en el primero que devuelve
            # S_OK: mandar los dos hace que el segundo pise al primero.
            for atributo in (20, 19):
                if ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        ventana, atributo, ctypes.byref(prendido),
                        ctypes.sizeof(prendido)) == 0:
                    break
            # La barra ya dibujada no se repinta con el atributo nuevo. Hay
            # que esconder la ventana y volver a mostrarla para que el sistema
            # la redibuje.
            self.withdraw()
            self.deiconify()
        except Exception:
            pass

    def _estilos(self):
        estilo = ttk.Style(self)
        try:
            # clam es el unico tema de los que trae tkinter que deja cambiar
            # el color del borde y del fondo de los campos. Los de Windows
            # dibujan con el tema del sistema operativo y quedan claros.
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure(".", background=FONDO, foreground=TINTA,
                         font=(MONO, 9), borderwidth=0)
        estilo.configure("TFrame", background=FONDO)
        estilo.configure("Panel.TFrame", background=PANEL)
        estilo.configure("Borde.TFrame", background=BORDE)

        estilo.configure("TLabel", background=FONDO, foreground=TINTA)
        estilo.configure("Marca.TLabel", font=(MONO, 17, "bold"),
                         foreground=TINTA)
        estilo.configure("Lema.TLabel", font=(MONO, 8), foreground=GRIS)
        estilo.configure("Seccion.TLabel", font=(MONO, 8, "bold"),
                         foreground=ACENTO)
        estilo.configure("Campo.TLabel", font=(MONO, 8), foreground=GRIS)
        estilo.configure("Requerido.TLabel", font=(MONO, 9, "bold"),
                         foreground=ACENTO)
        estilo.configure("Ayuda.TLabel", font=(MONO, 8), foreground="#46505C")
        estilo.configure("Estado.TLabel", font=(MONO, 9), foreground=TINTA)
        estilo.configure("Metrica.TLabel", font=(MONO, 8), foreground=GRIS)

        # Campos de texto. fieldbackground es el fondo de adentro, background
        # el del marco: en clam hay que poner los dos o queda un borde claro.
        estilo.configure("Consola.TEntry",
                         fieldbackground=CAMPO_FONDO, background=CAMPO_FONDO,
                         foreground=TINTA, insertcolor=ACENTO,
                         bordercolor=BORDE, lightcolor=BORDE, darkcolor=BORDE,
                         borderwidth=1, padding=5)
        estilo.map("Consola.TEntry",
                   bordercolor=[("focus", ACENTO)],
                   lightcolor=[("focus", ACENTO)],
                   darkcolor=[("focus", ACENTO)])

        for nombre, fuente, relleno in (("TButton", (MONO, 9), (14, 7)),
                                        ("Chico.TButton", (MONO, 8), (8, 5))):
            estilo.configure(nombre, font=fuente, padding=relleno,
                             background=PANEL, foreground=TINTA,
                             bordercolor=BORDE, lightcolor=BORDE,
                             darkcolor=BORDE, borderwidth=1, relief="flat",
                             focuscolor=PANEL)
            estilo.map(nombre,
                       background=[("pressed", BORDE), ("active", BORDE_VIVO),
                                   ("disabled", PANEL)],
                       foreground=[("disabled", "#3A434E")],
                       bordercolor=[("active", ACENTO)],
                       lightcolor=[("active", ACENTO)],
                       darkcolor=[("active", ACENTO)])

        # El boton principal se distingue por el borde, no por el relleno: un
        # bloque de color solido en una pantalla oscura tira demasiado la
        # vista para algo que se aprieta una vez por corrida.
        estilo.configure("Principal.TButton", font=(MONO, 9, "bold"),
                         foreground=ACENTO, background=PANEL,
                         bordercolor=ACENTO, lightcolor=ACENTO,
                         darkcolor=ACENTO, borderwidth=1, padding=(14, 7),
                         focuscolor=PANEL)
        estilo.map("Principal.TButton",
                   background=[("pressed", BORDE), ("active", "#16212A"),
                               ("disabled", PANEL)],
                   foreground=[("disabled", "#2F4A47")])

        estilo.configure("Vertical.TScrollbar", background=BORDE,
                         troughcolor=FONDO, bordercolor=FONDO,
                         arrowcolor=GRIS, lightcolor=BORDE, darkcolor=BORDE,
                         borderwidth=0, arrowsize=12)
        estilo.map("Vertical.TScrollbar",
                   background=[("active", BORDE_VIVO)])

    def _regla(self, padre, fila, texto):
        """Encabezado de seccion: rotulo en versalita y linea al ras."""
        franja = ttk.Frame(padre)
        franja.grid(row=fila, column=0, sticky="ew", pady=(16, 8))
        franja.columnconfigure(1, weight=1)
        ttk.Label(franja, text=espaciado(texto), style="Seccion.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 10))
        linea = ttk.Frame(franja, style="Borde.TFrame", height=1)
        linea.grid(row=0, column=1, sticky="ew")

    def _armar(self):
        raiz = ttk.Frame(self, padding=(20, 16, 20, 14))
        raiz.pack(fill="both", expand=True)
        raiz.columnconfigure(0, weight=1)

        # --- encabezado ---
        encabezado = ttk.Frame(raiz)
        encabezado.grid(row=0, column=0, sticky="ew")
        encabezado.columnconfigure(1, weight=1)

        izq = ttk.Frame(encabezado)
        izq.grid(row=0, column=0, sticky="w")
        ttk.Label(izq, text="LEGAJO", style="Marca.TLabel").pack(anchor="w")
        ttk.Label(izq, text=espaciado("circuito pla/ft"),
                  style="Lema.TLabel").pack(anchor="w", pady=(2, 0))

        der = ttk.Frame(encabezado)
        der.grid(row=0, column=2, sticky="e")
        fila_led = ttk.Frame(der)
        fila_led.pack(anchor="e")
        self.led = tk.Label(fila_led, text="●", bg=FONDO, fg=VERDE,
                            font=(MONO, 11))
        self.led.pack(side="left", padx=(0, 6))
        self.estado = ttk.Label(fila_led, text="OPERATIVO", style="Estado.TLabel")
        self.estado.pack(side="left")
        self.reloj = ttk.Label(der, text="--:--  ·  0 líneas",
                               style="Metrica.TLabel")
        self.reloj.pack(anchor="e", pady=(3, 0))

        separador = ttk.Frame(raiz, style="Borde.TFrame", height=1)
        separador.grid(row=1, column=0, sticky="ew", pady=(14, 0))

        # --- entradas ---
        self._regla(raiz, 2, "fuentes de datos")
        caja = ttk.Frame(raiz)
        caja.grid(row=3, column=0, sticky="ew")
        _columnas(caja)

        self.padron = Campo(caja, 0, "Padrón de clientes",
                            "CSV o XLSX con los clientes a cotejar",
                            requerido=True)
        self.listas = Campo(caja, 2, "Carpeta de listas",
                            "Directorio con SDN.CSV, consolidated.xml y los "
                            "archivos de RePET",
                            modo="carpeta", requerido=True)
        self.societaria = Campo(caja, 4, "Estructura societaria",
                                "Opcional. Sin esto no se resuelve el "
                                "beneficiario final")
        self.peps = Campo(caja, 6, "Declaraciones de PEP",
                          "Opcional. Sin esto no se aplican los factores PEP")
        self.operaciones = Campo(caja, 8, "Operatoria",
                                 "Opcional. Sin esto no corre el monitoreo "
                                 "transaccional")
        self.perfiles = Campo(caja, 10, "Perfiles transaccionales",
                              "Opcional. Sin esto todo cliente con operaciones "
                              "queda sin perfil declarado")

        # --- parametros ---
        self._regla(raiz, 4, "parámetros")
        params = ttk.Frame(raiz)
        params.grid(row=5, column=0, sticky="ew")
        _columnas(params)

        self.salida = Campo(params, 0, "Informe de salida",
                            "Se sobrescribe si ya existe",
                            modo="guardar", requerido=True)

        ttk.Label(params, text="UMBRAL DE REPORTE", style="Campo.TLabel").grid(
            row=2, column=0, sticky="w", pady=(6, 0))
        self.umbral = tk.StringVar()
        ttk.Entry(params, textvariable=self.umbral, width=20, font=(MONO, 9),
                  style="Consola.TEntry").grid(
            row=2, column=2, sticky="w", pady=(6, 0))
        ttk.Label(params, style="Ayuda.TLabel",
                  text="En pesos. Vacío usa 40 SMVM según la Res. UIF 78/2025").grid(
            row=3, column=2, sticky="w", pady=(1, 0))

        # --- acciones ---
        self._regla(raiz, 6, "acciones")
        acciones = ttk.Frame(raiz)
        acciones.grid(row=7, column=0, sticky="ew")

        self.btn_circuito = ttk.Button(acciones, text="CORRER CIRCUITO",
                                       style="Principal.TButton", width=20,
                                       command=self._correr_circuito)
        self.btn_circuito.pack(side="left")

        self.btn_ros = ttk.Button(acciones, text="BORRADORES DE ROS",
                                  width=22, command=self._correr_ros)
        self.btn_ros.pack(side="left", padx=8)

        self.btn_listas = ttk.Button(acciones, text="ACTUALIZAR LISTAS",
                                     width=20, command=self._actualizar_listas)
        self.btn_listas.pack(side="left")

        self.btn_abrir = ttk.Button(acciones, text="ABRIR INFORME", width=17,
                                    command=self._abrir_informe,
                                    state="disabled")
        self.btn_abrir.pack(side="right")

        self.btn_visor = ttk.Button(acciones, text="ABRIR VISOR", width=15,
                                    style="Principal.TButton",
                                    command=self._abrir_visor)
        self.btn_visor.pack(side="right", padx=(0, 8))

        # --- consola ---
        self._regla(raiz, 8, "salida")
        consola = ttk.Frame(raiz, style="Borde.TFrame", padding=1)
        consola.grid(row=9, column=0, sticky="nsew")
        raiz.rowconfigure(9, weight=1)
        consola.columnconfigure(0, weight=1)
        consola.rowconfigure(0, weight=1)

        self.log = tk.Text(consola, height=13, wrap="none", bd=0,
                           bg=CAMPO_FONDO, fg=TINTA, insertbackground=ACENTO,
                           selectbackground=BORDE_VIVO,
                           font=(MONO, 9), padx=12, pady=10,
                           highlightthickness=0)
        self.log.grid(row=0, column=0, sticky="nsew")

        barra = ttk.Scrollbar(consola, orient="vertical", command=self.log.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.log.configure(yscrollcommand=barra.set, state="disabled")

        self.log.tag_configure("aviso", foreground=AMBAR)
        self.log.tag_configure("error", foreground=ROJO)
        self.log.tag_configure("ok", foreground=VERDE)
        self.log.tag_configure("orden", foreground=ACENTO)
        self.log.tag_configure("tenue", foreground=GRIS)

        self._escribir("Sin corridas todavía. Completá las fuentes de datos "
                       "y apretá CORRER CIRCUITO.\n", "tenue")
        self.lineas = 0   # el cartel de bienvenida no es salida de una corrida

    # --- telemetria --------------------------------------------------------

    def _senal(self, color: str, texto: str):
        self.led.configure(fg=color)
        self.estado.configure(text=texto)

    def _latido(self):
        """Refresca el cronometro y el contador de lineas de la corrida."""
        if self.corriendo and self.inicio is not None:
            transcurrido = int(time.monotonic() - self.inicio)
        else:
            # Terminada la corrida el reloj queda congelado en lo que tardo.
            # Volver a cero borraria el unico dato de cuanto costo.
            transcurrido = self.duracion
        reloj = ("--:--" if transcurrido is None
                 else f"{transcurrido // 60:02d}:{transcurrido % 60:02d}")
        plural = "línea" if self.lineas == 1 else "líneas"
        self.reloj.configure(text=f"{reloj}  ·  {self.lineas} {plural}")
        self.after(250, self._latido)

    # --- ejecucion ---------------------------------------------------------

    def _lanzar(self, argv: list[str], etiqueta: str):
        """Corre el CLI en un hilo aparte para no congelar la ventana."""
        if self.corriendo:
            return
        self.corriendo = True
        self.inicio = time.monotonic()
        self.duracion = None
        self.lineas = 0
        for boton in (self.btn_circuito, self.btn_ros, self.btn_listas, self.btn_visor):
            boton.configure(state="disabled")
        self._senal(AMBAR, etiqueta.upper() + " EN CURSO")
        self._limpiar_log()
        self._escribir(f"$ python -m legajo {' '.join(argv)}\n\n", "orden")

        def trabajo():
            salida = _Tubo(self.cola)
            codigo = 1
            try:
                with redirect_stdout(salida), redirect_stderr(salida):
                    codigo = cli_main(argv)
            except SystemExit as e:
                codigo = int(e.code or 0)
            except Exception as e:
                self.cola.put(f"\n[error] {type(e).__name__}: {e}\n")
            finally:
                self.cola.put(f"\x00FIN{codigo}")

        threading.Thread(target=trabajo, daemon=True).start()

    def _correr_circuito(self):
        faltan = [n for n, c in (("padrón", self.padron),
                                 ("carpeta de listas", self.listas),
                                 ("informe de salida", self.salida))
                  if not c.get()]
        if faltan:
            messagebox.showwarning(
                "Faltan datos",
                "Hay que completar:\n\n  " + "\n  ".join(faltan))
            return

        argv = ["circuito",
                "--padron", self.padron.get(),
                "--listas", self.listas.get(),
                "--salida", self.salida.get()]
        for bandera, campo in (("--societaria", self.societaria),
                               ("--peps", self.peps),
                               ("--operaciones", self.operaciones),
                               ("--perfiles", self.perfiles)):
            if campo.get():
                argv += [bandera, campo.get()]
        if self.umbral.get():
            argv += ["--umbral-reporte", self.umbral.get().replace(".", "")]

        self.ultimo_informe = Path(self.salida.get())
        self._lanzar(argv, "Circuito")

    def _correr_ros(self):
        informe = self.salida.get()
        if not informe or not Path(informe).exists():
            messagebox.showwarning(
                "Falta el informe",
                "Primero hay que correr el circuito y completar en Excel\n"
                "las columnas de decisión de la hoja Alertas.")
            return
        if not self.operaciones.get():
            messagebox.showwarning(
                "Falta la operatoria",
                "Para armar los ROS hace falta el archivo de operaciones.")
            return

        argv = ["ros", "--informe", informe,
                "--padron", self.padron.get(),
                "--listas", self.listas.get(),
                "--operaciones", self.operaciones.get()]
        for bandera, campo in (("--societaria", self.societaria),
                               ("--peps", self.peps),
                               ("--perfiles", self.perfiles)):
            if campo.get():
                argv += [bandera, campo.get()]

        self.ultimo_informe = Path(informe)
        self._lanzar(argv, "Armado de ROS")

    def _actualizar_listas(self):
        if not self.listas.get():
            messagebox.showwarning(
                "Falta la carpeta",
                "Elegí dónde guardar las listas descargadas.")
            return
        self._lanzar(["actualizar-listas", "--listas", self.listas.get()],
                     "Descarga de listas")

    # --- consola -----------------------------------------------------------

    def _drenar_cola(self):
        try:
            while True:
                pieza = self.cola.get_nowait()
                if pieza.startswith("\x00FIN"):
                    self._terminar(int(pieza[4:]))
                else:
                    self._escribir(pieza)
        except queue.Empty:
            pass
        self.after(80, self._drenar_cola)

    def _escribir(self, texto: str, forzar: str = ""):
        self.log.configure(state="normal")
        for linea in texto.splitlines(keepends=True):
            plano = linea.lower()
            etiqueta = forzar or ("error" if "error" in plano else
                                  "aviso" if ("atencion" in plano or "aviso" in plano
                                              or "atención" in plano) else
                                  "ok" if "informe:" in plano else "")
            self.log.insert("end", linea, etiqueta)
            self.lineas += 1
        self.log.see("end")
        self.log.configure(state="disabled")

    def _limpiar_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def _terminar(self, codigo: int):
        self.corriendo = False
        if self.inicio is not None:
            self.duracion = int(time.monotonic() - self.inicio)
        for boton in (self.btn_circuito, self.btn_ros, self.btn_listas, self.btn_visor):
            boton.configure(state="normal")

        if codigo == 0:
            self._senal(VERDE, "TERMINADO SIN ERRORES")
            if self.ultimo_informe and self.ultimo_informe.exists():
                self.btn_abrir.configure(state="normal")
            if self.visor_pendiente is not None:
                pagina = self.visor_pendiente
                self.visor_pendiente = None
                if pagina.exists():
                    try:
                        self._abrir_en_el_sistema(str(pagina))
                    except Exception as e:
                        messagebox.showerror("No se pudo abrir el visor", str(e))
                else:
                    messagebox.showerror(
                        "Falta el visor",
                        f"No encuentro {pagina}.")
        else:
            self._senal(ROJO, f"TERMINÓ CON CÓDIGO {codigo}")
            self.visor_pendiente = None
        self._guardar_config()

    def _abrir_visor(self):
        """Corre `exportar` y abre el visor en el navegador.

        Arma el mismo comando que la terminal y lo manda por cli.main, igual
        que el resto de los botones. El visor se abre solo cuando el comando
        termino bien: mostrar un visor con datos de la corrida anterior es
        peor que no mostrar nada.
        """
        faltan = [n for n, c in (("padrón", self.padron),
                                 ("carpeta de listas", self.listas))
                  if not c.get()]
        if faltan:
            messagebox.showwarning(
                "Faltan datos",
                "Hay que completar:\n\n  " + "\n  ".join(faltan))
            return

        destino = Path(__file__).resolve().parent / "visor" / "datos.json"
        argv = ["exportar",
                "--padron", self.padron.get(),
                "--listas", self.listas.get(),
                "--salida", str(destino)]
        for bandera, campo in (("--societaria", self.societaria),
                               ("--peps", self.peps),
                               ("--operaciones", self.operaciones),
                               ("--perfiles", self.perfiles)):
            if campo.get():
                argv += [bandera, campo.get()]
        if self.umbral.get():
            argv += ["--umbral-reporte", self.umbral.get().replace(".", "")]

        self.visor_pendiente = destino.parent / "index.html"
        self._lanzar(argv, "Exportación al visor")

    def _abrir_en_el_sistema(self, ruta: str) -> None:
        if sys.platform.startswith("win"):
            import os
            os.startfile(ruta)  # noqa: S606
        elif sys.platform == "darwin":
            import subprocess
            subprocess.Popen(["open", ruta])
        else:
            import subprocess
            subprocess.Popen(["xdg-open", ruta])

    def _abrir_informe(self):
        if not self.ultimo_informe or not self.ultimo_informe.exists():
            return
        ruta = str(self.ultimo_informe)
        try:
            if sys.platform.startswith("win"):
                import os
                os.startfile(ruta)  # noqa: S606
            elif sys.platform == "darwin":
                import subprocess
                subprocess.Popen(["open", ruta])
            else:
                import subprocess
                subprocess.Popen(["xdg-open", ruta])
        except Exception as e:
            messagebox.showerror("No se pudo abrir", str(e))

    # --- persistencia ------------------------------------------------------

    def _campos(self):
        return {"padron": self.padron, "listas": self.listas,
                "societaria": self.societaria, "peps": self.peps,
                "operaciones": self.operaciones, "perfiles": self.perfiles,
                "salida": self.salida}

    def _cargar_config(self):
        if not CONFIG.exists():
            return
        try:
            datos = json.loads(CONFIG.read_text(encoding="utf-8"))
        except Exception:
            return
        for clave, campo in self._campos().items():
            campo.set(datos.get(clave, ""))
        self.umbral.set(datos.get("umbral", ""))

    def _guardar_config(self):
        datos = {k: c.get() for k, c in self._campos().items()}
        datos["umbral"] = self.umbral.get()
        try:
            CONFIG.write_text(json.dumps(datos, indent=2), encoding="utf-8")
        except Exception:
            pass

    def _cerrar(self):
        self._guardar_config()
        self.destroy()


class _Tubo:
    """Redirige lo que imprime el CLI hacia la cola de la interfaz."""

    def __init__(self, cola: queue.Queue):
        self.cola = cola

    def write(self, texto: str):
        if texto:
            self.cola.put(texto)

    def flush(self):
        pass


def main():
    Aplicacion().mainloop()


if __name__ == "__main__":
    main()
