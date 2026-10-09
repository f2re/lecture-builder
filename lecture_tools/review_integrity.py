from __future__ import annotations

import hashlib
import re
from pathlib import Path, PureWindowsPath
from typing import Any

from .models import ValidationResult

REQUIRED_CHECKS = {
    "scientific": (
        "formula_and_unit_accuracy",
        "worked_example_arithmetic",
        "visual_data_integrity",
        "claim_evidence_alignment",
        "technical_accuracy",
        "uncertainty_and_limitations",
    ),
    "pedagogical": (
        "assessment_and_answer_alignment",
        "delivery_time_fit",
        "methodical_insert_value",
        "learning_objective_alignment",
        "prerequisite_scaffolding",
        "instructional_clarity",
    ),
    "fact_check": (
        "unmarked_claim_detection",
        "post_edit_scope_and_negation",
        "final_formula_and_visual_checks",
        "claim_source_traceability",
        "citation_support",
        "date_and_quantifier_accuracy",
    ),
}
_ROLES = ("scientific", "pedagogical", "fact_check")
_ROLE_ARTIFACT = {
    "scientific": "output/lecture_final.md",
    "pedagogical": "output/lecture_final.md",
    "fact_check": "output/lecture_final.md",
}
_SHARED_ARTIFACTS = ("output/evidence_ledger.json", "output/bibliography.json")
_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")


def validate_review_integrity(
    reports: Any,
    resolution: Any,
    root: str | Path,
    *,
    strict: bool = True,
    required_claim_ids: set[str] | None = None,
) -> ValidationResult:
    """Validate review traceability and artifact integrity, not review correctness."""
    result = ValidationResult(name="review-integrity")
    try:
        if not isinstance(reports, dict):
            result.add("review.reports_type", "Reports must be an object")
            return result
        try:
            base = Path(root).resolve()
        except (TypeError, ValueError, OSError):
            result.add("review.root_invalid", "Review root is not a usable path")
            return result

        if required_claim_ids is not None and (
            not isinstance(required_claim_ids, set)
            or any(not isinstance(item, str) or not item for item in required_claim_ids)
        ):
            result.add("review.required_claim_ids_invalid", "required_claim_ids must be a set of nonempty strings")
            return result

        if strict:
            for role in _ROLES:
                if role not in reports:
                    result.add("review.report_missing", f"Required {role} report is missing")
        resolution_map: dict[tuple[str, str], dict[str, Any]] = {}
        resolution_items = resolution.get("resolutions") if isinstance(resolution, dict) else None
        if not isinstance(resolution_items, list):
            result.add("review.resolutions_invalid", "Resolution must contain a resolutions array")
            resolution_items = []
        for item in resolution_items:
            if not isinstance(item, dict):
                result.add("review.resolution_invalid", "Resolution entry must be an object")
                continue
            role, finding_id = item.get("review_type"), item.get("finding_id")
            if not isinstance(role, str) or not isinstance(finding_id, str) or not finding_id:
                result.add("review.resolution_identity", "Resolution entry has invalid review_type or finding_id")
                continue
            key = (role, finding_id)
            if key in resolution_map:
                result.add("review.resolution_duplicate", f"Duplicate resolution for {role}/{finding_id}")
            else:
                resolution_map[key] = item

        reviewer_ids: list[str] = []
        for role in (*_ROLES, *sorted(key for key in reports if key not in _ROLES)):
            if role not in reports:
                continue
            report = reports[role]
            if not isinstance(report, dict):
                result.add("review.report_invalid", f"{role} report must be an object")
                continue
            if report.get("review_type") != role:
                result.add("review.type_mismatch", f"Report key {role} does not match review_type")
            status = report.get("status")
            if status not in {"pass", "revise", "block"}:
                result.add("review.status_invalid", f"{role} has an invalid status")
            if strict and status != "pass":
                result.add("review.status_blocks_release", f"{role} status must be pass for strict release")
            findings = report.get("findings")
            if not isinstance(findings, list):
                result.add("review.findings_invalid", f"{role} findings must be an array")
                findings = []
            if status in {"revise", "block"} and not findings:
                result.add("review.findings_required", f"{role} status {status} requires findings")
            for finding in findings:
                if not isinstance(finding, dict):
                    result.add("review.finding_invalid", f"{role} contains a malformed finding")
                    continue
                severity = finding.get("severity")
                finding_id = finding.get("finding_id")
                if severity in {"critical", "major"}:
                    if status == "pass":
                        result.add("review.pass_with_major_finding", f"{role}/{finding_id} is {severity} in a pass report")
                    if role in {"scientific", "pedagogical"}:
                        _check_resolution(result, role, finding_id, report, resolution_map, base)
            if strict:
                reviewer = report.get("reviewer_id")
                if not isinstance(reviewer, str) or not reviewer.strip():
                    result.add("review.reviewer_missing", f"{role} requires a nonempty reviewer_id")
                else:
                    reviewer_ids.append(reviewer.strip())

            checks = report.get("checks")
            if not isinstance(checks, dict):
                result.add("review.checks_invalid", f"{role} checks must be an object")
                checks = {}
            if strict and role in REQUIRED_CHECKS:
                for check in REQUIRED_CHECKS[role]:
                    if check not in checks:
                        result.add("review.check_missing", f"{role} mandatory check {check} is missing")
            reasons = report.get("not_applicable_reasons", {})
            if not isinstance(reasons, dict):
                result.add("review.not_applicable_reasons_invalid", f"{role} not_applicable_reasons must be an object")
                reasons = {}
            for check, value in sorted(checks.items(), key=lambda pair: str(pair[0])):
                if value not in {"pass", "fail", "warning", "not_applicable"}:
                    result.add("review.check_status_invalid", f"{role} check {check} has an invalid status")
                elif strict and value in {"fail", "warning"}:
                    result.add("review.check_blocks_release", f"{role} check {check} is {value}")
                elif strict and value == "not_applicable" and check in {"claim_evidence_alignment", "learning_objective_alignment", "claim_source_traceability", "citation_support", "unmarked_claim_detection"}:
                    result.add("review.core_check_waived", f"{role} core check {check} cannot be waived")
                elif value == "not_applicable" and (
                    not isinstance(reasons.get(check), str) or not reasons[check].strip()
                ):
                    result.add("review.check_reason_missing", f"{role} check {check} needs a not-applicable reason")

            artifacts = report.get("reviewed_artifacts")
            if not isinstance(artifacts, dict):
                result.add("review.artifacts_invalid", f"{role} reviewed_artifacts must be a path-to-SHA256 object")
                continue
            required_paths = list(_SHARED_ARTIFACTS)
            if role in _ROLE_ARTIFACT:
                required_paths.insert(0, _ROLE_ARTIFACT[role])
            for optional in ("output/lecture_blueprint.json", "output/methodical_inserts.json", "output/chart_specs.json", "output/figures_index.json"):
                if (base / optional).is_file():
                    required_paths.append(optional)
            for path in required_paths:
                if path not in artifacts:
                    result.add("review.artifact_missing", f"{role} did not record {path}")
            for path, digest in sorted(artifacts.items(), key=lambda pair: str(pair[0])):
                _check_artifact(result, base, role, path, digest)

        for (role, finding_id), item in resolution_map.items():
            if role in {"scientific", "pedagogical"} and item.get("status") == "resolved":
                _check_resolution(result, role, finding_id, reports.get(role, {}), resolution_map, base)
            elif strict and item.get("status") != "resolved":
                result.add("review.fix_unresolved", f"Unresolved correction: {role}/{finding_id}")

        if strict and len(reviewer_ids) != len(set(reviewer_ids)):
            result.add("review.reviewer_not_isolated", "Strict release requires distinct reviewer_id values")

        fact = reports.get("fact_check")
        if isinstance(fact, dict):
            coverage = fact.get("coverage")
            claim_ids = coverage.get("claim_ids") if isinstance(coverage, dict) else None
            if not isinstance(claim_ids, list) or any(not isinstance(item, str) or not item for item in claim_ids):
                result.add("review.coverage_invalid", "fact_check coverage.claim_ids must be an array of nonempty strings")
            else:
                if len(claim_ids) != len(set(claim_ids)):
                    result.add("review.coverage_duplicate", "fact_check coverage.claim_ids contains duplicates")
                if not claim_ids and required_claim_ids != set():
                    result.add("review.coverage_empty", "Empty claim coverage is allowed only when required_claim_ids is empty")
                if required_claim_ids is not None:
                    missing = sorted(required_claim_ids - set(claim_ids))
                    if missing:
                        result.add("review.coverage_missing", "fact_check coverage omits required claim ids", details={"claim_ids": missing})

        result.metrics = {"reports": len(reports), "resolutions": len(resolution_map)}
    except Exception as exc:  # Fail closed for malformed, externally supplied data.
        result.add("review.validation_error", "Malformed review input prevented integrity validation", details={"error": type(exc).__name__})
    return result


def _check_artifact(result: ValidationResult, base: Path, role: str, path: Any, digest: Any) -> None:
    if not isinstance(path, str) or not path or not isinstance(digest, str) or not _SHA256.fullmatch(digest):
        result.add("review.artifact_entry_invalid", f"{role} has an invalid artifact path or SHA256")
        return
    try:
        if Path(path).is_absolute() or PureWindowsPath(path).drive:
            raise ValueError("artifact path must be relative")
        target = (base / path).resolve()
        target.relative_to(base)
        if not target.is_file():
            raise OSError("not a file")
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
    except (OSError, ValueError, RuntimeError):
        result.add("review.artifact_unavailable", f"{role} artifact is missing or escapes the review root: {path}")
        return
    if actual.lower() != digest.lower():
        result.add("review.artifact_stale", f"{role} artifact hash is stale: {path}")


def _check_resolution(
    result: ValidationResult,
    role: str,
    finding_id: Any,
    report: dict[str, Any],
    resolutions: dict[tuple[str, str], dict[str, Any]],
    base: Path,
) -> None:
    if not isinstance(finding_id, str) or not finding_id:
        result.add("review.finding_id_missing", f"{role} major/critical finding requires finding_id")
        return
    item = resolutions.get((role, finding_id))
    if not item or item.get("status") != "resolved":
        result.add("review.fix_unresolved", f"{role}/{finding_id} must have a resolved resolution")
        return
    recheck = item.get("recheck")
    if not isinstance(recheck, dict) or recheck.get("verdict") != "pass":
        result.add("review.fix_unchecked", f"{role}/{finding_id} requires a passing recheck")
        return
    original_reviewer = report.get("reviewer_id")
    if not isinstance(original_reviewer, str) or recheck.get("reviewer_id") != original_reviewer:
        result.add("review.recheck_reviewer_mismatch", f"{role}/{finding_id} must be rechecked by its original reviewer")
    editor = item.get("editor_id")
    if not isinstance(editor, str) or not editor.strip():
        result.add("review.editor_missing", f"{role}/{finding_id} resolution requires editor_id to exclude self-approval")
    elif recheck.get("reviewer_id") == editor:
        result.add("review.recheck_self_approval", f"{role}/{finding_id} editor cannot approve their own fix")
    artifacts = recheck.get("reviewed_artifacts")
    digest = artifacts.get("output/lecture_final.md") if isinstance(artifacts, dict) else None
    if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
        result.add("review.recheck_artifact_missing", f"{role}/{finding_id} recheck must hash output/lecture_final.md")
    else:
        _check_artifact(result, base, role, "output/lecture_final.md", digest)
