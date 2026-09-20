# -*- mode: python ; coding: utf-8 -*-
"""Receta de empaquetado para PyInstaller.

Un solo archivo, sin consola de fondo. El paquete `legajo` entra entero
porque la interfaz llama a `cli.main`, asi que no hay logica duplicada que
pueda quedar afuera.

Los ejemplos van incluidos para que el ejecutable sirva de demo apenas se
abre, sin tener que conseguir datos antes.
"""

from PyInstaller.utils.hooks import collect_submodules

analisis = Analysis(
    ["legajo_gui.py"],
    pathex=["."],
    binaries=[],
    datas=[
        ("ejemplos", "ejemplos"),
    ],
    hiddenimports=collect_submodules("legajo") + ["openpyxl"],
    hookspath=[],
    runtime_hooks=[],
    # Peso muerto que PyInstaller arrastra si no se lo frena.
    excludes=[
        "matplotlib", "numpy", "pandas", "scipy", "PIL",
        "PyQt5", "PySide2", "notebook", "IPython", "pytest",
    ],
    noarchive=False,
)

pyz = PYZ(analisis.pure)

exe = EXE(
    pyz,
    analisis.scripts,
    analisis.binaries,
    analisis.datas,
    [],
    name="legajo",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # sin ventana negra de fondo
    disable_windowed_traceback=False,
    icon=None,              # poner "recursos/legajo.ico" si se agrega uno
)
