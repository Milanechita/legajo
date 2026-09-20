@echo off
REM ---------------------------------------------------------------------
REM  Arma legajo.exe para Windows.
REM
REM  Requiere Python 3.10 o mas nuevo instalado y en el PATH.
REM  Correr parado en la carpeta del repositorio:
REM
REM      build.bat
REM
REM  El ejecutable queda en  dist\legajo.exe  y anda solo, sin Python.
REM ---------------------------------------------------------------------

echo.
echo  == legajo :: armado del ejecutable ==
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo  [x] No encuentro Python en el PATH.
    echo      Instalalo desde python.org y marca "Add Python to PATH".
    exit /b 1
)

echo  [1/4] Instalando dependencias...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet openpyxl pyinstaller
if errorlevel 1 (
    echo  [x] Fallo la instalacion de dependencias.
    exit /b 1
)

echo  [2/4] Corriendo las pruebas...
python -m pip install --quiet pytest
python -m pytest tests/ -q
if errorlevel 1 (
    echo.
    echo  [x] Hay pruebas que fallan. No se arma el ejecutable.
    echo      Un .exe que sale de codigo roto es peor que no tenerlo.
    exit /b 1
)

echo  [3/4] Empaquetando...
python -m PyInstaller --noconfirm --clean legajo.spec
if errorlevel 1 (
    echo  [x] Fallo el empaquetado.
    exit /b 1
)

echo  [4/4] Listo.
echo.
echo      dist\legajo.exe
echo.
echo  Acordate de copiar la carpeta de listas al lado del ejecutable,
echo  o de apuntarla desde la interfaz.
echo.
