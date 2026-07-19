from pathlib import Path

from lecture_tools.io import dump_json, load_json
from lecture_tools.visuals import validate_chart_specs
from scripts.render_charts import render_specs


def test_schematic_chart_is_rendered_and_synchronized(tmp_path: Path) -> None:
    (tmp_path / "output").mkdir()
    specs_path = tmp_path / "output/chart_specs.json"
    figures_path = tmp_path / "output/figures_index.json"
    specs = {
        "schema_version": "3.0",
        "lecture_number": 17,
        "charts": [
            {
                "chart_id": "chart:q1:concept",
                "figure_id": "fig:q1:concept",
                "section_id": "q1",
                "question_number": "17.1",
                "title": "Схематическая зависимость",
                "caption": "Схематическое изменение величины при росте аргумента.",
                "alt_text": "Линия монотонно возрастает слева направо.",
                "purpose": "Показать направление качественной зависимости.",
                "chart_type": "line",
                "data_policy": "schematic",
                "data_source_ids": [],
                "claim_ids": ["claim_q1_01"],
                "evidence_ids": ["ev_q1_01"],
                "x_axis": {"label": "Аргумент", "unit": None, "scale": "linear"},
                "y_axis": {"label": "Отклик", "unit": None, "scale": "linear"},
                "series": [{"name": "Схема", "x": [0, 1, 2], "y": [0, 0.4, 1]}],
                "schematic_note": "Схематично; не является наблюдательными данными.",
                "output_path": "output/figures/chart_q1-concept.png",
                "status": "planned",
            }
        ],
    }
    figures = {
        "schema_version": "3.0",
        "lecture_number": 17,
        "total_figures": 1,
        "figures": [
            {
                "figure_id": "fig:q1:concept",
                "number": "17.1",
                "title": "Схематическая зависимость",
                "caption": "Схематическое изменение величины при росте аргумента.",
                "alt_text": "Линия монотонно возрастает слева направо.",
                "type": "chart",
                "section": "q1",
                "section_number": "17.1",
                "purpose": "Показать направление качественной зависимости.",
                "status": "planned",
                "data_source_ids": [],
                "placeholder": "[fig:q1:concept]",
                "asset_path": None,
                "chart_id": "chart:q1:concept",
                "prompt_id": None,
            }
        ],
    }
    dump_json(specs_path, specs)
    dump_json(figures_path, figures)

    assert render_specs(specs_path, figures_path, tmp_path) == 1
    rendered_specs = load_json(specs_path)
    rendered_figures = load_json(figures_path)
    asset = tmp_path / rendered_specs["charts"][0]["output_path"]
    assert asset.is_file() and asset.stat().st_size > 0
    assert rendered_specs["charts"][0]["status"] == "generated"
    assert rendered_figures["figures"][0]["status"] == "generated"

    report = validate_chart_specs(
        rendered_specs,
        rendered_figures,
        {"lecture_number": 17, "visuals": {"require_graphs": True}},
        set(),
        claim_ids={"claim_q1_01"},
        evidence_ids={"ev_q1_01"},
        root=tmp_path,
    )
    assert report.ok, report.to_dict()
