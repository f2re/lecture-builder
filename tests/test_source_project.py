from pathlib import Path

from lecture_tools.config import validate_config
from lecture_tools.project import validate_project

ROOT = Path(__file__).resolve().parents[1]


def test_project_source_is_structurally_valid() -> None:
    result = validate_project(ROOT)
    assert result.ok, result.to_dict()
    assert result.metrics["skills"] >= 15
    assert result.metrics["codex_agents"] >= 12
    assert result.metrics["schemas"] >= 10


def test_repository_config_is_valid() -> None:
    result = validate_config(ROOT / "input/lecture_config.md", ROOT)
    assert result.ok, result.to_dict()
