from lecture_tools.citations import (
    validate_bibliography,
    validate_citations,
    validate_claim_markers,
    validate_evidence,
)


def test_verified_citations_and_claim_markers_pass(bibliography, evidence) -> None:
    markdown = (
        "Толщина слоя зависит от температуры [@src_001, с. 45]. "
        "<!-- claim:claim_q1_01 -->"
    )
    assert validate_bibliography(bibliography).ok
    assert validate_evidence(evidence, bibliography).ok
    assert validate_citations(markdown, bibliography).ok
    assert validate_claim_markers(
        markdown,
        evidence,
        required_claim_ids={"claim_q1_01"},
    ).ok


def test_unknown_source_and_unverified_page_fail(bibliography) -> None:
    unverified = [dict(bibliography[0], metadata_status="partial", verified_pages=False)]
    result = validate_citations(
        "Факт [@src_missing]. Другой факт [@src_001, с. 45].",
        unverified,
    )
    codes = {item.code for item in result.errors}
    assert "citation.unknown_source" in codes
    assert "citation.unverified_page" in codes


def test_missing_required_claim_marker_fails(evidence) -> None:
    result = validate_claim_markers(
        "Текст без маркера.",
        evidence,
        required_claim_ids={"claim_q1_01"},
    )
    assert any(item.code == "claim_marker.missing" for item in result.errors)
