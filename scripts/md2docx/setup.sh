#!/bin/bash
# setup.sh — Настройка окружения для md2docx

cd "$(dirname "$0")"
VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "[i] Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "[i] Installing dependencies..."
./"$VENV_DIR"/bin/pip install -q --upgrade pip
./"$VENV_DIR"/bin/pip install -q -r requirements.txt

echo "[✓] Environment ready."
