#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lecture_tools.evals import evaluate_project  # noqa: E402
from lecture_tools.io import dump_json, load_json  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run weighted Lecture Builder quality evaluation")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--output", default="output/eval_report.json")
    parser.add_argument("--baseline", default=None, help="Optional prior eval report")
    parser.add_argument("--non-strict", action="store_true")
    args = parser.parse_args()

    report = evaluate_project(args.root, strict=not args.non_strict)
    if args.baseline:
        baseline = load_json(args.baseline)
        report["baseline"] = {
            "total_score": baseline.get("total_score"),
            "delta": round(report["total_score"] - float(baseline.get("total_score", 0)), 2),
        }
    output = Path(args.output)
    if not output.is_absolute():
        output = Path(args.root) / output
    dump_json(output, report)
    print(json.dumps({key: report[key] for key in ("release", "total_score", "minimum_dimension_score")}, ensure_ascii=False, indent=2))
    return 0 if report["release"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
