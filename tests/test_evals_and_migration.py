from pathlib import Path

import yaml

from lecture_tools.config import validate_config
from scripts.migrate_v2 import migrate

ROOT = Path(__file__).resolve().parents[1]


def test_all_eval_fixtures_match_config_schema() -> None:
    for fixture in sorted((ROOT / "evals/fixtures").glob("*.yaml")):
        result = validate_config(fixture, ROOT)
        assert result.ok, (fixture, result.to_dict())


def test_v2_config_migration_adds_explicit_contracts() -> None:
    old = yaml.safe_load(
        """
topic: Test topic
discipline: Test
specialty: Test
course: "2 курс, Лекция 7"
hours: 2
fgos_version: Test
competencies: ["ОПК-1: test"]
audience_level: students
questions: ["1. Question"]
language: ru
formulas_required: false
"""
    )
    migrated, changes = migrate(old)
    assert migrated["lecture_number"] == 7
    assert migrated["research"]["cover_all_questions"] is True
    assert migrated["quality"]["require_fact_check_after_edit"] is True
    assert len(changes) == 3
