#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from copy import deepcopy
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lecture_tools.io import atomic_write_text, load_yaml  # noqa: E402
from lecture_tools.numbering import parse_config_question  # noqa: E402

LECTURE_RE = re.compile(r"(?:лекция|lecture)\s*№?\s*(\d+)", re.IGNORECASE)

DEFAULT_RESEARCH = {
    "cover_all_questions": True,
    "languages": ["ru", "en"],
    "max_queries_per_question": 4,
    "max_results_per_query": 10,
    "max_sources_to_extract": 30,
    "minimum_sources_per_question": {"textbooks": 1, "peer_reviewed": 2, "normative": 0},
}
DEFAULT_METHODICAL = {
    "enabled": True,
    "min_inserts_per_section": 4,
    "max_inserts_per_section": 5,
    "required_functions": ["understand", "remember", "apply", "self_check"],
    "max_word_share": 0.15,
}
DEFAULT_VISUALS = {
    "require_graphs": False,
    "require_image_prompts": True,
    "max_figures_per_section": 3,
    "chart_output_format": "png",
}
DEFAULT_QUALITY = {
    "word_budget_per_hour": 4000,
    "section_words": {"min": 1200, "max": 2400},
    "require_evidence_for_claims": True,
    "require_fact_check_after_edit": True,
    "require_numbered_question_plan": True,
    "max_review_cycles": 2,
}


def migrate(config: dict) -> tuple[dict, list[str]]:
    migrated = deepcopy(config)
    changes: list[str] = []
    if "lecture_number" not in migrated:
        match = LECTURE_RE.search(str(migrated.get("course", "")))
        if not match:
            raise ValueError("lecture_number отсутствует и не может быть извлечён из course")
        migrated["lecture_number"] = int(match.group(1))
        changes.append("added lecture_number from course")
    lecture_number = int(migrated["lecture_number"])

    questions = migrated.get("questions") or []
    canonical_questions: list[str] = []
    for index, question in enumerate(questions, start=1):
        descriptor = parse_config_question(str(question), index)
        title = descriptor.title if descriptor else str(question).strip()
        canonical_questions.append(f"{lecture_number}.{index}. {title}")
    if canonical_questions != questions:
        migrated["questions"] = canonical_questions
        changes.append("normalized question numbers to lecture.question format")

    if "research" not in migrated:
        migrated["research"] = deepcopy(DEFAULT_RESEARCH)
        changes.append("added evidence-first research defaults")
    if "methodical" not in migrated:
        migrated["methodical"] = deepcopy(DEFAULT_METHODICAL)
        changes.append("added methodical insert defaults")
    if "visuals" not in migrated:
        migrated["visuals"] = deepcopy(DEFAULT_VISUALS)
        changes.append("added visualization defaults")
    if "quality" not in migrated:
        migrated["quality"] = deepcopy(DEFAULT_QUALITY)
        changes.append("added strict quality defaults")
    return migrated, changes


def main() -> int:
    parser = argparse.ArgumentParser(description="Safely migrate a Lecture Builder 2.x/3.0 config to 3.1")
    parser.add_argument("input", nargs="?", default="input/lecture_config.md")
    parser.add_argument("-o", "--output", default="input/lecture_config.v3.md")
    parser.add_argument("--in-place", action="store_true", help="Explicitly overwrite input after creating .v2.bak")
    args = parser.parse_args()

    source = Path(args.input)
    value = load_yaml(source)
    if not isinstance(value, dict):
        print("Configuration must be a YAML mapping", file=sys.stderr)
        return 2
    try:
        migrated, changes = migrate(value)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.in_place:
        backup = source.with_suffix(source.suffix + ".v2.bak")
        if backup.exists():
            print(f"Backup already exists: {backup}", file=sys.stderr)
            return 1
        backup.write_bytes(source.read_bytes())
        target = source
    else:
        target = Path(args.output)
        if target.exists():
            print(f"Refusing to overwrite existing file: {target}", file=sys.stderr)
            return 1
    atomic_write_text(target, yaml.safe_dump(migrated, allow_unicode=True, sort_keys=False))
    print(f"Migrated config: {target}")
    for change in changes:
        print(f"- {change}")
    if not changes:
        print("- configuration already contains current fields")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
