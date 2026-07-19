#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lecture_tools.config import load_config  # noqa: E402
from lecture_tools.numbering import validate_document_numbering  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate lecture-wide document numbering")
    parser.add_argument("markdown")
    parser.add_argument("--config", default="input/lecture_config.md")
    args = parser.parse_args()
    markdown_path = Path(args.markdown)
    if not markdown_path.is_absolute():
        markdown_path = ROOT / markdown_path
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    result = validate_document_numbering(
        markdown_path.read_text(encoding="utf-8"),
        load_config(config_path),
        path=markdown_path,
    )
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
