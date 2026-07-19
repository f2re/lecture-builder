#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 INPUT.md [-o OUTPUT.docx] [converter options]" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT="$1"
shift

resolve_path() {
  python3 - "$1" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).expanduser().resolve())
PY
}

INPUT_ABS="$(resolve_path "$INPUT")"
ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--output|--ref-docx)
      [[ $# -ge 2 ]] || { echo "Missing value for $1" >&2; exit 2; }
      ARGS+=("$1" "$(resolve_path "$2")")
      shift 2
      ;;
    *)
      ARGS+=("$1")
      shift
      ;;
  esac
done

VENV_PYTHON="$SCRIPT_DIR/venv/bin/python3"
if [[ ! -x "$VENV_PYTHON" ]] || ! "$VENV_PYTHON" -c 'import docx, lxml' >/dev/null 2>&1; then
  "$SCRIPT_DIR/setup.sh"
fi

exec "$VENV_PYTHON" "$SCRIPT_DIR/md2docx_gost.py" "$INPUT_ABS" "${ARGS[@]}"
