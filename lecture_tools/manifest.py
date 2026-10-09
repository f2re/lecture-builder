from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
import json

from .stage_graph import STAGE_DEPENDENCIES, expected_outputs_present

from .io import dump_json, hash_paths, load_json, sha256_file

SCHEMA_VERSION = "3.0"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def new_manifest(*, platform: str, config_hash: str, literature_hash: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": utc_now(),
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "platform": platform,
        "config_hash": config_hash,
        "literature_hash": literature_hash,
        "stages": {},
    }


def load_or_create_manifest(root: str | Path, *, platform: str) -> dict[str, Any]:
    base = Path(root)
    manifest_path = base / "output/run_manifest.json"
    config_hash = sha256_file(base / "input/lecture_config.md")
    literature_hash = hash_paths(base, ["input/existing_refs.md", "input/literature"])
    if manifest_path.is_file():
        manifest = load_json(manifest_path)
        if not isinstance(manifest, dict):
            raise ValueError("run_manifest.json must contain an object")
        manifest.pop("prompt_version", None)
        if manifest.get("config_hash") != config_hash or manifest.get("literature_hash") != literature_hash:
            for record in (manifest.get("stages") or {}).values():
                if isinstance(record, dict):
                    record["status"] = "stale"
            manifest["config_hash"] = config_hash
            manifest["literature_hash"] = literature_hash
        return manifest
    return new_manifest(platform=platform, config_hash=config_hash, literature_hash=literature_hash)


def calculate_stage_input_hash(root: str | Path, inputs: list[str]) -> str:
    base = Path(root)
    dependencies = {"AGENTS.md", "pyproject.toml"}
    for folder, pattern in ((".agents", "*.md"), ("contracts", "*.json"), ("lecture_tools", "*.py"), ("scripts", "*.py")):
        dependencies.update(p.relative_to(base).as_posix() for p in (base / folder).rglob(pattern) if "__pycache__" not in p.parts)
    return hash_paths(base, sorted(set(inputs) | dependencies))


def stage_is_fresh(
    manifest: dict[str, Any],
    root: str | Path,
    stage: str,
    inputs: list[str],
    outputs: list[str],
    *,
    validator: Callable[[], Any] | None = None,
) -> bool:
    record = (manifest.get("stages") or {}).get(stage)
    if not isinstance(record, dict) or record.get("status") != "complete":
        return False
    if record.get("inputs") != inputs or record.get("outputs") != outputs:
        return False
    base = Path(root)
    config = base / "input/lecture_config.md"
    if config.is_file() and manifest.get("config_hash") != sha256_file(config):
        return False
    if stage in STAGE_DEPENDENCIES and not expected_outputs_present(stage, outputs):
        return False
    for dependency in STAGE_DEPENDENCIES.get(stage, ()):
        parent = (manifest.get("stages") or {}).get(dependency) or {}
        if not stage_is_fresh(manifest, root, dependency, parent.get("inputs", []), parent.get("outputs", [])):
            return False
    current_input_hash = calculate_stage_input_hash(root, inputs)
    if record.get("input_hash") != current_input_hash:
        return False
    base = Path(root)
    output_hashes = record.get("output_hashes") or {}
    for relative in outputs:
        path = base / relative
        if not path.is_file() or output_hashes.get(relative) != sha256_file(path):
            return False
    if not _outputs_valid(base, outputs):
        return False
    if validator is not None:
        try:
            outcome = validator()
            return outcome is True or getattr(outcome, "ok", False) is True
        except (OSError, ValueError, TypeError):
            return False
    return True


def _outputs_valid(base: Path, outputs: list[str]) -> bool:
    """Current syntax/schema validation; semantic release gates run separately."""
    from .schemas import load_schema, validate_instance
    try:
        for relative in outputs:
            path = (base / relative).resolve()
            path.relative_to(base.resolve())
            if not path.is_file() or not path.stat().st_size:
                return False
            if path.suffix == ".json":
                value = load_json(path)
                name = path.stem.replace("_", "-")
                if path.name in {"scientific.json", "pedagogical.json", "fact_check.json"}:
                    name = "review-report"
                if (base / "contracts" / f"{name}.schema.json").is_file():
                    if not validate_instance(value, load_schema(base, name), name=f"stage-output:{relative}").ok:
                        return False
    except (OSError, ValueError, TypeError):
        return False
    return True


def mark_stage(
    manifest: dict[str, Any],
    root: str | Path,
    stage: str,
    *,
    status: str,
    inputs: list[str],
    outputs: list[str],
    notes: list[str] | None = None,
) -> dict[str, Any]:
    base = Path(root)
    stages = manifest.setdefault("stages", {})
    if status not in {"complete", "failed", "blocked", "in_progress", "stale"}:
        raise ValueError(f"Unknown stage status: {status}")
    if status == "complete":
        if stage in STAGE_DEPENDENCIES and not expected_outputs_present(stage, outputs):
            raise ValueError(f"Stage {stage} is missing required declared outputs")
        if not _outputs_valid(base, outputs):
            raise ValueError("Cannot complete a stage with missing or invalid outputs")
        for dependency in STAGE_DEPENDENCIES.get(stage, ()):
            record = stages.get(dependency) or {}
            if record.get("status") != "complete":
                raise ValueError(f"Stage {stage} requires completed {dependency}")
    stages[stage] = {
        "status": status,
        "updated_at": utc_now(),
        "inputs": inputs,
        "input_hash": calculate_stage_input_hash(root, inputs),
        "outputs": outputs,
        "output_hashes": {
            relative: sha256_file(base / relative)
            for relative in outputs
            if (base / relative).is_file()
        },
        "notes": notes or [],
    }
    manifest["updated_at"] = utc_now()
    return manifest


def save_manifest(root: str | Path, manifest: dict[str, Any]) -> None:
    dump_json(Path(root) / "output/run_manifest.json", manifest)
