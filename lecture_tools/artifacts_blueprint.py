from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .artifact_common import _claim_map
from .models import ValidationResult


def validate_blueprint(
    blueprint: Any,
    config: dict[str, Any],
    evidence: Any,
    *,
    path: str | Path | None = None,
) -> ValidationResult:
    result = ValidationResult(name="lecture-blueprint-crossrefs")
    if not isinstance(blueprint, dict):
        result.add("blueprint.type", "Blueprint должен быть объектом", path=path)
        return result

    sections = blueprint.get("sections") or []
    if not isinstance(sections, list):
        result.add("blueprint.sections", "Поле sections должно быть массивом", path=path)
        return result

    questions = config.get("questions") or []
    numbers = [item.get("number") for item in sections if isinstance(item, dict)]
    expected = list(range(1, len(questions) + 1))
    if numbers != expected:
        result.add(
            "blueprint.section_sequence",
            f"Ожидалась последовательность разделов {expected}, получено {numbers}",
            path=path,
        )

    claim_map = _claim_map(evidence)
    total_minutes = 0
    total_words = 0
    formula_owners: dict[str, int] = {}
    covered_competencies: set[str] = set()
    for index, section in enumerate(sections, start=1):
        if not isinstance(section, dict):
            result.add("blueprint.section_type", "Раздел blueprint должен быть объектом", path=path, location=str(index - 1))
            continue
        total_minutes += int(section.get("minutes") or 0)
        total_words += int(section.get("word_budget") or 0)
        claims = section.get("claim_ids") or []
        if not claims:
            result.add(
                "blueprint.claims_empty",
                f"Раздел {index} не содержит обязательных научных claim_id",
                path=path,
                location=f"sections/{index - 1}",
            )
        for claim_id in claims:
            claim = claim_map.get(str(claim_id))
            if claim is None:
                result.add(
                    "blueprint.unknown_claim",
                    f"Раздел {index} ссылается на неизвестный claim_id {claim_id}",
                    path=path,
                    location=f"sections/{index - 1}",
                )
            elif claim.get("status") == "unsupported":
                result.add(
                    "blueprint.unsupported_claim",
                    f"Раздел {index} включает неподтверждённый тезис {claim_id}",
                    path=path,
                    location=f"sections/{index - 1}",
                )
            elif claim.get("status") == "partial":
                result.add(
                    "blueprint.partial_claim",
                    f"Тезис {claim_id} подтверждён частично; ограничение должно быть включено в brief",
                    severity="warning",
                    path=path,
                    location=f"sections/{index - 1}",
                )
        for formula_id in section.get("formula_ids") or []:
            if formula_id in formula_owners:
                result.add(
                    "blueprint.formula_owner",
                    f"Формула {formula_id} назначена разделам {formula_owners[formula_id]} и {index}",
                    path=path,
                )
            else:
                formula_owners[str(formula_id)] = index
        covered_competencies.update(str(item) for item in section.get("competency_codes") or [])

    academic_minutes = round(float(config.get("hours") or 0) * 45)
    if total_minutes > academic_minutes:
        result.add(
            "blueprint.time_budget",
            f"Сумма времени разделов {total_minutes} мин превышает {academic_minutes} мин",
            path=path,
        )
    elif academic_minutes and total_minutes < academic_minutes * 0.75:
        result.add(
            "blueprint.time_underuse",
            f"Распределено только {total_minutes} из {academic_minutes} мин",
            severity="warning",
            path=path,
        )

    word_limit = int((config.get("quality") or {}).get("word_budget_per_hour", 4000) * float(config.get("hours") or 0))
    if word_limit and total_words > word_limit:
        result.add(
            "blueprint.word_budget",
            f"Суммарный бюджет {total_words} слов превышает лимит {word_limit}",
            path=path,
        )

    competency_codes = set()
    competency_re = re.compile(r"\b(?:ОК|УК|ОПК|ПК)-\d+(?:\.\d+)?\b", re.IGNORECASE)
    for item in config.get("competencies") or []:
        match = competency_re.search(str(item))
        if match:
            competency_codes.add(match.group(0).upper())
    missing_competencies = sorted(competency_codes - {item.upper() for item in covered_competencies})
    if missing_competencies:
        result.add(
            "blueprint.competency_coverage",
            "Не все компетенции сопоставлены разделам",
            path=path,
            details={"missing": missing_competencies},
        )

    graph = blueprint.get("concept_graph") or {}
    nodes = graph.get("nodes") or [] if isinstance(graph, dict) else []
    edges = graph.get("edges") or [] if isinstance(graph, dict) else []
    node_ids = [str(item.get("id")) for item in nodes if isinstance(item, dict) and item.get("id")]
    if len(node_ids) != len(set(node_ids)):
        result.add("blueprint.concept_duplicate", "В графе понятий есть повторные id", path=path)
    node_set = set(node_ids)
    adjacency: dict[str, list[str]] = {node: [] for node in node_set}
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        source = str(edge.get("from"))
        target = str(edge.get("to"))
        if source not in node_set or target not in node_set:
            result.add(
                "blueprint.concept_edge",
                f"Ребро {source} → {target} ссылается на неизвестный узел",
                path=path,
            )
            continue
        adjacency[source].append(target)

    state: dict[str, int] = {node: 0 for node in node_set}

    def visit(node: str) -> bool:
        state[node] = 1
        for target in adjacency[node]:
            if state[target] == 1:
                return True
            if state[target] == 0 and visit(target):
                return True
        state[node] = 2
        return False

    if any(state[node] == 0 and visit(node) for node in node_set):
        result.add("blueprint.concept_cycle", "Граф зависимостей понятий содержит цикл", path=path)

    result.metrics = {
        "sections": len(sections),
        "minutes": total_minutes,
        "word_budget": total_words,
        "claims_available": len(claim_map),
        "competencies_covered": len(covered_competencies),
        "concept_nodes": len(node_set),
    }
    return result
