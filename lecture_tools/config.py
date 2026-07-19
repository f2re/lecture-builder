from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .io import load_yaml
from .models import ValidationResult
from .schemas import load_schema, validate_instance

QUESTION_NUMBER_RE = re.compile(r"^\s*(\d+)[.)]\s+")
LECTURE_NUMBER_RE = re.compile(r"(?:лекция|lecture)\s*№?\s*(\d+)", re.IGNORECASE)
COMPETENCY_RE = re.compile(r"\b(?:ОК|ОПК|ПК|УК)-\d+(?:\.\d+)?\b", re.IGNORECASE)


def load_config(path: str | Path) -> dict[str, Any]:
    value = load_yaml(path)
    if not isinstance(value, dict):
        raise ValueError("lecture_config.md must contain a YAML mapping")
    return value


def validate_config(path: str | Path, root: str | Path) -> ValidationResult:
    source = Path(path)
    result = ValidationResult(name="lecture-config")
    if not source.is_file():
        result.add("config.missing", "Файл конфигурации отсутствует", path=source)
        return result

    try:
        config = load_config(source)
    except Exception as exc:  # YAML parsers expose several exception types.
        result.add("config.parse", f"Не удалось прочитать YAML: {exc}", path=source)
        return result

    result.extend(
        validate_instance(
            config,
            load_schema(root, "lecture-config"),
            name="lecture-config-schema",
            path=source,
        )
    )

    questions = config.get("questions") or []
    parsed_numbers: list[int] = []
    for index, question in enumerate(questions, start=1):
        match = QUESTION_NUMBER_RE.match(str(question))
        if not match:
            result.add(
                "config.question_number",
                f"Вопрос {index} должен начинаться с номера вида '{index}.'",
                path=source,
                location=f"questions/{index - 1}",
            )
            continue
        parsed_numbers.append(int(match.group(1)))

    expected = list(range(1, len(questions) + 1))
    if parsed_numbers and parsed_numbers != expected:
        result.add(
            "config.question_sequence",
            f"Нумерация вопросов должна быть последовательной: ожидалось {expected}, получено {parsed_numbers}",
            path=source,
        )

    lecture_number = config.get("lecture_number")
    course_match = LECTURE_NUMBER_RE.search(str(config.get("course", "")))
    if course_match and lecture_number is not None and int(course_match.group(1)) != lecture_number:
        result.add(
            "config.lecture_number_mismatch",
            "Поле lecture_number не совпадает с номером лекции в поле course",
            path=source,
            details={
                "lecture_number": lecture_number,
                "course_number": int(course_match.group(1)),
            },
        )

    competencies = config.get("competencies") or []
    missing_codes = [item for item in competencies if not COMPETENCY_RE.search(str(item))]
    if missing_codes:
        result.add(
            "config.competency_code",
            "Каждая компетенция должна содержать код ОК/УК/ОПК/ПК",
            severity="warning",
            path=source,
            details={"items": missing_codes},
        )

    research = config.get("research", {})
    if research.get("cover_all_questions") is not True:
        result.add(
            "config.research_coverage",
            "Для научной лекции рекомендуется cover_all_questions: true",
            severity="warning",
            path=source,
        )

    result.metrics = {
        "questions": len(questions),
        "competencies": len(competencies),
        "lecture_number": lecture_number,
        "hours": config.get("hours"),
    }
    return result
