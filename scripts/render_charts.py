#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lecture_tools.io import dump_json, load_json, load_yaml  # noqa: E402
from lecture_tools.visuals import _series_hash  # noqa: E402


def _slug(value: str) -> str:
    value = value.lower().replace(":", "-").replace("_", "-")
    value = re.sub(r"[^a-z0-9-]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-") or "chart"



def _safe_output(root: Path, value: str) -> Path:
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Небезопасный output_path: {value}")
    target = (root / relative).resolve()
    allowed = (root / "output/figures").resolve()
    if target.parent != allowed or target.suffix.lower() not in {".png", ".svg"}:
        raise ValueError(f"График должен записываться только в output/figures/*.png|*.svg: {value}")
    return target

def _axis_label(axis: dict[str, Any]) -> str:
    label = str(axis.get("label") or "")
    unit = axis.get("unit")
    return f"{label}, {unit}" if unit else label


def _render_chart(chart: dict[str, Any], output: Path) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as exc:  # pragma: no cover - dependency gate.
        raise RuntimeError("Для генерации графиков требуется matplotlib") from exc

    chart_type = str(chart["chart_type"])
    fig, ax = plt.subplots(figsize=(8.4, 5.2))

    if chart_type in {"contour", "heatmap"}:
        grid = chart["grid"]
        x = np.asarray(grid["x"], dtype=float)
        y = np.asarray(grid["y"], dtype=float)
        z = np.asarray(grid["z"], dtype=float)
        expected_shape = (len(y), len(x))
        if z.shape != expected_shape:
            raise ValueError(f"grid.z имеет shape={z.shape}, ожидается {expected_shape}")
        if chart_type == "contour":
            artist = ax.contourf(x, y, z)
        else:
            artist = ax.imshow(
                z,
                origin="lower",
                aspect="auto",
                extent=(float(x.min()), float(x.max()), float(y.min()), float(y.max())),
            )
        fig.colorbar(artist, ax=ax)
    else:
        series = chart.get("series") or []
        if not series:
            raise ValueError("Для выбранного типа графика отсутствуют series")
        if chart_type == "bar":
            labels = list(series[0]["x"])
            positions = list(range(len(labels)))
            width = 0.8 / max(len(series), 1)
            for index, item in enumerate(series):
                offset = (index - (len(series) - 1) / 2) * width
                ax.bar(
                    [position + offset for position in positions],
                    item["y"],
                    width=width,
                    label=str(item.get("name") or ""),
                )
            ax.set_xticks(positions, labels)
        else:
            for item in series:
                x = item["x"]
                y = item["y"]
                name = str(item.get("name") or "")
                if chart_type == "scatter":
                    ax.scatter(x, y, label=name)
                else:
                    ax.plot(x, y, marker="o" if len(x) <= 20 else None, label=name)

    x_axis = chart.get("x_axis") or {}
    y_axis = chart.get("y_axis") or {}
    ax.set_xlabel(_axis_label(x_axis))
    ax.set_ylabel(_axis_label(y_axis))
    if x_axis.get("scale") == "log":
        ax.set_xscale("log")
    if y_axis.get("scale") == "log":
        ax.set_yscale("log")
    if x_axis.get("invert"):
        ax.invert_xaxis()
    if y_axis.get("invert"):
        ax.invert_yaxis()
    ax.set_title(str(chart.get("title") or ""))
    ax.grid(True, alpha=0.3)
    labels = [str(item.get("name") or "") for item in chart.get("series") or []]
    if any(labels):
        ax.legend()
    if chart.get("data_policy") == "schematic":
        note = str(chart.get("schematic_note") or "Схематично; не в масштабе")
        fig.text(0.5, 0.01, note, ha="center", fontsize=9)
        fig.tight_layout(rect=(0, 0.035, 1, 1))
    else:
        fig.tight_layout()

    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220, metadata={"Title": str(chart.get("title") or "")})
    plt.close(fig)


def render_specs(spec_path: Path, figures_path: Path, root: Path) -> int:
    specs = load_json(spec_path)
    figures = load_json(figures_path)
    if not isinstance(specs, dict) or not isinstance(figures, dict):
        raise ValueError("chart_specs.json и figures_index.json должны быть объектами")
    figure_map = {
        str(item.get("figure_id")): item
        for item in figures.get("figures") or []
        if isinstance(item, dict)
    }
    config_path = root / "input/lecture_config.md"
    config = load_yaml(config_path) if config_path.is_file() else {}
    extension_default = str(((config or {}).get("visuals") or {}).get("chart_output_format") or "png")
    rendered = 0
    for chart in specs.get("charts") or []:
        if not isinstance(chart, dict) or chart.get("status") == "omitted":
            continue
        output_path = chart.get("output_path")
        if not output_path:
            extension = "svg" if extension_default == "svg" else "png"
            output_path = f"output/figures/chart_{_slug(str(chart.get('chart_id') or 'chart'))}.{extension}"
            chart["output_path"] = output_path
        output = _safe_output(root, str(output_path))
        _render_chart(chart, output)
        chart["data_hash"] = "sha256:" + _series_hash(chart)
        chart["asset_hash"] = "sha256:" + hashlib.sha256(output.read_bytes()).hexdigest()
        chart["status"] = "generated"
        figure = figure_map.get(str(chart.get("figure_id") or ""))
        if figure is None:
            raise ValueError(f"Не найден figure_id={chart.get('figure_id')}")
        figure["asset_path"] = str(output_path)
        figure["asset_hash"] = chart["asset_hash"]
        figure["status"] = "generated"
        rendered += 1
    dump_json(spec_path, specs)
    dump_json(figures_path, figures)
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render evidence-safe lecture charts")
    parser.add_argument("--spec", default="output/chart_specs.json")
    parser.add_argument("--figures", default="output/figures_index.json")
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args()
    root = Path(args.root).resolve()
    spec = Path(args.spec)
    figures = Path(args.figures)
    if not spec.is_absolute():
        spec = root / spec
    if not figures.is_absolute():
        figures = root / figures
    try:
        count = render_specs(spec, figures, root)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Rendered charts: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
