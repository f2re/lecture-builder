#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lecture_tools.config import load_config  # noqa: E402
from lecture_tools.formulas import number_file  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Assign deterministic lecture-wide equation numbers")
    parser.add_argument("input")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--registry", default="output/formula_registry.json")
    parser.add_argument("--config", default="input/lecture_config.md")
    parser.add_argument("--lecture-number", type=int, default=None)
    args = parser.parse_args()

    lecture_number = args.lecture_number
    if lecture_number is None:
        lecture_number = int(load_config(args.config)["lecture_number"])
    result = number_file(args.input, args.output, args.registry, lecture_number)
    for finding in result.findings:
        print(f"{finding.severity.upper()} {finding.code}: {finding.message}", file=sys.stderr)
    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
