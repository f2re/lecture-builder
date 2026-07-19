from pathlib import Path

from lecture_tools.artifacts import (
    validate_blueprint,
    validate_review_state,
    validate_section_briefs,
)


def _config() -> dict:
    return {
        "questions": ["1. Первый вопрос"],
        "hours": 1,
        "competencies": ["ОПК-1: test"],
        "quality": {"word_budget_per_hour": 4000},
    }


def _blueprint() -> dict:
    return {
        "schema_version": "3.0",
        "topic": "Тестовая тема",
        "thesis": "Проверяемый тезис лекции связывает механизм и его применение.",
        "audience_prerequisites": [],
        "learning_objectives": {"know": ["объяснить"], "apply": ["применить"], "master": ["интерпретировать"]},
        "concept_graph": {
            "nodes": [{"id": "c1", "term": "Понятие"}],
            "edges": [],
        },
        "sections": [
            {
                "section_id": "q1",
                "number": 1,
                "question": "1. Первый вопрос",
                "purpose": "Объяснить основной механизм",
                "prerequisites": [],
                "introduces": ["Понятие"],
                "claim_ids": ["claim_q1_01"],
                "bridge_in": "Исходная задача требует определить основной механизм.",
                "bridge_out": "Полученный механизм служит основой для дальнейшего применения.",
                "examples": ["Расчётный пример"],
                "misconceptions": ["Типичная ошибка"],
                "minutes": 45,
                "word_budget": 1800,
                "competency_codes": ["ОПК-1"],
            }
        ],
    }


def test_blueprint_and_brief_crossrefs_pass(tmp_path: Path, bibliography, evidence) -> None:
    blueprint = _blueprint()
    assert validate_blueprint(blueprint, _config(), evidence).ok
    brief = {
        "schema_version": "3.0",
        "section_id": "q1",
        "number": 1,
        "title": "Первый вопрос",
        "purpose": "Объяснить основной механизм",
        "bridge_in": "Исходная задача требует определить основной механизм.",
        "bridge_out": "Полученный механизм служит основой для дальнейшего применения.",
        "required_claim_ids": ["claim_q1_01"],
        "allowed_source_ids": ["src_001"],
        "required_evidence_ids": ["ev_q1_01"],
        "structure": ["Постановка", "Механизм", "Выводы"],
        "word_budget": {"min": 1200, "target": 1800, "max": 2200},
        "examples": ["Расчётный пример"],
        "output_file": "output/sections/section_1_pervyi-vopros.md",
    }
    result = validate_section_briefs(
        [(tmp_path / "section_1.json", brief)],
        _config(),
        blueprint,
        evidence,
        bibliography,
    )
    assert result.ok, result.to_dict()


def test_unresolved_major_review_finding_blocks() -> None:
    report = {
        "review_type": "scientific",
        "status": "revise",
        "findings": [
            {
                "finding_id": "sci-1",
                "severity": "major",
                "section": "q1",
                "problem": "Unsupported scope",
                "required_action": "Narrow the claim",
            }
        ],
        "checks": {},
    }
    result = validate_review_state({"scientific": report}, {"resolutions": []}, strict=False)
    assert any(item.code == "review.unresolved" for item in result.errors)
