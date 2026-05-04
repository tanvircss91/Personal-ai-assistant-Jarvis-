"""
╔══════════════════════════════════════════════════════════════════╗
║           J.A.R.V.I.S  — Phase 1+2+3+4+5  COMPLETE             ║
║  Auto Voice | Always Speaks | CMD Boot | GUI Dashboard           ║
╚══════════════════════════════════════════════════════════════════╝
"""
import os,sys,time,json,random,platform,datetime,threading,subprocess,webbrowser,re,socket
import smtplib,imaplib,email as email_lib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ── core install ──────────────────────────────────────────────────
CORE={"requests":"requests","pyttsx3":"pyttsx3","speech_recognition":"SpeechRecognition","psutil":"psutil","colorama":"colorama"}
def _pip(p): subprocess.check_call([sys.executable,"-m","pip","install",p,"-q"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def install_core():
    import importlib
    for mod,pkg in CORE.items():
        try: importlib.import_module(mod)
        except ImportError: print(f"  Installing {pkg}..."); _pip(pkg)
print("\n  Checking dependencies..."); install_core()
import requests,pyttsx3,speech_recognition as sr,psutil,colorama
from colorama import Fore,Style; colorama.init(autoreset=True)

# ── config ────────────────────────────────────────────────────────
CONFIG={"name":"JARVIS","user_name":"Tanvir Boss","voice_enabled":True,
        "voice_rate":168,"voice_volume":1.0,"ollama_model":"llama3.2",
        "ollama_url":"http://localhost:11434","memory_file":"jarvis_memory.json",
        "max_memory":30,"city":"Dhaka","auto_listen":True}

C={"gold":Fore.YELLOW+Style.BRIGHT,"cyan":Fore.CYAN+Style.BRIGHT,
   "green":Fore.GREEN+Style.BRIGHT,"red":Fore.RED+Style.BRIGHT,
   "white":Fore.WHITE+Style.BRIGHT,"dim":Fore.WHITE+Style.DIM,
   "magenta":Fore.MAGENTA+Style.BRIGHT,"reset":Style.RESET_ALL}

def line():     print(C["cyan"]+"  "+"─"*58+C["reset"])
def success(m): print(C["green"]+f"  ✓  {m}"+C["reset"])
def error(m):   print(C["red"]+f"  ✗  {m}"+C["reset"])
def status(m):  print(C["dim"]+f"  ⟳  {m}"+C["reset"])

def typing_effect(text,delay=0.013):
    ts=datetime.datetime.now().strftime("%H:%M:%S")
    print(C["cyan"]+f"\n  [{ts}] JARVIS » "+C["reset"],end="",flush=True)
    for ch in text: print(C["white"]+ch+C["reset"],end="",flush=True); time.sleep(delay)
    print()

def user_print(text):
    ts=datetime.datetime.now().strftime("%H:%M:%S")
    print(C["green"]+f"\n  [{ts}] {CONFIG['user_name']} » "+C["white"]+text+C["reset"])

# ══════════════════════════════════════════════════════════════════
#  VOICE ENGINE
# ══════════════════════════════════════════════════════════════════
class VoiceEngine:
    def __init__(self):
        self.engine=None;self.mic=None
        self.recognizer=sr.Recognizer()
        self._tts_lock=threading.Lock();self._busy=False
        self._init_tts();self._init_mic()

    def _init_tts(self):
        try:
            self.engine=pyttsx3.init()
            self.engine.setProperty("rate",CONFIG["voice_rate"])
            self.engine.setProperty("volume",CONFIG["voice_volume"])
            for v in self.engine.getProperty("voices"):
                if "male" in v.name.lower() or "david" in v.name.lower():
                    self.engine.setProperty("voice",v.id); break
            success("TTS ready.")
        except Exception as e: error(f"TTS:{e}"); self.engine=None

    def _init_mic(self):
        try: self.mic=sr.Microphone(); success("Microphone ready.")
        except Exception: error("No microphone."); self.mic=None

    def speak(self,text:str):
        typing_effect(text)
        if not self.engine: return
        with self._tts_lock:
            try: self.engine.say(text); self.engine.runAndWait()
            except Exception: pass

    def listen_once(self,timeout=7):
        if not self.mic: return None
        print(C["magenta"]+"  🎙  Listening..."+C["reset"])
        self._busy=True
        try:
            with self.mic as s:
                self.recognizer.adjust_for_ambient_noise(s,duration=0.4)
                audio=self.recognizer.listen(s,timeout=timeout,phrase_time_limit=15)
            t=self.recognizer.recognize_google(audio,language="en-US")
            user_print(f"(Voice) {t}"); self._busy=False; return t.lower()
        except sr.WaitTimeoutError: self._busy=False; return None
        except sr.UnknownValueError: self._busy=False; return None
        except Exception as e: self._busy=False; error(f"Listen:{e}"); return None

    def start_auto_listen(self,on_heard):
        if not self.mic: error("Auto-listen disabled."); return
        def _loop():
            r=sr.Recognizer(); r.energy_threshold=280; r.dynamic_energy_threshold=True; r.pause_threshold=0.75
            with self.mic as s: r.adjust_for_ambient_noise(s,duration=1.5)
            success("Auto-listen ON — just speak anytime!")
            while CONFIG["auto_listen"]:
                if self._busy: time.sleep(0.3); continue
                try:
                    with self.mic as s: audio=r.listen(s,timeout=4,phrase_time_limit=15)
                    text=r.recognize_google(audio,language="en-US").strip()
                    if len(text.split())>=1: self._busy=True; on_heard(text.lower()); time.sleep(0.5); self._busy=False
                except Exception: pass
        threading.Thread(target=_loop,daemon=True).start()

# ══════════════════════════════════════════════════════════════════
#  MEMORY
# ══════════════════════════════════════════════════════════════════
class Memory:
    def __init__(self):
        self.history=[];self.notes=[];self.reminders=[];self.load()
    def load(self):
        if os.path.exists(CONFIG["memory_file"]):
            try:
                with open(CONFIG["memory_file"],"r",encoding="utf-8") as f:
                    d=json.load(f);self.history=d.get("history",[]);self.notes=d.get("notes",[]);self.reminders=d.get("reminders",[])
                success("Memory loaded.")
            except Exception: pass
    def save(self):
        with open(CONFIG["memory_file"],"w",encoding="utf-8") as f:
            json.dump({"history":self.history[-CONFIG["max_memory"]:],"notes":self.notes,"reminders":self.reminders},f,ensure_ascii=False,indent=2)
    def add_turn(self,role,content):
        self.history.append({"role":role,"content":content,"time":datetime.datetime.now().isoformat()})
        if len(self.history)>CONFIG["max_memory"]: self.history=self.history[-CONFIG["max_memory"]:]
        self.save()
    def add_note(self,note):
        self.notes.append({"note":note,"time":datetime.datetime.now().isoformat()}); self.save()
    def add_reminder(self,reminder,remind_at):
        self.reminders.append({"reminder":reminder,"time":remind_at,"done":False}); self.save()
    def get_context(self):
        return [{"role":t["role"],"content":t["content"]} for t in self.history[-12:]]

# ══════════════════════════════════════════════════════════════════
#  AI CORE
# ══════════════════════════════════════════════════════════════════
class AICore:
    def __init__(self,memory):
        self.memory=memory; self.available=self._check()
    def _check(self):
        try:
            r=requests.get(f"{CONFIG['ollama_url']}/api/tags",timeout=3)
            if r.ok:
                models=[m["name"] for m in r.json().get("models",[])]
                if models: success(f"Ollama:{', '.join(models)}"); return True
                error("No models. Run: ollama pull llama3.2")
            return False
        except Exception: error("Ollama offline."); return False
    def ask(self,prompt):
        if not self.available: return self._fb(prompt)
        sys_msg=(f"You are JARVIS, Iron Man's AI — bilingual. User:{CONFIG['user_name']}. "
                 f"Now:{datetime.datetime.now().strftime('%A %d %B %Y %H:%M')}. "
                 f"Be concise, witty, helpful. Keep answers short for voice.")
        msgs=[{"role":"system","content":sys_msg}]+self.memory.get_context()+[{"role":"user","content":prompt}]
        try:
            r=requests.post(f"{CONFIG['ollama_url']}/api/chat",json={"model":CONFIG["ollama_model"],"messages":msgs,"stream":False},timeout=60)
            if r.ok: return r.json()["message"]["content"].strip()
        except Exception as e: error(f"AI:{e}")
        return self._fb(prompt)
    def _fb(self,p):
        p=p.lower()
        if any(w in p for w in ["hello","hi","হ্যালো"]): return f"All systems ready, {CONFIG['user_name']}! কী সাহায্য করতে পারি?"
        if any(w in p for w in ["thank","ধন্যবাদ"]): return f"Always a pleasure, {CONFIG['user_name']}!"
        return "Ollama install করুন: https://ollama.com → ollama pull llama3.2"

# ══════════════════════════════════════════════════════════════════
#  EMAIL
# ══════════════════════════════════════════════════════════════════
class EmailManager:
    CFG="jarvis_email.json"
    def __init__(self):
        self.cfg=json.load(open(self.CFG)) if os.path.exists(self.CFG) else {"configured":False}
    def setup(self,addr,pwd):
        self.cfg={"email":addr,"password":pwd,"configured":True}; json.dump(self.cfg,open(self.CFG,"w")); return "Email configured! ✅"
    def send(self,to,subject,body):
        if not self.cfg.get("configured"): return "email setup করুন আগে।"
        try:
            msg=MIMEMultipart();msg["From"]=self.cfg["email"];msg["To"]=to;msg["Subject"]=subject;msg.attach(MIMEText(body,"plain","utf-8"))
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as s: s.login(self.cfg["email"],self.cfg["password"]); s.send_message(msg)
            return f"Email sent to {to}! ✅"
        except Exception as e: return f"Email:{e}"
    def read_inbox(self,count=5):
        if not self.cfg.get("configured"): return "Email not configured."
        try:
            m=imaplib.IMAP4_SSL("imap.gmail.com"); m.login(self.cfg["email"],self.cfg["password"]); m.select("inbox")
            _,data=m.search(None,"ALL"); ids=data[0].split()[-count:]; result=f"Last {count} emails:\n"
            for i,eid in enumerate(reversed(ids),1):
                _,d=m.fetch(eid,"(RFC822)"); msg=email_lib.message_from_bytes(d[0][1])
                result+=f"  {i}. {msg.get('From','?')[:30]} | {msg.get('Subject','?')[:40]}\n"
            m.logout(); return result
        except Exception as e: return f"Email:{e}"

# ══════════════════════════════════════════════════════════════════
#  MUSIC PLAYER
# ══════════════════════════════════════════════════════════════════
class MusicPlayer:
    EXT=[".mp3",".wav",".ogg",".flac",".m4a"]
    def __init__(self):
        self.pg=None;self.playlist=[];self.current=0;self.playing=False;self.music_dir=str(Path.home()/"Music")
        try: import pygame; pygame.mixer.init(); self.pg=pygame; success("Music ready.")
        except Exception: _pip("pygame")
    def _scan(self):
        import glob; songs=[]
        for ext in self.EXT: songs+=glob.glob(os.path.join(self.music_dir,"**",f"*{ext}"),recursive=True)
        return songs
    def play(self,query=None):
        if not self.pg: return "pip install pygame"
        songs=self._scan()
        if not songs: return f"No music in {self.music_dir}"
        if query: m=[s for s in songs if query.lower() in Path(s).name.lower()]; songs=m if m else songs
        self.playlist=songs; random.shuffle(self.playlist); self.current=0
        self.pg.mixer.music.load(self.playlist[0]); self.pg.mixer.music.play(); self.playing=True
        return f"🎵 Playing:{Path(self.playlist[0]).name}"
    def next_song(self):
        if not self.playlist: return "No playlist."
        self.current=(self.current+1)%len(self.playlist); self.pg.mixer.music.load(self.playlist[self.current]); self.pg.mixer.music.play()
        return f"🎵 Next:{Path(self.playlist[self.current]).name}"
    def pause(self):
        if self.pg and self.playing: self.pg.mixer.music.pause(); self.playing=False; return "⏸ Paused."
        return "Nothing playing."
    def resume(self):
        if self.pg and not self.playing: self.pg.mixer.music.unpause(); self.playing=True; return "▶ Resumed."
        return "Already playing."
    def stop(self):
        if self.pg: self.pg.mixer.music.stop(); self.playing=False; return "⏹ Stopped."
        return "Nothing playing."
    def list_songs(self):
        songs=self._scan()
        if not songs: return f"No music in {self.music_dir}"
        out=f"🎵 Music ({len(songs)} songs):\n"
        for i,s in enumerate(songs[:12],1): out+=f"  {i}. {Path(s).name}\n"
        return out

QUOTES=["The only way to do great work is to love what you do. Steve Jobs","সফলতা হলো প্রতিদিন ছোট ছোট প্রচেষ্টার সমষ্টি।","Don't watch the clock; keep going. Sam Levenson","স্বপ্ন দেখো, কারণ স্বপ্ন থেকেই লক্ষ্য জন্ম নেয়।"]
FACTS=["Honey never spoils — 3000-year-old Egyptian honey is still edible!","Octopuses have three hearts and blue blood.","বাংলাদেশ বিশ্বের বৃহত্তম ব-দ্বীপে অবস্থিত।","Sharks are older than trees — 400 million years old!"]

# ══════════════════════════════════════════════════════════════════
#  MASTER PARSER  (Phase 1+2+3+4+5)
# ══════════════════════════════════════════════════════════════════
class MasterParser:
    def __init__(self,voice,memory,ai,email_m,music):
        self.voice=voice;self.memory=memory;self.ai=ai;self.email=email_m;self.music=music
        self.todos=[];self.alarms=[];self.sw_start=None;self.sw_running=False;self.pom_running=False
        self._load_todos();self._start_threads();self._install_extras()
        # Phase 5 components
        try:
            from jarvis_phase5 import JarvisDashboard,ClipboardHistory,AppTracker,AutoScreenshot,Phase5Parser,CMDBootAnimation
            self.dashboard   = JarvisDashboard(voice.speak)
            self.clip_hist   = ClipboardHistory()
            self.app_tracker = AppTracker()
            self.auto_ss     = AutoScreenshot()
            self.p5          = Phase5Parser(self.dashboard,self.clip_hist,self.app_tracker,self.auto_ss,voice.speak,voice.engine)
            self.boot_anim   = CMDBootAnimation()
            self.clip_hist.start()
            self.app_tracker.start()
            success("Phase 5 loaded.")
        except Exception as e:
            error(f"Phase 5: {e}"); self.p5=None; self.boot_anim=None
        # Phase 3 components
        try:
            from jarvis_phase3 import EmailManager as EM3,MusicPlayer as MP3,Phase3Parser,PomodoroTimer,TaskScheduler,WakeWordEngine,PHASE3_HELP
            self.pomodoro   = PomodoroTimer(voice.speak)
            self.scheduler  = TaskScheduler(voice.speak)
            self.p3         = Phase3Parser(email_m,music,self.pomodoro,self.scheduler,memory.history,voice.speak,voice)
            self.p3_help    = PHASE3_HELP
            success("Phase 3 loaded.")
        except Exception as e:
            error(f"Phase 3: {e}"); self.p3=None; self.p3_help=""
        # Phase 2
        try:
            from jarvis_phase2 import Phase2Skills,Phase2Parser,PHASE2_HELP
            self.p2skills = Phase2Skills(CONFIG,voice.speak)
            self.p2       = Phase2Parser(self.p2skills)
            self.p2_help  = PHASE2_HELP
            success("Phase 2 loaded.")
        except Exception as e:
            error(f"Phase 2: {e}"); self.p2=None; self.p2_help=""

    def _install_extras(self):
        for mod,pkg in {"pyperclip":"pyperclip","deep_translator":"deep-translator","qrcode":"qrcode[pil]","wikipedia":"wikipedia"}.items():
            try: __import__(mod)
            except ImportError:
                try: _pip(pkg)
                except Exception: pass

    def _load_todos(self):
        if os.path.exists("jarvis_todos.json"):
            with open("jarvis_todos.json","r",encoding="utf-8") as f: self.todos=json.load(f)

    def _save_todos(self):
        with open("jarvis_todos.json","w",encoding="utf-8") as f: json.dump(self.todos,f,ensure_ascii=False,indent=2)

    def _start_threads(self):
        def _alarm():
            while True:
                now=datetime.datetime.now()
                for a in self.alarms:
                    if not a["done"] and a["h"]==now.hour and a["m"]==now.minute:
                        self.voice.speak(f"Alarm! {a['label']}"); a["done"]=True
                time.sleep(30)
        def _remind():
            while True:
                now=datetime.datetime.now()
                for r in self.memory.reminders:
                    if not r["done"] and now>=datetime.datetime.fromisoformat(r["time"]):
                        self.voice.speak(f"Reminder:{r['reminder']}"); r["done"]=True; self.memory.save()
                time.sleep(30)
        threading.Thread(target=_alarm,daemon=True).start()
        threading.Thread(target=_remind,daemon=True).start()

    def parse(self,text:str)->str:
        t=text.lower().strip()

        if any(w in t for w in ["exit","quit","bye","shutdown","বিদায়"]): return "__EXIT__"
        if any(w in t for w in ["help","commands","সাহায্য"]): return HELP_ALL
        if "voice on" in t: CONFIG["voice_enabled"]=True; return "Voice enabled."
        if "voice off" in t: CONFIG["voice_enabled"]=False; return "Voice disabled."
        if "auto listen on" in t: CONFIG["auto_listen"]=True; return "Auto-listen ON."
        if "auto listen off" in t: CONFIG["auto_listen"]=False; return "Auto-listen OFF."

        # Phase 5 first
        if self.p5:
            r=self.p5.parse(t)
            if r is not None: return r

        # Phase 3
        if self.p3:
            r=self.p3.parse(t)
            if r is not None: return r

        # Phase 2
        if self.p2:
            r=self.p2.parse(t)
            if r is not None: return r

        # Phase 1 built-in
        if any(w in t for w in ["time","date","সময়","তারিখ","আজকে"]):
            n=datetime.datetime.now(); return f"🕐 {n.strftime('%I:%M %p')}  |  📅 {n.strftime('%A, %d %B %Y')}"
        if any(w in t for w in ["world clock","timezone"]):
            from datetime import timezone,timedelta
            cities={"Dhaka":6,"London":1,"New York":-4,"Dubai":4,"Tokyo":9,"Sydney":10}
            out="🌍 World Clock:\n"
            for c,off in cities.items():
                tz=timezone(timedelta(hours=off)); out+=f"  {c:<12}: {datetime.datetime.now(tz).strftime('%I:%M %p, %a %d %b')}\n"
            return out
        if any(w in t for w in ["system","cpu","ram","battery","সিস্টেম","ব্যাটারি"]):
            cpu=psutil.cpu_percent(interval=1);ram=psutil.virtual_memory();bat=psutil.sensors_battery()
            freq=psutil.cpu_freq(); bat_s=(f"{bat.percent:.0f}% {'Charging' if bat.power_plugged else 'Battery'}" if bat else "N/A")
            return f"CPU:{cpu}%  RAM:{ram.percent}%  Battery:{bat_s}  OS:{platform.system()} {platform.release()}"
        if any(w in t for w in ["weather","আবহাওয়া","forecast"]):
            city=CONFIG["city"]
            for w in t.split():
                if w not in ["weather","in","of","আবহাওয়া","forecast","what","is","the"]: city=w; break
            try: r=requests.get(f"https://wttr.in/{city}?format=3",timeout=8); return f"🌦 {r.text.strip()}" if r.ok else "Weather unavailable."
            except Exception: return "Weather offline."
        if any(w in t for w in ["news","headlines","খবর"]):
            try:
                import xml.etree.ElementTree as ET
                r=requests.get("https://feeds.bbci.co.uk/news/rss.xml",timeout=8)
                root=ET.fromstring(r.content); items=root.findall(".//item")[:5]
                return "📰 Headlines:\n"+"\n".join(f"  {i}. {it.find('title').text}" for i,it in enumerate(items,1))
            except Exception: return "News unavailable."
        if any(w in t for w in ["network","my ip","নেটওয়ার্ক"]):
            try: d=requests.get("https://ipinfo.io/json",timeout=5).json(); return f"🌐 IP:{d.get('ip')}  City:{d.get('city')}  ISP:{d.get('org')}"
            except Exception: return "Network unavailable."
        if "wifi" in t:
            flag="networks" if "scan" in t else "interfaces"
            r=subprocess.run(["netsh","wlan","show",flag],capture_output=True,text=True); return r.stdout[:800]
        if t.startswith("ping"):
            host=t.split()[1] if len(t.split())>1 else "google.com"
            try: r=subprocess.run(["ping","-n","4",host],capture_output=True,text=True,timeout=15); return "\n".join([l for l in r.stdout.splitlines() if l.strip()][-3:])
            except Exception as e: return f"Ping:{e}"
        if any(w in t for w in ["screenshot","স্ক্রিনশট"]):
            try:
                from PIL import ImageGrab; ts=datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); fname=f"screenshot_{ts}.png"; ImageGrab.grab().save(fname); return f"📸 Screenshot:{fname}"
            except Exception: _pip("Pillow"); return "Pillow installed. Try again."
        if any(w in t for w in ["open","visit","go to","খোলো","চালু"]):
            apps={"notepad":"notepad","calculator":"calc","paint":"mspaint","chrome":"chrome","firefox":"firefox","vscode":"code","explorer":"explorer","cmd":"cmd","task manager":"taskmgr"}
            for a,cmd in apps.items():
                if a in t: subprocess.Popen(cmd,shell=True); return f"Opening {a}."
            known=["youtube","google","facebook","github","wikipedia","twitter"]
            for s in known:
                if s in t: webbrowser.open(f"https://{s}.com"); return f"Opening {s}.com"
        if any(w in t for w in ["search","সার্চ","খোঁজ"]):
            q=re.sub(r"search for|search|সার্চ করো|খোঁজো","",t).strip()
            webbrowser.open(f"https://www.google.com/search?q={q.replace(' ','+')}"); return f"🔍 Searching:{q}"
        if "youtube" in t or "ইউটিউব" in t:
            q=re.sub(r"youtube|ইউটিউব|search|open","",t).strip() or "trending"
            import urllib.parse; webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}"); return f"🎬 YouTube:{q}"
        if any(w in t for w in ["email","ইমেইল","mail"]):
            if "setup" in t:
                parts=t.split()
                if len(parts)>=4: return self.email.setup(parts[-2],parts[-1])
                return "Format: email setup your@gmail.com APP_PASSWORD"
            if any(w in t for w in ["read","inbox","check"]): return self.email.read_inbox()
            if "send" in t:
                m=re.search(r"to\s+(\S+@\S+)\s+subject\s+(.+?)\s+body\s+(.+)",t)
                if m: return self.email.send(m.group(1),m.group(2),m.group(3))
                return "Format: send email to x@y.com subject TITLE body MESSAGE"
        if any(w in t for w in ["music","song","গান"]) or "play" in t:
            if "list" in t: return self.music.list_songs()
            if "next" in t: return self.music.next_song()
            if "pause" in t: return self.music.pause()
            if "resume" in t or "continue" in t: return self.music.resume()
            if "stop" in t and "music" in t: return self.music.stop()
            q=re.sub(r"play|music|song|গান|চালাও","",t).strip(); return self.music.play(q or None)
        if "volume" in t or "ভলিউম" in t:
            try:
                key=175 if "up" in t else 174 if "down" in t else 173
                subprocess.run(["powershell","-c",f"(New-Object -ComObject WScript.Shell).SendKeys([char]{key})"],capture_output=True)
                return f"🔊 Volume {'up' if key==175 else 'down' if key==174 else 'muted'}."
            except Exception as e: return f"Volume:{e}"
        if any(w in t for w in ["wikipedia","wiki","উইকি"]):
            q=re.sub(r"wikipedia|wiki|about|উইকি","",t).strip()
            try: import wikipedia as wp; wp.set_lang("en"); return "📖 "+wp.summary(q,sentences=3)
            except Exception as e: return f"Wiki:{e}"
        if any(w in t for w in ["stock","share price","শেয়ার"]):
            m=re.search(r"\b([A-Z]{2,5})\b",t.upper()); sym=m.group(1) if m else "AAPL"
            try:
                r=requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}",timeout=8,headers={"User-Agent":"Mozilla/5.0"})
                price=r.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]; return f"📈 {sym}:${price:.2f}"
            except Exception as e: return f"Stock:{e}"
        if any(w in t for w in ["cricket","ক্রিকেট"]): webbrowser.open("https://www.cricbuzz.com/cricket-match/live-scores"); return "🏏 Opening cricket scores!"
        if any(w in t for w in ["football","soccer"]): webbrowser.open("https://www.espn.com/soccer/"); return "⚽ Opening football scores!"
        if any(w in t for w in ["quote","motivation","অনুপ্রেরণা"]): return "💬 "+random.choice(QUOTES)
        if any(w in t for w in ["fact","amazing","তথ্য"]): return "🤓 "+random.choice(FACTS)
        if any(w in t for w in ["briefing","daily report","morning","ব্রিফিং"]):
            now=datetime.datetime.now(); h=now.hour; gr="Good morning" if h<12 else "Good afternoon" if h<17 else "Good evening"
            out=[f"{gr} {CONFIG['user_name']}! {now.strftime('%A %d %B %Y')}"]
            try: r=requests.get(f"https://wttr.in/{CONFIG['city']}?format=3",timeout=5); out.append(r.text.strip())
            except Exception: pass
            out.append(random.choice(QUOTES)); return "\n".join(out)
        if "clipboard" in t:
            try:
                import pyperclip
                if any(w in t for w in ["get","show","paste"]): return f"📋 {pyperclip.paste()[:300]}"
                m=re.search(r"copy (.+)",t)
                if m: pyperclip.copy(m.group(1)); return "Copied ✓"
            except Exception as e: return f"Clipboard:{e}"
        if "organize downloads" in t:
            import shutil; dl=Path.home()/"Downloads"; moved=0
            cats={"Images":[".jpg",".jpeg",".png",".gif"],"Videos":[".mp4",".mkv",".avi"],"Audio":[".mp3",".wav",".flac"],"Documents":[".pdf",".doc",".docx",".txt",".xlsx"],"Archives":[".zip",".rar",".7z"]}
            for f in dl.iterdir():
                if f.is_file():
                    for cat,exts in cats.items():
                        if f.suffix.lower() in exts:
                            dest=dl/cat; dest.mkdir(exist_ok=True)
                            try: shutil.move(str(f),str(dest/f.name)); moved+=1
                            except Exception: pass; break
            return f"✅ Downloads organized! {moved} files sorted."
        if "disk" in t and any(w in t for w in ["analyze","usage","space"]):
            import shutil; u=shutil.disk_usage("C:/"); return f"💾 C:\\ Total:{u.total//(1024**3)}GB Used:{u.used//(1024**3)}GB Free:{u.free//(1024**3)}GB"
        if any(w in t for w in ["process","task list","running","প্রসেস"]):
            procs=sorted(psutil.process_iter(['pid','name','cpu_percent','memory_info']),key=lambda p:p.info.get('cpu_percent') or 0,reverse=True)
            out=""
            for p in procs[:8]:
                try: ram=p.info['memory_info'].rss//(1024**2) if p.info.get('memory_info') else 0; out+=f"  {p.info['pid']:<7}{p.info['name'][:22]:<24}{p.info.get('cpu_percent',0):.1f}%  {ram}MB\n"
                except Exception: pass
            return out or "No processes."
        if "kill" in t:
            m=re.search(r"kill\s+(.+)",t)
            if m:
                name=m.group(1).strip(); killed=[]
                for p in psutil.process_iter(['pid','name']):
                    try:
                        if name.lower() in p.name().lower(): p.kill(); killed.append(p.name())
                    except Exception: pass
                return f"Killed:{', '.join(killed)}" if killed else f"Not found:{name}"
        if any(w in t for w in ["cleanup","clean pc"]): 
            freed=0
            for tp in [os.environ.get("TEMP",""),os.environ.get("TMP","")]:
                if tp and os.path.exists(tp):
                    for f in os.scandir(tp):
                        try:
                            if f.is_file(): freed+=f.stat().st_size; os.unlink(f.path)
                        except Exception: pass
            return f"✅ Cleaned! ~{freed//(1024**2)}MB freed."
        if any(w in t for w in ["password","পাসওয়ার্ড"]):
            import string as st_; m=re.search(r"(\d+)",t); ln=int(m.group(1)) if m else 16
            chars=st_.ascii_letters+st_.digits+"!@#$%^&*"; pwd=''.join(random.SystemRandom().choice(chars) for _ in range(ln))
            try: import pyperclip; pyperclip.copy(pwd); return f"🔑 {pwd} (Copied!)"
            except Exception: return f"🔑 {pwd}"
        if "qr" in t:
            m=re.search(r"qr(?:\s+code)?\s+(.+)",t)
            if m:
                try:
                    import qrcode; qr=qrcode.QRCode(box_size=10,border=4); qr.add_data(m.group(1).strip()); qr.make(fit=True)
                    ts=datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); fname=f"qr_{ts}.png"; qr.make_image().save(fname); webbrowser.open(fname); return f"📱 QR saved:{fname}"
                except Exception as e: return f"QR:{e}"
        if any(w in t for w in ["translate","অনুবাদ"]):
            lang="en" if "english" in t else "bn"; txt=re.sub(r"translate|to (bangla|english|বাংলা|ইংরেজি)|অনুবাদ","",t).strip()
            try: from deep_translator import GoogleTranslator; return "🌐 "+GoogleTranslator(source="auto",target=lang).translate(txt)
            except Exception as e: return f"Translate:{e}"
        if any(w in t for w in ["define","meaning","definition","অর্থ"]):
            word=re.sub(r"define|meaning of|definition of|অর্থ","",t).strip().split()
            if word:
                try:
                    r=requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word[0]}",timeout=8); data=r.json()
                    if isinstance(data,list):
                        out=f"📚 '{word[0]}':\n"
                        for m2 in data[0].get("meanings",[])[:2]:
                            for d2 in m2.get("definitions",[])[:1]: out+=f"  [{m2.get('partOfSpeech','')}] {d2['definition']}\n"
                        return out
                except Exception as e: return f"Dict:{e}"
        if "hash" in t:
            import hashlib as hl; c=re.sub(r"hash","",t).strip()
            if c: return f"🔐 MD5:{hl.md5(c.encode()).hexdigest()}\nSHA256:{hl.sha256(c.encode()).hexdigest()}"
        if any(w in t for w in ["currency","usd","bdt","eur","টাকা"]):
            m=re.search(r"(\d+\.?\d*)\s*([a-zA-Z]+)\s+(?:to|থেকে)\s+([a-zA-Z]+)",t)
            if m:
                try:
                    r=requests.get(f"https://api.exchangerate-api.com/v4/latest/{m.group(2).upper()}",timeout=8); rate=r.json().get("rates",{}).get(m.group(3).upper())
                    if rate: return f"💱 {m.group(1)} {m.group(2).upper()} = {float(m.group(1))*rate:.2f} {m.group(3).upper()}"
                except Exception as e: return f"Currency:{e}"
        if "convert" in t:
            m=re.search(r"(\d+\.?\d*)\s*(\w+)\s+to\s+(\w+)",t)
            if m:
                v,fu,tu=float(m.group(1)),m.group(2).lower(),m.group(3).lower()
                conv={"km":1000,"m":1,"cm":0.01,"mm":0.001,"mile":1609.34,"foot":0.3048,"inch":0.0254,"kg":1,"g":0.001,"lb":0.453592}
                if fu=="c" and tu=="f": return f"🌡 {v}°C = {v*9/5+32:.1f}°F"
                if fu=="f" and tu=="c": return f"🌡 {v}°F = {(v-32)*5/9:.1f}°C"
                if fu in conv and tu in conv: return f"📐 {v} {fu} = {v*conv[fu]/conv[tu]:.4g} {tu}"
        if "alarm" in t or "এলার্ম" in t:
            if any(w in t for w in ["list","show"]):
                return ("Alarms:\n"+"\n".join(f"  {'✓' if a['done'] else '⏰'} {a['h']:02d}:{a['m']:02d} {a['label']}" for a in self.alarms)) if self.alarms else "No alarms."
            m=re.search(r"(\d{1,2}):(\d{2})",t)
            if m:
                label=re.sub(r"set alarm|alarm|at \d{1,2}:\d{2}","",t).strip()
                self.alarms.append({"h":int(m.group(1)),"m":int(m.group(2)),"label":label or "Alarm","done":False}); return f"⏰ Alarm:{m.group(1)}:{m.group(2)}"
        if "stopwatch" in t or "স্টপওয়াচ" in t:
            if "start" in t: self.sw_start=time.time(); self.sw_running=True; return "⏱ Stopwatch started!"
            if "stop" in t and self.sw_running:
                e=time.time()-self.sw_start; self.sw_running=False; h2,r2=divmod(int(e),3600); m2,s=divmod(r2,60); return f"⏱ {h2:02d}:{m2:02d}:{s:02d}"
            if self.sw_running:
                e=time.time()-self.sw_start; h2,r2=divmod(int(e),3600); m2,s=divmod(r2,60); return f"⏱ Elapsed:{h2:02d}:{m2:02d}:{s:02d}"
        if "timer" in t or "টাইমার" in t:
            m=re.search(r"(\d+)",t); secs=int(m.group(1)) if m else 60
            if "min" in t: secs*=60
            label=re.sub(r"timer|set|for|\d+\s*(?:min|sec|s|m)","",t).strip()
            def _r(): time.sleep(secs); self.voice.speak(f"Timer done! {label or 'Time is up!'}")
            threading.Thread(target=_r,daemon=True).start(); m2,s=divmod(secs,60); return f"⏳ Timer:{m2}m {s}s"
        if "pomodoro" in t:
            if self.pom_running: return "Pomodoro already running!"
            m=re.search(r"(\d+)",t); work=int(m.group(1)) if m else 25; self.pom_running=True
            def _p():
                self.voice.speak(f"Pomodoro! Focus for {work} minutes.")
                time.sleep(work*60); self.voice.speak("Done! 5-minute break."); time.sleep(300); self.voice.speak("Break over!"); self.pom_running=False
            threading.Thread(target=_p,daemon=True).start(); return f"🍅 Pomodoro:{work}min!"
        if "todo" in t or ("task" in t and "list" in t):
            if any(w in t for w in ["show","list"]):
                return ("📋 Todos:\n"+"\n".join(f"  {i}. {'✓' if td['done'] else '○'} {td['task']}" for i,td in enumerate(self.todos,1))) if self.todos else "No todos."
            if "done" in t or "complete" in t:
                m=re.search(r"(\d+)",t)
                if m:
                    idx=int(m.group(1))-1
                    if 0<=idx<len(self.todos): self.todos[idx]["done"]=True; self._save_todos(); return f"✓ Todo #{idx+1} done!"
            c=re.sub(r"add|todo|task|new","",t).strip()
            if c: self.todos.append({"task":c,"done":False,"created":datetime.datetime.now().isoformat()}); self._save_todos(); return f"✅ Added:{c}"
        if "note" in t or "নোট" in t:
            if any(w in t for w in ["show","list","দেখাও"]):
                return ("📝 Notes:\n"+"\n".join(f"  {i}. {n['note']}" for i,n in enumerate(self.memory.notes,1))) if self.memory.notes else "No notes."
            c=re.sub(r"add note|save note|note|নোট","",t).strip()
            if c: self.memory.add_note(c); return f"📝 Saved:{c}"
        if any(w in t for w in ["remind","reminder","রিমাইন্ড"]):
            m=re.search(r"(\d+)\s*min",t); mins=int(m.group(1)) if m else 5
            msg=re.sub(r"remind me|reminder|remind|রিমাইন্ড করো","",t); msg=re.sub(r"in \d+ min.*","",msg).strip()
            remind_at=(datetime.datetime.now()+datetime.timedelta(minutes=mins)).isoformat(); self.memory.add_reminder(msg or "Reminder!",remind_at)
            def _r(): time.sleep(mins*60); self.voice.speak(f"Reminder:{msg or 'Time!'}")
            threading.Thread(target=_r,daemon=True).start(); return f"⏰ Reminder in {mins} min!"
        if any(w in t for w in ["calculate","calc","হিসাব","math"]):
            expr=re.sub(r"[^0-9+\-*/().**% ]","",t).strip()
            try:
                if expr: return f"🔢 {expr} = {eval(expr)}"
            except Exception as e: return f"Calc:{e}"
        if any(w in t for w in ["export chat","save chat"]): 
            ts=datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); fname=f"jarvis_chat_{ts}.txt"
            with open(fname,"w",encoding="utf-8") as f:
                f.write(f"JARVIS Chat — {datetime.datetime.now()}\n\n")
                for turn in self.memory.history: f.write(f"[{turn.get('time','')[:19]}] {'You' if turn['role']=='user' else 'JARVIS'}:\n{turn.get('content','')}\n\n")
            return f"💾 Chat saved:{fname}"
        if any(w in t for w in ["joke","funny","জোকস","হাসাও"]):
            return random.choice(["Why don't scientists trust atoms? They make up everything!","আমি একটা AI — কখনো ক্লান্ত হই না, শুধু CPU গরম হয়!","There are 10 types: those who get binary, and those who don't.","প্রোগ্রামার কেন চশমা পরে? কারণ সে C# দেখে!"])
        if "scan ports" in t:
            open_p=[]
            for port in [21,22,80,443,3306,3389,8080,8443]:
                try: s=socket.socket(); s.settimeout(0.3); [open_p.append(port) if s.connect_ex(("127.0.0.1",port))==0 else None]; s.close()
                except Exception: pass
            return "Open ports:"+", ".join(map(str,open_p)) if open_p else "No common ports open."

        return self.ai.ask(text)

HELP_ALL="""
  ╔══════════════════════════════════════════════════════════╗
  ║          JARVIS Phase 1-5 — ALL COMMANDS                 ║
  ╠══════════════════════════════════════════════════════════╣
  ║  🎙 Just SPEAK — Auto-listen always active!             ║
  ╠══════════════════════════════════════════════════════════╣
  ║  PHASE 1: time  date  weather  news  network  wifi      ║
  ║           ping  screenshot  open  search  youtube       ║
  ║           note  remind  calculate  joke  help  exit     ║
  ║  PHASE 2: clipboard  password  qr code  translate       ║
  ║           define  hash  currency  unit convert          ║
  ║           world clock  alarm  stopwatch  timer          ║
  ║           todo  process  kill  cleanup  disk  speedtest ║
  ║  PHASE 3: email setup/read/send  play music  pause      ║
  ║           next song  wiki  stock  cricket  football     ║
  ║           quote  fact  briefing  pomodoro  export chat  ║
  ║  PHASE 4: auto listen on/off  voice on/off              ║
  ║           (all answers spoken automatically)            ║
  ║  PHASE 5: dashboard  notify [msg]  ocr 'img.png'        ║
  ║           read pdf  zip  unzip  bulk rename             ║
  ║           duplicate  clipboard history  network live    ║
  ║           app usage  auto screenshot  speak bangla      ║
  ╚══════════════════════════════════════════════════════════╝"""

# ══════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════
def main():
    # CMD ASCII boot animation (Phase 5 — no browser!)
    try:
        from jarvis_phase5 import CMDBootAnimation
        CMDBootAnimation().run(CONFIG["user_name"])
    except Exception:
        os.system("cls" if os.name=="nt" else "clear")
        print(Fore.CYAN+Style.BRIGHT+"\n  J.A.R.V.I.S — Booting...\n"+Style.RESET_ALL)

    line(); status("Loading all systems..."); line()
    memory=Memory(); voice=VoiceEngine(); ai=AICore(memory)
    email_m=EmailManager(); music=MusicPlayer()
    parser=MasterParser(voice,memory,ai,email_m,music)

    def on_heard(text:str):
        if not text or len(text.split())<1: return
        memory.add_turn("user",text); response=parser.parse(text)
        if response=="__EXIT__": voice.speak(f"Goodbye {CONFIG['user_name']}!"); os._exit(0)
        if response: voice.speak(response); memory.add_turn("assistant",response)

    if voice.mic and CONFIG["auto_listen"]: voice.start_auto_listen(on_heard)

    line()
    voice.speak(f"Hello {CONFIG['user_name']}, I am Your Assistant JARVIS. {CONFIG['user_name']}, How Can I Help You?")
    line()
    print(C["dim"]+"  Just speak — auto-listen is ON! Or type below.\n"+C["reset"])

    while True:
        try:
            print(C["green"]+f"\n  {CONFIG['user_name']} » "+C["reset"],end=""); user_input=input().strip()
            if not user_input: continue
            memory.add_turn("user",user_input); response=parser.parse(user_input)
            if response=="__EXIT__": voice.speak(f"Goodbye {CONFIG['user_name']}!"); line(); sys.exit(0)
            voice.speak(response); memory.add_turn("assistant",response)
        except KeyboardInterrupt: voice.speak(f"Goodbye {CONFIG['user_name']}!"); line(); break
        except Exception as e: error(f"Error:{e}")

if __name__=="__main__": main()
