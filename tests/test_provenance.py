import hashlib

from lecture_tools.provenance import validate_source_provenance


def fixture(tmp_path):
    text = "Opening text. Exact source passage with enough characters. Ending."
    source_file = tmp_path / "normalized.txt"
    raw = text.encode("utf-8")
    source_file.write_bytes(raw)
    exact = "Exact source passage with enough characters."
    start = text.index(exact)
    digest = "sha256:" + hashlib.sha256(raw).hexdigest()
    document_hash = digest
    (tmp_path / "original.txt").write_bytes(raw)
    fragments = [{
        "fragment_id": "frag_1", "source_id": "src_1", "exact_fragment": exact,
        "document_hash": document_hash, "document_path": "original.txt", "text_path": "normalized.txt", "text_hash": digest,
        "location": {"offset_start": start, "offset_end": start + len(exact), "page": 2, "page_label": "2"},
        "location_status": "verified",
    }]
    ledger = {
        "claims": [{"claim_id": "claim_1", "status": "supported", "evidence_ids": ["ev_1"]}],
        "evidence": [{
            "evidence_id": "ev_1", "fragment_id": "frag_1", "source_id": "src_1",
            "document_hash": document_hash, "exact_fragment": exact,
            "location": {"page": 2, "page_label": "2"}, "location_status": "verified",
            "supports_claims": ["claim_1"],
        }],
    }
    bibliography = [{"source_id": "src_1"}]
    return text, fragments, ledger, bibliography


def test_valid_local_provenance(tmp_path):
    _, fragments, ledger, bibliography = fixture(tmp_path)
    result = validate_source_provenance(tmp_path, fragments, ledger, bibliography)
    assert result.ok
    assert result.metrics["active_evidence"] == 1


def test_altered_local_text_fails_slice_and_hash(tmp_path):
    _, fragments, ledger, bibliography = fixture(tmp_path)
    (tmp_path / "normalized.txt").write_text("tampered local text", encoding="utf-8")
    result = validate_source_provenance(tmp_path, fragments, ledger, bibliography)
    assert not result.ok
    assert {finding.code for finding in result.errors} & {"provenance.text_hash", "provenance.slice"}


def test_altered_declared_text_hash_fails(tmp_path):
    _, fragments, ledger, bibliography = fixture(tmp_path)
    fragments[0]["text_hash"] = "sha256:" + "0" * 64
    result = validate_source_provenance(tmp_path, fragments, ledger, bibliography)
    assert "provenance.text_hash" in {finding.code for finding in result.errors}


def test_invented_fragment_fails(tmp_path):
    _, fragments, ledger, bibliography = fixture(tmp_path)
    ledger["evidence"][0]["fragment_id"] = "frag_invented"
    result = validate_source_provenance(tmp_path, fragments, ledger, bibliography)
    assert "provenance.unknown_fragment" in {finding.code for finding in result.errors}


def test_path_escape_fails(tmp_path):
    _, fragments, ledger, bibliography = fixture(tmp_path)
    outside = tmp_path.parent / "outside.txt"
    outside.write_text("Exact source passage with enough characters.", encoding="utf-8")
    fragments[0]["text_path"] = "../outside.txt"
    result = validate_source_provenance(tmp_path, fragments, ledger, bibliography)
    assert "provenance.path" in {finding.code for finding in result.errors}


def test_malformed_inputs_fail_closed(tmp_path):
    result = validate_source_provenance(tmp_path, {}, {"claims": [], "evidence": []}, [])
    assert not result.ok
    assert result.errors


def test_changed_original_source_is_rejected(tmp_path):
    _, fragments, ledger, bibliography = fixture(tmp_path)
    (tmp_path / "original.txt").write_text("changed original", encoding="utf-8")
    assert not validate_source_provenance(tmp_path, fragments, ledger, bibliography).ok


def test_unhashable_external_status_fails_closed(tmp_path):
    _, fragments, ledger, bibliography = fixture(tmp_path)
    ledger["claims"][0]["status"] = []
    assert not validate_source_provenance(tmp_path, fragments, ledger, bibliography).ok
