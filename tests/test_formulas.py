import json
from pathlib import Path

from lecture_tools.formulas import number_file, number_markdown, validate_formula_markdown


SOURCE = r"""
## Вопрос 1. Первая формула

$$
a = b + c \label{eq:first}
$$

где a, b и c — величины, единицы которых указаны в условии.

Из @eq:first следует следующий результат.

## Вопрос 2. Вторая формула

$$
d = 2a \label{eq:second}
$$

где d — искомая величина; a — ранее определённая величина.

Сочетая @eq:first и @eq:second, получаем итог.
"""


def test_numbering_is_lecture_wide_and_resolves_references() -> None:
    numbered, records, result = number_markdown(SOURCE, 4)
    assert result.ok, result.to_dict()
    assert [record.number for record in records] == ["4.1", "4.2"]
    assert r"\tag{4.1}" in numbered
    assert r"\tag{4.2}" in numbered
    assert "@eq:" not in numbered
    assert "(4.1)" in numbered and "(4.2)" in numbered
    validation = validate_formula_markdown(numbered, 4)
    assert validation.ok, validation.to_dict()


def test_duplicate_formula_label_is_rejected() -> None:
    duplicate = SOURCE + "\n$$\nx=y \\label{eq:first}\n$$\n\nгде x и y — величины.\n"
    _, _, result = number_markdown(duplicate, 4)
    assert any(item.code == "formula.duplicate_label" for item in result.errors)


def test_number_file_can_update_in_place(tmp_path: Path) -> None:
    source = tmp_path / "lecture.md"
    registry = tmp_path / "formula_registry.json"
    source.write_text(SOURCE, encoding="utf-8")
    result = number_file(source, source, registry, 9)
    assert result.ok
    assert r"\tag{9.1}" in source.read_text(encoding="utf-8")
    data = json.loads(registry.read_text(encoding="utf-8"))
    assert data["lecture_number"] == 9
    assert [item["number"] for item in data["formulas"]] == ["9.1", "9.2"]
