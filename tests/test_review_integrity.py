import hashlib

from lecture_tools.review_integrity import REQUIRED_CHECKS, validate_review_integrity


def _digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fixture(tmp_path, *, major=False):
    paths = (
        "output/lecture_draft.md",
        "output/lecture_final.md",
        "output/evidence_ledger.json",
        "output/bibliography.json",
    )
    for relative in paths:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(relative, encoding="utf-8")
    reports = {}
    for role in ("scientific", "pedagogical", "fact_check"):
        artifacts = {path: _digest(tmp_path / path) for path in paths}
        checks = {key: "pass" for key in REQUIRED_CHECKS[role]}
        report = {
            "review_type": role,
            "status": "pass",
            "reviewer_id": f"reviewer-{role}",
            "findings": [],
            "checks": checks,
            "not_applicable_reasons": {},
            "reviewed_artifacts": artifacts,
        }
        if role == "fact_check":
            report["coverage"] = {"claim_ids": ["claim-1"]}
        reports[role] = report
    if major:
        reports["scientific"]["findings"] = [
            {"finding_id": "f-1", "severity": "major"}
        ]
    return reports


def test_empty_findings_pass_reports_are_valid(tmp_path):
    reports = _fixture(tmp_path)
    result = validate_review_integrity(
        reports, {"resolutions": []}, tmp_path, required_claim_ids={"claim-1"}
    )
    assert result.ok, result.to_dict()


def test_stale_artifact_hash_fails(tmp_path):
    reports = _fixture(tmp_path)
    reports["scientific"]["reviewed_artifacts"]["output/lecture_draft.md"] = "0" * 64
    result = validate_review_integrity(reports, {"resolutions": []}, tmp_path, required_claim_ids={"claim-1"})
    assert "review.artifact_stale" in {item.code for item in result.errors}


def test_missing_fact_check_coverage_fails(tmp_path):
    reports = _fixture(tmp_path)
    reports["fact_check"]["coverage"]["claim_ids"] = []
    result = validate_review_integrity(reports, {"resolutions": []}, tmp_path, required_claim_ids={"claim-1"})
    assert "review.coverage_missing" in {item.code for item in result.errors}


def test_major_fix_must_be_resolved_and_rechecked(tmp_path):
    reports = _fixture(tmp_path, major=True)
    result = validate_review_integrity(reports, {"resolutions": []}, tmp_path, required_claim_ids={"claim-1"})
    assert {"review.fix_unresolved", "review.pass_with_major_finding"} <= {item.code for item in result.errors}


def test_valid_resolved_fix_has_original_reviewer_recheck(tmp_path):
    reports = _fixture(tmp_path)
    final_hash = _digest(tmp_path / "output/lecture_final.md")
    resolution = {
        "resolutions": [{
            "review_type": "scientific",
            "finding_id": "f-1",
            "status": "resolved",
            "editor_id": "editor-1",
            "recheck": {
                "verdict": "pass",
                "reviewer_id": "reviewer-scientific",
                "reviewed_artifacts": {"output/lecture_final.md": final_hash},
            },
        }]
    }
    result = validate_review_integrity(reports, resolution, tmp_path, required_claim_ids={"claim-1"})
    assert "review.fix_unresolved" not in {item.code for item in result.errors}
    assert "review.fix_unchecked" not in {item.code for item in result.errors}
    assert result.ok, result.to_dict()


def test_empty_pass_cannot_certify_lecture(tmp_path):
    reports = _fixture(tmp_path)
    reports["fact_check"]["checks"] = {}
    assert not validate_review_integrity(reports, {"resolutions":[]}, tmp_path, required_claim_ids={"claim-1"}).ok


def test_same_reviewer_for_multiple_roles_fails(tmp_path):
    reports = _fixture(tmp_path)
    reports["pedagogical"]["reviewer_id"] = reports["scientific"]["reviewer_id"]
    assert not validate_review_integrity(reports, {"resolutions":[]}, tmp_path, required_claim_ids={"claim-1"}).ok
