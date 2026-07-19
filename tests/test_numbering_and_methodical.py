from lecture_tools.methodical import render_methodical_insert, validate_methodical_inserts
from lecture_tools.numbering import normalize_structure, validate_document_numbering
from lecture_tools.visuals import validate_chart_specs


def _config() -> dict:
    return {
        "lecture_number": 17,
        "questions": ["17.1. Первый вопрос", "17.2. Второй вопрос"],
        "methodical": {
            "enabled": True,
            "min_inserts_per_section": 4,
            "max_inserts_per_section": 5,
            "required_functions": ["understand", "remember", "apply", "self_check"],
            "max_word_share": 0.20,
        },
        "visuals": {"require_graphs": True},
    }


def test_structure_normalization_and_validation() -> None:
    source = """# ЛЕКЦИЯ 17

## Вопрос 1. Первый вопрос

### Определение
Текст.

### Выводы
Итог.

## 2. Второй вопрос

### Применение
Текст.

### Выводы
Итог.

## Заключение
Текст.
"""
    normalized, report = normalize_structure(source, 17)
    assert report.ok
    assert "## 17.1. Первый вопрос" in normalized
    assert "### 17.1.1. Определение" in normalized
    assert "## 17.2. Второй вопрос" in normalized
    assert validate_document_numbering(normalized, _config()).ok


def test_methodical_insert_render_and_validation(evidence) -> None:
    blueprint = {
        "sections": [
            {"section_id": "q1", "number": 1, "display_number": "17.1", "word_budget": 1000},
            {"section_id": "q2", "number": 2, "display_number": "17.2", "word_budget": 1000},
        ]
    }
    types = [
        ("key_idea", "understand"),
        ("mnemonic", "remember"),
        ("thematic_example", "apply"),
        ("self_check", "self_check"),
    ]
    evidence = {
        "claims": [
            *evidence["claims"],
            {"claim_id": "claim_q2_01", "status": "supported"},
        ],
        "evidence": [
            *evidence["evidence"],
            {"evidence_id": "ev_q2_01"},
        ],
    }
    inserts = []
    markdown = []
    for section in (1, 2):
        for index, (insert_type, function) in enumerate(types, start=1):
            insert = {
                "insert_id": f"ins:q{section}:{insert_type}:{index}",
                "section_id": f"q{section}",
                "question_number": f"17.{section}",
                "type": insert_type,
                "learning_functions": [function],
                "title": "Короткая опора",
                "body": "Краткое объяснение помогает связать понятие с его правильным применением.",
                "rationale": "Снижает когнитивную нагрузку без изменения научного смысла.",
                "placement": {"strategy": "after_heading"},
                "claim_ids": [] if insert_type == "self_check" else [f"claim_q{section}_01"],
                "evidence_ids": [] if insert_type == "self_check" else [f"ev_q{section}_01"],
                "hypothetical": False,
                "required": True,
                "word_count": 9,
            }
            inserts.append(insert)
            markdown.append(render_methodical_insert(insert))
    value = {"schema_version": "3.0", "lecture_number": 17, "inserts": inserts}
    report = validate_methodical_inserts(
        value,
        _config(),
        blueprint,
        evidence,
        {"output/lecture_final.md": "\n\n".join(markdown)},
    )
    assert report.ok, report.to_dict()


def test_chart_specs_require_source_bound_data() -> None:
    figures = {
        "figures": [
            {"figure_id": "fig:test", "type": "chart", "number": "17.1"}
        ]
    }
    charts = {
        "schema_version": "3.0",
        "lecture_number": 17,
        "charts": [
            {
                "chart_id": "chart:test",
                "figure_id": "fig:test",
                "section_id": "q1",
                "question_number": "17.1",
                "title": "Зависимость",
                "purpose": "Показать зависимость величин",
                "chart_type": "line",
                "data_policy": "source_bound",
                "data_source_ids": [],
                "x_axis": {"label": "X"},
                "y_axis": {"label": "Y"},
                "status": "planned",
            }
        ],
    }
    report = validate_chart_specs(charts, figures, _config(), set())
    assert any(item.code == "charts.missing_source" for item in report.errors)
