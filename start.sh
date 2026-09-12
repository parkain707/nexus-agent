#!/usr/bin/env bash
set -e

echo "========================================================"
echo "  NEXUS-AGENT: Autonomous AI Engineering Agent"
echo "  Starting Mission Control Web Dashboard..."
echo "========================================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 is not installed or not in PATH."
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "[*] Creating virtual environment (.venv)..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -e .
else
    source .venv/bin/activate
fi

echo "[*] Launching Web Mission Control..."
nexus-agent web --port 8000
