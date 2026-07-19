from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .io import hash_paths, sha256_file
from .models import ValidationResult

TAG_RE = re.compile(r"\\tag\{(?P<number>\d+\.\d+)\}")


def validate_review_state(
    reports: dict[str, Any],
    resolution: Any | None,
    *,
    strict: bool,
) -> ValidationResult:
    result = ValidationResult(name="review-state")
    resolution_map: dict[tuple[str, str], dict[str, Any]] = {}
    if isinstance(resolution, dict):
        for item in resolution.get("resolutions") or []:
            if not isinstance(item, dict):
                continue
            key = (str(item.get("review_type")), str(item.get("finding_id")))
            if key in resolution_map:
                result.add("review.resolution_duplicate", f"Повторное решение для {key}")
            resolution_map[key] = item

    for expected_type, report in reports.items():
        if not isinstance(report, dict):
            continue
        if report.get("review_type") != expected_type:
            result.add(
                "review.type_mismatch",
                f"Ожидался review_type={expected_type}, получено {report.get('review_type')}",
            )
        if report.get("status") == "block":
            result.add("review.block", f"Рецензия {expected_type} имеет status=block")
        for check, status in (report.get("checks") or {}).items():
            if status == "fail":
                result.add("review.failed_check", f"{expected_type}: проверка {check} имеет status=fail")
        for finding in report.get("findings") or []:
            if not isinstance(finding, dict):
                continue
            severity = finding.get("severity")
            finding_id = str(finding.get("finding_id"))
            if expected_type in {"scientific", "pedagogical"} and severity in {"critical", "major"}:
                item = resolution_map.get((expected_type, finding_id))
                if not item or item.get("status") != "resolved":
                    result.add(
                        "review.unresolved",
                        f"Не разрешено замечание {expected_type}/{finding_id} ({severity})",
                    )
            if expected_type == "fact_check" and severity in {"critical", "major"}:
                result.add(
                    "review.fact_check_finding",
                    f"Fact check содержит блокирующее замечание {finding_id} ({severity})",
                )

    fact_check = reports.get("fact_check")
    if strict and (not isinstance(fact_check, dict) or fact_check.get("status") != "pass"):
        result.add("review.fact_check_status", "Финальный fact check должен иметь status=pass")

    result.metrics = {"reports": len(reports), "resolutions": len(resolution_map)}
    return result


def validate_formula_registry(
    registry: Any,
    markdown: str,
    *,
    lecture_number: int,
    path: str | Path | None = None,
) -> ValidationResult:
    result = ValidationResult(name="formula-registry-crossrefs")
    if not isinstance(registry, dict):
        result.add("formula.registry_type", "Formula registry должен быть объектом", path=path)
        return result
    formulas = registry.get("formulas") or []
    registry_numbers = [str(item.get("number")) for item in formulas if isinstance(item, dict)]
    markdown_numbers = [match.group("number") for match in TAG_RE.finditer(markdown)]
    if registry_numbers != markdown_numbers:
        result.add(
            "formula.registry_mismatch",
            "Номера в formula_registry.json не совпадают с Markdown",
            path=path,
            details={"registry": registry_numbers, "markdown": markdown_numbers},
        )
    ids = [str(item.get("formula_id")) for item in formulas if isinstance(item, dict)]
    if len(ids) != len(set(ids)):
        result.add("formula.registry_duplicate_id", "В реестре повторяются formula_id", path=path)
    expected_numbers = [f"{lecture_number}.{index}" for index in range(1, len(formulas) + 1)]
    if registry_numbers != expected_numbers:
        result.add(
            "formula.registry_sequence",
            f"Ожидалась последовательность {expected_numbers}, получено {registry_numbers}",
            path=path,
        )
    result.metrics = {"formulas": len(formulas)}
    return result


def validate_figure_index(
    figures_value: Any,
    markdown: str,
    *,
    lecture_number: int,
    source_ids: set[str],
    path: str | Path | None = None,
) -> ValidationResult:
    result = ValidationResult(name="figure-index-crossrefs")
    if not isinstance(figures_value, dict):
        result.add("figures.type", "Figure index должен быть объектом", path=path)
        return result
    figures = figures_value.get("figures") or []
    if figures_value.get("total_figures") != len(figures):
        result.add("figures.total", "total_figures не совпадает с длиной figures", path=path)
    numbers: list[str] = []
    ids: set[str] = set()
    for index, figure in enumerate(figures, start=1):
        if not isinstance(figure, dict):
            continue
        figure_id = str(figure.get("figure_id"))
        number = str(figure.get("number"))
        numbers.append(number)
        if figure_id in ids:
            result.add("figures.duplicate_id", f"Повторный figure_id {figure_id}", path=path)
        ids.add(figure_id)
        expected = f"{lecture_number}.{index}"
        if number != expected:
            result.add("figures.sequence", f"Ожидался номер {expected}, получено {number}", path=path)
        placeholder = figure.get("placeholder")
        if placeholder and str(placeholder) not in markdown and figure.get("status") != "omitted":
            result.add("figures.placeholder", f"Placeholder для {figure_id} отсутствует в лекции", path=path)
        for source_id in figure.get("data_source_ids") or []:
            if str(source_id) not in source_ids:
                result.add("figures.unknown_source", f"Рисунок {figure_id} использует неизвестный источник {source_id}", path=path)
    result.metrics = {"figures": len(figures)}
    return result


def validate_manifest_state(
    manifest: Any,
    root: str | Path,
    *,
    path: str | Path | None = None,
) -> ValidationResult:
    result = ValidationResult(name="manifest-freshness")
    if not isinstance(manifest, dict):
        result.add("manifest.type", "Manifest должен быть объектом", path=path)
        return result
    base = Path(root)
    config_path = base / "input/lecture_config.md"
    if config_path.is_file() and manifest.get("config_hash") != sha256_file(config_path):
        result.add("manifest.config_stale", "config_hash не соответствует текущей конфигурации", path=path)
    literature_hash = hash_paths(base, ["input/existing_refs.md", "input/literature"])
    if manifest.get("literature_hash") != literature_hash:
        result.add("manifest.literature_stale", "literature_hash не соответствует текущим входам", path=path)
    for stage, record in (manifest.get("stages") or {}).items():
        if not isinstance(record, dict) or record.get("status") != "complete":
            continue
        output_hashes = record.get("output_hashes") or {}
        for relative in record.get("outputs") or []:
            target = base / relative
            if not target.is_file():
                result.add("manifest.output_missing", f"Этап {stage}: отсутствует {relative}", path=path)
            elif output_hashes.get(relative) != sha256_file(target):
                result.add("manifest.output_stale", f"Этап {stage}: изменён {relative}", path=path)
    result.metrics = {"stages": len(manifest.get("stages") or {})}
    return result
