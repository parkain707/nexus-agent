@echo off
chcp 65001 >nul
cd /d "%~dp0\.."
echo [NEXUS-AGENT] Launching Viral Distribution Autopilot...
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" launch\autopilot.py
) else (
    python launch\autopilot.py
)
pause
