from __future__ import annotations

from typing import Any

import pytest


@pytest.fixture
def bibliography() -> list[dict[str, Any]]:
    return [
        {
            "source_id": "src_001",
            "source_type": "web_downloaded",
            "category": "article",
            "authors": ["Иванов И. И."],
            "title": "Проверенный источник",
            "year": 2021,
            "publisher": None,
            "pages_total": 120,
            "verified_pages": True,
            "metadata_status": "verified",
            "provenance": {
                "method": "publisher_page",
                "verified_fields": ["title", "authors", "year", "pages_total"],
            },
        }
    ]


@pytest.fixture
def evidence() -> dict[str, Any]:
    return {
        "schema_version": "3.0",
        "claims": [
            {
                "claim_id": "claim_q1_01",
                "section_id": "q1",
                "statement": "Толщина слоя зависит от средней виртуальной температуры.",
                "claim_type": "fact",
                "status": "supported",
                "evidence_ids": ["ev_q1_01"],
                "confidence": 0.98,
            }
        ],
        "evidence": [
            {
                "evidence_id": "ev_q1_01",
                "source_id": "src_001",
                "document_hash": "sha256:" + "a" * 64,
                "exact_fragment": "Толщина изобарического слоя пропорциональна его средней виртуальной температуре.",
                "location": {"page": 45, "section": "2.1", "paragraph": 3},
                "location_status": "verified",
                "supports_claims": ["claim_q1_01"],
            }
        ],
    }
