#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lecture_tools.pipeline import run_validation  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Lecture Builder source and artifacts")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--mode", choices=("source", "artifacts", "all"), default="all")
    parser.add_argument("--strict", action="store_true", help="Require the complete generated artifact set")
    parser.add_argument("--report", default=None, help="Optional JSON report path")
    args = parser.parse_args()

    report = run_validation(
        args.root,
        mode=args.mode,
        strict=args.strict,
        report_path=args.report,
    )
    print(json.dumps(report["summary"] | {"ok": report["ok"], "score": report["score"]}, ensure_ascii=False, indent=2))
    if not report["ok"]:
        for check in report["checks"]:
            for finding in check["findings"]:
                if finding["severity"] == "error":
                    where = f" [{finding['path']}]" if finding.get("path") else ""
                    print(f"ERROR {finding['code']}{where}: {finding['message']}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
