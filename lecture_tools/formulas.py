from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .io import atomic_write_text, dump_json
from .models import ValidationResult

FENCED_CODE_RE = re.compile(r"(```.*?```|~~~.*?~~~)", re.DOTALL)
DISPLAY_MATH_RE = re.compile(r"\$\$(?P<body>.*?)\$\$|\\\[(?P<bracket>.*?)\\\]", re.DOTALL)
LABEL_RE = re.compile(r"\\label\{(?P<label>eq:[A-Za-z0-9_.:-]+)\}")
TAG_RE = re.compile(r"\\tag\{(?P<tag>\d+\.\d+)\}")
REFERENCE_RE = re.compile(r"@(?P<label>eq:[A-Za-z0-9_.:-]+)")
SYMBOL_EXPLANATION_RE = re.compile(r"(?:^|\n)\s*(?:где|здесь)\s+[^\n]{3,}", re.IGNORECASE)


@dataclass(slots=True)
class FormulaRecord:
    formula_id: str
    number: str
    expression: str
    ordinal: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "formula_id": self.formula_id,
            "number": self.number,
            "expression": self.expression.strip(),
            "ordinal": self.ordinal,
        }


def _outside_code_segments(text: str) -> Iterable[tuple[bool, str]]:
    parts = FENCED_CODE_RE.split(text)
    for index, part in enumerate(parts):
        yield index % 2 == 0, part


def _normalize_expression(body: str) -> str:
    body = LABEL_RE.sub("", body)
    body = TAG_RE.sub("", body)
    return body.strip()


def number_markdown(text: str, lecture_number: int) -> tuple[str, list[FormulaRecord], ValidationResult]:
    result = ValidationResult(name="formula-numbering")
    records: list[FormulaRecord] = []
    seen: set[str] = set()

    def process_segment(segment: str) -> str:
        def replace(match: re.Match[str]) -> str:
            body = match.group("body") if match.group("body") is not None else match.group("bracket")
            body = body or ""
            label_match = LABEL_RE.search(body)
            if not label_match:
                result.add(
                    "formula.missing_label",
                    "Каждая блочная формула должна содержать стабильный идентификатор \\label{eq:...}",
                    location=f"offset:{match.start()}",
                )
                return match.group(0)
            label = label_match.group("label")
            if label in seen:
                result.add(
                    "formula.duplicate_label",
                    f"Повторный идентификатор формулы: {label}",
                    location=f"offset:{match.start()}",
                )
                return match.group(0)
            seen.add(label)
            ordinal = len(records) + 1
            number = f"{lecture_number}.{ordinal}"
            expression = _normalize_expression(body)
            records.append(
                FormulaRecord(
                    formula_id=label,
                    number=number,
                    expression=expression,
                    ordinal=ordinal,
                )
            )
            return f"$$\n{expression} \\tag{{{number}}}\n$$"

        return DISPLAY_MATH_RE.sub(replace, segment)

    processed_parts: list[str] = []
    for is_text, segment in _outside_code_segments(text):
        processed_parts.append(process_segment(segment) if is_text else segment)
    numbered = "".join(processed_parts)

    registry = {record.formula_id: record.number for record in records}

    def replace_reference(match: re.Match[str]) -> str:
        label = match.group("label")
        number = registry.get(label)
        if number is None:
            result.add(
                "formula.unresolved_reference",
                f"Ссылка указывает на неизвестную формулу {label}",
                location=f"offset:{match.start()}",
            )
            return match.group(0)
        return f"({number})"

    final_parts: list[str] = []
    for is_text, segment in _outside_code_segments(numbered):
        final_parts.append(REFERENCE_RE.sub(replace_reference, segment) if is_text else segment)
    numbered = "".join(final_parts)

    result.metrics = {"formulas": len(records), "lecture_number": lecture_number}
    return numbered, records, result


def validate_formula_markdown(text: str, lecture_number: int | None = None) -> ValidationResult:
    result = ValidationResult(name="formulas")
    labels: list[str] = []
    tags: list[str] = []
    unresolved_refs: list[str] = []
    display_count = 0

    for is_text, segment in _outside_code_segments(text):
        if not is_text:
            continue
        for match in DISPLAY_MATH_RE.finditer(segment):
            display_count += 1
            body = match.group("body") if match.group("body") is not None else match.group("bracket")
            body = body or ""
            label = LABEL_RE.search(body)
            tag = TAG_RE.search(body)
            if label:
                labels.append(label.group("label"))
            if tag:
                tags.append(tag.group("tag"))
            if not label and not tag:
                result.add(
                    "formula.unnumbered_display",
                    "Блочная формула не содержит ни \\label, ни \\tag",
                    location=f"offset:{match.start()}",
                )
            tail = segment[match.end() : match.end() + 500]
            if not SYMBOL_EXPLANATION_RE.search(tail):
                result.add(
                    "formula.symbols",
                    "После блочной формулы не найдена расшифровка символов, начинающаяся с 'где' или 'здесь'",
                    severity="warning",
                    location=f"offset:{match.start()}",
                )
        unresolved_refs.extend(match.group("label") for match in REFERENCE_RE.finditer(segment))

    for label in sorted({item for item in labels if labels.count(item) > 1}):
        result.add("formula.duplicate_label", f"Повторный идентификатор: {label}")
    for tag in sorted({item for item in tags if tags.count(item) > 1}):
        result.add("formula.duplicate_tag", f"Повторный номер формулы: {tag}")

    if tags:
        expected_prefix = f"{lecture_number}." if lecture_number is not None else None
        ordinals: list[int] = []
        for tag in tags:
            prefix, ordinal = tag.split(".", maxsplit=1)
            if expected_prefix and not tag.startswith(expected_prefix):
                result.add(
                    "formula.lecture_prefix",
                    f"Номер {tag} не соответствует lecture_number={lecture_number}",
                )
            if ordinal.isdigit():
                ordinals.append(int(ordinal))
            if not prefix.isdigit():
                result.add("formula.tag_format", f"Некорректный номер формулы: {tag}")
        if ordinals and ordinals != list(range(1, len(ordinals) + 1)):
            result.add(
                "formula.sequence",
                f"Номера формул должны идти последовательно: получено {ordinals}",
            )

    known_labels = set(labels)
    for reference in unresolved_refs:
        if reference not in known_labels:
            result.add(
                "formula.unresolved_reference",
                f"Ссылка указывает на неизвестную формулу {reference}",
            )

    result.metrics = {
        "display_formulas": display_count,
        "labels": len(labels),
        "tags": len(tags),
        "references": len(unresolved_refs),
    }
    return result


def number_file(
    input_path: str | Path,
    output_path: str | Path,
    registry_path: str | Path,
    lecture_number: int,
) -> ValidationResult:
    source = Path(input_path)
    text = source.read_text(encoding="utf-8")
    numbered, records, result = number_markdown(text, lecture_number)
    if result.errors:
        return result
    atomic_write_text(output_path, numbered)
    dump_json(
        registry_path,
        {
            "schema_version": "3.0",
            "lecture_number": lecture_number,
            "formulas": [record.to_dict() for record in records],
        },
    )
    return result
