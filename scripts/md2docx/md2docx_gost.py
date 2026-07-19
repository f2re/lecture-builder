#!/usr/bin/env python3
"""Convert validated Lecture Builder Markdown to a ГОСТ-oriented DOCX.

Pandoc creates native OMML equations. The preprocessing stage moves
``\\tag{N.M}`` outside display math as a temporary marker; postprocessing
replaces each formula/marker pair with a borderless, centered equation row and
a right-aligned number.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:  # Direct execution from scripts/md2docx.
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from scripts.md2docx.constants import REFERENCE_NAME
    from scripts.md2docx.pandoc_runner import convert_with_pandoc
    from scripts.md2docx.postprocess import postprocess
    from scripts.md2docx.preprocess import preprocess_markdown
    from scripts.md2docx.reference import build_reference
else:
    from .constants import REFERENCE_NAME
    from .pandoc_runner import convert_with_pandoc
    from .postprocess import postprocess
    from .preprocess import preprocess_markdown
    from .reference import build_reference

__all__ = [
    "build_reference",
    "preprocess_markdown",
    "convert_with_pandoc",
    "postprocess",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Markdown → DOCX: ГОСТ-ориентированные стили и нативные формулы Word"
    )
    parser.add_argument("input", help="Validated final Markdown")
    parser.add_argument("-o", "--output", default=None)
    parser.add_argument("--toc", dest="toc", action="store_true", default=True)
    parser.add_argument("--no-toc", dest="toc", action="store_false")
    parser.add_argument("--rebuild-ref", action="store_true")
    parser.add_argument("--ref-docx", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = Path(args.input).expanduser().resolve()
    if not source.is_file():
        print(f"Файл не найден: {source}", file=sys.stderr)
        return 2
    output = Path(args.output).expanduser().resolve() if args.output else source.with_suffix(".docx")
    reference = (
        Path(args.ref_docx).expanduser().resolve()
        if args.ref_docx
        else Path(__file__).resolve().parent / REFERENCE_NAME
    )

    try:
        if args.rebuild_ref or not reference.is_file():
            build_reference(reference)
        markdown, equation_numbers = preprocess_markdown(source)
        convert_with_pandoc(markdown, reference, output, toc=args.toc)
        postprocess(output, equation_numbers)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"DOCX conversion failed: {exc}", file=sys.stderr)
        return 1

    print(f"DOCX created: {output} ({output.stat().st_size} bytes, equations: {len(equation_numbers)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
