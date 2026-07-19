from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .io import load_json
from .models import ValidationResult

CANONICAL_CITATION_RE = re.compile(
    r"\[@(?P<source>[A-Za-z0-9_.:-]+)(?:\s*,\s*(?:p\.|pp\.|с\.)\s*(?P<pages>[0-9]+(?:\s*[–-]\s*[0-9]+)?))?\]"
)
HUMAN_CITATION_RE = re.compile(r"\[[А-ЯЁA-Z][^\]\n]{1,80},\s*(?:19|20)\d{2}[^\]\n]*\]")
CLAIM_MARKER_RE = re.compile(r"<!--\s*claim:(?P<claim>claim_[A-Za-z0-9_.:-]+)\s*-->")


def normalize_bibliography(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict) and isinstance(value.get("sources"), list):
        return [item for item in value["sources"] if isinstance(item, dict)]
    raise ValueError("bibliography.json must be an array or an object with a sources array")


def _source_id(source: dict[str, Any]) -> str | None:
    value = source.get("source_id") or source.get("id")
    return str(value) if value else None


def _page_is_verified(source: dict[str, Any], page_spec: str) -> bool:
    status = source.get("metadata_status")
    if status != "verified":
        return False
    verified_pages = source.get("verified_pages")
    if verified_pages is True:
        return True
    page_ranges = source.get("page_ranges") or source.get("relevant_pages")
    if isinstance(page_ranges, dict) and page_ranges:
        return True
    if source.get("pages_total") or source.get("page_count"):
        first = int(re.split(r"[–-]", page_spec)[0].strip())
        total = int(source.get("pages_total") or source.get("page_count"))
        return 1 <= first <= total
    return False


def validate_bibliography(value: Any, *, path: str | Path | None = None) -> ValidationResult:
    result = ValidationResult(name="bibliography")
    try:
        sources = normalize_bibliography(value)
    except ValueError as exc:
        result.add("bibliography.type", str(exc), path=path)
        return result

    ids: dict[str, int] = {}
    for index, source in enumerate(sources):
        sid = _source_id(source)
        if not sid:
            result.add(
                "bibliography.id",
                "Запись не содержит source_id/id",
                path=path,
                location=str(index),
            )
            continue
        if sid in ids:
            result.add(
                "bibliography.duplicate_id",
                f"Повторный идентификатор источника: {sid}",
                path=path,
                location=str(index),
                details={"first_index": ids[sid]},
            )
        ids[sid] = index

        for field in ("title", "source_type", "metadata_status"):
            if not source.get(field):
                result.add(
                    "bibliography.required",
                    f"Источник {sid} не содержит поле {field}",
                    path=path,
                    location=str(index),
                )

        if source.get("metadata_status") != "verified":
            for risky in ("doi", "publisher", "pages_total", "volume_issue"):
                if source.get(risky):
                    result.add(
                        "bibliography.unverified_metadata",
                        f"Поле {risky} заполнено у источника {sid}, но metadata_status не verified",
                        severity="warning",
                        path=path,
                        location=str(index),
                    )

        provenance = source.get("provenance")
        if not isinstance(provenance, dict) or not provenance.get("method"):
            result.add(
                "bibliography.provenance",
                f"Источник {sid} не содержит происхождение метаданных",
                path=path,
                location=str(index),
            )

    result.metrics = {"sources": len(sources), "unique_ids": len(ids)}
    return result


def validate_citations(
    markdown: str,
    bibliography: Any,
    *,
    path: str | Path | None = None,
) -> ValidationResult:
    result = ValidationResult(name="citations")
    try:
        sources = normalize_bibliography(bibliography)
    except ValueError as exc:
        result.add("citation.bibliography", str(exc), path=path)
        return result

    source_map = {sid: source for source in sources if (sid := _source_id(source))}
    matches = list(CANONICAL_CITATION_RE.finditer(markdown))
    for match in matches:
        sid = match.group("source")
        pages = match.group("pages")
        if sid not in source_map:
            result.add(
                "citation.unknown_source",
                f"Ссылка указывает на неизвестный источник {sid}",
                path=path,
                location=f"offset:{match.start()}",
            )
            continue
        if pages and not _page_is_verified(source_map[sid], pages):
            result.add(
                "citation.unverified_page",
                f"Страница '{pages}' для {sid} не подтверждена метаданными",
                path=path,
                location=f"offset:{match.start()}",
            )

    human_matches = list(HUMAN_CITATION_RE.finditer(markdown))
    if human_matches:
        result.add(
            "citation.noncanonical",
            "Найдены ссылки вида [Автор, год]. Используйте стабильный формат [@source_id] или [@source_id, с. 45]",
            severity="warning",
            path=path,
            details={"count": len(human_matches)},
        )

    result.metrics = {
        "canonical_citations": len(matches),
        "legacy_citations": len(human_matches),
        "bibliography_sources": len(source_map),
    }
    return result


def validate_evidence(
    evidence_value: Any,
    bibliography: Any,
    *,
    path: str | Path | None = None,
) -> ValidationResult:
    result = ValidationResult(name="evidence-ledger")
    if not isinstance(evidence_value, dict):
        result.add("evidence.type", "Evidence ledger должен быть объектом", path=path)
        return result

    try:
        sources = normalize_bibliography(bibliography)
    except ValueError as exc:
        result.add("evidence.bibliography", str(exc), path=path)
        return result
    source_ids = {sid for source in sources if (sid := _source_id(source))}

    evidence = evidence_value.get("evidence") or []
    claims = evidence_value.get("claims") or []
    if not isinstance(evidence, list) or not isinstance(claims, list):
        result.add("evidence.collections", "Поля claims и evidence должны быть массивами", path=path)
        return result

    evidence_map: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            result.add("evidence.item_type", "Элемент evidence должен быть объектом", path=path, location=f"evidence/{index}")
            continue
        eid = item.get("evidence_id")
        if not eid:
            result.add("evidence.id", "Отсутствует evidence_id", path=path, location=f"evidence/{index}")
            continue
        if eid in evidence_map:
            result.add("evidence.duplicate_id", f"Повторный evidence_id: {eid}", path=path, location=f"evidence/{index}")
        evidence_map[str(eid)] = item
        sid = item.get("source_id")
        if sid not in source_ids:
            result.add(
                "evidence.unknown_source",
                f"Evidence {eid} указывает на неизвестный источник {sid}",
                path=path,
                location=f"evidence/{index}",
            )
        if not str(item.get("exact_fragment", "")).strip():
            result.add(
                "evidence.fragment",
                f"Evidence {eid} не содержит точный фрагмент источника",
                path=path,
                location=f"evidence/{index}",
            )
        location = item.get("location") or {}
        if location.get("page") is not None and item.get("location_status") != "verified":
            result.add(
                "evidence.page_status",
                f"Evidence {eid} содержит страницу без location_status=verified",
                path=path,
                location=f"evidence/{index}",
            )

    claim_ids: set[str] = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            result.add("claim.item_type", "Элемент claims должен быть объектом", path=path, location=f"claims/{index}")
            continue
        cid = claim.get("claim_id")
        if not cid:
            result.add("claim.id", "Отсутствует claim_id", path=path, location=f"claims/{index}")
            continue
        if cid in claim_ids:
            result.add("claim.duplicate_id", f"Повторный claim_id: {cid}", path=path, location=f"claims/{index}")
        claim_ids.add(str(cid))
        status = claim.get("status")
        refs = claim.get("evidence_ids") or []
        if status == "supported" and not refs:
            result.add(
                "claim.support",
                f"Тезис {cid} помечен supported, но не имеет evidence_ids",
                path=path,
                location=f"claims/{index}",
            )
        if status == "unsupported":
            result.add(
                "claim.unsupported",
                f"Неподтверждённый тезис {cid} блокирует публикацию",
                path=path,
                location=f"claims/{index}",
            )
        for eid in refs:
            if eid not in evidence_map:
                result.add(
                    "claim.unknown_evidence",
                    f"Тезис {cid} указывает на неизвестный evidence_id {eid}",
                    path=path,
                    location=f"claims/{index}",
                )

    result.metrics = {
        "claims": len(claims),
        "evidence": len(evidence),
        "unsupported_claims": sum(1 for item in claims if isinstance(item, dict) and item.get("status") == "unsupported"),
    }
    return result



def validate_claim_markers(
    markdown: str,
    evidence_value: Any,
    *,
    required_claim_ids: set[str] | None = None,
    path: str | Path | None = None,
) -> ValidationResult:
    result = ValidationResult(name="claim-markers")
    if not isinstance(evidence_value, dict):
        result.add("claim_marker.evidence", "Evidence ledger должен быть объектом", path=path)
        return result
    claim_map = {
        str(item.get("claim_id")): item
        for item in evidence_value.get("claims", [])
        if isinstance(item, dict) and item.get("claim_id")
    }
    markers = [match.group("claim") for match in CLAIM_MARKER_RE.finditer(markdown)]
    for claim_id in markers:
        claim = claim_map.get(claim_id)
        if claim is None:
            result.add(
                "claim_marker.unknown",
                f"Маркер указывает на неизвестный тезис {claim_id}",
                path=path,
            )
        elif claim.get("status") == "unsupported":
            result.add(
                "claim_marker.unsupported",
                f"В текст включён неподтверждённый тезис {claim_id}",
                path=path,
            )
    missing = sorted((required_claim_ids or set()) - set(markers))
    if missing:
        result.add(
            "claim_marker.missing",
            "Не все обязательные тезисы имеют точку трассировки в Markdown",
            path=path,
            details={"missing": missing},
        )
    result.metrics = {
        "markers": len(markers),
        "unique_markers": len(set(markers)),
        "required_claims": len(required_claim_ids or set()),
    }
    return result

def load_and_validate_citations(
    markdown_path: str | Path,
    bibliography_path: str | Path,
) -> ValidationResult:
    markdown = Path(markdown_path).read_text(encoding="utf-8")
    bibliography = load_json(bibliography_path)
    result = validate_bibliography(bibliography, path=bibliography_path)
    result.extend(validate_citations(markdown, bibliography, path=markdown_path))
    return result
