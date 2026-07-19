from pathlib import Path

from lecture_tools.config import validate_config


def _base_config(lecture_number: int, question: str, course: str = "2 курс") -> str:
    return f"""
topic: Test topic
discipline: Test
specialty: Test
course: "{course}"
lecture_number: {lecture_number}
hours: 2
fgos_version: "ФГОС"
competencies: ["ОПК-1: test"]
audience_level: students
questions: ["{question}"]
language: ru
formulas_required: false
""".strip()


def test_mismatched_lecture_number_is_rejected(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    config = tmp_path / "lecture_config.md"
    config.write_text(_base_config(4, "4.1. First question", "2 курс, Лекция 7"), encoding="utf-8")
    result = validate_config(config, root)
    assert any(item.code == "config.lecture_number_mismatch" for item in result.errors)


def test_question_prefix_must_match_lecture_number(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    config = tmp_path / "lecture_config.md"
    config.write_text(_base_config(17, "16.1. Wrong prefix"), encoding="utf-8")
    result = validate_config(config, root)
    assert any(item.code == "config.question_sequence" for item in result.errors)
