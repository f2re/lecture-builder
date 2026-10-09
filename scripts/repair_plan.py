#!/usr/bin/env python3
"""Create bounded, specialist-owned correction requests; never edit lecture content."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from lecture_tools.config import load_config
from lecture_tools.io import dump_json, load_json
from lecture_tools.stage_graph import route_findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("draft", "final"), default="draft")
    parser.add_argument("--cycle", type=int, required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        config = load_config(root / "input/lecture_config.md")
        reports = {}
        for role in ("scientific", "pedagogical", "fact_check"):
            directory = "output/reviews/draft" if args.phase == "draft" else "output/reviews"
            path = root / directory / (role + ".json")
            if path.is_file():
                reports[role] = load_json(path)
        if not reports:
            raise ValueError("No review reports; no corrections can be inferred")
        plan = route_findings(reports, cycle=args.cycle, max_cycles=int((config.get("quality") or {}).get("max_review_cycles", 2)))
        destination = args.output or root / "output/change_requests.json"
        destination.resolve().relative_to(root / "output")
        dump_json(destination, plan)
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 1 if plan["status"] == "blocked" else 0
    except (OSError, ValueError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
