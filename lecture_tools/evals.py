from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import load_json
from .pipeline import run_validation

CATEGORY_PREFIXES = {
    "scientific_accuracy": (
        "claim.",
        "claim_marker.unsupported",
        "evidence.",
        "review.fact_check",
        "review.block",
        "formula.",
    ),
    "source_fidelity": ("bibliography.", "citation.", "evidence.", "claim_marker."),
    "logical_coherence": ("coherence.", "blueprint.section", "blueprint.concept", "brief.blueprint"),
    "pedagogical_accessibility": (
        "readability.",
        "brief.",
        "blueprint.competency",
        "blueprint.time",
        "review.unresolved",
    ),
    "terminology": ("blueprint.concept", "coherence.duplicate", "config.competency"),
    "formulas_units": ("formula.", "docx.equation", "docx.omml"),
    "formatting": ("docx.", "figures.", "schema.", "artifact."),
}


def _dimension_penalty(findings: list[dict[str, Any]], prefixes: tuple[str, ...]) -> tuple[int, list[dict[str, Any]]]:
    relevant = [item for item in findings if any(str(item.get("code", "")).startswith(prefix) for prefix in prefixes)]
    penalty = 0
    for item in relevant:
        penalty += 20 if item.get("severity") == "error" else 5 if item.get("severity") == "warning" else 1
    return min(100, penalty), relevant


def evaluate_project(root: str | Path, *, strict: bool = True) -> dict[str, Any]:
    base = Path(root)
    rubric = load_json(base / "evals/rubrics/lecture-quality.json")
    validation = run_validation(base, mode="all", strict=strict)
    findings = [
        finding
        for check in validation["checks"]
        for finding in check.get("findings", [])
    ]
    dimensions: list[dict[str, Any]] = []
    weighted_total = 0.0
    for dimension in rubric["dimensions"]:
        penalty, relevant = _dimension_penalty(findings, CATEGORY_PREFIXES[dimension["id"]])
        score = max(0, 100 - penalty)
        weighted_total += score * float(dimension["weight"])
        dimensions.append(
            {
                **dimension,
                "score": score,
                "findings": relevant,
            }
        )

    policy = rubric["release_policy"]
    minimum_dimension = min((item["score"] for item in dimensions), default=0)
    blockers = [item for item in findings if item.get("severity") == "error"]
    total = round(weighted_total, 2)
    release = (
        (not policy.get("block_on_validation_error") or not blockers)
        and total >= policy["minimum_total"]
        and minimum_dimension >= policy["minimum_dimension"]
    )
    return {
        "schema_version": "3.0",
        "root": str(base.resolve()),
        "strict": strict,
        "release": release,
        "total_score": total,
        "minimum_dimension_score": minimum_dimension,
        "dimensions": dimensions,
        "validation_summary": validation["summary"],
        "validation_score": validation["score"],
        "blockers": blockers,
    }
