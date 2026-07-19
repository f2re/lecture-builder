from pathlib import Path

from lecture_tools.config import validate_config


def test_mismatched_lecture_number_is_rejected(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    config = tmp_path / "lecture_config.md"
    config.write_text(
        """
topic: Test topic
discipline: Test
specialty: Test
course: "2 курс, Лекция 7"
lecture_number: 4
hours: 2
fgos_version: "ФГОС"
competencies: ["ОПК-1: test"]
audience_level: students
questions: ["1. First question"]
language: ru
formulas_required: false
""".strip(),
        encoding="utf-8",
    )
    result = validate_config(config, root)
    assert any(item.code == "config.lecture_number_mismatch" for item in result.errors)
