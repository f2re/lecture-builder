from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from .artifacts import (
    validate_blueprint,
    validate_figure_index,
    validate_formula_registry,
    validate_manifest_state,
    validate_review_state,
    validate_section_briefs,
)
from .citations import (
    normalize_bibliography,
    validate_bibliography,
    validate_citations,
    validate_claim_markers,
    validate_evidence,
)
from .coherence import validate_coherence
from .config import load_config, validate_config
from .docx_validation import validate_docx
from .formulas import validate_formula_markdown
from .io import dump_json, load_json
from .methodical import validate_methodical_inserts
from .models import Finding, ValidationResult
from .numbering import validate_document_numbering
from .project import validate_project
from .schemas import load_schema, validate_instance
from .visuals import validate_chart_specs, validate_figure_metadata

Mode = Literal["source", "artifacts", "all"]

ARTIFACT_SCHEMAS = {
    "output/lit/local_index.json": "local-index",
    "output/lit/search_results.json": "search-results",
    "output/lit/extracted_fragments.json": "extracted-fragments",
    "output/bibliography.json": "bibliography",
    "output/evidence_ledger.json": "evidence-ledger",
    "output/lecture_blueprint.json": "lecture-blueprint",
    "output/methodical_inserts.json": "methodical-inserts",
    "output/chart_specs.json": "chart-specs",
    "output/run_manifest.json": "run-manifest",
    "output/formula_registry.json": "formula-registry",
    "output/figures_index.json": "figures-index",
    "output/reviews/scientific.json": "review-report",
    "output/reviews/pedagogical.json": "review-report",
    "output/reviews/fact_check.json": "review-report",
    "output/reviews/resolution.json": "review-resolution",
}

REQUIRED_ARTIFACTS = [
    "output/lit/local_index.json",
    "output/lit/search_results.json",
    "output/lit/search_log.md",
    "output/lit/extracted_fragments.json",
    "output/lit/fetch_log.md",
    "output/bibliography.json",
    "output/evidence_ledger.json",
    "output/literature_map.md",
    "output/key_concepts.md",
    "output/lecture_blueprint.json",
    "output/lecture_blueprint.md",
    "output/methodical_inserts.json",
    "output/chart_specs.json",
    "output/lecture_draft.md",
    "output/reviews/scientific.json",
    "output/reviews/pedagogical.json",
    "output/reviews/resolution.json",
    "output/reviews/fact_check.json",
    "output/review_report.md",
    "output/lecture_final.md",
    "output/edit_log.md",
    "output/formula_registry.json",
    "output/image_prompts.md",
    "output/figures_index.json",
    "output/run_manifest.json",
]


def _read_json_result(path: Path) -> tuple[Any | None, ValidationResult]:
    result = ValidationResult(name=f"json:{path.name}")
    try:
        return load_json(path), result
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        result.add("json.parse", str(exc), path=path)
        return None, result


def _merge_findings(results: list[ValidationResult]) -> list[Finding]:
    return [finding for result in results for finding in result.findings]


def _score(findings: list[Finding]) -> int:
    errors = sum(1 for item in findings if item.severity == "error")
    warnings = sum(1 for item in findings if item.severity == "warning")
    return max(0, 100 - errors * 10 - warnings * 2)


def _attach_path(result: ValidationResult, path: Path) -> ValidationResult:
    result.findings = [
        Finding(**{**finding.to_dict(), "path": finding.path or str(path)})
        for finding in result.findings
    ]
    return result


def _required_artifacts_result(base: Path, config: dict[str, Any]) -> ValidationResult:
    result = ValidationResult(name="required-artifacts")
    for relative in REQUIRED_ARTIFACTS:
        path = base / relative
        if not path.is_file() or path.stat().st_size == 0:
            result.add("artifact.missing", "Обязательный артефакт отсутствует или пуст", path=path)
    expected = len(config.get("questions") or [])
    section_briefs = list((base / "output/section_briefs").glob("section_*.json"))
    section_files = list((base / "output/sections").glob("section_*.md"))
    if expected and len(section_briefs) != expected:
        result.add(
            "artifact.section_briefs",
            f"Ожидалось {expected} section briefs, найдено {len(section_briefs)}",
            path=base / "output/section_briefs",
        )
    if expected and len(section_files) != expected:
        result.add(
            "artifact.sections",
            f"Ожидалось {expected} section files, найдено {len(section_files)}",
            path=base / "output/sections",
        )
    return result


def validate_artifacts(root: str | Path, *, strict: bool = False) -> list[ValidationResult]:
    base = Path(root)
    results: list[ValidationResult] = []
    config_path = base / "input/lecture_config.md"
    config: dict[str, Any] = {}
    if config_path.is_file():
        try:
            config = load_config(config_path)
        except ValueError:
            pass

    if strict:
        results.append(_required_artifacts_result(base, config))

    loaded: dict[str, Any] = {}
    for relative, schema_name in ARTIFACT_SCHEMAS.items():
        path = base / relative
        if not path.is_file():
            continue
        value, parse_result = _read_json_result(path)
        results.append(parse_result)
        if value is None:
            continue
        loaded[relative] = value
        results.append(
            validate_instance(
                value,
                load_schema(base, schema_name),
                name=f"schema:{relative}",
                path=path,
            )
        )

    briefs: list[tuple[Path, Any]] = []
    for path in sorted((base / "output/section_briefs").glob("section_*.json")):
        value, parse_result = _read_json_result(path)
        results.append(parse_result)
        if value is None:
            continue
        briefs.append((path, value))
        results.append(
            validate_instance(
                value,
                load_schema(base, "section-brief"),
                name=f"schema:{path.name}",
                path=path,
            )
        )

    bibliography_path = base / "output/bibliography.json"
    bibliography: Any | None = loaded.get("output/bibliography.json")
    if bibliography is not None:
        results.append(validate_bibliography(bibliography, path=bibliography_path))

    evidence_path = base / "output/evidence_ledger.json"
    evidence = loaded.get("output/evidence_ledger.json")
    if evidence is not None and bibliography is not None:
        results.append(validate_evidence(evidence, bibliography, path=evidence_path))

    blueprint_path = base / "output/lecture_blueprint.json"
    blueprint = loaded.get("output/lecture_blueprint.json")
    if blueprint is not None and evidence is not None:
        results.append(validate_blueprint(blueprint, config, evidence, path=blueprint_path))
    if briefs and blueprint is not None and evidence is not None and bibliography is not None:
        results.append(validate_section_briefs(briefs, config, blueprint, evidence, bibliography))

    required_claim_ids: set[str] = set()
    for _, brief in briefs:
        if isinstance(brief, dict):
            required_claim_ids.update(str(item) for item in brief.get("required_claim_ids") or [])

    lecture_number = int(config.get("lecture_number") or 0) if config else 0
    markdown_values: dict[str, str] = {}
    for relative in ("output/lecture_draft.md", "output/lecture_final.md"):
        path = base / relative
        if not path.is_file():
            continue
        markdown = path.read_text(encoding="utf-8")
        markdown_values[relative] = markdown
        results.append(validate_coherence(markdown, config, path=path))
        results.append(validate_document_numbering(markdown, config, path=path))
        results.append(_attach_path(validate_formula_markdown(markdown, lecture_number or None), path))
        if bibliography is not None:
            citation_result = validate_citations(markdown, bibliography, path=path)
            if strict and relative == "output/lecture_final.md":
                for finding in citation_result.findings:
                    if finding.code == "citation.noncanonical":
                        finding.severity = "error"
            results.append(citation_result)
        if evidence is not None:
            results.append(
                validate_claim_markers(
                    markdown,
                    evidence,
                    required_claim_ids=required_claim_ids,
                    path=path,
                )
            )

    methodical = loaded.get("output/methodical_inserts.json")
    if methodical is not None and blueprint is not None and evidence is not None:
        results.append(
            validate_methodical_inserts(
                methodical,
                config,
                blueprint,
                evidence,
                markdown_values,
                path=base / "output/methodical_inserts.json",
            )
        )

    final_markdown = markdown_values.get("output/lecture_final.md", "")
    registry = loaded.get("output/formula_registry.json")
    if registry is not None and final_markdown and lecture_number:
        results.append(
            validate_formula_registry(
                registry,
                final_markdown,
                lecture_number=lecture_number,
                path=base / "output/formula_registry.json",
            )
        )
    if strict and config.get("formulas_required") and final_markdown and "\\tag{" not in final_markdown:
        formula_required = ValidationResult(name="formula-required")
        formula_required.add(
            "formula.required",
            "Конфигурация требует формулы, но финальный Markdown не содержит пронумерованных формул",
            path=base / "output/lecture_final.md",
        )
        results.append(formula_required)

    reports: dict[str, Any] = {}
    for review_type, relative in (
        ("scientific", "output/reviews/scientific.json"),
        ("pedagogical", "output/reviews/pedagogical.json"),
        ("fact_check", "output/reviews/fact_check.json"),
    ):
        value = loaded.get(relative)
        if value is not None:
            reports[review_type] = value
    if reports or strict:
        results.append(
            validate_review_state(
                reports,
                loaded.get("output/reviews/resolution.json"),
                strict=strict,
            )
        )

    source_ids: set[str] = set()
    if bibliography is not None:
        try:
            source_ids = {
                str(item.get("source_id") or item.get("id"))
                for item in normalize_bibliography(bibliography)
                if item.get("source_id") or item.get("id")
            }
        except ValueError:
            pass
    figures = loaded.get("output/figures_index.json")
    if figures is not None and final_markdown and lecture_number:
        results.append(
            validate_figure_index(
                figures,
                final_markdown,
                lecture_number=lecture_number,
                source_ids=source_ids,
                path=base / "output/figures_index.json",
            )
        )
        results.append(
            validate_figure_metadata(
                figures,
                config,
                final_markdown,
                root=base,
                path=base / "output/figures_index.json",
            )
        )
    charts = loaded.get("output/chart_specs.json")
    if charts is not None:
        known_claim_ids = {
            str(item.get("claim_id"))
            for item in ((evidence or {}).get("claims") or [])
            if isinstance(item, dict) and item.get("claim_id")
        }
        known_evidence_ids = {
            str(item.get("evidence_id"))
            for item in ((evidence or {}).get("evidence") or [])
            if isinstance(item, dict) and item.get("evidence_id")
        }
        results.append(
            validate_chart_specs(
                charts,
                figures,
                config,
                source_ids,
                claim_ids=known_claim_ids,
                evidence_ids=known_evidence_ids,
                root=base,
                path=base / "output/chart_specs.json",
            )
        )

    manifest = loaded.get("output/run_manifest.json")
    if manifest is not None:
        results.append(
            validate_manifest_state(
                manifest,
                base,
                path=base / "output/run_manifest.json",
            )
        )

    docx_path = base / "output/lecture_final.docx"
    if docx_path.is_file():
        results.append(validate_docx(docx_path, expect_formulas=bool(config.get("formulas_required"))))
    elif strict:
        missing_docx = ValidationResult(name="docx-required")
        missing_docx.add("artifact.docx", "Финальный DOCX отсутствует", path=docx_path)
        results.append(missing_docx)

    return results


def run_validation(
    root: str | Path,
    *,
    mode: Mode = "all",
    strict: bool = False,
    report_path: str | Path | None = None,
) -> dict[str, Any]:
    base = Path(root).resolve()
    results: list[ValidationResult] = []
    if mode in ("source", "all"):
        results.append(validate_project(base))
        results.append(validate_config(base / "input/lecture_config.md", base))
    if mode in ("artifacts", "all"):
        results.extend(validate_artifacts(base, strict=strict))

    findings = _merge_findings(results)
    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]
    report = {
        "schema_version": "3.0",
        "root": str(base),
        "mode": mode,
        "strict": strict,
        "ok": not errors,
        "score": _score(findings),
        "summary": {
            "checks": len(results),
            "errors": len(errors),
            "warnings": len(warnings),
            "findings": len(findings),
        },
        "checks": [result.to_dict() for result in results],
    }
    if report_path is not None:
        dump_json(report_path, report)
    return report
