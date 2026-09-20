"""Interfaz de escritorio para legajo.

No reimplementa nada. Arma la linea de comandos y llama al mismo `cli.main`
que usa la terminal, capturando lo que imprime.

Esa es toda la gracia del diseño: si la logica viviera duplicada aca, en la
segunda correccion las dos versiones empezarian a dar resultados distintos y
nadie se enteraria hasta que un informe salga mal.

Corre con tkinter, que viene con Python, asi que el ejecutable no arrastra
ninguna dependencia grafica.
"""

from __future__ import annotations

import json
import queue
import sys
import threading
import tkinter as tk
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from legajo.cli import main as cli_main

TITULO = "legajo  ·  circuito PLA/FT"
CONFIG = Path.home() / ".legajo_gui.json"

# Paleta sobria. Esto lo abre alguien de cumplimiento, no de diseno.
FONDO = "#F4F5F7"
PANEL = "#FFFFFF"
TINTA = "#1F2933"
GRIS = "#6B7785"
ACENTO = "#1F5C8B"
CONSOLA_FONDO = "#1B222A"
CONSOLA_TEXTO = "#D8DEE6"


class Campo:
    """Una fila de la grilla: etiqueta, caja de texto y boton de examinar."""

    def __init__(self, padre, fila, etiqueta, ayuda, modo="archivo",
                 requerido=False, tipos=None):
        self.modo = modo
        self.tipos = tipos or [("CSV o Excel", "*.csv *.xlsx"), ("Todos", "*.*")]
        self.valor = tk.StringVar()

        marca = "  *" if requerido else ""
        ttk.Label(padre, text=etiqueta + marca).grid(
            row=fila, column=0, sticky="w", padx=(0, 10), pady=4)

        entrada = ttk.Entry(padre, textvariable=self.valor, width=54)
        entrada.grid(row=fila, column=1, sticky="ew", pady=4)

        ttk.Button(padre, text="Examinar", width=11, command=self._elegir).grid(
            row=fila, column=2, padx=(8, 0), pady=4)

        ttk.Label(padre, text=ayuda, foreground=GRIS, font=("Segoe UI", 8)).grid(
            row=fila + 1, column=1, sticky="w", pady=(0, 6))

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
        self.geometry("880x760")
        self.minsize(780, 640)
        self.configure(bg=FONDO)

        self.cola: queue.Queue[str] = queue.Queue()
        self.corriendo = False
        self.ultimo_informe: Path | None = None

        self._estilos()
        self._armar()
        self._cargar_config()
        self.after(80, self._drenar_cola)
        self.protocol("WM_DELETE_WINDOW", self._cerrar)

    # --- apariencia --------------------------------------------------------

    def _estilos(self):
        estilo = ttk.Style(self)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure(".", background=FONDO, foreground=TINTA,
                         font=("Segoe UI", 9))
        estilo.configure("TFrame", background=FONDO)
        estilo.configure("Panel.TFrame", background=PANEL, relief="flat")
        estilo.configure("TLabelframe", background=FONDO, foreground=TINTA)
        estilo.configure("TLabelframe.Label", background=FONDO,
                         foreground=ACENTO, font=("Segoe UI", 9, "bold"))
        estilo.configure("TLabel", background=FONDO)
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 15, "bold"),
                         foreground=TINTA)
        estilo.configure("Sub.TLabel", foreground=GRIS)
        estilo.configure("TButton", padding=(10, 5))
        estilo.configure("Principal.TButton", font=("Segoe UI", 9, "bold"))

    def _armar(self):
        raiz = ttk.Frame(self, padding=16)
        raiz.pack(fill="both", expand=True)
        raiz.columnconfigure(0, weight=1)

        encabezado = ttk.Frame(raiz)
        encabezado.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(encabezado, text="legajo", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(encabezado, style="Sub.TLabel",
                  text="Screening de listas, beneficiario final, riesgo, "
                       "monitoreo y armado de ROS").pack(anchor="w")

        # --- entradas ---
        caja = ttk.LabelFrame(raiz, text="  Archivos de entrada  ", padding=14)
        caja.grid(row=1, column=0, sticky="ew")
        caja.columnconfigure(1, weight=1)

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
        params = ttk.LabelFrame(raiz, text="  Parámetros  ", padding=14)
        params.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        params.columnconfigure(1, weight=1)

        self.salida = Campo(params, 0, "Informe de salida",
                            "Se sobrescribe si ya existe",
                            modo="guardar", requerido=True)

        ttk.Label(params, text="Umbral de reporte").grid(
            row=2, column=0, sticky="w", padx=(0, 10))
        self.umbral = tk.StringVar()
        ttk.Entry(params, textvariable=self.umbral, width=18).grid(
            row=2, column=1, sticky="w")
        ttk.Label(params, foreground=GRIS, font=("Segoe UI", 8),
                  text="En pesos. Vacío usa 40 SMVM según la Res. UIF 78/2025").grid(
            row=3, column=1, sticky="w", pady=(0, 4))

        # --- acciones ---
        acciones = ttk.Frame(raiz)
        acciones.grid(row=3, column=0, sticky="ew", pady=(14, 10))

        self.btn_circuito = ttk.Button(acciones, text="Correr circuito",
                                       style="Principal.TButton", width=20,
                                       command=self._correr_circuito)
        self.btn_circuito.pack(side="left")

        self.btn_ros = ttk.Button(acciones, text="Armar borradores de ROS",
                                  width=24, command=self._correr_ros)
        self.btn_ros.pack(side="left", padx=8)

        self.btn_listas = ttk.Button(acciones, text="Actualizar listas",
                                     width=18, command=self._actualizar_listas)
        self.btn_listas.pack(side="left")

        self.btn_abrir = ttk.Button(acciones, text="Abrir informe", width=16,
                                    command=self._abrir_informe,
                                    state="disabled")
        self.btn_abrir.pack(side="right")

        # --- consola ---
        consola = ttk.LabelFrame(raiz, text="  Salida  ", padding=8)
        consola.grid(row=4, column=0, sticky="nsew")
        raiz.rowconfigure(4, weight=1)
        consola.columnconfigure(0, weight=1)
        consola.rowconfigure(0, weight=1)

        self.log = tk.Text(consola, height=14, wrap="none", bd=0,
                           bg=CONSOLA_FONDO, fg=CONSOLA_TEXTO,
                           insertbackground=CONSOLA_TEXTO,
                           font=("Consolas", 9), padx=10, pady=8)
        self.log.grid(row=0, column=0, sticky="nsew")

        barra = ttk.Scrollbar(consola, orient="vertical", command=self.log.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.log.configure(yscrollcommand=barra.set, state="disabled")

        self.log.tag_configure("aviso", foreground="#E8B04B")
        self.log.tag_configure("error", foreground="#E86C60")
        self.log.tag_configure("ok", foreground="#7FBF7F")

        self.estado = ttk.Label(raiz, text="Listo", style="Sub.TLabel")
        self.estado.grid(row=5, column=0, sticky="w", pady=(8, 0))

    # --- ejecucion ---------------------------------------------------------

    def _lanzar(self, argv: list[str], etiqueta: str):
        """Corre el CLI en un hilo aparte para no congelar la ventana."""
        if self.corriendo:
            return
        self.corriendo = True
        for boton in (self.btn_circuito, self.btn_ros, self.btn_listas):
            boton.configure(state="disabled")
        self.estado.configure(text=f"{etiqueta} en curso...")
        self._limpiar_log()
        self._escribir(f"$ python -m legajo {' '.join(argv)}\n\n")

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

    def _escribir(self, texto: str):
        self.log.configure(state="normal")
        for linea in texto.splitlines(keepends=True):
            plano = linea.lower()
            etiqueta = ("error" if "error" in plano else
                        "aviso" if ("atencion" in plano or "aviso" in plano
                                    or "atención" in plano) else
                        "ok" if "informe:" in plano else "")
            self.log.insert("end", linea, etiqueta)
        self.log.see("end")
        self.log.configure(state="disabled")

    def _limpiar_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def _terminar(self, codigo: int):
        self.corriendo = False
        for boton in (self.btn_circuito, self.btn_ros, self.btn_listas):
            boton.configure(state="normal")

        if codigo == 0:
            self.estado.configure(text="Terminado sin errores")
            if self.ultimo_informe and self.ultimo_informe.exists():
                self.btn_abrir.configure(state="normal")
        else:
            self.estado.configure(text=f"Terminó con código {codigo}")
        self._guardar_config()

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
