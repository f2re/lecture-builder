from __future__ import annotations

from typing import Any
from fnmatch import fnmatchcase

# Final reviews certify the numbered, immutable final text; publication cannot edit it.
STAGE_DEPENDENCIES: dict[str, tuple[str, ...]] = {
    "config": (),
    "research-search": ("config",),
    "research-extract": ("research-search",),
    "evidence": ("research-extract",),
    "architecture": ("evidence",),
    "sections": ("architecture",),
    "number-structure": ("sections",),
    "methodical-enrichment": ("number-structure",),
    "visual-planning": ("number-structure",),
    "render-charts": ("visual-planning",),
    "assembly": ("methodical-enrichment", "render-charts"),
    "review-scientific": ("assembly",),
    "review-pedagogical": ("assembly",),
    "edit": ("review-scientific", "review-pedagogical"),
    "number-formulas": ("edit",),
    "final-reviews": ("number-formulas",),
    "fact-check": ("final-reviews",),
    "publish-docx": ("fact-check",),
}
REQUIRED_STAGES = tuple(STAGE_DEPENDENCIES)
OWNER_BY_CATEGORY = {
    "source": ("source-extractor", "research-extract"),
    "citation": ("evidence-curator", "evidence"),
    "evidence": ("evidence-curator", "evidence"),
    "formula": ("section-writer", "sections"),
    "example": ("section-writer", "sections"),
    "visual": ("visualization-planner", "visual-planning"),
    "methodical": ("methodical-enhancer", "methodical-enrichment"),
    "pedagogy": ("lecture-architect", "architecture"),
    "coherence": ("coherence-editor", "assembly"),
    "formatting": ("publisher", "publish-docx"),
}


def descendants(stage: str) -> set[str]:
    if stage not in STAGE_DEPENDENCIES:
        raise ValueError(f"Unknown stage: {stage}")
    affected = {stage}
    while True:
        added = {name for name, parents in STAGE_DEPENDENCIES.items() if set(parents) & affected}
        if added <= affected:
            return affected
        affected |= added


def invalidate(manifest: dict[str, Any], stage: str, reason: str) -> list[str]:
    affected = descendants(stage)
    records = manifest.setdefault("stages", {})
    for name in affected:
        if isinstance(records.get(name), dict):
            records[name]["status"] = "stale"
            records[name].setdefault("notes", []).append(reason)
    return [name for name in REQUIRED_STAGES if name in affected]


def ready_stages(manifest: dict[str, Any]) -> list[str]:
    records = manifest.get("stages") or {}
    complete = {name for name, item in records.items() if isinstance(item, dict) and item.get("status") == "complete"}
    return [name for name, parents in STAGE_DEPENDENCIES.items() if name not in complete and set(parents) <= complete]


def route_findings(reports: dict[str, Any], *, cycle: int, max_cycles: int) -> dict[str, Any]:
    """Build typed repair requests, never edit a scientific result in the orchestrator."""
    if type(cycle) is not int or type(max_cycles) is not int or cycle < 1 or max_cycles < 1:
        raise ValueError("cycle and max_cycles must be positive integers")
    requests = []
    seen = set()
    for role, report in sorted(reports.items()):
        if not isinstance(report, dict) or not isinstance(report.get("findings"), list):
            raise ValueError(f"Malformed review: {role}")
        for finding in report["findings"]:
            if not isinstance(finding, dict):
                raise ValueError("Malformed finding")
            if finding.get("severity") not in {"critical", "major"}:
                continue
            fid = finding.get("finding_id")
            if not isinstance(fid, str) or not fid or (role, fid) in seen:
                raise ValueError("Missing or duplicate finding id")
            seen.add((role, fid))
            category = finding.get("category", "pedagogy" if role == "pedagogical" else "evidence")
            if category not in OWNER_BY_CATEGORY:
                raise ValueError(f"Unknown repair category: {category}")
            owner, stage = OWNER_BY_CATEGORY[category]
            requests.append({
                "request_id": f"{role}:{fid}:{cycle}", "review_type": role,
                "finding_id": fid, "category": category, "owner": owner,
                "restart_stage": stage, "section": finding.get("section"),
                "required_action": finding.get("required_action", ""),
                "status": "pending", "cycle": cycle,
            })
    exhausted = bool(requests) and cycle > max_cycles
    return {"schema_version": "1.0", "status": "blocked" if exhausted else "ready",
            "reason": "review_cycle_budget_exhausted" if exhausted else None,
            "requests": requests, "cycle": cycle, "max_cycles": max_cycles}


STAGE_OUTPUTS: dict[str, tuple[str, ...]] = {
    "config": ("output/stages/config.json",),
    "research-search": ("output/lit/local_index.json", "output/lit/search_results.json", "output/lit/search_log.md"),
    "research-extract": ("output/lit/extracted_fragments.json", "output/lit/fetch_log.md"),
    "evidence": ("output/bibliography.json", "output/evidence_ledger.json", "output/literature_map.md", "output/key_concepts.md"),
    "architecture": ("output/lecture_blueprint.json", "output/lecture_blueprint.md", "output/section_briefs/section_*.json"),
    "sections": ("output/sections/section_*.md",),
    "number-structure": ("output/stages/number_structure.json",),
    "methodical-enrichment": ("output/methodical_inserts.json",),
    "visual-planning": ("output/plans/chart_specs.json", "output/plans/figures_index.json", "output/image_prompts.md"),
    "render-charts": ("output/chart_specs.json", "output/figures_index.json"),
    "assembly": ("output/lecture_draft.md",),
    "review-scientific": ("output/reviews/draft/scientific.json",),
    "review-pedagogical": ("output/reviews/draft/pedagogical.json",),
    "edit": ("output/lecture_edited.md", "output/edit_log.md", "output/reviews/resolution.pending.json"),
    "number-formulas": ("output/lecture_final.md", "output/formula_registry.json"),
    "final-reviews": ("output/reviews/scientific.json", "output/reviews/pedagogical.json", "output/reviews/resolution.json"),
    "fact-check": ("output/reviews/fact_check.json",),
    "publish-docx": ("output/lecture_final.docx",),
}


def expected_outputs_present(stage: str, outputs: list[str]) -> bool:
    return all(any(fnmatchcase(path, pattern) for path in outputs) for pattern in STAGE_OUTPUTS.get(stage, ()))


def next_stages(root: Any, manifest: dict[str, Any]) -> list[str]:
    from .manifest import stage_is_fresh
    for name in REQUIRED_STAGES:
        record = (manifest.get("stages") or {}).get(name) or {}
        if record.get("status") == "complete" and not stage_is_fresh(manifest, root, name, record.get("inputs", []), record.get("outputs", [])):
            invalidate(manifest, name, "Content or validation changed")
    return ready_stages(manifest)
