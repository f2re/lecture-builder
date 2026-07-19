from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from .artifact_common import _claim_map, _evidence_map
from .models import ValidationResult
from .numbering import question_number

WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+(?:[-–][A-Za-zА-Яа-яЁё0-9]+)?")
INSERT_LABELS = {
    "key_idea": "Ключевая идея",
    "mnemonic": "Мнемоника",
    "thematic_example": "Тематический пример",
    "formula_reading": "Как читать формулу",
    "common_mistake": "Типичная ошибка",
    "self_check": "Проверка понимания",
    "comparison": "Сопоставление",
    "professional_context": "Профессиональный контекст",
    "visual_cue": "Зрительная опора",
}
FACT_BEARING_TYPES = {
    "key_idea",
    "mnemonic",
    "thematic_example",
    "formula_reading",
    "common_mistake",
    "comparison",
    "professional_context",
    "visual_cue",
}


def insert_marker(insert_id: str) -> str:
    return f"<!-- methodical:{insert_id} -->"


def render_methodical_insert(insert: dict[str, Any]) -> str:
    insert_id = str(insert["insert_id"])
    insert_type = str(insert["type"])
    question_display = str(insert.get("question_number") or "")
    label = INSERT_LABELS.get(insert_type, "Методическая вставка")
    if insert_type in {"thematic_example", "professional_context"} and question_display:
        label = f"{label} к вопросу {question_display}"
    title = str(insert.get("title") or "").strip()
    body = str(insert.get("body") or "").strip()
    heading = f"{label}: {title}" if title else label
    return f"{insert_marker(insert_id)}\n> **{heading}.** {body}"


def validate_methodical_inserts(
    value: Any,
    config: dict[str, Any],
    blueprint: Any,
    evidence: Any,
    markdown_values: dict[str, str] | None = None,
    *,
    path: str | Path | None = None,
) -> ValidationResult:
    result = ValidationResult(name="methodical-inserts")
    settings = config.get("methodical") or {}
    enabled = settings.get("enabled") is True
    if not isinstance(value, dict):
        if enabled:
            result.add("methodical.type", "methodical_inserts.json должен быть объектом", path=path)
        return result

    lecture_number = int(config.get("lecture_number") or 0)
    if value.get("lecture_number") != lecture_number:
        result.add(
            "methodical.lecture_number",
            "Номер лекции в methodical_inserts.json не совпадает с конфигурацией",
            path=path,
        )

    sections = {
        str(item.get("section_id")): item
        for item in (blueprint.get("sections") or [])
        if isinstance(blueprint, dict) and isinstance(item, dict)
    }
    claim_map = _claim_map(evidence)
    evidence_map = _evidence_map(evidence)
    seen_ids: set[str] = set()
    per_section: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for index, insert in enumerate(value.get("inserts") or []):
        location = f"inserts/{index}"
        if not isinstance(insert, dict):
            result.add("methodical.insert_type", "Вставка должна быть объектом", path=path, location=location)
            continue
        insert_id = str(insert.get("insert_id") or "")
        if insert_id in seen_ids:
            result.add("methodical.duplicate_id", f"Повторный insert_id {insert_id}", path=path)
        seen_ids.add(insert_id)
        section_id = str(insert.get("section_id") or "")
        section = sections.get(section_id)
        if section is None:
            result.add(
                "methodical.unknown_section",
                f"Вставка {insert_id} ссылается на неизвестный section_id {section_id}",
                path=path,
                location=location,
            )
            continue
        per_section[section_id].append(insert)
        ordinal = int(section.get("number") or 0)
        expected_question_number = question_number(lecture_number, ordinal)
        if insert.get("question_number") != expected_question_number:
            result.add(
                "methodical.question_number",
                f"Для {insert_id} ожидается question_number={expected_question_number}",
                path=path,
                location=location,
            )

        insert_type = str(insert.get("type") or "")
        claim_ids = {str(item) for item in insert.get("claim_ids") or []}
        evidence_ids = {str(item) for item in insert.get("evidence_ids") or []}
        hypothetical = insert.get("hypothetical") is True
        for claim_id in claim_ids:
            claim = claim_map.get(claim_id)
            if claim is None:
                result.add("methodical.unknown_claim", f"Неизвестный claim_id {claim_id}", path=path)
            elif claim.get("status") == "unsupported":
                result.add("methodical.unsupported_claim", f"Вставка использует unsupported claim {claim_id}", path=path)
        for evidence_id in evidence_ids:
            if evidence_id not in evidence_map:
                result.add("methodical.unknown_evidence", f"Неизвестный evidence_id {evidence_id}", path=path)
        hypothetical_allowed = insert_type == "thematic_example"
        if hypothetical and not hypothetical_allowed:
            result.add(
                "methodical.hypothetical_type",
                f"hypothetical разрешён только для thematic_example, получено {insert_type}",
                path=path,
                location=location,
            )
        if insert_type in FACT_BEARING_TYPES and not (claim_ids or evidence_ids):
            if not (insert_type == "thematic_example" and hypothetical):
                result.add(
                    "methodical.missing_evidence",
                    f"Вставка {insert_id} должна ссылаться на claim/evidence; только illustrative thematic_example может быть hypothetical",
                    path=path,
                    location=location,
                )

        body_words = len(WORD_RE.findall(str(insert.get("body") or "")))
        declared_words = int(insert.get("word_count") or 0)
        if declared_words and abs(declared_words - body_words) > 3:
            result.add(
                "methodical.word_count",
                f"word_count для {insert_id} не соответствует тексту",
                severity="warning",
                path=path,
                details={"declared": declared_words, "actual": body_words},
            )

    if enabled:
        minimum = int(settings.get("min_inserts_per_section") or 3)
        maximum = int(settings.get("max_inserts_per_section") or 5)
        required_functions = {str(item) for item in settings.get("required_functions") or []}
        max_share = float(settings.get("max_word_share") or 0.15)
        for section_id, section in sections.items():
            inserts = per_section.get(section_id, [])
            if len(inserts) < minimum:
                result.add(
                    "methodical.too_few",
                    f"Для {section_id} требуется не менее {minimum} методических вставок",
                    path=path,
                )
            if len(inserts) > maximum:
                result.add(
                    "methodical.too_many",
                    f"Для {section_id} допускается не более {maximum} методических вставок",
                    path=path,
                )
            functions = {
                str(function)
                for insert in inserts
                for function in (insert.get("learning_functions") or [])
            }
            missing_functions = sorted(required_functions - functions)
            if missing_functions:
                result.add(
                    "methodical.function_coverage",
                    f"Для {section_id} не покрыты функции {missing_functions}",
                    path=path,
                )
            insert_words = sum(len(WORD_RE.findall(str(insert.get("body") or ""))) for insert in inserts)
            budget = int(section.get("word_budget") or 0)
            if budget and insert_words > budget * max_share:
                result.add(
                    "methodical.density",
                    f"Методические вставки {section_id} занимают слишком большую долю текста",
                    severity="warning",
                    path=path,
                    details={"insert_words": insert_words, "section_budget": budget, "max_share": max_share},
                )

    for relative, markdown in (markdown_values or {}).items():
        for insert in value.get("inserts") or []:
            if not isinstance(insert, dict) or insert.get("required") is False:
                continue
            marker = insert_marker(str(insert.get("insert_id") or ""))
            if marker not in markdown:
                result.add(
                    "methodical.marker_missing",
                    f"Обязательная вставка {insert.get('insert_id')} отсутствует в {relative}",
                    path=relative,
                )

    result.metrics = {
        "inserts": len(value.get("inserts") or []),
        "sections": len(per_section),
        "enabled": enabled,
    }
    return result
