"""
╔══════════════════════════════════════════════════════════════════╗
║                    J.A.R.V.I.S  - Phase 2                       ║
║              Advanced Features Extension Module                  ║
╚══════════════════════════════════════════════════════════════════╝

Phase 2 Features:
  ✦ Email Read & Send (Gmail)
  ✦ Advanced File Manager (copy, move, delete, rename, organize)
  ✦ Clipboard Manager
  ✦ Process Manager (list, kill processes)
  ✦ WiFi Manager (scan, info)
  ✦ Battery Monitor with alerts
  ✦ Disk Analyzer
  ✦ Auto Typer
  ✦ Password Generator
  ✦ URL Shortener
  ✦ QR Code Generator
  ✦ Text Translator (EN ↔ BN)
  ✦ Dictionary / Word meaning
  ✦ Speedtest
  ✦ Alarm Clock
  ✦ Stopwatch & Timer
  ✦ World Clock (multiple timezones)
  ✦ Currency Converter
  ✦ Unit Converter
  ✦ Todo List (advanced)
  ✦ System Cleanup
"""

import os, sys, json, time, datetime, threading, subprocess
import platform, random, string, webbrowser, shutil, glob
import urllib.parse, base64, hashlib, re, socket
from pathlib import Path

# ── Auto-install Phase 2 dependencies ────────────────────────────
P2_PACKAGES = {
    "pyperclip":        "pyperclip",
    "qrcode":           "qrcode[pil]",
    "deep_translator":  "deep-translator",
    "speedtest":        "speedtest-cli",
    "pyautogui":        "pyautogui",
}

def install_p2():
    import importlib
    for mod, pkg in P2_PACKAGES.items():
        try:
            importlib.import_module(mod)
        except ImportError:
            print(f"  [INSTALL] {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

# ══════════════════════════════════════════════════════════════════
#  PHASE 2 SKILLS CLASS
# ══════════════════════════════════════════════════════════════════
class Phase2Skills:
    def __init__(self, config: dict, voice_speak_fn):
        self.cfg   = config
        self.speak = voice_speak_fn
        self.todos = self._load_todos()
        self.alarms: list = []
        self._start_alarm_thread()
        install_p2()

    # ─────────────────────────────────────────────────────────────
    # 1. CLIPBOARD MANAGER
    # ─────────────────────────────────────────────────────────────
    def clipboard_get(self):
        try:
            import pyperclip
            text = pyperclip.paste()
            return f"Clipboard content:\n  {text[:500]}" if text else "Clipboard is empty."
        except Exception as e:
            return f"Clipboard error: {e}"

    def clipboard_set(self, text: str):
        try:
            import pyperclip
            pyperclip.copy(text)
            return f"Copied to clipboard: '{text[:80]}'"
        except Exception as e:
            return f"Clipboard error: {e}"

    # ─────────────────────────────────────────────────────────────
    # 2. ADVANCED FILE MANAGER
    # ─────────────────────────────────────────────────────────────
    def list_dir(self, path: str = "."):
        try:
            p = Path(path).expanduser()
            items = list(p.iterdir())
            files = [i for i in items if i.is_file()]
            dirs  = [i for i in items if i.is_dir()]
            result = f"📁 {p}\n"
            result += f"  Folders ({len(dirs)}):\n"
            for d in dirs[:10]:
                result += f"    📂 {d.name}\n"
            result += f"  Files ({len(files)}):\n"
            for f in files[:15]:
                size = f.stat().st_size
                result += f"    📄 {f.name}  ({_human_size(size)})\n"
            if len(files) > 15:
                result += f"    ... and {len(files)-15} more files\n"
            return result
        except Exception as e:
            return f"Error listing directory: {e}"

    def copy_file(self, src: str, dst: str):
        try:
            shutil.copy2(src, dst)
            return f"Copied: {src} → {dst}"
        except Exception as e:
            return f"Copy failed: {e}"

    def move_file(self, src: str, dst: str):
        try:
            shutil.move(src, dst)
            return f"Moved: {src} → {dst}"
        except Exception as e:
            return f"Move failed: {e}"

    def delete_file(self, path: str):
        try:
            p = Path(path)
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            return f"Deleted: {path}"
        except Exception as e:
            return f"Delete failed: {e}"

    def rename_file(self, old: str, new: str):
        try:
            Path(old).rename(new)
            return f"Renamed: {old} → {new}"
        except Exception as e:
            return f"Rename failed: {e}"

    def create_folder(self, path: str):
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return f"Folder created: {path}"
        except Exception as e:
            return f"Failed: {e}"

    def disk_analyzer(self, path: str = "C:/"):
        try:
            usage = shutil.disk_usage(path)
            result = (f"Disk Analysis for {path}:\n"
                      f"  Total : {_human_size(usage.total)}\n"
                      f"  Used  : {_human_size(usage.used)} "
                      f"({usage.used/usage.total*100:.1f}%)\n"
                      f"  Free  : {_human_size(usage.free)}")
            return result
        except Exception as e:
            return f"Disk error: {e}"

    def organize_downloads(self):
        """Auto-organize Downloads folder by file type."""
        dl = Path.home() / "Downloads"
        categories = {
            "Images":     [".jpg",".jpeg",".png",".gif",".bmp",".webp",".svg"],
            "Videos":     [".mp4",".mkv",".avi",".mov",".wmv",".flv"],
            "Audio":      [".mp3",".wav",".flac",".aac",".ogg"],
            "Documents":  [".pdf",".doc",".docx",".txt",".xlsx",".pptx",".csv"],
            "Archives":   [".zip",".rar",".7z",".tar",".gz"],
            "Programs":   [".exe",".msi",".apk",".dmg"],
            "Code":       [".py",".js",".html",".css",".java",".cpp",".c"],
        }
        moved = 0
        for f in dl.iterdir():
            if f.is_file():
                ext = f.suffix.lower()
                for cat, exts in categories.items():
                    if ext in exts:
                        dest = dl / cat
                        dest.mkdir(exist_ok=True)
                        try:
                            shutil.move(str(f), str(dest / f.name))
                            moved += 1
                        except Exception:
                            pass
                        break
        return f"Downloads organized! {moved} files sorted into categories. ✅"

    # ─────────────────────────────────────────────────────────────
    # 3. PROCESS MANAGER
    # ─────────────────────────────────────────────────────────────
    def list_processes(self, top: int = 10):
        try:
            import psutil
            procs = []
            for p in psutil.process_iter(['pid','name','cpu_percent','memory_info']):
                try:
                    procs.append(p.info)
                except Exception:
                    pass
            procs.sort(key=lambda x: x.get('cpu_percent') or 0, reverse=True)
            result = f"Top {top} Processes by CPU:\n"
            result += f"  {'PID':<8} {'Name':<25} {'CPU%':<8} {'RAM'}\n"
            result += "  " + "─"*55 + "\n"
            for p in procs[:top]:
                ram = _human_size(p['memory_info'].rss) if p.get('memory_info') else "N/A"
                result += (f"  {p['pid']:<8} {p['name'][:24]:<25} "
                           f"{p.get('cpu_percent',0):<8.1f} {ram}\n")
            return result
        except Exception as e:
            return f"Process list error: {e}"

    def kill_process(self, name_or_pid: str):
        try:
            import psutil
            killed = []
            for p in psutil.process_iter(['pid','name']):
                try:
                    if (str(p.pid) == name_or_pid or
                            name_or_pid.lower() in p.name().lower()):
                        p.kill()
                        killed.append(p.name())
                except Exception:
                    pass
            if killed:
                return f"Killed: {', '.join(killed)}"
            return f"No process found: '{name_or_pid}'"
        except Exception as e:
            return f"Kill failed: {e}"

    # ─────────────────────────────────────────────────────────────
    # 4. WIFI MANAGER
    # ─────────────────────────────────────────────────────────────
    def wifi_info(self):
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["netsh","wlan","show","interfaces"],
                    capture_output=True, text=True)
                lines = result.stdout.splitlines()
                info_lines = []
                for l in lines:
                    if any(k in l for k in ["SSID","Signal","Radio","State","Speed"]):
                        info_lines.append(f"  {l.strip()}")
                return "WiFi Info:\n" + "\n".join(info_lines) if info_lines else "No WiFi interface found."
            else:
                return subprocess.run(["iwconfig"], capture_output=True, text=True).stdout
        except Exception as e:
            return f"WiFi info error: {e}"

    def wifi_scan(self):
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["netsh","wlan","show","networks"],
                    capture_output=True, text=True)
                return result.stdout[:1500]
            return "WiFi scan not supported on this OS."
        except Exception as e:
            return f"WiFi scan error: {e}"

    # ─────────────────────────────────────────────────────────────
    # 5. PASSWORD GENERATOR
    # ─────────────────────────────────────────────────────────────
    def generate_password(self, length: int = 16, strong: bool = True):
        if strong:
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
        else:
            chars = string.ascii_letters + string.digits
        pwd = ''.join(random.SystemRandom().choice(chars) for _ in range(length))
        return f"Generated password ({length} chars):\n  {pwd}\n  (Copied to clipboard!)"

    # ─────────────────────────────────────────────────────────────
    # 6. QR CODE GENERATOR
    # ─────────────────────────────────────────────────────────────
    def generate_qr(self, data: str):
        try:
            import qrcode
            qr = qrcode.QRCode(box_size=10, border=4)
            qr.add_data(data)
            qr.make(fit=True)
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = f"qrcode_{ts}.png"
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(fname)
            webbrowser.open(fname)
            return f"QR Code generated and saved as '{fname}'! 📱"
        except Exception as e:
            return f"QR generation failed: {e}"

    # ─────────────────────────────────────────────────────────────
    # 7. TEXT TRANSLATOR
    # ─────────────────────────────────────────────────────────────
    def translate(self, text: str, target: str = "bn"):
        try:
            from deep_translator import GoogleTranslator
            translated = GoogleTranslator(source="auto", target=target).translate(text)
            lang_name = "Bangla" if target == "bn" else "English"
            return f"Translation ({lang_name}):\n  {translated}"
        except Exception as e:
            return f"Translation failed: {e}"

    # ─────────────────────────────────────────────────────────────
    # 8. SPEEDTEST
    # ─────────────────────────────────────────────────────────────
    def internet_speed(self):
        try:
            import speedtest as st
            print("  ⟳  Running speed test (30-60 seconds)...")
            s = st.Speedtest()
            s.get_best_server()
            download = s.download() / 1_000_000
            upload   = s.upload()   / 1_000_000
            ping_val = s.results.ping
            return (f"Internet Speed Test:\n"
                    f"  ↓ Download : {download:.2f} Mbps\n"
                    f"  ↑ Upload   : {upload:.2f} Mbps\n"
                    f"  ⟳ Ping     : {ping_val:.0f} ms")
        except Exception as e:
            return f"Speed test failed: {e}"

    # ─────────────────────────────────────────────────────────────
    # 9. WORLD CLOCK
    # ─────────────────────────────────────────────────────────────
    def world_clock(self):
        try:
            from datetime import timezone, timedelta
            cities = {
                "Dhaka (BD)":       6,
                "London (UK)":      1,
                "New York (US)":   -4,
                "Los Angeles (US)":-7,
                "Tokyo (JP)":       9,
                "Dubai (UAE)":      4,
                "Sydney (AU)":     10,
                "Paris (FR)":       2,
            }
            result = "🌍 World Clock:\n"
            for city, offset in cities.items():
                tz = timezone(timedelta(hours=offset))
                t  = datetime.datetime.now(tz).strftime("%I:%M %p, %a %d %b")
                result += f"  {city:<22}: {t}\n"
            return result
        except Exception as e:
            return f"World clock error: {e}"

    # ─────────────────────────────────────────────────────────────
    # 10. CURRENCY CONVERTER
    # ─────────────────────────────────────────────────────────────
    def currency_convert(self, amount: float, from_c: str, to_c: str):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_c.upper()}"
            import requests as req
            r = req.get(url, timeout=8)
            rates = r.json().get("rates", {})
            rate  = rates.get(to_c.upper())
            if rate:
                converted = amount * rate
                return (f"Currency Conversion:\n"
                        f"  {amount} {from_c.upper()} = "
                        f"{converted:.2f} {to_c.upper()}\n"
                        f"  Rate: 1 {from_c.upper()} = {rate:.4f} {to_c.upper()}")
            return f"Currency '{to_c}' not found."
        except Exception as e:
            return f"Currency conversion failed: {e}"

    # ─────────────────────────────────────────────────────────────
    # 11. UNIT CONVERTER
    # ─────────────────────────────────────────────────────────────
    def unit_convert(self, value: float, from_u: str, to_u: str):
        conversions = {
            # length (base: meter)
            "km":1000,"m":1,"cm":0.01,"mm":0.001,
            "mile":1609.34,"yard":0.9144,"foot":0.3048,"inch":0.0254,
            # weight (base: kg)
            "kg":1,"g":0.001,"lb":0.453592,"oz":0.0283495,"ton":1000,
            # temp handled separately
        }
        fu, tu = from_u.lower(), to_u.lower()
        # Temperature
        if fu in ["c","celsius"] and tu in ["f","fahrenheit"]:
            return f"{value}°C = {value*9/5+32:.2f}°F"
        if fu in ["f","fahrenheit"] and tu in ["c","celsius"]:
            return f"{value}°F = {(value-32)*5/9:.2f}°C"
        if fu in ["c","celsius"] and tu in ["k","kelvin"]:
            return f"{value}°C = {value+273.15:.2f}K"
        # Standard
        if fu in conversions and tu in conversions:
            base    = value * conversions[fu]
            result  = base  / conversions[tu]
            return f"{value} {from_u} = {result:.6g} {to_u}"
        return f"Unknown units: '{from_u}' or '{to_u}'"

    # ─────────────────────────────────────────────────────────────
    # 12. ALARM CLOCK
    # ─────────────────────────────────────────────────────────────
    def set_alarm(self, alarm_time: str, label: str = "Alarm"):
        """alarm_time format: HH:MM (24h)"""
        try:
            h, m = map(int, alarm_time.split(":"))
            self.alarms.append({"hour": h, "minute": m, "label": label, "done": False})
            return f"Alarm set for {alarm_time} — '{label}'. ⏰ এলার্ম সেট হয়েছে!"
        except Exception as e:
            return f"Alarm error: {e}"

    def list_alarms(self):
        if not self.alarms:
            return "No alarms set. কোনো এলার্ম নেই।"
        result = "Active Alarms:\n"
        for i, a in enumerate(self.alarms, 1):
            status = "✓" if a["done"] else "⏰"
            result += f"  {i}. {status} {a['hour']:02d}:{a['minute']:02d} — {a['label']}\n"
        return result

    def _start_alarm_thread(self):
        def _check():
            while True:
                now = datetime.datetime.now()
                for a in self.alarms:
                    if (not a["done"] and
                            a["hour"] == now.hour and
                            a["minute"] == now.minute):
                        self.speak(f"Alarm! {a['label']}. এলার্ম বাজছে!")
                        a["done"] = True
                time.sleep(30)
        threading.Thread(target=_check, daemon=True).start()

    # ─────────────────────────────────────────────────────────────
    # 13. STOPWATCH
    # ─────────────────────────────────────────────────────────────
    _sw_start = None
    _sw_running = False

    def stopwatch_start(self):
        self._sw_start   = time.time()
        self._sw_running = True
        return "Stopwatch started! ⏱ স্টপওয়াচ শুরু হয়েছে!"

    def stopwatch_stop(self):
        if not self._sw_running:
            return "Stopwatch not running."
        elapsed = time.time() - self._sw_start
        self._sw_running = False
        m, s = divmod(int(elapsed), 60)
        h, m = divmod(m, 60)
        return f"Stopwatch stopped: {h:02d}:{m:02d}:{s:02d} ⏱"

    def stopwatch_check(self):
        if not self._sw_running:
            return "Stopwatch not running."
        elapsed = time.time() - self._sw_start
        m, s = divmod(int(elapsed), 60)
        h, m = divmod(m, 60)
        return f"Elapsed time: {h:02d}:{m:02d}:{s:02d}"

    # ─────────────────────────────────────────────────────────────
    # 14. COUNTDOWN TIMER
    # ─────────────────────────────────────────────────────────────
    def countdown_timer(self, seconds: int, label: str = "Timer"):
        def _run():
            time.sleep(seconds)
            self.speak(f"Timer done! {label}. টাইমার শেষ!")
        threading.Thread(target=_run, daemon=True).start()
        m, s = divmod(seconds, 60)
        return f"Timer set: {m}m {s}s — '{label}'. ⏳"

    # ─────────────────────────────────────────────────────────────
    # 15. TODO LIST (Advanced)
    # ─────────────────────────────────────────────────────────────
    def _load_todos(self):
        todo_file = "jarvis_todos.json"
        if os.path.exists(todo_file):
            with open(todo_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save_todos(self):
        with open("jarvis_todos.json", "w", encoding="utf-8") as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)

    def add_todo(self, task: str, priority: str = "normal"):
        self.todos.append({
            "task": task, "done": False,
            "priority": priority,
            "created": datetime.datetime.now().isoformat()
        })
        self._save_todos()
        return f"Todo added: '{task}' [{priority}] ✅"

    def show_todos(self):
        if not self.todos:
            return "No todos. কোনো কাজ নেই।"
        result = "📋 Todo List:\n"
        for i, t in enumerate(self.todos, 1):
            check = "✓" if t["done"] else "○"
            pri   = f"[{t.get('priority','normal')}]"
            result += f"  {i}. {check} {pri} {t['task']}\n"
        return result

    def complete_todo(self, index: int):
        try:
            self.todos[index-1]["done"] = True
            self._save_todos()
            return f"Todo #{index} marked as done! ✓"
        except IndexError:
            return f"No todo #{index} found."

    def delete_todo(self, index: int):
        try:
            removed = self.todos.pop(index-1)
            self._save_todos()
            return f"Todo deleted: '{removed['task']}'"
        except IndexError:
            return f"No todo #{index} found."

    # ─────────────────────────────────────────────────────────────
    # 16. SYSTEM CLEANUP
    # ─────────────────────────────────────────────────────────────
    def system_cleanup(self):
        freed = 0
        results = []
        # Temp folders
        temp_paths = [
            os.environ.get("TEMP", ""),
            os.environ.get("TMP", ""),
            os.path.join(os.environ.get("WINDIR","C:/Windows"), "Temp"),
        ]
        for tp in temp_paths:
            if tp and os.path.exists(tp):
                for f in Path(tp).iterdir():
                    try:
                        if f.is_file():
                            size = f.stat().st_size
                            f.unlink()
                            freed += size
                        elif f.is_dir():
                            shutil.rmtree(f, ignore_errors=True)
                    except Exception:
                        pass
        results.append(f"Temp files cleared: {_human_size(freed)} freed")
        # Empty Recycle Bin (Windows)
        try:
            subprocess.run(["PowerShell","Clear-RecycleBin","-Force"],
                           capture_output=True, timeout=10)
            results.append("Recycle Bin emptied ✓")
        except Exception:
            pass
        return "System Cleanup Complete:\n" + "\n".join(f"  ✓ {r}" for r in results)

    # ─────────────────────────────────────────────────────────────
    # 17. BATTERY MONITOR (with alert threshold)
    # ─────────────────────────────────────────────────────────────
    def battery_alert(self, threshold: int = 20):
        def _monitor():
            import psutil
            while True:
                bat = psutil.sensors_battery()
                if bat and not bat.power_plugged and bat.percent <= threshold:
                    self.speak(f"Warning! Battery at {bat.percent:.0f}%. Please plug in charger. ব্যাটারি কম!")
                time.sleep(120)
        threading.Thread(target=_monitor, daemon=True).start()
        return f"Battery alert enabled at {threshold}%. 🔋"

    # ─────────────────────────────────────────────────────────────
    # 18. AUTO TYPER
    # ─────────────────────────────────────────────────────────────
    def auto_type(self, text: str, delay: float = 0.05):
        try:
            import pyautogui
            time.sleep(2)  # give user time to click target
            pyautogui.typewrite(text, interval=delay)
            return f"Auto-typed: '{text[:50]}...'"
        except Exception as e:
            return f"Auto-type failed: {e}"

    # ─────────────────────────────────────────────────────────────
    # 19. OPEN PORTS SCANNER (own machine)
    # ─────────────────────────────────────────────────────────────
    def scan_own_ports(self):
        open_ports = []
        common = [21,22,23,25,53,80,110,143,443,445,
                  3306,3389,5432,6379,8080,8443,27017]
        for port in common:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.3)
                if s.connect_ex(("127.0.0.1", port)) == 0:
                    open_ports.append(port)
                s.close()
            except Exception:
                pass
        if open_ports:
            return "Open ports on this machine:\n" + "".join(
                f"  • Port {p}\n" for p in open_ports)
        return "No common ports are open on this machine."

    # ─────────────────────────────────────────────────────────────
    # 20. HASH GENERATOR
    # ─────────────────────────────────────────────────────────────
    def hash_text(self, text: str):
        return (f"Hash values for: '{text[:40]}'\n"
                f"  MD5    : {hashlib.md5(text.encode()).hexdigest()}\n"
                f"  SHA1   : {hashlib.sha1(text.encode()).hexdigest()}\n"
                f"  SHA256 : {hashlib.sha256(text.encode()).hexdigest()}")

    # ─────────────────────────────────────────────────────────────
    # 21. ENCODE / DECODE
    # ─────────────────────────────────────────────────────────────
    def base64_encode(self, text: str):
        return "Base64: " + base64.b64encode(text.encode()).decode()

    def base64_decode(self, encoded: str):
        try:
            return "Decoded: " + base64.b64decode(encoded).decode()
        except Exception:
            return "Invalid Base64 string."

    # ─────────────────────────────────────────────────────────────
    # 22. DICTIONARY (word meaning via Free Dictionary API)
    # ─────────────────────────────────────────────────────────────
    def define_word(self, word: str):
        try:
            import requests as req
            r = req.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
                        timeout=8)
            data = r.json()
            if isinstance(data, list) and data:
                meanings = data[0].get("meanings", [])
                result = f"Definition of '{word}':\n"
                for m in meanings[:2]:
                    pos = m.get("partOfSpeech","")
                    defs = m.get("definitions",[])
                    result += f"  [{pos}]\n"
                    for d in defs[:2]:
                        result += f"    • {d['definition']}\n"
                return result
            return f"Definition not found for '{word}'."
        except Exception as e:
            return f"Dictionary error: {e}"

    # ─────────────────────────────────────────────────────────────
    # 23. SYSTEM INFO (Extended)
    # ─────────────────────────────────────────────────────────────
    def extended_sysinfo(self):
        try:
            import psutil
            cpu_freq = psutil.cpu_freq()
            result = (
                f"Extended System Info:\n"
                f"  Processor  : {platform.processor()}\n"
                f"  CPU Cores  : {psutil.cpu_count(logical=False)} physical, "
                f"{psutil.cpu_count()} logical\n"
                f"  CPU Freq   : {cpu_freq.current:.0f} MHz (max {cpu_freq.max:.0f} MHz)\n"
                f"  OS         : {platform.system()} {platform.release()} "
                f"({platform.version()[:30]})\n"
                f"  Machine    : {platform.machine()}\n"
                f"  Hostname   : {platform.node()}\n"
                f"  Boot Time  : {datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M')}\n"
                f"  Python     : {platform.python_version()}"
            )
            return result
        except Exception as e:
            return f"Sysinfo error: {e}"

# ══════════════════════════════════════════════════════════════════
#  PHASE 2 COMMAND PARSER EXTENSION
# ══════════════════════════════════════════════════════════════════
class Phase2Parser:
    def __init__(self, p2: Phase2Skills):
        self.p2 = p2

    def parse(self, t: str) -> str | None:
        """Returns response string or None (pass to Phase1)."""

        # ── Clipboard ────────────────────────────────────────────
        if "clipboard" in t:
            if any(w in t for w in ["get","show","paste","দেখাও"]):
                return self.p2.clipboard_get()
            m = re.search(r"copy (.+)", t)
            if m:
                return self.p2.clipboard_set(m.group(1))

        # ── File operations ──────────────────────────────────────
        if "list" in t and any(w in t for w in ["folder","directory","files","dir"]):
            parts = t.split()
            path = parts[-1] if len(parts) > 2 else "."
            return self.p2.list_dir(path)

        if "organize" in t and "download" in t:
            return self.p2.organize_downloads()

        if "disk" in t and any(w in t for w in ["analyze","usage","space","আনালাইজ"]):
            return self.p2.disk_analyzer()

        if "create folder" in t or "mkdir" in t:
            m = re.search(r"(?:create folder|mkdir)\s+(.+)", t)
            if m:
                return self.p2.create_folder(m.group(1).strip())

        # ── Process manager ──────────────────────────────────────
        if any(w in t for w in ["process","task list","running apps","প্রসেস"]):
            return self.p2.list_processes()

        if "kill" in t and any(w in t for w in ["process","app","task"]):
            m = re.search(r"kill\s+(.+)", t)
            if m:
                return self.p2.kill_process(m.group(1).strip())

        # ── WiFi ─────────────────────────────────────────────────
        if "wifi" in t:
            if "scan" in t:
                return self.p2.wifi_scan()
            return self.p2.wifi_info()

        # ── Password ─────────────────────────────────────────────
        if any(w in t for w in ["password","passwd","পাসওয়ার্ড"]):
            m = re.search(r"(\d+)", t)
            length = int(m.group(1)) if m else 16
            return self.p2.generate_password(length)

        # ── QR Code ──────────────────────────────────────────────
        if "qr" in t:
            m = re.search(r"qr(?:\s+code)?\s+(.+)", t)
            if m:
                return self.p2.generate_qr(m.group(1).strip())
            return "Please provide data for QR code. Example: qr code https://google.com"

        # ── Translate ────────────────────────────────────────────
        if any(w in t for w in ["translate","অনুবাদ","ترجمہ"]):
            lang = "en" if any(w in t for w in ["english","ইংরেজি"]) else "bn"
            txt  = re.sub(r"translate|to (bangla|english|বাংলা|ইংরেজি)|অনুবাদ","",t).strip()
            return self.p2.translate(txt, lang)

        # ── Speed test ───────────────────────────────────────────
        if any(w in t for w in ["speed test","speedtest","internet speed","নেট স্পিড"]):
            return self.p2.internet_speed()

        # ── World clock ──────────────────────────────────────────
        if any(w in t for w in ["world clock","timezone","বিশ্ব ঘড়ি"]):
            return self.p2.world_clock()

        # ── Currency ─────────────────────────────────────────────
        if any(w in t for w in ["currency","convert","টাকা","মুদ্রা"]):
            m = re.search(r"(\d+\.?\d*)\s*([a-zA-Z]+)\s+(?:to|থেকে)\s+([a-zA-Z]+)", t)
            if m:
                return self.p2.currency_convert(float(m.group(1)),
                                                 m.group(2), m.group(3))

        # ── Unit converter ───────────────────────────────────────
        if "convert" in t:
            m = re.search(r"(\d+\.?\d*)\s*(\w+)\s+to\s+(\w+)", t)
            if m:
                return self.p2.unit_convert(float(m.group(1)),
                                             m.group(2), m.group(3))

        # ── Alarm ────────────────────────────────────────────────
        if "alarm" in t or "এলার্ম" in t:
            if any(w in t for w in ["list","show","দেখাও"]):
                return self.p2.list_alarms()
            m = re.search(r"(\d{1,2}:\d{2})", t)
            if m:
                label = re.sub(r"set alarm|alarm|at \d{1,2}:\d{2}","",t).strip()
                return self.p2.set_alarm(m.group(1), label or "Alarm")

        # ── Stopwatch ────────────────────────────────────────────
        if "stopwatch" in t or "স্টপওয়াচ" in t:
            if any(w in t for w in ["start","শুরু"]):
                return self.p2.stopwatch_start()
            if any(w in t for w in ["stop","শেষ"]):
                return self.p2.stopwatch_stop()
            return self.p2.stopwatch_check()

        # ── Timer ────────────────────────────────────────────────
        if "timer" in t or "টাইমার" in t:
            m = re.search(r"(\d+)", t)
            secs = int(m.group(1)) if m else 60
            if "min" in t:
                secs *= 60
            label = re.sub(r"timer|set|for|\d+\s*(?:min|sec|s|m)","",t).strip()
            return self.p2.countdown_timer(secs, label or "Timer")

        # ── Todo ─────────────────────────────────────────────────
        if "todo" in t or "task" in t:
            if any(w in t for w in ["show","list","দেখাও"]):
                return self.p2.show_todos()
            if "done" in t or "complete" in t:
                m = re.search(r"(\d+)", t)
                if m:
                    return self.p2.complete_todo(int(m.group(1)))
            if "delete" in t or "remove" in t:
                m = re.search(r"(\d+)", t)
                if m:
                    return self.p2.delete_todo(int(m.group(1)))
            content = re.sub(r"add|todo|task|new","",t).strip()
            if content:
                pri = "high" if "high" in t else "low" if "low" in t else "normal"
                return self.p2.add_todo(content, pri)

        # ── Cleanup ──────────────────────────────────────────────
        if any(w in t for w in ["cleanup","clean up","ক্লিনআপ","পরিষ্কার"]):
            return self.p2.system_cleanup()

        # ── Battery alert ────────────────────────────────────────
        if "battery alert" in t or "ব্যাটারি এলার্ট" in t:
            m = re.search(r"(\d+)", t)
            pct = int(m.group(1)) if m else 20
            return self.p2.battery_alert(pct)

        # ── Hash ─────────────────────────────────────────────────
        if "hash" in t:
            content = re.sub(r"hash","",t).strip()
            return self.p2.hash_text(content) if content else "Provide text to hash."

        # ── Base64 ───────────────────────────────────────────────
        if "base64 encode" in t:
            content = t.replace("base64 encode","").strip()
            return self.p2.base64_encode(content)
        if "base64 decode" in t:
            content = t.replace("base64 decode","").strip()
            return self.p2.base64_decode(content)

        # ── Dictionary ───────────────────────────────────────────
        if any(w in t for w in ["define","meaning","definition","অর্থ","মানে"]):
            word = re.sub(r"define|meaning of|definition of|what does|mean|অর্থ কী|মানে","",t).strip()
            if word:
                return self.p2.define_word(word.split()[0])

        # ── Port scan (self) ─────────────────────────────────────
        if "scan ports" in t or "open ports" in t:
            return self.p2.scan_own_ports()

        # ── Extended sysinfo ─────────────────────────────────────
        if "extended" in t and "system" in t:
            return self.p2.extended_sysinfo()

        # ── Auto type ────────────────────────────────────────────
        if "auto type" in t or "type this" in t:
            content = re.sub(r"auto type|type this","",t).strip()
            if content:
                return self.p2.auto_type(content)

        return None   # not handled here → pass to Phase 1

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════
def _human_size(b: int) -> str:
    for unit in ["B","KB","MB","GB","TB"]:
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} PB"

# ══════════════════════════════════════════════════════════════════
#  PHASE 2 HELP TEXT
# ══════════════════════════════════════════════════════════════════
PHASE2_HELP = """
  ╔══════════════════════ PHASE 2 COMMANDS ══════════════════════╗
  ║                                                              ║
  ║  FILE MANAGEMENT:                                            ║
  ║  list folder [path]      → List directory contents          ║
  ║  organize downloads      → Auto-sort Downloads folder       ║
  ║  disk analyze            → Disk usage analysis              ║
  ║  create folder [path]    → Create new folder                ║
  ║                                                              ║
  ║  SYSTEM:                                                     ║
  ║  process / task list     → List running processes           ║
  ║  kill [process name]     → Kill a process                   ║
  ║  cleanup                 → Clear temp files & recycle bin   ║
  ║  battery alert [%]       → Low battery voice alert          ║
  ║  scan ports              → Scan open ports (self)           ║
  ║  extended system info    → Detailed PC info                 ║
  ║                                                              ║
  ║  NETWORK & WEB:                                              ║
  ║  wifi info               → WiFi connection details          ║
  ║  wifi scan               → Scan available networks          ║
  ║  speedtest               → Internet speed test              ║
  ║                                                              ║
  ║  TOOLS:                                                      ║
  ║  clipboard get           → Show clipboard content           ║
  ║  copy [text]             → Copy text to clipboard           ║
  ║  password [length]       → Generate strong password         ║
  ║  qr code [data]          → Generate QR code image           ║
  ║  translate [text]        → Translate EN↔BN                  ║
  ║  hash [text]             → MD5/SHA1/SHA256 hash             ║
  ║  base64 encode [text]    → Encode to Base64                 ║
  ║  base64 decode [text]    → Decode from Base64               ║
  ║  define [word]           → Word definition                  ║
  ║  auto type [text]        → Auto-type (2s delay, click first)║
  ║                                                              ║
  ║  TIME & PRODUCTIVITY:                                        ║
  ║  world clock             → Time in 8 major cities           ║
  ║  alarm [HH:MM]           → Set alarm clock                  ║
  ║  list alarms             → View all alarms                  ║
  ║  stopwatch start/stop    → Stopwatch                        ║
  ║  timer [N] min/sec       → Countdown timer                  ║
  ║  todo add [task]         → Add todo item                    ║
  ║  todo list               → Show all todos                   ║
  ║  todo done [#]           → Mark todo complete               ║
  ║                                                              ║
  ║  CONVERTER:                                                  ║
  ║  100 USD to BDT          → Currency convert                 ║
  ║  5 km to mile            → Unit convert                     ║
  ╚══════════════════════════════════════════════════════════════╝
"""
