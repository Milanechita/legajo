#!/usr/bin/env bash
# ---------------------------------------------------------------------
#  Arma el ejecutable de legajo para Linux o macOS.
#  En Linux hace falta tkinter aparte:  sudo apt install python3-tk
# ---------------------------------------------------------------------
set -e

echo
echo " == legajo :: armado del ejecutable =="
echo

python3 -c "import tkinter" 2>/dev/null || {
    echo " [x] Falta tkinter."
    echo "     Debian o Ubuntu:  sudo apt install python3-tk"
    echo "     Fedora:           sudo dnf install python3-tkinter"
    exit 1
}

echo " [1/4] Instalando dependencias..."
python3 -m pip install --quiet --upgrade pip
python3 -m pip install --quiet openpyxl pyinstaller pytest

echo " [2/4] Corriendo las pruebas..."
python3 -m pytest tests/ -q || {
    echo
    echo " [x] Hay pruebas que fallan. No se arma el ejecutable."
    exit 1
}

echo " [3/4] Empaquetando..."
python3 -m PyInstaller --noconfirm --clean legajo.spec

echo " [4/4] Listo."
echo
echo "     dist/legajo"
echo
