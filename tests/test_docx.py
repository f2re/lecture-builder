from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from lecture_tools.docx_validation import validate_docx
from scripts.md2docx.md2docx_gost import (
    build_reference,
    convert_with_pandoc,
    postprocess,
    preprocess_markdown,
)

pytestmark = pytest.mark.skipif(shutil.which("pandoc") is None, reason="pandoc is not installed")


def test_docx_contains_native_numbered_equation(tmp_path: Path) -> None:
    source = tmp_path / "lecture.md"
    source.write_text(
        r"""
# ЛЕКЦИЯ 4. Тест

## Вопрос 1. Формула

Рассмотрим зависимость.

$$
y = ax + b \tag{4.1}
$$

где y — зависимая величина; x — аргумент; a и b — параметры.

## Заключение

Формула задаёт линейную зависимость.
""".strip(),
        encoding="utf-8",
    )
    reference = tmp_path / "reference.docx"
    output = tmp_path / "lecture.docx"
    build_reference(reference)
    markdown, numbers = preprocess_markdown(source)
    assert numbers == ["4.1"]
    assert "[[EQNO:4.1]]" in markdown
    convert_with_pandoc(markdown, reference, output, toc=False)
    postprocess(output, numbers)
    result = validate_docx(output, expect_formulas=True)
    assert result.ok, result.to_dict()
    assert result.metrics["numbered_equation_tables"] == 1
    assert result.metrics["omml_nodes"] > 0
