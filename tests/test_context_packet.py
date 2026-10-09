import pytest
from lecture_tools.context_packet import build_section_packet


def test_packet_contains_only_required_content(bibliography, evidence):
    brief={"section_id":"q1", "required_claim_ids":["claim_q1_01"], "allowed_source_ids":["src_001"]}
    packet=build_section_packet(brief,evidence,bibliography)
    assert len(packet["claims"]) == len(packet["evidence"]) == len(packet["sources"]) == 1
    assert packet["section_id"] == "q1"


def test_packet_rejects_unsupported(bibliography, evidence):
    evidence["claims"][0]["status"]="unsupported"
    with pytest.raises(ValueError):
        build_section_packet({"required_claim_ids":["claim_q1_01"]},evidence,bibliography)
