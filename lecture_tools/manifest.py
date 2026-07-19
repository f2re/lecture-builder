from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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
        "prompt_version": SCHEMA_VERSION,
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
        return manifest
    return new_manifest(platform=platform, config_hash=config_hash, literature_hash=literature_hash)


def calculate_stage_input_hash(root: str | Path, inputs: list[str]) -> str:
    return hash_paths(root, inputs)


def stage_is_fresh(
    manifest: dict[str, Any],
    root: str | Path,
    stage: str,
    inputs: list[str],
    outputs: list[str],
) -> bool:
    record = (manifest.get("stages") or {}).get(stage)
    if not isinstance(record, dict) or record.get("status") != "complete":
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
    stages[stage] = {
        "status": status,
        "updated_at": utc_now(),
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
