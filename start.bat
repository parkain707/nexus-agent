@echo off
setlocal
title Nexus-Agent Mission Control Launcher

echo ========================================================
echo   NEXUS-AGENT: Autonomous AI Engineering Agent
echo   Starting Mission Control Web Dashboard...
echo ========================================================
echo.

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not found on your PATH.
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv" (
    echo [*] Creating virtual environment (.venv)...
    python -m venv .venv
    echo [*] Installing dependencies (one-time setup)...
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    python -m pip install -e .
) else (
    call .venv\Scripts\activate.bat
)

echo [*] Launching Web Mission Control and opening browser...
nexus-agent web --port 8000

pause
