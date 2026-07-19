from __future__ import annotations

import re
import tomllib
from pathlib import Path

import yaml

from .io import load_json
from .models import ValidationResult
from .schemas import validate_schema_file

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _validate_skill(path: Path, result: ValidationResult, names: dict[str, Path]) -> None:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        result.add("skill.frontmatter", "SKILL.md не содержит YAML frontmatter", path=path)
        return
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        result.add("skill.frontmatter_parse", str(exc), path=path)
        return
    if not isinstance(metadata, dict):
        result.add("skill.frontmatter_type", "Frontmatter должен быть mapping", path=path)
        return
    name = metadata.get("name")
    description = metadata.get("description")
    if not isinstance(name, str) or not name.strip():
        result.add("skill.name", "Поле name обязательно", path=path)
    elif name in names:
        result.add(
            "skill.duplicate_name",
            f"Имя skill '{name}' уже используется",
            path=path,
            details={"first": str(names[name])},
        )
    else:
        names[name] = path
    if not isinstance(description, str) or len(description.strip()) < 30:
        result.add(
            "skill.description",
            "Описание skill должно ясно задавать область применения и содержать не менее 30 символов",
            path=path,
        )
    if len(text) > 16_000:
        result.add(
            "skill.size",
            "SKILL.md длиннее 16 000 символов; вынесите справку в references/",
            severity="warning",
            path=path,
        )


def _validate_codex_agent(path: Path, result: ValidationResult, names: dict[str, Path]) -> None:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        result.add("codex.toml", str(exc), path=path)
        return
    for field in ("name", "description", "developer_instructions"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            result.add("codex.required", f"Обязательное поле '{field}' отсутствует", path=path)
    name = data.get("name")
    if isinstance(name, str):
        if name in names:
            result.add(
                "codex.duplicate_name",
                f"Имя агента '{name}' уже используется",
                path=path,
                details={"first": str(names[name])},
            )
        else:
            names[name] = path
    sandbox = data.get("sandbox_mode")
    if sandbox not in (None, "read-only", "workspace-write", "danger-full-access"):
        result.add("codex.sandbox", f"Неизвестный sandbox_mode: {sandbox}", path=path)


def validate_project(root: str | Path) -> ValidationResult:
    base = Path(root)
    result = ValidationResult(name="project-source")

    required_files = [
        "AGENTS.md",
        "README.md",
        ".codex/config.toml",
        ".agents/rules/00-project-core.md",
        ".agents/workflows/build-lecture.md",
        "scripts/validate_pipeline.py",
        "scripts/number_formulas.py",
        "scripts/md2docx/md2docx_gost.py",
    ]
    for relative in required_files:
        path = base / relative
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            result.add("project.required", "Обязательный файл отсутствует или пуст", path=path)

    agents_path = base / "AGENTS.md"
    if agents_path.is_file() and agents_path.stat().st_size > 32 * 1024:
        result.add(
            "project.agents_size",
            "AGENTS.md превышает стандартный лимит Codex 32 KiB",
            path=agents_path,
        )

    skill_names: dict[str, Path] = {}
    for path in sorted((base / ".agents/skills").glob("*/SKILL.md")):
        _validate_skill(path, result, skill_names)
    if len(skill_names) < 10:
        result.add(
            "project.skill_count",
            "Ожидается не менее 10 специализированных skills",
            path=base / ".agents/skills",
        )

    codex_names: dict[str, Path] = {}
    for path in sorted((base / ".codex/agents").glob("*.toml")):
        _validate_codex_agent(path, result, codex_names)
    if len(codex_names) < 8:
        result.add(
            "project.codex_agent_count",
            "Ожидается не менее 8 специализированных Codex agents",
            path=base / ".codex/agents",
        )

    legacy_profiles = [
        path
        for path in (base / ".codex/agents").glob("*.md")
        if path.name.lower() != "readme.md"
    ]
    if legacy_profiles:
        result.add(
            "project.legacy_codex_profiles",
            "Старые Markdown-профили Codex должны быть удалены",
            path=base / ".codex/agents",
            details={"files": [str(path) for path in legacy_profiles]},
        )

    for path in sorted((base / "contracts").glob("*.schema.json")):
        result.extend(validate_schema_file(path))
    if not list((base / "contracts").glob("*.schema.json")):
        result.add("project.schemas_missing", "JSON Schemas отсутствуют", path=base / "contracts")

    config_path = base / ".codex/config.toml"
    if config_path.is_file():
        try:
            codex_config = tomllib.loads(config_path.read_text(encoding="utf-8"))
            agents = codex_config.get("agents", {})
            if agents.get("max_depth", 1) > 1:
                result.add(
                    "project.codex_depth",
                    "max_depth > 1 повышает риск неконтролируемого fan-out",
                    severity="warning",
                    path=config_path,
                )
        except tomllib.TOMLDecodeError as exc:
            result.add("project.codex_config", str(exc), path=config_path)

    settings_path = base / ".gemini/settings.json"
    if settings_path.is_file():
        try:
            settings = load_json(settings_path)
            if str(settings.get("version", "")).startswith("2."):
                result.add(
                    "project.gemini_version",
                    "Gemini compatibility adapter должен иметь версию 3.x",
                    path=settings_path,
                )
        except ValueError as exc:
            result.add("project.gemini_settings", str(exc), path=settings_path)

    result.metrics = {
        "skills": len(skill_names),
        "codex_agents": len(codex_names),
        "schemas": len(list((base / "contracts").glob("*.schema.json"))),
        "rules": len(list((base / ".agents/rules").glob("*.md"))),
        "workflows": len(list((base / ".agents/workflows").glob("*.md"))),
    }
    return result
