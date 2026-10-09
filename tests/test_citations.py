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
    assert validate_citations(markdown, bibliography, evidence=evidence).ok
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


def test_page_counts_and_legacy_flags_are_not_evidence(bibliography):
    for pages in ("45", "45–999", "99999", "50–45"):
        result = validate_citations(f"Факт [@src_001, с. {pages}].", bibliography)
        assert any(f.code == "citation.unverified_page" for f in result.errors)


def test_printed_page_is_not_pdf_index(bibliography, evidence):
    evidence["evidence"][0]["location"]["page_label"] = "41"
    text = "Тезис [@src_001, с. 45]. <!-- claim:claim_q1_01 -->"
    assert not validate_citations(text, bibliography, evidence=evidence).ok
    assert validate_citations(text.replace("с. 45", "с. 41"), bibliography, evidence=evidence).ok


def test_page_citation_requires_adjacent_claim(bibliography, evidence):
    text = "Факт [@src_001, с. 45].\n\n<!-- claim:claim_q1_01 -->"
    assert not validate_citations(text, bibliography, evidence=evidence).ok


def test_unused_research_gap_does_not_block(bibliography, evidence):
    evidence["claims"].append({"claim_id":"claim_gap", "status":"unsupported", "evidence_ids":[]})
    assert validate_evidence(evidence, bibliography, used_claim_ids={"claim_q1_01"}).ok
    assert not validate_evidence(evidence, bibliography, used_claim_ids={"claim_gap"}).ok
