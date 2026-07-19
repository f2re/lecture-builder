#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lecture_tools.config import load_config  # noqa: E402
from lecture_tools.numbering import normalize_file  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize lecture question and subsection headings from lecture_number"
    )
    parser.add_argument("input")
    parser.add_argument("-o", "--output", default=None)
    parser.add_argument("--config", default="input/lecture_config.md")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    config = load_config(config_path)
    lecture_number = int(config["lecture_number"])

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT / input_path
    output_path = Path(args.output) if args.output else input_path
    if not output_path.is_absolute():
        output_path = ROOT / output_path

    result = normalize_file(input_path, output_path, lecture_number)
    if result.errors:
        for finding in result.errors:
            print(f"ERROR {finding.code}: {finding.message}", file=sys.stderr)
        return 1
    print(f"Normalized structure for lecture {lecture_number}: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
