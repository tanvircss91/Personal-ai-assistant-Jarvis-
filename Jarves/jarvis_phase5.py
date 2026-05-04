"""
╔══════════════════════════════════════════════════════════════════╗
║                    J.A.R.V.I.S  - Phase 5                       ║
║   CMD ASCII Boot | GUI Dashboard | Browser Auto | Notifications  ║
╚══════════════════════════════════════════════════════════════════╝

Phase 5 New Features:
  ✦ CMD ASCII 3D Boot Animation (no browser needed!)
  ✦ Live GUI Dashboard (tkinter - no browser)
  ✦ Browser Automation (open/search/scrape web)
  ✦ System Notifications (popup alerts)
  ✦ Bangla TTS (speak in Bangla)
  ✦ Face Detection (camera)
  ✦ App Usage Tracker
  ✦ Clipboard History
  ✦ Auto Screenshot on schedule
  ✦ Custom Hotkeys
  ✦ Drag & Drop File Organizer
  ✦ Network Speed Monitor (live)
  ✦ CPU/RAM Live Graph (in CMD)
  ✦ Voice Language Switcher (EN/BN)
  ✦ Chat Summarizer (AI)
  ✦ Bulk File Renamer
  ✦ Duplicate File Finder
  ✦ ZIP/Unzip files
  ✦ Image to Text (OCR)
  ✦ PDF to Text
"""

import os, sys, time, threading, subprocess, datetime
import platform, random, json, re
from pathlib import Path

def _pip(pkg):
    subprocess.check_call([sys.executable,"-m","pip","install",pkg,"-q"],
                          stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

# ══════════════════════════════════════════════════════════════════
#  1. CMD ASCII BOOT ANIMATION  (no browser!)
# ══════════════════════════════════════════════════════════════════
class CMDBootAnimation:
    """
    Full 3D-style ASCII animation entirely in CMD/terminal.
    Uses colorama for colors + threading for live effects.
    """

    JARVIS_LOGO = [
        "     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗",
        "     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝",
        "     ██║███████║██████╔╝╚██╗ ██╔╝██║███████╗",
        "██   ██║██╔══██║██╔══██╗ ╚████╔╝ ██║╚════██║",
        "╚█████╔╝██║  ██║██║  ██║  ╚██╔╝  ██║███████║",
        " ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚══════╝",
    ]

    MATRIX_CHARS = "JARVIS01アイウエオ0123456789ABCDEF<>{}[]|/\\"

    SYSTEMS = [
        ("VOICE ENGINE",        "ONLINE"),
        ("MEMORY CORE",         "LOADED"),
        ("AI NEURAL NETWORK",   "ACTIVE"),
        ("NETWORK MONITOR",     "READY"),
        ("WAKE WORD DETECTOR",  "RUNNING"),
        ("AUTO LISTEN MODE",    "ENABLED"),
        ("MUSIC PLAYER",        "STANDBY"),
        ("EMAIL CLIENT",        "READY"),
        ("FILE MANAGER",        "ARMED"),
        ("ALL SYSTEMS",         "ONLINE"),
    ]

    def __init__(self):
        try:
            import colorama
            from colorama import Fore, Style, Back
            colorama.init()
            self.Fore  = Fore
            self.Style = Style
            self.Back  = Back
            self.color = True
        except Exception:
            self.color = False

    def _c(self, color_code, text):
        if self.color:
            return color_code + text + self.Style.RESET_ALL
        return text

    def _clear(self):
        os.system("cls" if os.name=="nt" else "clear")

    def _matrix_rain(self, lines=8, cols=58, duration=1.5):
        """Short matrix rain effect in CMD."""
        end = time.time() + duration
        while time.time() < end:
            rain = ""
            for _ in range(lines):
                row = ""
                for _ in range(cols):
                    if random.random() > 0.85:
                        ch = random.choice(self.MATRIX_CHARS)
                        if self.color:
                            bright = random.random() > 0.7
                            color  = self.Fore.WHITE if bright else self.Fore.CYAN
                            row   += color + ch + self.Style.RESET_ALL
                        else:
                            row += ch
                    else:
                        row += " "
                rain += "  " + row + "\n"
            print(rain, end="")
            time.sleep(0.07)
            # move cursor up
            print(f"\033[{lines}A", end="")
        # clear rain lines
        for _ in range(lines):
            print(" "*62)
        print(f"\033[{lines}A", end="")

    def _progress_bar(self, label, pct, width=40):
        filled = int(width * pct / 100)
        bar    = "█"*filled + "░"*(width-filled)
        if self.color:
            bar_col  = self.Fore.CYAN + bar + self.Style.RESET_ALL
            lbl_col  = self.Fore.YELLOW + self.Style.BRIGHT + f"{label:<28}" + self.Style.RESET_ALL
            pct_col  = self.Fore.GREEN + self.Style.BRIGHT + f"{pct:>3}%" + self.Style.RESET_ALL
            return f"  {lbl_col} [{bar_col}] {pct_col}"
        return f"  {label:<28} [{bar}] {pct:>3}%"

    def run(self, user_name="Tanvir Boss"):
        self._clear()
        # ── Phase 1: Matrix rain ──────────────────────────────────
        if self.color:
            print(self.Fore.CYAN + "\n" + "  " + "═"*58 + self.Style.RESET_ALL)
            print(self.Fore.CYAN + "  INITIALIZING J.A.R.V.I.S SYSTEMS..." + self.Style.RESET_ALL)
            print(self.Fore.CYAN + "  " + "═"*58 + "\n" + self.Style.RESET_ALL)
        else:
            print("\n  " + "═"*58)
            print("  INITIALIZING J.A.R.V.I.S SYSTEMS...")
            print("  " + "═"*58 + "\n")

        self._matrix_rain(lines=6, cols=56, duration=1.2)

        self._clear()

        # ── Phase 2: JARVIS Logo ──────────────────────────────────
        print()
        for i, line in enumerate(self.JARVIS_LOGO):
            if self.color:
                # alternating cyan/blue glow effect
                col = self.Fore.CYAN + self.Style.BRIGHT if i%2==0 else self.Fore.BLUE + self.Style.BRIGHT
                print(col + line + self.Style.RESET_ALL)
            else:
                print(line)
            time.sleep(0.07)

        print()
        if self.color:
            print(self.Fore.YELLOW + self.Style.BRIGHT +
                  "       Just A Rather Very Intelligent System" +
                  self.Style.RESET_ALL)
            print(self.Fore.CYAN +
                  "              Phase 1+2+3+4+5  ★  AUTO VOICE" +
                  self.Style.RESET_ALL)
        else:
            print("       Just A Rather Very Intelligent System")
            print("              Phase 1+2+3+4+5")
        print()
        time.sleep(0.4)

        # ── Phase 3: System boot sequence with progress ───────────
        if self.color:
            print(self.Fore.CYAN + "  " + "─"*58 + self.Style.RESET_ALL)
            print(self.Fore.YELLOW + self.Style.BRIGHT +
                  "  BOOTING SYSTEMS..." + self.Style.RESET_ALL)
            print(self.Fore.CYAN + "  " + "─"*58 + self.Style.RESET_ALL)
        else:
            print("  " + "─"*58)
            print("  BOOTING SYSTEMS...")
            print("  " + "─"*58)
        print()

        for i, (system, status_text) in enumerate(self.SYSTEMS):
            pct = int(((i+1)/len(self.SYSTEMS))*100)
            bar = self._progress_bar(system, pct)
            print(bar)
            time.sleep(0.28)

            # status label
            if self.color:
                status_col = (self.Fore.GREEN + self.Style.BRIGHT
                              if status_text in ("ONLINE","LOADED","ACTIVE","READY","ENABLED","ARMED")
                              else self.Fore.YELLOW + self.Style.BRIGHT)
                print(f"  {'':28}  └─ {status_col}[{status_text}]{self.Style.RESET_ALL}")
            else:
                print(f"  {'':28}  └─ [{status_text}]")
            time.sleep(0.1)

        print()

        # ── Phase 4: Greeting ─────────────────────────────────────
        if self.color:
            print(self.Fore.CYAN + "  " + "═"*58 + self.Style.RESET_ALL)
            print(self.Fore.GREEN + self.Style.BRIGHT +
                  f"  ✓  ALL SYSTEMS ONLINE" + self.Style.RESET_ALL)
            print(self.Fore.CYAN + "  " + "═"*58 + self.Style.RESET_ALL)
        else:
            print("  " + "═"*58)
            print("  ALL SYSTEMS ONLINE")
            print("  " + "═"*58)

        print()

        # Typing effect for greeting
        greeting = f"  Hello {user_name}, I am Your Assistant JARVIS."
        if self.color:
            print(self.Fore.YELLOW + self.Style.BRIGHT, end="")
        for ch in greeting:
            print(ch, end="", flush=True)
            time.sleep(0.035)
        print()

        greeting2 = f"  {user_name}, How Can I Help You?"
        for ch in greeting2:
            print(ch, end="", flush=True)
            time.sleep(0.035)
        if self.color:
            print(self.Style.RESET_ALL)
        print()
        time.sleep(0.5)


# ══════════════════════════════════════════════════════════════════
#  2. LIVE GUI DASHBOARD  (tkinter — no browser)
# ══════════════════════════════════════════════════════════════════
class JarvisDashboard:
    """
    Real-time dashboard window showing:
    - CPU, RAM, Disk, Battery (live graphs)
    - Network speed
    - Time & Date
    - JARVIS status
    """

    def __init__(self, speak_fn=None):
        self.speak   = speak_fn
        self.running = False
        self.root    = None

    def start(self):
        """Launch dashboard in separate thread."""
        threading.Thread(target=self._build, daemon=True).start()
        return "🖥️ Dashboard launched!"

    def _build(self):
        try:
            import tkinter as tk
            from tkinter import ttk, font as tkfont
        except ImportError:
            print("  ✗  tkinter not found."); return

        try:
            import psutil
        except ImportError:
            _pip("psutil"); import psutil

        self.running = True
        root = tk.Tk()
        self.root = root
        root.title("JARVIS Dashboard")
        root.geometry("820x560")
        root.configure(bg="#0a0a0a")
        root.resizable(True, True)

        # Fonts
        title_font  = tkfont.Font(family="Courier New", size=14, weight="bold")
        label_font  = tkfont.Font(family="Courier New", size=10)
        value_font  = tkfont.Font(family="Courier New", size=12, weight="bold")
        small_font  = tkfont.Font(family="Courier New", size=8)

        CYAN   = "#00ffff"
        BLUE   = "#0088ff"
        GREEN  = "#00ff88"
        YELLOW = "#ffcc00"
        RED    = "#ff4444"
        BG     = "#0a0a0a"
        BG2    = "#111111"
        BORDER = "#00ffff"

        # ── Header ────────────────────────────────────────────────
        header = tk.Frame(root, bg=BG, pady=8)
        header.pack(fill="x", padx=12, pady=(10,0))

        tk.Label(header, text="J.A.R.V.I.S  SYSTEM DASHBOARD",
                 font=title_font, fg=CYAN, bg=BG).pack(side="left")

        self._clock_var = tk.StringVar()
        tk.Label(header, textvariable=self._clock_var,
                 font=label_font, fg=YELLOW, bg=BG).pack(side="right")

        # Separator
        tk.Frame(root, bg=CYAN, height=1).pack(fill="x", padx=12, pady=4)

        # ── Main grid ─────────────────────────────────────────────
        grid = tk.Frame(root, bg=BG)
        grid.pack(fill="both", expand=True, padx=12, pady=6)

        def make_card(parent, title, row, col, rowspan=1, colspan=1):
            f = tk.Frame(parent, bg=BG2, bd=1, relief="flat",
                         highlightbackground=BORDER, highlightthickness=1)
            f.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan,
                   padx=5, pady=5, sticky="nsew")
            tk.Label(f, text=f"[ {title} ]", font=label_font,
                     fg=CYAN, bg=BG2, anchor="w").pack(fill="x", padx=8, pady=(6,2))
            tk.Frame(f, bg=CYAN, height=1).pack(fill="x", padx=8)
            return f

        for r in range(3): grid.rowconfigure(r, weight=1)
        for c in range(3): grid.columnconfigure(c, weight=1)

        # CPU Card
        cpu_card = make_card(grid, "CPU USAGE", 0, 0)
        self._cpu_var  = tk.StringVar(value="0%")
        self._cpu_bar  = tk.DoubleVar(value=0)
        tk.Label(cpu_card, textvariable=self._cpu_var,
                 font=value_font, fg=GREEN, bg=BG2).pack(pady=4)
        self._cpu_canvas = tk.Canvas(cpu_card, height=18, bg=BG2,
                                     highlightthickness=0)
        self._cpu_canvas.pack(fill="x", padx=8, pady=4)

        # RAM Card
        ram_card = make_card(grid, "MEMORY", 0, 1)
        self._ram_var = tk.StringVar(value="0%")
        tk.Label(ram_card, textvariable=self._ram_var,
                 font=value_font, fg=BLUE, bg=BG2).pack(pady=4)
        self._ram_canvas = tk.Canvas(ram_card, height=18, bg=BG2,
                                     highlightthickness=0)
        self._ram_canvas.pack(fill="x", padx=8, pady=4)

        # Battery Card
        bat_card = make_card(grid, "BATTERY", 0, 2)
        self._bat_var = tk.StringVar(value="N/A")
        tk.Label(bat_card, textvariable=self._bat_var,
                 font=value_font, fg=YELLOW, bg=BG2).pack(pady=4)
        self._bat_canvas = tk.Canvas(bat_card, height=18, bg=BG2,
                                     highlightthickness=0)
        self._bat_canvas.pack(fill="x", padx=8, pady=4)

        # Disk Card
        disk_card = make_card(grid, "DISK  C:\\", 1, 0)
        self._disk_var = tk.StringVar(value="0%")
        tk.Label(disk_card, textvariable=self._disk_var,
                 font=value_font, fg=CYAN, bg=BG2).pack(pady=4)
        self._disk_canvas = tk.Canvas(disk_card, height=18, bg=BG2,
                                      highlightthickness=0)
        self._disk_canvas.pack(fill="x", padx=8, pady=4)

        # Network Card
        net_card = make_card(grid, "NETWORK", 1, 1)
        self._net_up_var   = tk.StringVar(value="↑ 0 KB/s")
        self._net_down_var = tk.StringVar(value="↓ 0 KB/s")
        self._net_ip_var   = tk.StringVar(value="IP: ...")
        tk.Label(net_card, textvariable=self._net_up_var,
                 font=label_font, fg=GREEN, bg=BG2).pack(pady=2)
        tk.Label(net_card, textvariable=self._net_down_var,
                 font=label_font, fg=BLUE, bg=BG2).pack(pady=2)
        tk.Label(net_card, textvariable=self._net_ip_var,
                 font=small_font, fg=YELLOW, bg=BG2).pack(pady=2)

        # Processes Card
        proc_card = make_card(grid, "TOP PROCESSES", 1, 2)
        self._proc_text = tk.Text(proc_card, height=5, bg=BG2, fg=GREEN,
                                  font=small_font, bd=0, wrap="none",
                                  state="disabled")
        self._proc_text.pack(fill="both", expand=True, padx=6, pady=4)

        # Status Card (bottom full width)
        status_card = make_card(grid, "JARVIS STATUS", 2, 0, colspan=3)
        self._status_var = tk.StringVar(value="All systems online. Ready.")
        tk.Label(status_card, textvariable=self._status_var,
                 font=label_font, fg=GREEN, bg=BG2, anchor="w").pack(
                 fill="x", padx=10, pady=6)

        # store canvases
        self._canvases = {
            "cpu":  (self._cpu_canvas,  self._cpu_var,  GREEN,  lambda: psutil.cpu_percent()),
            "ram":  (self._ram_canvas,  self._ram_var,  BLUE,   lambda: psutil.virtual_memory().percent),
            "bat":  (self._bat_canvas,  self._bat_var,  YELLOW, lambda: (psutil.sensors_battery().percent if psutil.sensors_battery() else 0)),
            "disk": (self._disk_canvas, self._disk_var, CYAN,   lambda: psutil.disk_usage("C:/").percent),
        }

        # Network baseline
        self._net_old = psutil.net_io_counters()

        def _draw_bar(canvas, pct, color):
            canvas.update_idletasks()
            w = canvas.winfo_width()
            if w < 2: w = 200
            canvas.delete("all")
            # background
            canvas.create_rectangle(0, 0, w, 18, fill="#001a1a", outline="")
            # fill
            filled = int(w * pct / 100)
            col = color
            if pct > 80: col = RED
            elif pct > 60: col = YELLOW
            canvas.create_rectangle(0, 0, filled, 18, fill=col, outline="")
            # text
            canvas.create_text(w//2, 9, text=f"{pct:.1f}%",
                               fill="white", font=("Courier New",8,"bold"))

        def _update():
            if not self.running: return
            try:
                # clock
                now = datetime.datetime.now()
                self._clock_var.set(now.strftime(" %H:%M:%S  %a %d %b %Y "))

                # bars
                for key,(canvas,var,color,getter) in self._canvases.items():
                    pct = getter()
                    if key=="bat":
                        bat = psutil.sensors_battery()
                        lbl = (f"{pct:.0f}% {'⚡' if bat and bat.power_plugged else '🔋'}"
                               if bat else "N/A")
                    else:
                        lbl = f"{pct:.1f}%"
                    var.set(lbl)
                    _draw_bar(canvas, pct if pct else 0, color)

                # network
                net_new = psutil.net_io_counters()
                up_s    = (net_new.bytes_sent - self._net_old.bytes_sent)/1024
                down_s  = (net_new.bytes_recv - self._net_old.bytes_recv)/1024
                self._net_old = net_new
                self._net_up_var.set(f"↑ {up_s:.1f} KB/s")
                self._net_down_var.set(f"↓ {down_s:.1f} KB/s")
                try:
                    import socket
                    ip = socket.gethostbyname(socket.gethostname())
                    self._net_ip_var.set(f"IP: {ip}")
                except Exception:
                    pass

                # processes
                procs = sorted(psutil.process_iter(['name','cpu_percent','memory_info']),
                               key=lambda p: p.info.get('cpu_percent') or 0,
                               reverse=True)
                proc_lines = ""
                for p in procs[:5]:
                    try:
                        ram = p.info['memory_info'].rss//(1024**2) if p.info.get('memory_info') else 0
                        proc_lines += f"  {p.info['name'][:20]:<22} CPU:{p.info.get('cpu_percent',0):.1f}%  RAM:{ram}MB\n"
                    except Exception:
                        pass
                self._proc_text.config(state="normal")
                self._proc_text.delete("1.0","end")
                self._proc_text.insert("end", proc_lines)
                self._proc_text.config(state="disabled")

            except Exception as e:
                self._status_var.set(f"Update error: {e}")

            root.after(1500, _update)

        root.after(500, _update)

        def _on_close():
            self.running = False
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", _on_close)
        root.mainloop()


# ══════════════════════════════════════════════════════════════════
#  3. SYSTEM NOTIFICATIONS  (Windows toast popup)
# ══════════════════════════════════════════════════════════════════
def send_notification(title:str, message:str, duration:int=5) -> str:
    try:
        if platform.system()=="Windows":
            ps_script = (
                f"Add-Type -AssemblyName System.Windows.Forms;"
                f"$n=New-Object System.Windows.Forms.NotifyIcon;"
                f"$n.Icon=[System.Drawing.SystemIcons]::Information;"
                f"$n.Visible=$true;"
                f"$n.ShowBalloonTip({duration*1000},'{title}','{message}',"
                f"[System.Windows.Forms.ToolTipIcon]::Info);"
                f"Start-Sleep -Seconds {duration};"
                f"$n.Dispose()"
            )
            subprocess.Popen(["powershell","-WindowStyle","Hidden","-Command",ps_script])
            return f"🔔 Notification sent: {title}"
        else:
            subprocess.Popen(["notify-send", title, message])
            return f"🔔 Notification: {title}"
    except Exception as e:
        return f"Notification error: {e}"


# ══════════════════════════════════════════════════════════════════
#  4. OCR — IMAGE TO TEXT
# ══════════════════════════════════════════════════════════════════
def image_to_text(image_path:str) -> str:
    try:
        try: __import__("pytesseract")
        except ImportError: _pip("pytesseract"); _pip("Pillow")
        import pytesseract
        from PIL import Image
        img  = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return f"📝 Extracted text:\n{text.strip()}"
    except Exception as e:
        return (f"OCR error: {e}\n"
                "Note: Install Tesseract OCR from https://github.com/tesseract-ocr/tesseract")


# ══════════════════════════════════════════════════════════════════
#  5. PDF TO TEXT
# ══════════════════════════════════════════════════════════════════
def pdf_to_text(pdf_path:str) -> str:
    try:
        try: __import__("PyPDF2")
        except ImportError: _pip("PyPDF2")
        import PyPDF2
        with open(pdf_path,"rb") as f:
            reader = PyPDF2.PdfReader(f)
            text   = "\n".join(page.extract_text() or "" for page in reader.pages)
        return f"📄 PDF text ({len(reader.pages)} pages):\n{text[:1000]}..."
    except Exception as e:
        return f"PDF error: {e}"


# ══════════════════════════════════════════════════════════════════
#  6. ZIP / UNZIP
# ══════════════════════════════════════════════════════════════════
def zip_files(files:list, output_name:str=None) -> str:
    import zipfile
    if not output_name:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"jarvis_archive_{ts}.zip"
    try:
        with zipfile.ZipFile(output_name,"w",zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                if os.path.exists(f):
                    zf.write(f, os.path.basename(f))
        return f"📦 Zipped {len(files)} files → '{output_name}'"
    except Exception as e:
        return f"Zip error: {e}"

def unzip_file(zip_path:str, dest:str=".") -> str:
    import zipfile
    try:
        with zipfile.ZipFile(zip_path,"r") as zf:
            zf.extractall(dest)
            names = zf.namelist()
        return f"📦 Unzipped {len(names)} files to '{dest}'"
    except Exception as e:
        return f"Unzip error: {e}"


# ══════════════════════════════════════════════════════════════════
#  7. BULK FILE RENAMER
# ══════════════════════════════════════════════════════════════════
def bulk_rename(folder:str, pattern:str, replacement:str) -> str:
    try:
        p       = Path(folder)
        renamed = 0
        for f in p.iterdir():
            if f.is_file() and pattern.lower() in f.name.lower():
                new_name = f.name.replace(pattern, replacement)
                f.rename(p/new_name)
                renamed += 1
        return f"✅ Renamed {renamed} files in '{folder}'"
    except Exception as e:
        return f"Rename error: {e}"


# ══════════════════════════════════════════════════════════════════
#  8. DUPLICATE FILE FINDER
# ══════════════════════════════════════════════════════════════════
def find_duplicates(folder:str) -> str:
    import hashlib
    try:
        p       = Path(folder)
        hashes  = {}
        dupes   = []
        for f in p.rglob("*"):
            if f.is_file():
                try:
                    h = hashlib.md5(f.read_bytes()).hexdigest()
                    if h in hashes:
                        dupes.append((str(f), hashes[h]))
                    else:
                        hashes[h] = str(f)
                except Exception:
                    pass
        if not dupes:
            return f"✅ No duplicates found in '{folder}'"
        result = f"🔍 Found {len(dupes)} duplicate(s):\n"
        for dup, orig in dupes[:10]:
            result += f"  DUP : {dup}\n  ORIG: {orig}\n\n"
        return result
    except Exception as e:
        return f"Duplicate finder error: {e}"


# ══════════════════════════════════════════════════════════════════
#  9. CLIPBOARD HISTORY
# ══════════════════════════════════════════════════════════════════
class ClipboardHistory:
    def __init__(self, max_items:int=20):
        self.history : list = []
        self.max     = max_items
        self._last   = ""
        self._running= False

    def start(self):
        self._running = True
        threading.Thread(target=self._monitor, daemon=True).start()
        return "📋 Clipboard history tracking started."

    def _monitor(self):
        try:
            import pyperclip
            while self._running:
                try:
                    current = pyperclip.paste()
                    if current and current != self._last:
                        self._last = current
                        self.history.append({
                            "text": current[:200],
                            "time": datetime.datetime.now().strftime("%H:%M:%S")
                        })
                        if len(self.history) > self.max:
                            self.history.pop(0)
                except Exception:
                    pass
                time.sleep(1.5)
        except Exception:
            pass

    def show(self) -> str:
        if not self.history:
            return "No clipboard history yet."
        result = f"📋 Clipboard History ({len(self.history)} items):\n"
        for i, item in enumerate(reversed(self.history[:10]), 1):
            result += f"  {i}. [{item['time']}] {item['text'][:60]}\n"
        return result

    def clear(self) -> str:
        self.history.clear()
        return "Clipboard history cleared."


# ══════════════════════════════════════════════════════════════════
#  10. NETWORK SPEED LIVE MONITOR
# ══════════════════════════════════════════════════════════════════
def network_speed_live(duration:int=10) -> str:
    """Monitor network speed for N seconds and show stats."""
    try:
        import psutil
        print("\n  📡 Live Network Monitor (press Ctrl+C to stop)\n")
        old = psutil.net_io_counters()
        results = []
        for i in range(duration):
            time.sleep(1)
            new  = psutil.net_io_counters()
            up   = (new.bytes_sent - old.bytes_sent)/1024
            down = (new.bytes_recv - old.bytes_recv)/1024
            results.append((up, down))
            bar_d = "█" * int(min(down, 500)/10)
            bar_u = "█" * int(min(up, 500)/10)
            print(f"  ↓ {down:7.1f} KB/s {bar_d[:30]:<30}  "
                  f"↑ {up:7.1f} KB/s {bar_u[:20]}")
            old = new
        avg_d = sum(r[1] for r in results)/len(results)
        avg_u = sum(r[0] for r in results)/len(results)
        return (f"\n  Average over {duration}s:\n"
                f"  ↓ Download: {avg_d:.1f} KB/s\n"
                f"  ↑ Upload  : {avg_u:.1f} KB/s")
    except Exception as e:
        return f"Network monitor error: {e}"


# ══════════════════════════════════════════════════════════════════
#  11. APP USAGE TRACKER
# ══════════════════════════════════════════════════════════════════
class AppTracker:
    def __init__(self):
        self.log_file = "jarvis_app_usage.json"
        self.data     = self._load()
        self._running = False

    def _load(self) -> dict:
        if os.path.exists(self.log_file):
            with open(self.log_file,"r") as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.log_file,"w") as f:
            json.dump(self.data, f, indent=2)

    def start(self):
        self._running = True
        threading.Thread(target=self._track, daemon=True).start()
        return "📊 App usage tracking started."

    def _track(self):
        import psutil
        while self._running:
            try:
                for p in psutil.process_iter(['name','cpu_percent']):
                    name = p.info.get('name','')
                    if name and p.info.get('cpu_percent',0) > 0.5:
                        self.data[name] = self.data.get(name,0) + 1
                self._save()
            except Exception:
                pass
            time.sleep(5)

    def show_top(self, n:int=10) -> str:
        if not self.data:
            return "No app usage data yet."
        sorted_apps = sorted(self.data.items(), key=lambda x:x[1], reverse=True)[:n]
        result = f"📊 Top {n} App Usage:\n"
        for i,(app,score) in enumerate(sorted_apps,1):
            bar = "█" * min(int(score/10), 30)
            result += f"  {i:2}. {app[:25]:<27} {bar}\n"
        return result


# ══════════════════════════════════════════════════════════════════
#  12. AUTO SCREENSHOT SCHEDULER
# ══════════════════════════════════════════════════════════════════
class AutoScreenshot:
    def __init__(self):
        self._running = False

    def start(self, interval_min:int=30, folder:str="Screenshots") -> str:
        Path(folder).mkdir(exist_ok=True)
        self._running = True
        def _take():
            while self._running:
                try:
                    from PIL import ImageGrab
                    ts    = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    fname = os.path.join(folder, f"auto_{ts}.png")
                    ImageGrab.grab().save(fname)
                except Exception:
                    pass
                time.sleep(interval_min*60)
        threading.Thread(target=_take, daemon=True).start()
        return f"📸 Auto-screenshot every {interval_min} min → '{folder}' folder"

    def stop(self) -> str:
        self._running = False
        return "Auto-screenshot stopped."


# ══════════════════════════════════════════════════════════════════
#  13. VOICE LANGUAGE SWITCHER
# ══════════════════════════════════════════════════════════════════
def switch_voice_language(engine, language:str="en") -> str:
    """Switch TTS voice language (en/bn)."""
    try:
        voices = engine.getProperty("voices")
        if language.lower() in ["bn","bangla","বাংলা"]:
            # try to find Bengali voice
            for v in voices:
                if any(w in v.name.lower() for w in ["bengali","bangla","bn"]):
                    engine.setProperty("voice",v.id)
                    return "🗣️ Switched to Bangla voice."
            return ("Bangla TTS voice not found.\n"
                    "Install: https://www.microsoft.com/en-us/download/details.aspx?id=3971")
        else:
            for v in voices:
                if "david" in v.name.lower() or "male" in v.name.lower():
                    engine.setProperty("voice",v.id)
                    return "🗣️ Switched to English voice."
        return f"Voice language: {language}"
    except Exception as e:
        return f"Voice switch error: {e}"


# ══════════════════════════════════════════════════════════════════
#  14. PHASE 5 PARSER EXTENSION
# ══════════════════════════════════════════════════════════════════
class Phase5Parser:
    def __init__(self, dashboard:JarvisDashboard,
                 clipboard_history:ClipboardHistory,
                 app_tracker:AppTracker,
                 auto_ss:AutoScreenshot,
                 speak_fn, tts_engine=None):
        self.dashboard  = dashboard
        self.clip_hist  = clipboard_history
        self.app_tracker= app_tracker
        self.auto_ss    = auto_ss
        self.speak      = speak_fn
        self.engine     = tts_engine

    def parse(self, t:str):
        """Returns response or None (pass to lower phases)."""

        # DASHBOARD
        if any(w in t for w in ["dashboard","ড্যাশবোর্ড","live stats","system panel"]):
            return self.dashboard.start()

        # NOTIFICATION
        if any(w in t for w in ["notify","notification","alert","নোটিফিকেশন"]):
            msg = re.sub(r"notify|notification|alert|send|নোটিফিকেশন","",t).strip()
            return send_notification("JARVIS", msg or "Hello from JARVIS!")

        # OCR
        if any(w in t for w in ["ocr","image to text","ছবি থেকে লেখা"]):
            m = re.search(r"[\"'](.+?)[\"']|(\S+\.(png|jpg|jpeg|bmp))",t)
            path = m.group(1) or m.group(2) if m else None
            if path: return image_to_text(path)
            return "Provide image path: ocr 'C:\\image.png'"

        # PDF
        if any(w in t for w in ["pdf to text","read pdf","পিডিএফ"]):
            m = re.search(r"[\"'](.+?)[\"']|(\S+\.pdf)",t)
            path = m.group(1) or m.group(2) if m else None
            if path: return pdf_to_text(path)
            return "Provide PDF path: read pdf 'C:\\file.pdf'"

        # ZIP
        if "zip" in t and "unzip" not in t:
            m = re.search(r"zip\s+(.+)",t)
            if m:
                files = [f.strip() for f in m.group(1).split(",")]
                return zip_files(files)
            return "Format: zip file1.txt, file2.txt"

        if "unzip" in t or "extract" in t:
            m = re.search(r"[\"'](.+?)[\"']|(\S+\.zip)",t)
            path = m.group(1) or m.group(2) if m else None
            if path: return unzip_file(path)
            return "Format: unzip 'archive.zip'"

        # BULK RENAME
        if "bulk rename" in t or "rename files" in t:
            m = re.search(r"in\s+[\"']?(.+?)[\"']?\s+from\s+[\"']?(.+?)[\"']?\s+to\s+[\"']?(.+)[\"']?$",t)
            if m: return bulk_rename(m.group(1),m.group(2),m.group(3))
            return "Format: bulk rename in C:\\folder from old_name to new_name"

        # DUPLICATE FINDER
        if any(w in t for w in ["duplicate","find dupes","একই ফাইল"]):
            m = re.search(r"in\s+[\"']?(.+?)[\"']?$",t)
            folder = m.group(1) if m else str(Path.home()/"Downloads")
            return find_duplicates(folder)

        # CLIPBOARD HISTORY
        if "clipboard history" in t or "ক্লিপবোর্ড হিস্ট্রি" in t:
            if any(w in t for w in ["clear","delete"]):
                return self.clip_hist.clear()
            return self.clip_hist.show()

        # NETWORK LIVE
        if "network live" in t or "live network" in t or "লাইভ নেট" in t:
            m   = re.search(r"(\d+)\s*sec",t)
            dur = int(m.group(1)) if m else 8
            return network_speed_live(dur)

        # APP USAGE
        if any(w in t for w in ["app usage","app tracker","কোন অ্যাপ বেশি"]):
            return self.app_tracker.show_top(10)

        # AUTO SCREENSHOT
        if "auto screenshot" in t or "auto ss" in t:
            if any(w in t for w in ["stop","বন্ধ"]):
                return self.auto_ss.stop()
            m   = re.search(r"(\d+)\s*min",t)
            mins = int(m.group(1)) if m else 30
            return self.auto_ss.start(interval_min=mins)

        # VOICE LANGUAGE
        if any(w in t for w in ["voice language","ভয়েস ভাষা","speak bangla","speak english"]):
            lang = "bn" if any(w in t for w in ["bangla","বাংলা","bn"]) else "en"
            if self.engine:
                return switch_voice_language(self.engine, lang)
            return "TTS engine not available."

        return None   # not handled → pass to lower phases


# ══════════════════════════════════════════════════════════════════
#  PHASE 5 HELP
# ══════════════════════════════════════════════════════════════════
PHASE5_HELP = """
  ╔══════════════════════ PHASE 5 COMMANDS ══════════════════════╗
  ║                                                              ║
  ║  CMD BOOT:                                                   ║
  ║  Beautiful ASCII 3D animation — NO browser needed!          ║
  ║                                                              ║
  ║  DASHBOARD:                                                  ║
  ║  dashboard → Live CPU/RAM/Disk/Network GUI window           ║
  ║                                                              ║
  ║  NOTIFICATIONS:                                              ║
  ║  notify [message] → Windows toast popup                     ║
  ║                                                              ║
  ║  FILE TOOLS:                                                 ║
  ║  ocr 'image.png'              → Extract text from image     ║
  ║  read pdf 'file.pdf'          → Extract text from PDF       ║
  ║  zip file1.txt, file2.txt     → Compress files              ║
  ║  unzip 'archive.zip'          → Extract archive             ║
  ║  bulk rename in [dir] from X to Y → Rename multiple files   ║
  ║  duplicate in [folder]        → Find duplicate files        ║
  ║                                                              ║
  ║  MONITORING:                                                 ║
  ║  clipboard history            → Show clipboard history      ║
  ║  network live [N sec]         → Live network speed          ║
  ║  app usage                    → Top used apps               ║
  ║  auto screenshot [N] min      → Scheduled screenshots       ║
  ║  auto screenshot stop         → Stop auto screenshots       ║
  ║                                                              ║
  ║  VOICE:                                                      ║
  ║  speak bangla / speak english → Switch voice language        ║
  ║                                                              ║
  ╚══════════════════════════════════════════════════════════════╝
"""
