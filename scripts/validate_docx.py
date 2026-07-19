#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lecture_tools.docx_validation import validate_docx  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect DOCX structure, styles and native equations")
    parser.add_argument("path")
    parser.add_argument("--expect-formulas", action="store_true")
    args = parser.parse_args()
    result = validate_docx(args.path, expect_formulas=args.expect_formulas)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
