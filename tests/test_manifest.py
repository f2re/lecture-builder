from pathlib import Path

from lecture_tools.manifest import (
    load_or_create_manifest,
    mark_stage,
    save_manifest,
    stage_is_fresh,
)


def test_stage_freshness_uses_input_and_output_hashes(tmp_path: Path) -> None:
    (tmp_path / "input/literature").mkdir(parents=True)
    (tmp_path / "input/lecture_config.md").write_text("topic: test\n", encoding="utf-8")
    (tmp_path / "output").mkdir()
    output = tmp_path / "output/result.json"
    output.write_text("{}\n", encoding="utf-8")

    manifest = load_or_create_manifest(tmp_path, platform="codex")
    mark_stage(
        manifest,
        tmp_path,
        "test",
        status="complete",
        inputs=["input/lecture_config.md"],
        outputs=["output/result.json"],
    )
    save_manifest(tmp_path, manifest)
    assert stage_is_fresh(
        manifest,
        tmp_path,
        "test",
        ["input/lecture_config.md"],
        ["output/result.json"],
    )

    output.write_text('{"changed": true}\n', encoding="utf-8")
    assert not stage_is_fresh(
        manifest,
        tmp_path,
        "test",
        ["input/lecture_config.md"],
        ["output/result.json"],
    )
