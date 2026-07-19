#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lecture_tools.manifest import (  # noqa: E402
    load_or_create_manifest,
    mark_stage,
    save_manifest,
    stage_is_fresh,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage hash-based Lecture Builder stage state")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--platform", choices=("antigravity", "codex", "gemini"), required=True)

    check = sub.add_parser("check")
    check.add_argument("stage")
    check.add_argument("--inputs", nargs="+", required=True)
    check.add_argument("--outputs", nargs="+", required=True)
    check.add_argument("--platform", default="codex")

    mark = sub.add_parser("mark")
    mark.add_argument("stage")
    mark.add_argument("--status", choices=("complete", "failed", "blocked", "in_progress"), required=True)
    mark.add_argument("--inputs", nargs="+", required=True)
    mark.add_argument("--outputs", nargs="*", default=[])
    mark.add_argument("--notes", nargs="*", default=[])
    mark.add_argument("--platform", default="codex")

    args = parser.parse_args()
    root = ROOT
    manifest = load_or_create_manifest(root, platform=args.platform)

    if args.command == "init":
        save_manifest(root, manifest)
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0
    if args.command == "check":
        fresh = stage_is_fresh(manifest, root, args.stage, args.inputs, args.outputs)
        print("fresh" if fresh else "stale")
        return 0 if fresh else 1
    if args.command == "mark":
        mark_stage(
            manifest,
            root,
            args.stage,
            status=args.status,
            inputs=args.inputs,
            outputs=args.outputs,
            notes=args.notes,
        )
        save_manifest(root, manifest)
        print(json.dumps(manifest["stages"][args.stage], ensure_ascii=False, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
