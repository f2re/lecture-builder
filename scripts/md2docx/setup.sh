#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

command -v python3 >/dev/null 2>&1 || { echo "python3 is required" >&2; exit 1; }
command -v pandoc >/dev/null 2>&1 || { echo "pandoc is required; install it before DOCX conversion" >&2; exit 1; }

if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi
"$VENV_DIR/bin/python" -m pip install --disable-pip-version-check -q --upgrade pip
"$VENV_DIR/bin/python" -m pip install --disable-pip-version-check -q -r "$SCRIPT_DIR/requirements.txt"
echo "DOCX environment ready: $VENV_DIR"
