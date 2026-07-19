from __future__ import annotations

from pathlib import Path
from typing import Any

from .artifact_common import _claim_map, _evidence_map
from .citations import normalize_bibliography
from .models import ValidationResult
from .numbering import question_number, subsection_number


def validate_section_briefs(
    briefs: list[tuple[Path, Any]],
    config: dict[str, Any],
    blueprint: Any,
    evidence: Any,
    bibliography: Any,
) -> ValidationResult:
    result = ValidationResult(name="section-brief-crossrefs")
    claim_map = _claim_map(evidence)
    evidence_map = _evidence_map(evidence)
    try:
        source_ids = {
            str(item.get("source_id") or item.get("id"))
            for item in normalize_bibliography(bibliography)
            if item.get("source_id") or item.get("id")
        }
    except ValueError:
        source_ids = set()

    lecture_number = int(config.get("lecture_number") or 0)
    expected = len(config.get("questions") or [])
    seen_numbers: set[int] = set()
    output_files: set[str] = set()
    formula_owners: dict[str, int] = {}
    blueprint_sections = {
        int(item.get("number")): item
        for item in (blueprint.get("sections") or [])
        if isinstance(blueprint, dict) and isinstance(item, dict) and item.get("number")
    }

    for path, brief in briefs:
        if not isinstance(brief, dict):
            result.add("brief.type", "Section brief должен быть объектом", path=path)
            continue
        number = int(brief.get("number") or 0)
        if number in seen_numbers:
            result.add("brief.duplicate_number", f"Повторный brief для раздела {number}", path=path)
        seen_numbers.add(number)
        expected_display = question_number(lecture_number, number)
        if brief.get("display_number") != expected_display:
            result.add(
                "brief.display_number",
                f"Brief {number} должен иметь display_number={expected_display}",
                path=path,
            )
        output_file = str(brief.get("output_file") or "")
        if output_file in output_files:
            result.add("brief.duplicate_output", f"Повторный output_file {output_file}", path=path)
        output_files.add(output_file)
        if output_file and not output_file.startswith(f"output/sections/section_{number}_"):
            result.add("brief.output_number", "Номер output_file не совпадает с number", path=path)

        required_claims = {str(item) for item in brief.get("required_claim_ids") or []}
        if not required_claims:
            result.add("brief.claims_empty", "Brief не содержит required_claim_ids", path=path)
        for claim_id in required_claims:
            claim = claim_map.get(claim_id)
            if claim is None:
                result.add("brief.unknown_claim", f"Неизвестный claim_id {claim_id}", path=path)
            elif claim.get("status") == "unsupported":
                result.add("brief.unsupported_claim", f"Brief включает unsupported claim {claim_id}", path=path)

        required_evidence = {str(item) for item in brief.get("required_evidence_ids") or []}
        for evidence_id in required_evidence:
            if evidence_id not in evidence_map:
                result.add("brief.unknown_evidence", f"Неизвестный evidence_id {evidence_id}", path=path)
        for source_id in brief.get("allowed_source_ids") or []:
            if str(source_id) not in source_ids:
                result.add("brief.unknown_source", f"Неизвестный source_id {source_id}", path=path)

        blueprint_section = blueprint_sections.get(number)
        if blueprint_section:
            blueprint_claims = {str(item) for item in blueprint_section.get("claim_ids") or []}
            if required_claims != blueprint_claims:
                result.add(
                    "brief.blueprint_claims",
                    "required_claim_ids не совпадают с blueprint",
                    path=path,
                    details={"brief": sorted(required_claims), "blueprint": sorted(blueprint_claims)},
                )
            if brief.get("subsections") != blueprint_section.get("subsections"):
                result.add(
                    "brief.blueprint_subsections",
                    "Подразделы brief должны совпадать с blueprint",
                    path=path,
                )
            if set(brief.get("methodical_requirements") or []) != set(blueprint_section.get("methodical_requirements") or []):
                result.add(
                    "brief.blueprint_methodical",
                    "methodical_requirements brief должны совпадать с blueprint",
                    path=path,
                )
            if brief.get("visual_opportunities") != blueprint_section.get("visual_opportunities"):
                result.add(
                    "brief.blueprint_visuals",
                    "visual_opportunities brief должны совпадать с blueprint",
                    path=path,
                )

        subsections = brief.get("subsections") or []
        for sub_index, subsection in enumerate(subsections, start=1):
            expected_sub = subsection_number(lecture_number, number, sub_index)
            if not isinstance(subsection, dict) or subsection.get("number") != expected_sub:
                result.add(
                    "brief.subsection_number",
                    f"Ожидался номер подраздела {expected_sub}",
                    path=path,
                    location=f"subsections/{sub_index - 1}",
                )

        budget = brief.get("word_budget") or {}
        minimum = int(budget.get("min") or 0)
        target = int(budget.get("target") or 0)
        maximum = int(budget.get("max") or 0)
        if not (minimum <= target <= maximum):
            result.add("brief.word_budget", "Требуется min <= target <= max", path=path)

        for formula_id in brief.get("formula_ids") or []:
            formula_id = str(formula_id)
            if formula_id in formula_owners:
                result.add(
                    "brief.formula_owner",
                    f"Формула {formula_id} определена более чем в одном brief",
                    path=path,
                    details={"first_section": formula_owners[formula_id], "second_section": number},
                )
            else:
                formula_owners[formula_id] = number

    expected_numbers = set(range(1, expected + 1))
    if seen_numbers != expected_numbers:
        result.add(
            "brief.coverage",
            "Набор section briefs не совпадает с вопросами конфигурации",
            details={"expected": sorted(expected_numbers), "actual": sorted(seen_numbers)},
        )
    result.metrics = {"briefs": len(briefs), "claims": len(claim_map), "evidence": len(evidence_map)}
    return result
