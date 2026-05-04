"""
╔══════════════════════════════════════════════════════════════════╗
║                    J.A.R.V.I.S  - Phase 4                       ║
║   Auto Voice | Always Speaks | 3D Boot | Custom Greeting        ║
╚══════════════════════════════════════════════════════════════════╝

Phase 4 Fixes & Features:
  ✦ Auto Voice — always listening, NO command needed
  ✦ Every answer spoken aloud automatically
  ✦ Boot greeting: "Hello Tanvir Boss, I am Your Assistant JARVIS..."
  ✦ 3D Hacker Matrix Boot Animation (opens in browser)
  ✦ No "listen" command needed anymore
  ✦ Continuous background listening
"""

import os, webbrowser, time

# ══════════════════════════════════════════════════════════════════
#  3D BOOT ANIMATION HTML
# ══════════════════════════════════════════════════════════════════
BOOT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>JARVIS Booting...</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;overflow:hidden;font-family:'Courier New',monospace;color:#00ffff}
canvas{position:fixed;top:0;left:0;width:100%;height:100%}
#overlay{position:fixed;top:0;left:0;width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:10;pointer-events:none}
#title{font-size:3.5rem;font-weight:bold;color:#00ffff;text-shadow:0 0 30px #00ffff,0 0 60px #00ffff;letter-spacing:0.3em;animation:pulse 1.5s infinite}
#subtitle{font-size:.85rem;color:#00aaff;letter-spacing:0.5em;margin-top:8px;opacity:.85}
#greeting{font-size:1.3rem;color:#fff;margin-top:26px;text-align:center;text-shadow:0 0 10px #00ffff;min-height:2em;transition:opacity 1s}
#bar-wrap{width:420px;margin-top:36px}
#bar-label{font-size:.72rem;color:#00aaff;margin-bottom:7px;letter-spacing:.2em}
#bar{height:3px;background:#001a1a;border:1px solid #00ffff;border-radius:2px;overflow:hidden}
#bar-fill{height:100%;width:0%;background:linear-gradient(90deg,#00ffff,#0055ff);transition:width .08s;box-shadow:0 0 8px #00ffff}
#systems{margin-top:18px;font-size:.68rem;color:#006666;letter-spacing:.1em;text-align:left;line-height:1.9;width:420px}
@keyframes pulse{0%,100%{text-shadow:0 0 30px #00ffff,0 0 60px #00ffff}50%{text-shadow:0 0 55px #00ffff,0 0 110px #0044ff}}
</style>
</head>
<body>
<canvas id="c"></canvas>
<div id="overlay">
  <div id="title">J.A.R.V.I.S</div>
  <div id="subtitle">Just A Rather Very Intelligent System</div>
  <div id="greeting"></div>
  <div id="bar-wrap">
    <div id="bar-label">INITIALIZING SYSTEMS...</div>
    <div id="bar"><div id="bar-fill"></div></div>
  </div>
  <div id="systems"></div>
</div>
<script>
const cv=document.getElementById('c'),cx=cv.getContext('2d');
cv.width=window.innerWidth; cv.height=window.innerHeight;
const cols=Math.floor(cv.width/15);
const drops=Array(cols).fill(1);
const chars='JARVIS01アイウエオカキクケコサシスセソ0123456789ABCDEF<>{}[]|/\\';
function drawMatrix(){
  cx.fillStyle='rgba(0,0,0,0.055)';
  cx.fillRect(0,0,cv.width,cv.height);
  drops.forEach((y,i)=>{
    const ch=chars[Math.floor(Math.random()*chars.length)];
    cx.globalAlpha=Math.random()*.45+.08;
    cx.fillStyle=Math.random()>.9?'#ffffff':Math.random()>.5?'#00ffff':'#0088ff';
    cx.font='13px monospace';
    cx.fillText(ch,i*15,y*15);
    if(y*15>cv.height&&Math.random()>.975) drops[i]=0;
    drops[i]++;
  });
  cx.globalAlpha=1;
}
setInterval(drawMatrix,50);

const sysLines=[
  'VOICE ENGINE................ONLINE',
  'MEMORY CORE.................LOADED',
  'AI NEURAL NETWORK...........ACTIVE',
  'NETWORK MONITOR.............READY',
  'THREAT ANALYSIS.............ARMED',
  'WAKE WORD DETECTOR..........RUNNING',
  'AUTO LISTEN MODE............ENABLED',
  'MUSIC PLAYER................STANDBY',
  'EMAIL CLIENT................READY',
  'ALL SYSTEMS.................ONLINE'
];

const sysDiv=document.getElementById('systems');
const greetDiv=document.getElementById('greeting');
const fillEl=document.getElementById('bar-fill');
const labelEl=document.getElementById('bar-label');
let idx=0;

function nextSystem(){
  if(idx<sysLines.length){
    sysDiv.innerHTML+=sysLines[idx]+'<br>';
    idx++;
    fillEl.style.width=Math.round((idx/sysLines.length)*100)+'%';
    setTimeout(nextSystem, idx<sysLines.length?300:500);
  } else {
    setTimeout(()=>{
      greetDiv.textContent='Hello Tanvir Boss — JARVIS is Online. How Can I Help You?';
      labelEl.textContent='ALL SYSTEMS ONLINE';
      labelEl.style.color='#00ff88';
      fillEl.style.background='#00ff88';
      setTimeout(()=>window.close(), 3500);
    }, 400);
  }
}
setTimeout(nextSystem, 600);
window.addEventListener('resize',()=>{cv.width=window.innerWidth;cv.height=window.innerHeight});
</script>
</body>
</html>"""


def show_boot_animation():
    """Show 3D hacker matrix boot animation in browser."""
    html_path = os.path.abspath("jarvis_boot.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(BOOT_HTML)
    webbrowser.open(f"file:///{html_path}")
    time.sleep(4.5)


# ══════════════════════════════════════════════════════════════════
#  AUTO VOICE LISTENER CLASS
# ══════════════════════════════════════════════════════════════════
class AutoVoiceListener:
    """
    Always-on background voice listener.
    No command needed — just speak and JARVIS responds.
    """
    def __init__(self, on_heard_fn, speak_fn):
        self.on_heard  = on_heard_fn
        self.speak     = speak_fn
        self._running  = False
        self._busy     = False

    def start(self):
        self._running = True
        import threading
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self._running = False

    def _loop(self):
        try:
            import speech_recognition as sr
            r   = sr.Recognizer()
            mic = sr.Microphone()
            r.energy_threshold         = 280
            r.dynamic_energy_threshold = True
            r.pause_threshold          = 0.75

            with mic as src:
                r.adjust_for_ambient_noise(src, duration=1.5)

            print("  ✓  Auto-voice active — just speak anytime!")

            while self._running:
                if self._busy:
                    import time; time.sleep(0.3); continue
                try:
                    with mic as src:
                        audio = r.listen(src, timeout=4, phrase_time_limit=15)
                    text = r.recognize_google(audio, language="en-US").strip()
                    if len(text.split()) >= 1:
                        self._busy = True
                        self.on_heard(text.lower())
                        import time; time.sleep(0.5)
                        self._busy = False
                except Exception:
                    pass
        except Exception as e:
            print(f"  ✗  Auto-voice error: {e}")


# ══════════════════════════════════════════════════════════════════
#  BOOT GREETING  (exact format requested)
# ══════════════════════════════════════════════════════════════════
def get_boot_greeting(user_name:str="Tanvir Boss") -> str:
    return (f"Hello {user_name}, "
            f"I am Your Assistant JARVIS. "
            f"{user_name}, How Can I Help You?")


# ══════════════════════════════════════════════════════════════════
#  PHASE 4 HELP
# ══════════════════════════════════════════════════════════════════
PHASE4_HELP = """
  ╔══════════════════════ PHASE 4 FEATURES ══════════════════════╗
  ║                                                              ║
  ║  🎙 AUTO VOICE — Just speak! No command needed.             ║
  ║  🔊 ALL ANSWERS — Every reply is spoken aloud.              ║
  ║  🎬 3D BOOT ANIMATION — Matrix effect on startup.           ║
  ║  👋 CUSTOM GREETING — Hello Tanvir Boss...                  ║
  ║                                                              ║
  ║  VOICE CONTROLS:                                             ║
  ║  auto listen on/off  → Toggle auto-voice                    ║
  ║  voice on/off        → Toggle voice output                  ║
  ║                                                              ║
  ║  All Phase 1+2+3 features are still available!              ║
  ╚══════════════════════════════════════════════════════════════╝
"""
