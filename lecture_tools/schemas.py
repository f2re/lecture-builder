from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from .io import load_json
from .models import ValidationResult


def contracts_dir(root: str | Path) -> Path:
    return Path(root) / "contracts"


def load_schema(root: str | Path, name: str) -> dict[str, Any]:
    filename = name if name.endswith(".json") else f"{name}.schema.json"
    return load_json(contracts_dir(root) / filename)


def validate_schema_file(path: str | Path) -> ValidationResult:
    result = ValidationResult(name=f"schema:{Path(path).name}")
    try:
        schema = load_json(path)
        Draft202012Validator.check_schema(schema)
    except (OSError, ValueError, SchemaError) as exc:
        result.add("schema.invalid", str(exc), path=path)
    return result


def validate_instance(
    instance: Any,
    schema: dict[str, Any],
    *,
    name: str,
    path: str | Path | None = None,
) -> ValidationResult:
    result = ValidationResult(name=name)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
        location = "/".join(str(item) for item in error.absolute_path) or "$"
        result.add(
            "schema.instance",
            error.message,
            path=path,
            location=location,
        )
    return result
