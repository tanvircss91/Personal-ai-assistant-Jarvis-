@echo off
title JARVIS Phase 1+2+3 — Launcher
color 0B
echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║        JARVIS Phase 1+2+3 — Launcher            ║
echo  ║     Just A Rather Very Intelligent System        ║
echo  ╚══════════════════════════════════════════════════╝
echo.

python --version >nul 2>&1
if errorlevel 1 ( echo [ERROR] Python not found! & pause & exit /b 1 )
echo  [OK] Python found.

ollama --version >nul 2>&1
if errorlevel 1 (
    echo  [WARNING] Ollama not found. AI limited.
    echo  Install: https://ollama.com  then: ollama pull llama3.2
) else (
    echo  [OK] Ollama found. Starting server...
    start /b ollama serve
    timeout /t 3 /nobreak >nul
)

echo  [INFO] Installing dependencies...
pip install requests pyttsx3 SpeechRecognition psutil colorama pyperclip deep-translator "qrcode[pil]" pygame wikipedia Pillow pynput -q
echo  [OK] All ready!
echo.
echo  ════════════════════════════════════════════════════
echo    STARTING JARVIS — Say "Hey JARVIS" anytime!
echo  ════════════════════════════════════════════════════
echo.
python jarvis.py
pause
