"""
╔══════════════════════════════════════════════════════════════════╗
║                    J.A.R.V.I.S  - Phase 3                       ║
║         Wake Word + Email + Music + Advanced Automation          ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os, sys, json, time, datetime, threading, subprocess
import platform, random, re, webbrowser, smtplib, imaplib
import email as email_lib, urllib.parse, base64, hashlib, socket
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def _pip(pkg):
    subprocess.check_call([sys.executable,"-m","pip","install",pkg,"-q"],
                          stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def _try_import(mod, pkg):
    try: __import__(mod)
    except ImportError: print(f"  [INSTALL] {pkg}..."); _pip(pkg)

for mod,pkg in {"wikipedia":"wikipedia","pygame":"pygame","requests":"requests","pynput":"pynput"}.items():
    _try_import(mod,pkg)

import requests

# ══════════════════════════════════════════════════════════════════
#  WAKE WORD ENGINE
# ══════════════════════════════════════════════════════════════════
class WakeWordEngine:
    WAKE_PHRASES = ["hey jarvis","jarvis","hey jarves","হেই জারভিস","জারভিস","এই জারভিস"]

    def __init__(self, on_wake_detected, speak_fn):
        self.on_wake   = on_wake_detected
        self.speak     = speak_fn
        self.enabled   = True
        self._running  = False

    def start(self):
        self._running = True
        threading.Thread(target=self._loop, daemon=True).start()
        print("  ✓  Wake word engine running. Say 'Hey JARVIS' anytime!")

    def stop(self):
        self._running = False

    def _loop(self):
        try:
            import speech_recognition as sr
            r   = sr.Recognizer()
            mic = sr.Microphone()
            r.energy_threshold         = 300
            r.dynamic_energy_threshold = True
            r.pause_threshold          = 0.6
            with mic as source:
                r.adjust_for_ambient_noise(source, duration=1)
            while self._running:
                if not self.enabled:
                    time.sleep(0.5); continue
                try:
                    with mic as source:
                        audio = r.listen(source, timeout=3, phrase_time_limit=4)
                    text = r.recognize_google(audio, language="en-US").lower()
                    if any(phrase in text for phrase in self.WAKE_PHRASES):
                        self.enabled = False
                        self.on_wake()
                        time.sleep(1.5)
                        self.enabled = True
                except Exception:
                    pass
        except Exception as e:
            print(f"  ✗  Wake word error: {e}")

# ══════════════════════════════════════════════════════════════════
#  EMAIL MANAGER
# ══════════════════════════════════════════════════════════════════
class EmailManager:
    CFG_FILE = "jarvis_email.json"

    def __init__(self):
        self.cfg = json.load(open(self.CFG_FILE)) if os.path.exists(self.CFG_FILE) else {"configured":False}

    def setup(self, addr:str, app_pwd:str) -> str:
        self.cfg = {"email":addr,"password":app_pwd,"configured":True}
        json.dump(self.cfg, open(self.CFG_FILE,"w"))
        return ("Email configured! ✅\n"
                "Note: Use Gmail App Password.\n"
                "Get it: Google Account → Security → 2-Step Verification → App Passwords")

    def send(self, to:str, subject:str, body:str) -> str:
        if not self.cfg.get("configured"):
            return "Email not set up.\nCommand: email setup your@gmail.com YOUR_APP_PASSWORD"
        try:
            msg = MIMEMultipart()
            msg["From"] = self.cfg["email"]; msg["To"] = to; msg["Subject"] = subject
            msg.attach(MIMEText(body,"plain","utf-8"))
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as s:
                s.login(self.cfg["email"],self.cfg["password"]); s.send_message(msg)
            return f"Email sent to {to}! ✅"
        except smtplib.SMTPAuthenticationError:
            return "Auth failed. Check your App Password."
        except Exception as e:
            return f"Email error: {e}"

    def read_inbox(self, count:int=5) -> str:
        if not self.cfg.get("configured"):
            return "Email not configured."
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.cfg["email"],self.cfg["password"])
            mail.select("inbox")
            _,data = mail.search(None,"ALL"); ids = data[0].split()[-count:]
            result = f"Last {count} emails:\n"
            for i,eid in enumerate(reversed(ids),1):
                _,d   = mail.fetch(eid,"(RFC822)")
                msg   = email_lib.message_from_bytes(d[0][1])
                result += (f"  {i}. From: {msg.get('From','?')[:35]}\n"
                           f"     Sub : {msg.get('Subject','?')[:45]}\n\n")
            mail.logout(); return result
        except Exception as e:
            return f"Email read error: {e}"

# ══════════════════════════════════════════════════════════════════
#  MUSIC PLAYER
# ══════════════════════════════════════════════════════════════════
class MusicPlayer:
    EXTENSIONS = [".mp3",".wav",".ogg",".flac",".m4a",".wma"]

    def __init__(self):
        self.pg       = None
        self.playlist : list = []
        self.current  : int  = 0
        self.playing  : bool = False
        self.music_dir: str  = str(Path.home()/"Music")
        try:
            import pygame; pygame.mixer.init(); self.pg = pygame
            print("  ✓  Music player ready.")
        except Exception:
            _pip("pygame")

    def _scan(self) -> list:
        import glob; songs=[]
        for ext in self.EXTENSIONS:
            songs += glob.glob(os.path.join(self.music_dir,"**",f"*{ext}"),recursive=True)
        return songs

    def play(self, query:str=None) -> str:
        if not self.pg: return "pip install pygame first."
        songs = self._scan()
        if not songs: return f"No music files found in {self.music_dir}"
        if query:
            matched = [s for s in songs if query.lower() in Path(s).name.lower()]
            songs = matched if matched else songs
        self.playlist = songs; random.shuffle(self.playlist); self.current = 0
        self.pg.mixer.music.load(self.playlist[0])
        self.pg.mixer.music.play(); self.playing = True
        return f"🎵 Playing: {Path(self.playlist[0]).name}"

    def next_song(self) -> str:
        if not self.playlist: return "No playlist loaded."
        self.current = (self.current+1) % len(self.playlist)
        self.pg.mixer.music.load(self.playlist[self.current])
        self.pg.mixer.music.play()
        return f"🎵 Next: {Path(self.playlist[self.current]).name}"

    def prev_song(self) -> str:
        if not self.playlist: return "No playlist loaded."
        self.current = (self.current-1) % len(self.playlist)
        self.pg.mixer.music.load(self.playlist[self.current])
        self.pg.mixer.music.play()
        return f"🎵 Previous: {Path(self.playlist[self.current]).name}"

    def pause(self) -> str:
        if self.pg and self.playing:
            self.pg.mixer.music.pause(); self.playing=False; return "⏸ Music paused."
        return "Nothing playing."

    def resume(self) -> str:
        if self.pg and not self.playing:
            self.pg.mixer.music.unpause(); self.playing=True; return "▶ Music resumed."
        return "Already playing."

    def stop(self) -> str:
        if self.pg:
            self.pg.mixer.music.stop(); self.playing=False; return "⏹ Music stopped."
        return "Nothing playing."

    def list_songs(self) -> str:
        songs = self._scan()
        if not songs: return f"No music in {self.music_dir}"
        result = f"🎵 Music ({len(songs)} songs):\n"
        for i,s in enumerate(songs[:15],1): result += f"  {i}. {Path(s).name}\n"
        if len(songs)>15: result += f"  ... and {len(songs)-15} more\n"
        return result

    def set_volume(self, level:int) -> str:
        if self.pg:
            self.pg.mixer.music.set_volume(max(0,min(100,level))/100)
            return f"🔊 Music volume: {level}%"
        return "pygame not available."

# ══════════════════════════════════════════════════════════════════
#  WIKIPEDIA
# ══════════════════════════════════════════════════════════════════
def wiki_summary(query:str) -> str:
    try:
        import wikipedia
        wikipedia.set_lang("en")
        result = wikipedia.summary(query, sentences=3, auto_suggest=True)
        return f"📖 Wikipedia — {query}:\n{result}"
    except Exception as e:
        return f"Wikipedia: {e}"

# ══════════════════════════════════════════════════════════════════
#  STOCK PRICE
# ══════════════════════════════════════════════════════════════════
def stock_price(symbol:str) -> str:
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol.upper()}"
        r   = requests.get(url,timeout=8,headers={"User-Agent":"Mozilla/5.0"})
        meta  = r.json()["chart"]["result"][0]["meta"]
        price = meta["regularMarketPrice"]
        prev  = meta["previousClose"]
        change= price-prev; pct=(change/prev)*100
        arrow = "▲" if change>=0 else "▼"
        return (f"📈 {symbol.upper()}:\n"
                f"  Price : ${price:.2f}\n"
                f"  Change: {arrow} {change:+.2f} ({pct:+.2f}%)")
    except Exception as e:
        return f"Stock error: {e}"

# ══════════════════════════════════════════════════════════════════
#  QUOTES & FACTS
# ══════════════════════════════════════════════════════════════════
MOTIVATIONAL_QUOTES = [
    "The only way to do great work is to love what you do. — Steve Jobs",
    "In the middle of every difficulty lies opportunity. — Albert Einstein",
    "It does not matter how slowly you go as long as you do not stop. — Confucius",
    "সফলতা হলো প্রতিদিন ছোট ছোট প্রচেষ্টার সমষ্টি।",
    "স্বপ্ন দেখো, কারণ স্বপ্ন থেকেই লক্ষ্য জন্ম নেয়।",
    "The future belongs to those who believe in the beauty of their dreams. — Eleanor Roosevelt",
    "কঠিন পরিশ্রমের কোনো বিকল্প নেই।",
    "Don't watch the clock; do what it does. Keep going. — Sam Levenson",
]

RANDOM_FACTS = [
    "Honey never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs, still edible!",
    "A group of flamingos is called a 'flamboyance'.",
    "Octopuses have three hearts and blue blood.",
    "বাংলাদেশ বিশ্বের বৃহত্তম ব-দ্বীপের উপর অবস্থিত।",
    "The human brain generates about 23 watts of power.",
    "Sharks are older than trees — they've existed for over 400 million years.",
    "The Eiffel Tower grows about 6 inches taller in summer due to heat expansion.",
]

def get_quote() -> str:
    return "💬 " + random.choice(MOTIVATIONAL_QUOTES)

def get_fact() -> str:
    return "🤓 Fun Fact: " + random.choice(RANDOM_FACTS)

# ══════════════════════════════════════════════════════════════════
#  DAILY BRIEFING
# ══════════════════════════════════════════════════════════════════
def daily_briefing(city:str="Dhaka") -> str:
    now  = datetime.datetime.now(); h = now.hour
    gr   = "Good morning" if h<12 else "Good afternoon" if h<17 else "Good evening"
    lines= [f"━━━ Daily Briefing ━━━",
            f"  {gr}! Today is {now.strftime('%A, %d %B %Y')}.",
            f"  Time: {now.strftime('%I:%M %p')}",""]
    try:
        r = requests.get(f"https://wttr.in/{city}?format=3",timeout=6)
        lines.append(f"  🌦 {r.text.strip()}")
    except Exception:
        lines.append("  🌦 Weather unavailable.")
    lines.append(f"\n  {get_quote()}")
    lines.append(f"\n  {get_fact()}")
    lines.append("\n━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(lines)

# ══════════════════════════════════════════════════════════════════
#  POMODORO TIMER
# ══════════════════════════════════════════════════════════════════
class PomodoroTimer:
    def __init__(self, speak_fn):
        self.speak   = speak_fn
        self.session = 0
        self.running = False

    def start(self, work_min:int=25, break_min:int=5) -> str:
        if self.running: return "Pomodoro already running!"
        self.running = True; self.session += 1; s = self.session
        def _run():
            self.speak(f"Pomodoro session {s} started! Focus for {work_min} minutes. 🍅")
            time.sleep(work_min*60)
            self.speak(f"Session {s} complete! Take a {break_min}-minute break!")
            time.sleep(break_min*60)
            self.speak("Break over! Ready for next session?")
            self.running = False
        threading.Thread(target=_run,daemon=True).start()
        return f"🍅 Pomodoro #{s}: {work_min}min work + {break_min}min break. Starting now!"

# ══════════════════════════════════════════════════════════════════
#  TASK SCHEDULER
# ══════════════════════════════════════════════════════════════════
class TaskScheduler:
    def __init__(self, speak_fn):
        self.speak = speak_fn
        self.tasks : list = []
        threading.Thread(target=self._run,daemon=True).start()

    def add_task(self, name:str, hour:int, minute:int) -> str:
        self.tasks.append({"name":name,"hour":hour,"minute":minute,"last_run":None})
        return f"Scheduled: '{name}' at {hour:02d}:{minute:02d} ✅"

    def list_tasks(self) -> str:
        if not self.tasks: return "No scheduled tasks."
        return "Scheduled Tasks:\n"+"\n".join(
            f"  ⏰ {t['hour']:02d}:{t['minute']:02d} — {t['name']}" for t in self.tasks)

    def _run(self):
        while True:
            now = datetime.datetime.now()
            for t in self.tasks:
                if (t["hour"]==now.hour and t["minute"]==now.minute and
                        t.get("last_run")!=now.date().isoformat()):
                    self.speak(f"Scheduled task: {t['name']}")
                    t["last_run"] = now.date().isoformat()
            time.sleep(45)

# ══════════════════════════════════════════════════════════════════
#  CHAT HISTORY EXPORT
# ══════════════════════════════════════════════════════════════════
def export_chat(history:list, fmt:str="txt") -> str:
    ts    = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"jarvis_chat_{ts}.{fmt}"
    with open(fname,"w",encoding="utf-8") as f:
        f.write(f"JARVIS Chat Export — {datetime.datetime.now()}\n"+"═"*60+"\n\n")
        for turn in history:
            role    = "You" if turn["role"]=="user" else "JARVIS"
            f.write(f"[{turn.get('time','')[:19]}] {role}:\n{turn.get('content','')}\n\n")
    return f"Chat exported: '{fname}' ✅"

# ══════════════════════════════════════════════════════════════════
#  SAVE TEXT TO FILE
# ══════════════════════════════════════════════════════════════════
def save_to_file(text:str, filename:str=None) -> str:
    if not filename:
        ts       = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"jarvis_note_{ts}.txt"
    with open(filename,"w",encoding="utf-8") as f:
        f.write(text)
    return f"Saved to '{filename}' ✅"

# ══════════════════════════════════════════════════════════════════
#  YOUTUBE SEARCH
# ══════════════════════════════════════════════════════════════════
def youtube_search(query:str) -> str:
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return f"🎬 Opening YouTube: '{query}'"

# ══════════════════════════════════════════════════════════════════
#  SYSTEM VOLUME CONTROL
# ══════════════════════════════════════════════════════════════════
def system_volume(action:str) -> str:
    try:
        key = {"up":175,"down":174,"mute":173}[action]
        subprocess.run(
            ["powershell","-c",
             f"(New-Object -ComObject WScript.Shell).SendKeys([char]{key})"],
            capture_output=True)
        icons = {"up":"🔊","down":"🔉","mute":"🔇"}
        return f"{icons[action]} Volume {action}."
    except Exception as e:
        return f"Volume error: {e}"

# ══════════════════════════════════════════════════════════════════
#  TYPING SPEED TEST
# ══════════════════════════════════════════════════════════════════
TYPING_SENTENCES = [
    "The quick brown fox jumps over the lazy dog.",
    "JARVIS is an AI assistant created to help you every day.",
    "Python is a powerful programming language for everyone.",
    "Technology is best when it brings people together.",
]

def typing_speed_test() -> str:
    sentence = random.choice(TYPING_SENTENCES)
    print(f"\n  Type this:\n  ► {sentence}\n")
    print("  Press ENTER when ready...")
    input()
    start = time.time()
    print("  GO! → ",end="",flush=True)
    typed   = input()
    elapsed = time.time()-start
    words   = len(sentence.split())
    wpm     = int((words/elapsed)*60)
    acc     = sum(a==b for a,b in zip(typed,sentence))/len(sentence)*100
    return (f"⌨ Typing Test:\n"
            f"  WPM      : {wpm}\n"
            f"  Accuracy : {acc:.1f}%\n"
            f"  Time     : {elapsed:.1f}s\n"
            f"  {'✅ Perfect!' if typed.strip()==sentence else '❌ Some errors'}")

# ══════════════════════════════════════════════════════════════════
#  CONTINUOUS VOICE MODE
# ══════════════════════════════════════════════════════════════════
class ContinuousVoiceMode:
    STOP = ["stop","exit voice","voice off","enough","বন্ধ","থামো"]

    def __init__(self, voice_engine, parse_fn, speak_fn):
        self.ve    = voice_engine
        self.parse = parse_fn
        self.speak = speak_fn

    def run(self):
        self.speak("Continuous voice mode active. Say 'stop' to exit.")
        while True:
            heard = self.ve.listen_once(timeout=8)
            if not heard: continue
            if any(p in heard for p in self.STOP):
                self.speak("Exiting voice mode."); break
            response = self.parse(heard)
            if response in ("__EXIT__","__LISTEN__","__CONTINUOUS__"): break
            self.speak(response)

# ══════════════════════════════════════════════════════════════════
#  PHASE 3 PARSER EXTENSION
# ══════════════════════════════════════════════════════════════════
class Phase3Parser:
    def __init__(self, email_mgr:EmailManager, music:MusicPlayer,
                 pomodoro:PomodoroTimer, scheduler:TaskScheduler,
                 memory_history:list, speak_fn, voice_engine):
        self.email     = email_mgr
        self.music     = music
        self.pomodoro  = pomodoro
        self.scheduler = scheduler
        self.history   = memory_history
        self.speak     = speak_fn
        self.ve        = voice_engine

    def parse(self, t:str):
        """Returns response string or None (pass to lower phases)."""

        # EMAIL
        if any(w in t for w in ["email","ইমেইল","mail"]):
            if "setup" in t:
                parts=t.split()
                if len(parts)>=4: return self.email.setup(parts[-2],parts[-1])
                return "Format: email setup your@gmail.com APP_PASSWORD"
            if any(w in t for w in ["read","inbox","check","দেখাও"]):
                return self.email.read_inbox(5)
            if "send" in t or "পাঠাও" in t:
                m=re.search(r"to\s+(\S+@\S+)\s+subject\s+(.+?)\s+body\s+(.+)",t)
                if m: return self.email.send(m.group(1),m.group(2),m.group(3))
                return "Format: send email to x@gmail.com subject Hello body Message"

        # MUSIC
        if any(w in t for w in ["music","song","গান"]) or "play" in t:
            if "list" in t or "songs" in t: return self.music.list_songs()
            if "next" in t: return self.music.next_song()
            if any(w in t for w in ["prev","previous","back"]): return self.music.prev_song()
            if "pause" in t: return self.music.pause()
            if "resume" in t or "continue" in t: return self.music.resume()
            if "stop" in t: return self.music.stop()
            if "volume" in t:
                m=re.search(r"(\d+)",t)
                if m: return self.music.set_volume(int(m.group(1)))
            q=re.sub(r"play|music|song|গান|চালাও","",t).strip()
            return self.music.play(q or None)

        # YOUTUBE
        if "youtube" in t or "ইউটিউব" in t:
            q=re.sub(r"youtube|ইউটিউব|search|play|open","",t).strip()
            return youtube_search(q if q else "trending")

        # VOLUME
        if "volume" in t or "ভলিউম" in t:
            if "up" in t or "বাড়াও" in t:  return system_volume("up")
            if "down" in t or "কমাও" in t: return system_volume("down")
            if "mute" in t or "বন্ধ" in t:  return system_volume("mute")

        # WIKIPEDIA
        if any(w in t for w in ["wikipedia","wiki","উইকি"]):
            q=re.sub(r"wikipedia|wiki|about|উইকি","",t).strip()
            return wiki_summary(q) if q else "What should I search on Wikipedia?"

        # STOCK
        if any(w in t for w in ["stock","share price","শেয়ার"]):
            m=re.search(r"\b([A-Z]{2,5})\b",t.upper())
            return stock_price(m.group(1) if m else "AAPL")

        # FORECAST
        if "forecast" in t or "5 day" in t or "সাপ্তাহিক আবহাওয়া" in t:
            city=re.sub(r"forecast|5 day|weather|আবহাওয়া","",t).strip() or "Dhaka"
            try:
                r=requests.get(f"https://wttr.in/{city}?format=4",timeout=8)
                return f"🌦 {r.text.strip()}"
            except Exception: return "Forecast unavailable."

        # SPORTS
        if any(w in t for w in ["cricket","football","sports","score","ক্রিকেট","ফুটবল"]):
            sport="cricket" if "cricket" in t or "ক্রিকেট" in t else "football"
            if sport=="cricket":
                webbrowser.open("https://www.cricbuzz.com/cricket-match/live-scores")
                return "🏏 Opening live cricket scores!"
            webbrowser.open("https://www.espn.com/soccer/")
            return "⚽ Opening football scores!"

        # QUOTE
        if any(w in t for w in ["quote","motivation","অনুপ্রেরণা","উদ্ধৃতি"]):
            return get_quote()

        # FACT
        if any(w in t for w in ["fact","তথ্য","amazing","interesting"]):
            return get_fact()

        # DAILY BRIEFING
        if any(w in t for w in ["briefing","daily report","morning report","ব্রিফিং"]):
            return daily_briefing()

        # POMODORO
        if "pomodoro" in t or "পোমোডোরো" in t:
            m=re.search(r"(\d+)\s*min",t)
            work=int(m.group(1)) if m else 25
            return self.pomodoro.start(work_min=work)

        # EXPORT CHAT
        if any(w in t for w in ["export chat","save chat","চ্যাট সেভ"]):
            return export_chat(self.history)

        # SAVE TO FILE
        if "save to file" in t or "ফাইলে সেভ" in t:
            content=re.sub(r"save to file|ফাইলে সেভ","",t).strip()
            return save_to_file(content)

        # SCHEDULE TASK
        if "schedule" in t and any(w in t for w in ["task","কাজ"]):
            m=re.search(r"(\d{1,2}):(\d{2})",t)
            name=re.sub(r"schedule|task|at \d{1,2}:\d{2}","",t).strip()
            if m: return self.scheduler.add_task(name,int(m.group(1)),int(m.group(2)))
            return "Format: schedule task [name] at HH:MM"

        if any(w in t for w in ["scheduled tasks","list tasks"]):
            return self.scheduler.list_tasks()

        # TYPING TEST
        if "typing test" in t or "typing speed" in t:
            return typing_speed_test()

        # CONTINUOUS VOICE
        if any(w in t for w in ["continuous voice","always listen","ভয়েস মোড"]):
            return "__CONTINUOUS_VOICE__"

        return None   # not handled → pass to Phase 1+2

# ══════════════════════════════════════════════════════════════════
#  PHASE 3 HELP
# ══════════════════════════════════════════════════════════════════
PHASE3_HELP = """
  ╔══════════════════════ PHASE 3 COMMANDS ══════════════════════╗
  ║  EMAIL:                                                      ║
  ║  email setup your@gmail.com APP_PWD                         ║
  ║  read email / check inbox                                    ║
  ║  send email to x@y.com subject S body B                     ║
  ║                                                              ║
  ║  MUSIC:                                                      ║
  ║  play music [name]  pause  resume  stop                     ║
  ║  next song  previous song  list songs  music volume 80      ║
  ║                                                              ║
  ║  KNOWLEDGE:                                                  ║
  ║  youtube [query]     wiki [topic]    stock AAPL             ║
  ║  forecast [city]     cricket         football               ║
  ║  quote               fact            briefing               ║
  ║                                                              ║
  ║  PRODUCTIVITY:                                               ║
  ║  pomodoro [25] min   typing test                            ║
  ║  schedule task [name] at HH:MM                              ║
  ║  scheduled tasks     export chat     save to file [text]    ║
  ║                                                              ║
  ║  VOICE:                                                      ║
  ║  continuous voice → Always-listening voice mode             ║
  ║  volume up / volume down / volume mute                      ║
  ║                                                              ║
  ║  🎙 Say "Hey JARVIS" anytime — wake word always active!    ║
  ╚══════════════════════════════════════════════════════════════╝
"""
