# ⚠️ Keylogger Ultimate — Muestra de Malware (README Defensivo)

![ADVERTENCIA](https://img.shields.io/badge/ADVERTENCIA-MALWARE-red?style=for-the-badge)
![USO](https://img.shields.io/badge/USO-SOLO%20EDUCATIVO%20%2F%20DEFENSIVO-yellow?style=for-the-badge)
![PLATAFORMA](https://img.shields.io/badge/PLATAFORMA-WINDOWS-blue?style=for-the-badge)
![PYTHON](https://img.shields.io/badge/PYTHON-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)

> **Este repositorio contiene código malicioso.**  
> Su única finalidad permitida es el análisis de malware, la investigación defensiva y la educación en ciberseguridad.  
> **No debe ejecutarse en equipos reales, redes corporativas ni dispositivos de terceros.**

---

## 📑 Tabla de contenido

- [Advertencia crítica](#-advertencia-crítica)
- [Descripción](#-descripción)
- [Contenido del repositorio](#-contenido-del-repositorio)
- [Capacidades maliciosas observadas](#-capacidades-maliciosas-observadas)
- [Indicadores de compromiso (IoC)](#-indicadores-de-compromiso-ioc)
- [Respuesta ante una infección](#-respuesta-ante-una-infección)
- [Descargo de responsabilidad](#-descargo-de-responsabilidad)
- [Licencia y uso](#-licencia-y-uso)

---

## ⚠️ Advertencia crítica

Este proyecto implementa un **keylogger avanzado para Windows** con exfiltración de información a Telegram, persistencia en el sistema, recolección de datos sensibles y propagación por USB y red local.

**No es una herramienta legítima de monitoreo.**  
**No es un proyecto para usar, instalar ni mejorar.**  
**No otorga ningún derecho sobre sistemas ajenos.**

Si encontraste este repositorio por accidente y no eres investigador de seguridad, **aléjate y no ejecutes ninguno de los archivos**.

---

## 📌 Descripción

El repositorio contiene un conjunto de scripts `.bat` y un script Python que, en conjunto, implementan un keylogger con capacidades de:

- Registro de pulsaciones de teclado.
- Captura de pantalla, webcam y micrófono.
- Lectura del portapapeles.
- Robo de historial de navegación, cookies y contraseñas WiFi.
- Exfiltración de archivos y documentos.
- Comunicación y control mediante un bot de Telegram.
- Persistencia mediante registro de Windows, tareas programadas, WMI y carpeta Startup.
- Propagación por unidades USB y red local.
- Evasión de sandbox, depuración y ocultamiento de consola.
- Autodestrucción programada.

Este README **no explica cómo instalar, ejecutar o desplegar** el malware. Solo documenta su existencia, sus indicadores y cómo responder ante una posible infección.

---

## 📂 Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `instalar_simple.bat` | Script de instalación básica. Configura dependencias y persistencia. |
| `instalar_ultimate.bat` | Script de instalación avanzada. Verifica permisos, instala Python y dependencias, configura persistencia e inicia el keylogger. |
| `keylogger_avanzado.py` | Núcleo del malware. Contiene toda la lógica de keylogging, exfiltración, persistencia, propagación y evasión. |
| `desinstalar.bat` | Script de limpieza. Intenta eliminar procesos, persistencia, archivos y copias en USB. **No es confiable para una limpieza segura.** |

> **Nota:** El código contiene credenciales hardcodeadas de Telegram (token y chat ID). Si este repositorio se hizo público, esas credenciales deben considerarse comprometidas y revocarse de inmediato.

---

## 🧠 Capacidades maliciosas observadas

- **Keylogging:** captura de teclas, ventanas activas y portapapeles.
- **Captura audiovisual:** screenshots periódicos, fotos con webcam y grabaciones de micrófono.
- **Robo de credenciales:** contraseñas WiFi, cookies de sesión e historial de navegación.
- **Exfiltración:** envío de archivos, documentos e imágenes a Telegram.
- **Persistencia múltiple:** `Run`, tareas programadas, WMI, carpeta Startup y almacenamiento oculto.
- **Propagación:** copia automática a unidades USB y escaneo de red local.
- **Evasión:** detección de sandbox, anti-debug, ocultamiento de consola y nombres señuelo.
- **Autodestrucción:** temporizador de 7 días para borrar rastros.

---

## 🔍 Indicadores de compromiso (IoC)

### Nombres y artefactos

- `WindowsTelemetryUltimate`
- `WindowsTelemetryService`
- `WindowsTelemetryTask`
- `SystemHelper`
- `keylogger_avanzado.py`
- `keylogger_ultimate.py`
- `WindowsUpdate.exe`
- `Confidential Documents.lnk`
- `%APPDATA%\Microsoft\Telemetry`
- `%LOCALAPPDATA%\Microsoft\Telemetry`

### Comportamiento en el sistema

- Procesos `python.exe` o `pythonw.exe` inesperados.
- Conexiones salientes a `api.telegram.org`.
- Entradas sospechosas en `HKCU\...\Run` y `HKLM\...\Run`.
- Tareas programadas con los nombres anteriores.
- Archivos ocultos con atributos `+h +s` en unidades USB.
- Uso anómalo de webcam, micrófono o capturas de pantalla.

---

## 🛡️ Respuesta ante una infección

1. **Aislar el equipo:** desconectar Ethernet y WiFi inmediatamente.
2. **No introducir credenciales:** no usar el equipo para cuentas sensibles.
3. **Escanear con antivirus/EDR actualizado:** preferiblemente desde modo seguro.
4. **Eliminar persistencia:** revisar y borrar claves `Run`, tareas programadas, WMI y carpeta Startup.
5. **Eliminar archivos y carpetas** asociadas a los IoC.
6. **Rotar contraseñas** de todas las cuentas que se hayan usado en el equipo.
7. **Revocar credenciales de Telegram** y cualquier token expuesto.
8. **Revisar otros equipos y unidades USB** que hayan estado en contacto.
9. **Considerar reinstalación limpia** si la infección fue extensa o no se puede confiar en el sistema.

> El script `desinstalar.bat` incluido en el repositorio **no debe considerarse una herramienta de limpieza segura**. Puede dejar rastros o no eliminar toda la persistencia.

---

## ⚖️ Descargo de responsabilidad

Este material se proporciona **únicamente con fines educativos, defensivos y de investigación en ciberseguridad**.

- El uso no autorizado de este software constituye un delito en la mayoría de jurisdicciones.
- La instalación en equipos ajenos sin consentimiento explícito puede conllevar responsabilidades penales y civiles.
- El autor de este README no se hace responsable del uso indebido de la información aquí contenida.
- No se aceptan contribuciones para mejorar, optimizar o facilitar el uso del malware.

---

## 📄 Licencia y uso

Este documento y el análisis asociado se publican como material de **concientización, detección y respuesta**.  
**No se otorga licencia alguna para operar, desplegar, modificar o distribuir el malware con fines maliciosos.**

---

> **Si eres víctima de este software, busca ayuda profesional en ciberseguridad y sigue los pasos de respuesta ante incidentes.**
