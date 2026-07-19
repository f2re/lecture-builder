from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .io import atomic_write_text
from .models import ValidationResult

CANONICAL_CONFIG_QUESTION_RE = re.compile(
    r"^\s*(?P<lecture>\d+)\.(?P<question>\d+)[.)]?\s+(?P<title>.+?)\s*$"
)
LEGACY_CONFIG_QUESTION_RE = re.compile(r"^\s*(?P<question>\d+)[.)]\s+(?P<title>.+?)\s*$")
CANONICAL_QUESTION_HEADING_RE = re.compile(
    r"^##\s+(?P<lecture>\d+)\.(?P<question>\d+)\.\s+(?P<title>.+?)\s*$",
    re.MULTILINE,
)
QUESTION_HEADING_CANDIDATE_RE = re.compile(
    r"^##\s+(?:Вопрос\s+)?(?:(?P<lecture>\d+)\.(?P<question>\d+)|(?P<legacy>\d+))[.)]?\s+(?P<title>.+?)\s*$"
)
CANONICAL_SUBSECTION_RE = re.compile(
    r"^###\s+(?P<lecture>\d+)\.(?P<question>\d+)\.(?P<subsection>\d+)\.\s+(?P<title>.+?)\s*$"
)
CANONICAL_NESTED_RE = re.compile(
    r"^####\s+(?P<lecture>\d+)\.(?P<question>\d+)\.(?P<subsection>\d+)\.(?P<nested>\d+)\.\s+(?P<title>.+?)\s*$"
)
NUMBER_PREFIX_RE = re.compile(r"^\s*(?:\d+\.){1,4}\s*")
FIGURE_CAPTION_RE = re.compile(r"\*\*Рисунок\s+(?P<number>\d+\.\d+)\.\*\*", re.IGNORECASE)
TABLE_CAPTION_RE = re.compile(r"\*\*Таблица\s+(?P<number>\d+\.\d+)\.\*\*", re.IGNORECASE)
PLAN_HEADING_RE = re.compile(r"^##\s+(?:Учебные вопросы|План лекции)(?:\s*\([^)]*\))?\s*$", re.IGNORECASE)
PLAN_ENTRY_RE = re.compile(r"^\s*[-*]\s+(?:\*\*)?(?P<number>\d+\.\d+)\.\s+(?P<title>.+?)(?:\*\*)?\s*$")


@dataclass(frozen=True, slots=True)
class QuestionDescriptor:
    ordinal: int
    title: str
    lecture_prefix: int | None
    explicit_question: int
    legacy: bool

    @property
    def canonical_number(self) -> str:
        if self.lecture_prefix is None:
            raise ValueError("Canonical number requires a lecture prefix")
        return f"{self.lecture_prefix}.{self.ordinal}"


def question_number(lecture_number: int, ordinal: int) -> str:
    return f"{lecture_number}.{ordinal}"


def subsection_number(lecture_number: int, question_ordinal: int, subsection_ordinal: int) -> str:
    return f"{lecture_number}.{question_ordinal}.{subsection_ordinal}"


def parse_config_question(value: str, ordinal: int) -> QuestionDescriptor | None:
    text = str(value)
    canonical = CANONICAL_CONFIG_QUESTION_RE.match(text)
    if canonical:
        return QuestionDescriptor(
            ordinal=ordinal,
            title=canonical.group("title").strip(),
            lecture_prefix=int(canonical.group("lecture")),
            explicit_question=int(canonical.group("question")),
            legacy=False,
        )
    legacy = LEGACY_CONFIG_QUESTION_RE.match(text)
    if legacy:
        return QuestionDescriptor(
            ordinal=ordinal,
            title=legacy.group("title").strip(),
            lecture_prefix=None,
            explicit_question=int(legacy.group("question")),
            legacy=True,
        )
    return None


def strip_number_prefix(title: str) -> str:
    return NUMBER_PREFIX_RE.sub("", title).strip()


def normalize_structure(markdown: str, lecture_number: int) -> tuple[str, ValidationResult]:
    """Normalize question/subsection headings without touching prose or equations."""

    result = ValidationResult(name="structure-numbering")
    lines = markdown.splitlines()
    output: list[str] = []
    question_ordinal = 0
    subsection_ordinal = 0
    nested_ordinal = 0
    current_question: int | None = None
    current_subsection: int | None = None

    for line_number, line in enumerate(lines, start=1):
        if line.startswith("## "):
            candidate = QUESTION_HEADING_CANDIDATE_RE.match(line)
            if candidate:
                question_ordinal += 1
                current_question = question_ordinal
                subsection_ordinal = 0
                nested_ordinal = 0
                current_subsection = None
                title = strip_number_prefix(candidate.group("title"))
                output.append(f"## {question_number(lecture_number, question_ordinal)}. {title}")
                continue
            current_question = None
            current_subsection = None
            subsection_ordinal = 0
            nested_ordinal = 0
            output.append(line)
            continue

        if line.startswith("### ") and current_question is not None:
            subsection_ordinal += 1
            current_subsection = subsection_ordinal
            nested_ordinal = 0
            title = strip_number_prefix(line[4:])
            output.append(
                f"### {subsection_number(lecture_number, current_question, subsection_ordinal)}. {title}"
            )
            continue

        if line.startswith("#### ") and current_question is not None and current_subsection is not None:
            nested_ordinal += 1
            title = strip_number_prefix(line[5:])
            output.append(
                f"#### {lecture_number}.{current_question}.{current_subsection}.{nested_ordinal}. {title}"
            )
            continue

        output.append(line)

    if question_ordinal == 0:
        result.add(
            "numbering.no_questions",
            "Не найдены заголовки учебных вопросов для нормализации",
        )
    result.metrics = {
        "lecture_number": lecture_number,
        "questions": question_ordinal,
    }
    normalized = "\n".join(output)
    if markdown.endswith("\n"):
        normalized += "\n"
    return normalized, result


def _validate_global_sequence(
    numbers: list[str], lecture_number: int, *, kind: str, path: str | Path | None
) -> ValidationResult:
    result = ValidationResult(name=f"{kind}-numbering")
    expected = [f"{lecture_number}.{index}" for index in range(1, len(numbers) + 1)]
    if numbers != expected:
        result.add(
            f"numbering.{kind}_sequence",
            f"Нумерация {kind} должна быть сквозной по лекции: ожидалось {expected}, получено {numbers}",
            path=path,
        )
    return result


def validate_document_numbering(
    markdown: str,
    config: dict[str, Any],
    *,
    path: str | Path | None = None,
) -> ValidationResult:
    result = ValidationResult(name="document-numbering")
    lecture_number = int(config.get("lecture_number") or 0)
    questions = config.get("questions") or []
    lines = markdown.splitlines()
    current_question: int | None = None
    subsection_expected = 0
    nested_expected = 0
    question_numbers: list[str] = []

    for line_number, line in enumerate(lines, start=1):
        if line.startswith("## "):
            match = CANONICAL_QUESTION_HEADING_RE.match(line)
            if match:
                question_ordinal = len(question_numbers) + 1
                current_question = question_ordinal
                subsection_expected = 0
                nested_expected = 0
                actual = f"{match.group('lecture')}.{match.group('question')}"
                expected = question_number(lecture_number, question_ordinal)
                question_numbers.append(actual)
                if actual != expected:
                    result.add(
                        "numbering.question",
                        f"Заголовок вопроса должен иметь номер {expected}, получено {actual}",
                        path=path,
                        location=f"line:{line_number}",
                    )
                descriptor = (
                    parse_config_question(str(questions[question_ordinal - 1]), question_ordinal)
                    if question_ordinal <= len(questions)
                    else None
                )
                if descriptor and strip_number_prefix(match.group("title")) != descriptor.title:
                    result.add(
                        "numbering.question_title",
                        "Название вопроса не совпадает с конфигурацией",
                        severity="warning",
                        path=path,
                        location=f"line:{line_number}",
                        details={"expected": descriptor.title, "actual": match.group("title")},
                    )
                continue
            if QUESTION_HEADING_CANDIDATE_RE.match(line):
                result.add(
                    "numbering.question_format",
                    f"Учебный вопрос должен иметь формат '## {lecture_number}.N. Название'",
                    path=path,
                    location=f"line:{line_number}",
                )
                current_question = None
                continue
            current_question = None
            continue

        if line.startswith("### ") and current_question is not None:
            subsection_expected += 1
            nested_expected = 0
            match = CANONICAL_SUBSECTION_RE.match(line)
            expected = subsection_number(lecture_number, current_question, subsection_expected)
            if not match:
                result.add(
                    "numbering.subsection_format",
                    f"Подраздел должен иметь формат '### {expected}. Название'",
                    path=path,
                    location=f"line:{line_number}",
                )
                continue
            actual = f"{match.group('lecture')}.{match.group('question')}.{match.group('subsection')}"
            if actual != expected:
                result.add(
                    "numbering.subsection_sequence",
                    f"Ожидался номер подраздела {expected}, получено {actual}",
                    path=path,
                    location=f"line:{line_number}",
                )
            continue

        if line.startswith("#### ") and current_question is not None and subsection_expected:
            nested_expected += 1
            match = CANONICAL_NESTED_RE.match(line)
            expected = f"{lecture_number}.{current_question}.{subsection_expected}.{nested_expected}"
            if not match:
                result.add(
                    "numbering.nested_format",
                    f"Вложенный подраздел должен иметь формат '#### {expected}. Название'",
                    path=path,
                    location=f"line:{line_number}",
                )
                continue
            actual = (
                f"{match.group('lecture')}.{match.group('question')}."
                f"{match.group('subsection')}.{match.group('nested')}"
            )
            if actual != expected:
                result.add(
                    "numbering.nested_sequence",
                    f"Ожидался номер вложенного подраздела {expected}, получено {actual}",
                    path=path,
                    location=f"line:{line_number}",
                )

    expected_question_numbers = [
        question_number(lecture_number, index) for index in range(1, len(questions) + 1)
    ]
    if question_numbers != expected_question_numbers:
        result.add(
            "numbering.question_sequence",
            f"Ожидалась последовательность вопросов {expected_question_numbers}, получено {question_numbers}",
            path=path,
        )

    plan_numbers: list[str] = []
    plan_titles: list[str] = []
    in_plan = False
    for line in lines:
        if line.startswith("## "):
            in_plan = bool(PLAN_HEADING_RE.match(line))
            continue
        if in_plan:
            match = PLAN_ENTRY_RE.match(line)
            if match:
                plan_numbers.append(match.group("number"))
                plan_titles.append(strip_number_prefix(match.group("title").strip("* ")))
    require_plan = bool((config.get("quality") or {}).get("require_numbered_question_plan"))
    if require_plan and not plan_numbers:
        result.add(
            "numbering.plan_missing",
            "Раздел 'Учебные вопросы' должен содержать маркированный список с номерами L.Q",
            path=path,
        )
    if plan_numbers:
        if plan_numbers != expected_question_numbers:
            result.add(
                "numbering.plan_sequence",
                f"План лекции должен содержать {expected_question_numbers}, получено {plan_numbers}",
                path=path,
            )
        expected_titles = [
            parse_config_question(str(item), index).title
            for index, item in enumerate(questions, start=1)
            if parse_config_question(str(item), index) is not None
        ]
        if len(plan_titles) == len(expected_titles) and plan_titles != expected_titles:
            result.add(
                "numbering.plan_titles",
                "Названия вопросов в плане не совпадают с конфигурацией",
                severity="warning",
                path=path,
                details={"expected": expected_titles, "actual": plan_titles},
            )

    figures = [match.group("number") for match in FIGURE_CAPTION_RE.finditer(markdown)]
    tables = [match.group("number") for match in TABLE_CAPTION_RE.finditer(markdown)]
    result.extend(_validate_global_sequence(figures, lecture_number, kind="figures", path=path))
    result.extend(_validate_global_sequence(tables, lecture_number, kind="tables", path=path))
    result.metrics = {
        "lecture_number": lecture_number,
        "questions": len(question_numbers),
        "figures": len(figures),
        "tables": len(tables),
        "plan_questions": len(plan_numbers),
    }
    return result


def normalize_file(
    input_path: str | Path,
    output_path: str | Path,
    lecture_number: int,
) -> ValidationResult:
    source = Path(input_path)
    normalized, result = normalize_structure(source.read_text(encoding="utf-8"), lecture_number)
    if result.errors:
        return result
    atomic_write_text(output_path, normalized)
    return result
