from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .io import load_yaml
from .models import ValidationResult
from .numbering import parse_config_question, question_number
from .schemas import load_schema, validate_instance

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

    lecture_number = int(config.get("lecture_number") or 0)
    questions = config.get("questions") or []
    for index, question in enumerate(questions, start=1):
        descriptor = parse_config_question(str(question), index)
        if descriptor is None:
            result.add(
                "config.question_number",
                f"Вопрос {index} должен начинаться с номера вида '{lecture_number}.{index}.'",
                path=source,
                location=f"questions/{index - 1}",
            )
            continue
        if descriptor.legacy:
            result.add(
                "config.question_legacy_numbering",
                f"Используется устаревший номер '{descriptor.explicit_question}.'; канонический номер — {question_number(lecture_number, index)}.",
                severity="warning",
                path=source,
                location=f"questions/{index - 1}",
            )
            if descriptor.explicit_question != index:
                result.add(
                    "config.question_sequence",
                    f"Ожидался порядковый номер {index}, получено {descriptor.explicit_question}",
                    path=source,
                    location=f"questions/{index - 1}",
                )
            continue
        if descriptor.lecture_prefix != lecture_number or descriptor.explicit_question != index:
            result.add(
                "config.question_sequence",
                (
                    f"Вопрос {index} должен иметь номер {question_number(lecture_number, index)}, "
                    f"получено {descriptor.lecture_prefix}.{descriptor.explicit_question}"
                ),
                path=source,
                location=f"questions/{index - 1}",
            )

    course_match = LECTURE_NUMBER_RE.search(str(config.get("course", "")))
    if course_match and lecture_number and int(course_match.group(1)) != lecture_number:
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

    methodical = config.get("methodical") or {}
    minimum = int(methodical.get("min_inserts_per_section") or 0)
    maximum = int(methodical.get("max_inserts_per_section") or 0)
    if methodical.get("enabled") and (minimum <= 0 or maximum < minimum):
        result.add(
            "config.methodical_limits",
            "Для methodical.enabled требуется 1 <= min_inserts_per_section <= max_inserts_per_section",
            path=source,
        )

    result.metrics = {
        "questions": len(questions),
        "competencies": len(competencies),
        "lecture_number": lecture_number,
        "hours": config.get("hours"),
        "methodical_enabled": methodical.get("enabled") is True,
    }
    return result
