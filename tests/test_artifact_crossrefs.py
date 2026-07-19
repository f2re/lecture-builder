from pathlib import Path

from lecture_tools.artifacts import validate_blueprint, validate_review_state, validate_section_briefs


def _config() -> dict:
    return {
        "lecture_number": 17,
        "questions": ["17.1. Первый вопрос"],
        "hours": 1,
        "competencies": ["ОПК-1: test"],
        "methodical": {
            "enabled": True,
            "min_inserts_per_section": 4,
            "max_inserts_per_section": 5,
            "required_functions": ["understand", "remember", "apply", "self_check"],
            "max_word_share": 0.15,
        },
        "quality": {"word_budget_per_hour": 4000},
    }


def _subsections() -> list[dict]:
    return [
        {"number": "17.1.1", "title": "Постановка", "purpose": "Ввести основной вопрос"},
        {"number": "17.1.2", "title": "Механизм", "purpose": "Объяснить научный механизм"},
        {"number": "17.1.3", "title": "Выводы", "purpose": "Сформулировать итог раздела"},
    ]


def _blueprint() -> dict:
    return {
        "schema_version": "3.0",
        "lecture_number": 17,
        "topic": "Тестовая тема",
        "thesis": "Проверяемый тезис лекции связывает механизм и его применение.",
        "audience_prerequisites": [],
        "learning_objectives": {"know": ["объяснить"], "apply": ["применить"], "master": ["интерпретировать"]},
        "concept_graph": {"nodes": [{"id": "c1", "term": "Понятие"}], "edges": []},
        "sections": [
            {
                "section_id": "q1",
                "number": 1,
                "display_number": "17.1",
                "question": "Первый вопрос",
                "purpose": "Объяснить основной механизм",
                "prerequisites": [],
                "introduces": ["Понятие"],
                "claim_ids": ["claim_q1_01"],
                "bridge_in": "Исходная задача требует определить основной механизм.",
                "bridge_out": "Полученный механизм служит основой для дальнейшего применения.",
                "examples": ["Расчётный пример"],
                "misconceptions": ["Типичная ошибка"],
                "subsections": _subsections(),
                "methodical_requirements": ["understand", "remember", "apply", "self_check"],
                "visual_opportunities": [{"type": "chart", "purpose": "Показать зависимость величин"}],
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
        "display_number": "17.1",
        "title": "Первый вопрос",
        "purpose": "Объяснить основной механизм",
        "bridge_in": "Исходная задача требует определить основной механизм.",
        "bridge_out": "Полученный механизм служит основой для дальнейшего применения.",
        "required_claim_ids": ["claim_q1_01"],
        "allowed_source_ids": ["src_001"],
        "required_evidence_ids": ["ev_q1_01"],
        "subsections": _subsections(),
        "structure": ["Постановка", "Механизм", "Выводы"],
        "word_budget": {"min": 1200, "target": 1800, "max": 2200},
        "examples": ["Расчётный пример"],
        "methodical_requirements": ["understand", "remember", "apply", "self_check"],
        "visual_opportunities": [{"type": "chart", "purpose": "Показать зависимость величин"}],
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
