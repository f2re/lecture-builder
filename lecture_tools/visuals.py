from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .models import ValidationResult
from .numbering import question_number


def _series_hash(chart: dict[str, Any]) -> str:
    payload = {
        "chart_type": chart.get("chart_type"),
        "data_policy": chart.get("data_policy"),
        "series": chart.get("series"),
        "grid": chart.get("grid"),
        "x_axis": chart.get("x_axis"),
        "y_axis": chart.get("y_axis"),
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_chart_specs(
    value: Any,
    figures: Any,
    config: dict[str, Any],
    source_ids: set[str],
    *,
    claim_ids: set[str] | None = None,
    evidence_ids: set[str] | None = None,
    root: str | Path | None = None,
    path: str | Path | None = None,
) -> ValidationResult:
    result = ValidationResult(name="chart-specs")
    settings = config.get("visuals") or {}
    require_graphs = settings.get("require_graphs") is True
    if not isinstance(value, dict):
        if require_graphs:
            result.add("charts.type", "chart_specs.json должен быть объектом", path=path)
        return result

    lecture_number = int(config.get("lecture_number") or 0)
    if value.get("lecture_number") != lecture_number:
        result.add("charts.lecture_number", "Номер лекции в chart_specs не совпадает с config", path=path)

    figure_map = {
        str(item.get("figure_id")): item
        for item in ((figures or {}).get("figures") or [])
        if isinstance(item, dict)
    }
    seen: set[str] = set()
    generated = 0
    active = 0
    base = Path(root) if root is not None else None
    known_claim_ids = claim_ids or set()
    known_evidence_ids = evidence_ids or set()

    for index, chart in enumerate(value.get("charts") or []):
        location = f"charts/{index}"
        if not isinstance(chart, dict):
            result.add("charts.item", "Chart spec должен быть объектом", path=path, location=location)
            continue
        chart_id = str(chart.get("chart_id") or "")
        if chart_id in seen:
            result.add("charts.duplicate_id", f"Повторный chart_id {chart_id}", path=path)
        seen.add(chart_id)

        status = str(chart.get("status") or "")
        if status != "omitted":
            active += 1
        if status in {"generated", "verified"}:
            generated += 1

        section_id = str(chart.get("section_id") or "")
        if section_id.startswith("q") and section_id[1:].isdigit():
            expected_question = question_number(lecture_number, int(section_id[1:]))
            if chart.get("question_number") != expected_question:
                result.add(
                    "charts.question_number",
                    f"Chart {chart_id}: ожидается question_number={expected_question}",
                    path=path,
                    location=location,
                )

        figure_id = str(chart.get("figure_id") or "")
        figure = figure_map.get(figure_id)
        if figure is None:
            result.add(
                "charts.unknown_figure",
                f"Chart {chart_id} ссылается на неизвестный figure_id {figure_id}",
                path=path,
                location=location,
            )
        elif figure.get("type") != "chart":
            result.add(
                "charts.figure_type",
                f"Связанный рисунок {figure_id} должен иметь type=chart",
                path=path,
                location=location,
            )
        elif status in {"generated", "verified"} and figure.get("status") not in {"generated", "verified"}:
            result.add(
                "charts.figure_status",
                f"Статус рисунка {figure_id} не синхронизирован с chart {chart_id}",
                path=path,
                location=location,
            )

        chart_claims = {str(item) for item in chart.get("claim_ids") or []}
        chart_evidence = {str(item) for item in chart.get("evidence_ids") or []}
        if status != "omitted" and not (chart_claims or chart_evidence):
            result.add(
                "charts.missing_support",
                f"Chart {chart_id} должен ссылаться на claim_ids/evidence_ids",
                path=path,
                location=location,
            )
        for claim_id in chart_claims:
            if known_claim_ids and claim_id not in known_claim_ids:
                result.add("charts.unknown_claim", f"Неизвестный claim_id {claim_id}", path=path)
        for evidence_id in chart_evidence:
            if known_evidence_ids and evidence_id not in known_evidence_ids:
                result.add("charts.unknown_evidence", f"Неизвестный evidence_id {evidence_id}", path=path)

        data_policy = str(chart.get("data_policy") or "")
        chart_sources = {str(item) for item in chart.get("data_source_ids") or []}
        for source_id in chart_sources:
            if source_id not in source_ids:
                result.add("charts.unknown_source", f"Неизвестный source_id {source_id}", path=path)
        if data_policy == "source_bound" and not chart_sources:
            result.add(
                "charts.missing_source",
                f"Chart {chart_id} с source_bound должен иметь data_source_ids",
                path=path,
            )
        if data_policy == "source_bound" and not (chart.get("evidence_ids") or []):
            result.add(
                "charts.missing_evidence",
                f"Chart {chart_id} с source_bound должен иметь evidence_ids",
                path=path,
            )
        if data_policy == "schematic" and not str(chart.get("schematic_note") or "").strip():
            result.add(
                "charts.schematic_note",
                f"Схематический chart {chart_id} должен явно сообщать, что он не является наблюдательными данными",
                path=path,
            )

        for axis_name in ("x_axis", "y_axis"):
            axis = chart.get(axis_name) or {}
            if not isinstance(axis, dict) or not str(axis.get("label") or "").strip():
                result.add(
                    "charts.axis",
                    f"Chart {chart_id}: {axis_name} должен содержать label",
                    path=path,
                )

        chart_type = str(chart.get("chart_type") or "")
        series = chart.get("series") or []
        grid = chart.get("grid")
        if status != "omitted":
            if chart_type in {"contour", "heatmap"}:
                if not isinstance(grid, dict):
                    result.add("charts.grid", f"Chart {chart_id} требует grid", path=path)
            elif not series:
                result.add("charts.series", f"Chart {chart_id} не содержит series", path=path)

        for series_index, item in enumerate(series):
            if not isinstance(item, dict):
                result.add("charts.series_item", f"Chart {chart_id}: series должен быть объектом", path=path)
                continue
            x_values = item.get("x") or []
            y_values = item.get("y") or []
            if len(x_values) != len(y_values) or not x_values:
                result.add(
                    "charts.series_length",
                    f"Chart {chart_id}, series {series_index}: x и y должны иметь одинаковую ненулевую длину",
                    path=path,
                )
            series_source = item.get("source_id")
            if series_source and str(series_source) not in chart_sources:
                result.add(
                    "charts.series_source",
                    f"Chart {chart_id}, series {series_index}: source_id не включён в data_source_ids",
                    path=path,
                )
            series_evidence = item.get("evidence_id")
            if series_evidence and str(series_evidence) not in chart_evidence:
                result.add(
                    "charts.series_evidence",
                    f"Chart {chart_id}, series {series_index}: evidence_id не включён в evidence_ids",
                    path=path,
                )

        declared_hash = chart.get("data_hash")
        if declared_hash and str(declared_hash).removeprefix("sha256:") != _series_hash(chart):
            result.add("charts.data_hash", f"Chart {chart_id}: data_hash не соответствует данным", path=path)

        output_path = chart.get("output_path")
        if status in {"generated", "verified"}:
            if not output_path:
                result.add("charts.output_path", f"Chart {chart_id} не содержит output_path", path=path)
            elif base is not None:
                asset = base / str(output_path)
                if not asset.is_file() or asset.stat().st_size == 0:
                    result.add("charts.asset_missing", f"Файл графика отсутствует: {output_path}", path=path)
                else:
                    actual_hash = hashlib.sha256(asset.read_bytes()).hexdigest()
                    declared_asset_hash = str(chart.get("asset_hash") or "").removeprefix("sha256:")
                    if declared_asset_hash and declared_asset_hash != actual_hash:
                        result.add("charts.asset_hash", f"Chart {chart_id}: asset_hash не совпадает", path=path)
                if figure and figure.get("asset_path") != output_path:
                    result.add(
                        "charts.figure_asset",
                        f"asset_path рисунка {figure_id} не совпадает с output_path chart",
                        path=path,
                    )

    if require_graphs and active == 0:
        result.add("charts.required", "Конфигурация требует хотя бы один график", path=path)
    if require_graphs and generated == 0:
        result.add(
            "charts.not_rendered",
            "Конфигурация требует графики, но ни один график не имеет status=generated/verified",
            path=path,
        )
    result.metrics = {
        "charts": len(value.get("charts") or []),
        "active": active,
        "generated": generated,
    }
    return result


def validate_figure_metadata(
    figures: Any,
    config: dict[str, Any],
    markdown: str,
    *,
    root: str | Path | None = None,
    path: str | Path | None = None,
) -> ValidationResult:
    result = ValidationResult(name="figure-metadata")
    if not isinstance(figures, dict):
        result.add("figures.type", "figures_index.json должен быть объектом", path=path)
        return result
    lecture_number = int(config.get("lecture_number") or 0)
    settings = config.get("visuals") or {}
    max_per_section = int(settings.get("max_figures_per_section") or 0)
    base = Path(root) if root is not None else None
    seen_ids: set[str] = set()
    section_counts: dict[str, int] = {}
    items = figures.get("figures") or []
    if figures.get("lecture_number") != lecture_number:
        result.add("figures.lecture_number", "lecture_number рисунков не совпадает с config", path=path)
    if figures.get("total_figures") != len(items):
        result.add("figures.total", "total_figures не совпадает с длиной figures", path=path)

    for index, figure in enumerate(items, start=1):
        if not isinstance(figure, dict):
            result.add("figures.item", "Запись рисунка должна быть объектом", path=path)
            continue
        figure_id = str(figure.get("figure_id") or "")
        if figure_id in seen_ids:
            result.add("figures.duplicate_id", f"Повторный figure_id {figure_id}", path=path)
        seen_ids.add(figure_id)
        expected_number = f"{lecture_number}.{index}"
        if str(figure.get("number") or "") != expected_number:
            result.add(
                "figures.sequence",
                f"Ожидался номер рисунка {expected_number}, получено {figure.get('number')}",
                path=path,
            )
        section_id = str(figure.get("section") or "")
        section_counts[section_id] = section_counts.get(section_id, 0) + 1
        if section_id.startswith("q") and section_id[1:].isdigit():
            expected_section = question_number(lecture_number, int(section_id[1:]))
            if figure.get("section_number") != expected_section:
                result.add(
                    "figures.section_number",
                    f"Рисунок {figure_id}: ожидается section_number={expected_section}",
                    path=path,
                )
        caption_marker = f"**Рисунок {expected_number}.**"
        if figure.get("status") != "omitted" and markdown and caption_marker not in markdown:
            result.add(
                "figures.caption_missing",
                f"В лекции отсутствует подпись {caption_marker}",
                path=path,
            )
        if figure.get("type") == "chart" and not figure.get("chart_id"):
            result.add("figures.chart_id", f"Рисунок {figure_id} type=chart требует chart_id", path=path)
        if figure.get("type") != "chart" and figure.get("status") == "planned" and not figure.get("prompt_id"):
            result.add(
                "figures.prompt_id",
                f"Планируемая иллюстрация {figure_id} должна иметь prompt_id",
                path=path,
            )
        if figure.get("status") in {"generated", "verified"}:
            asset_path = figure.get("asset_path")
            if not asset_path:
                result.add("figures.asset_path", f"Рисунок {figure_id} не содержит asset_path", path=path)
            elif base is not None:
                asset = base / str(asset_path)
                if not asset.is_file() or asset.stat().st_size == 0:
                    result.add("figures.asset_missing", f"Файл рисунка отсутствует: {asset_path}", path=path)
                else:
                    actual_hash = hashlib.sha256(asset.read_bytes()).hexdigest()
                    declared_hash = str(figure.get("asset_hash") or "").removeprefix("sha256:")
                    if declared_hash and declared_hash != actual_hash:
                        result.add("figures.asset_hash", f"Рисунок {figure_id}: asset_hash не совпадает", path=path)

    if max_per_section:
        for section_id, count in section_counts.items():
            if count > max_per_section:
                result.add(
                    "figures.section_density",
                    f"Для {section_id} запланировано {count} рисунков при лимите {max_per_section}",
                    path=path,
                )
    result.metrics = {"figures": len(items), "sections": len(section_counts)}
    return result
