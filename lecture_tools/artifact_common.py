from __future__ import annotations

from typing import Any


def _claim_map(evidence: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(evidence, dict):
        return {}
    return {
        str(item["claim_id"]): item
        for item in evidence.get("claims", [])
        if isinstance(item, dict) and item.get("claim_id")
    }


def _evidence_map(evidence: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(evidence, dict):
        return {}
    return {
        str(item["evidence_id"]): item
        for item in evidence.get("evidence", [])
        if isinstance(item, dict) and item.get("evidence_id")
    }
