from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


def pandoc_binary() -> str:
    configured = shutil.which("pandoc")
    if configured:
        return configured
    candidates = (
        Path.home() / "bin/pandoc",
        Path("/usr/bin/pandoc"),
        Path("/usr/local/bin/pandoc"),
    )
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    raise RuntimeError("Pandoc не найден. Установите pandoc и повторите конвертацию.")


def convert_with_pandoc(markdown: str, reference: Path, output: Path, *, toc: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as handle:
        handle.write(markdown)
        temporary = Path(handle.name)
    command = [
        pandoc_binary(),
        str(temporary),
        "--from=markdown+tex_math_dollars+tex_math_double_backslash+smart",
        "--to=docx",
        f"--reference-doc={reference}",
        "--standalone",
        "--wrap=none",
        "--output",
        str(output),
    ]
    if toc:
        command.extend(("--toc", "--toc-depth=3"))
    try:
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
    finally:
        temporary.unlink(missing_ok=True)
    if completed.returncode:
        raise RuntimeError(f"Pandoc завершился с кодом {completed.returncode}:\n{completed.stderr.strip()}")
