from __future__ import annotations

import hashlib
import re
from pathlib import Path, PureWindowsPath
from typing import Any

from .models import ValidationResult

_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_STATUS = {"unavailable": 0, "approximate": 1, "verified": 2}


def _validate_source_provenance(
    root: str | Path,
    fragments_value: Any,
    evidence_value: Any,
    bibliography: Any,
) -> ValidationResult:
    """Check active claim evidence against extracted fragments and local UTF-8 text."""
    result = ValidationResult(name="source-provenance")

    def issue(code: str, message: str, location: str | None = None) -> None:
        result.add(code, message, location=location)

    try:
        base = Path(root).resolve(strict=True)
        if not base.is_dir():
            raise ValueError("root is not a directory")
    except (OSError, RuntimeError, ValueError, TypeError):
        issue("provenance.root", "Root must be an existing local directory")
        return result

    if not isinstance(fragments_value, list):
        issue("provenance.fragments", "Extracted fragments must be an array")
        return result
    if not isinstance(evidence_value, dict):
        issue("provenance.ledger", "Evidence ledger must be an object")
        return result
    evidence_items = evidence_value.get("evidence")
    claims = evidence_value.get("claims")
    if not isinstance(evidence_items, list) or not isinstance(claims, list):
        issue("provenance.collections", "Ledger claims and evidence must be arrays")
        return result

    if isinstance(bibliography, list):
        sources = bibliography
    elif isinstance(bibliography, dict) and isinstance(bibliography.get("sources"), list):
        sources = bibliography["sources"]
    else:
        issue("provenance.bibliography", "Bibliography must be an array or contain a sources array")
        return result
    source_ids = {
        str(item.get("source_id") or item.get("id"))
        for item in sources
        if isinstance(item, dict) and (item.get("source_id") or item.get("id"))
    }

    fragments: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(fragments_value):
        loc = f"fragments/{index}"
        if not isinstance(item, dict):
            issue("provenance.fragment_type", "Fragment must be an object", loc)
            continue
        fid = item.get("fragment_id")
        if not isinstance(fid, str) or not fid:
            issue("provenance.fragment_id", "Fragment has no valid fragment_id", loc)
            continue
        if fid in fragments:
            issue("provenance.duplicate_fragment", f"Duplicate fragment_id: {fid}", loc)
        else:
            fragments[fid] = item

    evidence_map: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(evidence_items):
        loc = f"evidence/{index}"
        if not isinstance(item, dict):
            issue("provenance.evidence_type", "Evidence item must be an object", loc)
            continue
        eid = item.get("evidence_id")
        if not isinstance(eid, str) or not eid:
            issue("provenance.evidence_id", "Evidence has no valid evidence_id", loc)
            continue
        if eid in evidence_map:
            issue("provenance.duplicate_evidence", f"Duplicate evidence_id: {eid}", loc)
        else:
            evidence_map[eid] = item

    claim_map: dict[str, dict[str, Any]] = {}
    active_claims: dict[str, set[str]] = {}
    for index, claim in enumerate(claims):
        loc = f"claims/{index}"
        if not isinstance(claim, dict):
            issue("provenance.claim_type", "Claim must be an object", loc)
            continue
        cid = claim.get("claim_id")
        if not isinstance(cid, str) or not cid:
            issue("provenance.claim_id", "Claim has no valid claim_id", loc)
            continue
        if cid in claim_map:
            issue("provenance.duplicate_claim", f"Duplicate claim_id: {cid}", loc)
        claim_map[cid] = claim
        refs = claim.get("evidence_ids", [])
        if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
            issue("provenance.claim_refs", "Claim evidence_ids must be an array of strings", loc)
            continue
        if claim.get("status") in {"supported", "partial"}:
            if claim.get("status") == "supported" and not refs:
                issue("provenance.claim_support", f"Supported claim {cid} has no evidence", loc)
            for eid in refs:
                active_claims.setdefault(eid, set()).add(cid)
                if eid not in evidence_map:
                    issue("provenance.unknown_evidence", f"Claim {cid} references unknown evidence {eid}", loc)

    used_ids = set(active_claims)
    for eid in sorted(used_ids):
        evidence = evidence_map.get(eid)
        if evidence is None:
            continue
        loc = f"evidence/{eid}"
        backrefs = evidence.get("supports_claims")
        if not isinstance(backrefs, list) or any(not isinstance(ref, str) for ref in backrefs):
            issue("provenance.backrefs", f"Evidence {eid} supports_claims must be an array of strings", loc)
        elif set(backrefs) != active_claims[eid]:
            issue("provenance.backrefs", f"Evidence {eid} supports_claims does not match active claim references", loc)

        fid = evidence.get("fragment_id")
        fragment = fragments.get(fid) if isinstance(fid, str) else None
        if fragment is None:
            issue("provenance.unknown_fragment", f"Evidence {eid} does not link to a known extraction fragment", loc)
            continue
        sid = evidence.get("source_id")
        if sid != fragment.get("source_id") or sid not in source_ids:
            issue("provenance.source_id", f"Evidence {eid} source_id does not agree with its fragment and bibliography", loc)
        fragment_hash = fragment.get("document_hash", fragment.get("content_hash"))
        if not isinstance(fragment_hash, str) or not _HASH_RE.fullmatch(fragment_hash):
            issue("provenance.document_hash", f"Fragment for evidence {eid} has no valid document hash", loc)
        elif evidence.get("document_hash") != fragment_hash:
            issue("provenance.document_hash", f"Evidence {eid} document_hash differs from its extraction", loc)

        document_path = fragment.get("document_path")
        try:
            if not isinstance(document_path, str) or not document_path or Path(document_path).is_absolute() or PureWindowsPath(document_path).drive:
                raise ValueError("document_path must be relative")
            original = (base / document_path).resolve(strict=True)
            original.relative_to(base)
            if not original.is_file():
                raise ValueError("source is not a file")
            if "sha256:" + hashlib.sha256(original.read_bytes()).hexdigest() != fragment_hash:
                issue("provenance.source_hash", f"Original document changed for evidence {eid}", loc)
        except (OSError, ValueError, RuntimeError):
            issue("provenance.document_path", f"Original document missing or outside root for evidence {eid}", loc)

        exact = next((fragment[key] for key in ("exact_fragment", "exact_text", "text")
                      if isinstance(fragment.get(key), str)), None)
        if exact is None or evidence.get("exact_fragment") != exact:
            issue("provenance.exact_text", f"Evidence {eid} exact_fragment differs from its extraction", loc)

        text_path = fragment.get("text_path")
        text_hash = fragment.get("text_hash")
        if not isinstance(text_path, str) or not text_path or not isinstance(text_hash, str) or not _HASH_RE.fullmatch(text_hash):
            issue("provenance.text_source", f"Fragment for evidence {eid} lacks valid local text_path/text_hash", loc)
            continue
        if Path(text_path).is_absolute() or PureWindowsPath(text_path).is_absolute() or PureWindowsPath(text_path).drive:
            issue("provenance.path", f"Fragment text path for evidence {eid} must be relative to root", loc)
            continue
        try:
            text_file = (base / text_path).resolve(strict=True)
            text_file.relative_to(base)
            if not text_file.is_file():
                raise ValueError("not a file")
            raw = text_file.read_bytes()
            text = raw.decode("utf-8", errors="strict")
        except (OSError, RuntimeError, ValueError, UnicodeError):
            issue("provenance.path", f"Fragment text path for evidence {eid} is inaccessible or outside root", loc)
            continue
        actual_hash = "sha256:" + hashlib.sha256(raw).hexdigest()
        if actual_hash != text_hash:
            issue("provenance.text_hash", f"Local text hash differs for evidence {eid}", loc)

        location = fragment.get("location")
        location = location if isinstance(location, dict) else {}
        start = location.get("offset_start", fragment.get("offset_start"))
        end = location.get("offset_end", fragment.get("offset_end"))
        if (not isinstance(start, int) or isinstance(start, bool) or
                not isinstance(end, int) or isinstance(end, bool) or
                start < 0 or end < start or end > len(text)):
            issue("provenance.offset", f"Fragment for evidence {eid} has invalid text offsets", loc)
        elif exact is None or text[start:end] != exact:
            issue("provenance.slice", f"Local text slice differs from fragment for evidence {eid}", loc)

        status = evidence.get("location_status")
        extraction_status = fragment.get("location_status")
        if status not in _STATUS or extraction_status not in _STATUS or _STATUS.get(status, 9) > _STATUS.get(extraction_status, -1):
            issue("provenance.location_status", f"Evidence {eid} location status exceeds its extraction", loc)
        ev_location = evidence.get("location")
        if isinstance(ev_location, dict) and ev_location.get("page") is not None:
            if (ev_location.get("page") != location.get("page") or
                    ev_location.get("page_label") != location.get("page_label")):
                issue("provenance.page", f"Evidence {eid} page and page_label differ from its extraction", loc)

    result.metrics = {"fragments": len(fragments), "evidence": len(evidence_map), "active_evidence": len(used_ids)}
    return result


def validate_source_provenance(root: str | Path, fragments_value: Any, evidence_value: Any, bibliography: Any) -> ValidationResult:
    """Fail closed; this verifies provenance, not the semantic truth of claims."""
    try:
        return _validate_source_provenance(root, fragments_value, evidence_value, bibliography)
    except (TypeError, ValueError, OSError, KeyError, AttributeError) as exc:
        result = ValidationResult(name="source-provenance")
        result.add("provenance.malformed", "Malformed source provenance", details={"error": type(exc).__name__})
        return result
