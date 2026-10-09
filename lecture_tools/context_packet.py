from __future__ import annotations
from typing import Any
from .citations import normalize_bibliography


def build_section_packet(brief: dict[str, Any], ledger: dict[str, Any], bibliography: Any) -> dict[str, Any]:
    claims = {c["claim_id"]: c for c in ledger.get("claims", [])}
    evidence = {e["evidence_id"]: e for e in ledger.get("evidence", [])}
    sources = {s.get("source_id", s.get("id")): s for s in normalize_bibliography(bibliography)}
    required = brief.get("required_claim_ids") or []
    if not required:
        raise ValueError("Section brief contains no required claims")
    selected_claims, selected_evidence, selected_sources = [], {}, {}
    allowed_sources = set(brief.get("allowed_source_ids") or [])
    for cid in required:
        claim = claims.get(cid)
        if not claim or claim.get("status") not in {"supported", "partial"}:
            raise ValueError(f"Required claim is missing or unsupported: {cid}")
        if not claim.get("evidence_ids"):
            raise ValueError(f"Claim has no evidence: {cid}")
        selected_claims.append(claim)
        for eid in claim["evidence_ids"]:
            item = evidence.get(eid)
            if not item or item.get("source_id") not in sources:
                raise ValueError(f"Evidence/source missing: {eid}")
            if item["source_id"] not in allowed_sources:
                raise ValueError(f"Source not allowed by brief: {item['source_id']}")
            selected_evidence[eid] = item
            selected_sources[item["source_id"]] = sources[item["source_id"]]
    return {"schema_version":"1.0", "section_id":brief.get("section_id"), "brief":brief,
            "claims":selected_claims, "evidence":list(selected_evidence.values()),
            "sources":list(selected_sources.values()),
            "missing_evidence_action":"return_evidence_request"}
