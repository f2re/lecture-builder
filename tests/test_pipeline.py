from pathlib import Path

from lecture_tools.pipeline import run_validation

ROOT = Path(__file__).resolve().parents[1]


def test_source_validation_scores_100() -> None:
    report = run_validation(ROOT, mode="source")
    assert report["ok"], report
    assert report["score"] == 100


def test_strict_artifact_validation_rejects_empty_output(tmp_path: Path) -> None:
    (tmp_path / "input").mkdir()
    (tmp_path / "output").mkdir()
    (tmp_path / "input/lecture_config.md").write_text(
        """
topic: Test topic
discipline: Test
specialty: Test
course: Course
lecture_number: 1
hours: 1
fgos_version: Test
competencies: ["ОПК-1: test"]
audience_level: students
questions: ["1. Question"]
language: ru
formulas_required: false
""".strip(),
        encoding="utf-8",
    )
    report = run_validation(tmp_path, mode="artifacts", strict=True)
    assert not report["ok"]
    assert report["summary"]["errors"] > 0
