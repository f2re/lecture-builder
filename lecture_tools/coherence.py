from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

from .models import ValidationResult
from .numbering import CANONICAL_QUESTION_HEADING_RE

HEADING_RE = re.compile(r"^#{1,6}\s+", re.MULTILINE)
SENTENCE_RE = re.compile(r"(?<=[.!?…])\s+(?=[А-ЯЁA-Z])")
WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+(?:[-–][A-Za-zА-Яа-яЁё0-9]+)?")
TRANSITION_RE = re.compile(
    r"\b(?:таким образом|следовательно|поскольку|поэтому|однако|вместе с тем|"
    r"на основании|из этого следует|полученный результат|далее|следующий раздел|"
    r"предыдущий раздел|перейд[её]м|сначала|затем|наконец)\b",
    re.IGNORECASE,
)
BRIDGE_IN_RE = re.compile(
    r"\b(?:предыдущ|ранее|опираясь|исходя из|после рассмотрения|прежде чем)\w*",
    re.IGNORECASE,
)
BRIDGE_OUT_RE = re.compile(
    r"\b(?:далее|следующ|перейд[её]м|это позволяет|служит основой|подводит к)\w*",
    re.IGNORECASE,
)


def _strip_nonprose(text: str) -> str:
    text = re.sub(r"```.*?```|~~~.*?~~~", " ", text, flags=re.DOTALL)
    text = re.sub(r"\$\$.*?\$\$|\\\[.*?\\\]", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", " ", text)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = HEADING_RE.sub("", text)
    return text


def _words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def _split_sections(text: str) -> list[tuple[int, int, str, str]]:
    matches = list(CANONICAL_QUESTION_HEADING_RE.finditer(text))
    sections: list[tuple[int, int, str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append(
            (
                int(match.group("lecture")),
                int(match.group("question")),
                match.group("title").strip(),
                text[match.end() : end],
            )
        )
    return sections


def _normalized_paragraph(paragraph: str) -> str:
    paragraph = re.sub(r"\s+", " ", paragraph.strip().lower())
    paragraph = re.sub(r"[^a-zа-яё0-9 ]", "", paragraph)
    return paragraph


def validate_coherence(
    markdown: str,
    config: dict[str, Any] | None = None,
    *,
    path: str | Path | None = None,
) -> ValidationResult:
    result = ValidationResult(name="coherence-readability")
    prose = _strip_nonprose(markdown)
    words = _words(prose)
    sentences = [item.strip() for item in SENTENCE_RE.split(prose) if item.strip()]
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", prose) if item.strip()]
    sections = _split_sections(markdown)

    if not sections:
        result.add("coherence.sections", "Не найдены заголовки вида '## L.N. Название вопроса'", path=path)
    else:
        question_numbers = [question for _, question, _, _ in sections]
        expected = list(range(1, len(sections) + 1))
        if question_numbers != expected:
            result.add(
                "coherence.section_sequence",
                f"Вопросы должны идти последовательно: ожидалось {expected}, получено {question_numbers}",
                path=path,
            )
        if config:
            lecture_number = int(config.get("lecture_number") or 0)
            prefixes = [lecture for lecture, _, _, _ in sections]
            if any(prefix != lecture_number for prefix in prefixes):
                result.add(
                    "coherence.lecture_prefix",
                    f"Все вопросы должны иметь префикс лекции {lecture_number}",
                    path=path,
                    details={"prefixes": prefixes},
                )

    if config:
        questions = config.get("questions") or []
        if sections and len(sections) != len(questions):
            result.add(
                "coherence.section_count",
                f"Количество вопросов ({len(sections)}) не совпадает с конфигурацией ({len(questions)})",
                path=path,
            )
        quality = config.get("quality") or {}
        section_bounds = quality.get("section_words") or {"min": 1000, "max": 2600}
    else:
        section_bounds = {"min": 1000, "max": 2600}

    for _, number, title, body in sections:
        section_words = _words(_strip_nonprose(body))
        count = len(section_words)
        if count < int(section_bounds.get("min", 1000)):
            result.add(
                "coherence.section_short",
                f"Вопрос {number} слишком короткий: {count} слов",
                severity="warning",
                path=path,
                location=f"section:{number}",
            )
        if count > int(section_bounds.get("max", 2600)):
            result.add(
                "coherence.section_long",
                f"Вопрос {number} слишком длинный: {count} слов",
                severity="warning",
                path=path,
                location=f"section:{number}",
            )
        first_words = " ".join(section_words[:170])
        last_words = " ".join(section_words[-220:])
        if number > 1 and not BRIDGE_IN_RE.search(first_words):
            result.add(
                "coherence.bridge_in",
                f"В начале вопроса {number} не обнаружена содержательная связь с предыдущим материалом",
                severity="warning",
                path=path,
                location=f"section:{number}",
            )
        if number < len(sections) and not BRIDGE_OUT_RE.search(last_words):
            result.add(
                "coherence.bridge_out",
                f"В конце вопроса {number} не обнаружен переход к следующему вопросу",
                severity="warning",
                path=path,
                location=f"section:{number}",
            )
        if not re.search(r"^###\s+\d+\.\d+\.\d+\.\s+(?:Выводы|Итоги)", body, re.MULTILINE | re.IGNORECASE):
            result.add(
                "coherence.micro_conclusion",
                f"Вопрос {number} не содержит пронумерованный подраздел «Выводы»",
                path=path,
                location=f"section:{number}",
            )

    normalized = [
        _normalized_paragraph(item)
        for item in paragraphs
        if len(_words(item)) >= 18 and not item.lstrip().startswith(("|", ">"))
    ]
    duplicates = [paragraph for paragraph, count in Counter(normalized).items() if count > 1]
    if duplicates:
        result.add(
            "coherence.duplicate_paragraphs",
            "В лекции найдены повторяющиеся смысловые абзацы",
            path=path,
            details={"count": len(duplicates), "samples": duplicates[:3]},
        )

    long_paragraphs = [len(_words(item)) for item in paragraphs if len(_words(item)) > 180]
    if long_paragraphs:
        result.add(
            "readability.long_paragraph",
            "Есть абзацы длиннее 180 слов; их следует разделить по смыслу",
            severity="warning",
            path=path,
            details={"lengths": long_paragraphs[:10]},
        )

    average_sentence = round(len(words) / max(len(sentences), 1), 2)
    if average_sentence > 28:
        result.add(
            "readability.sentence_length",
            f"Средняя длина предложения {average_sentence} слов; целевой диапазон 12–25",
            severity="warning",
            path=path,
        )

    transition_count = len(TRANSITION_RE.findall(prose))
    transition_density = transition_count / max(len(words), 1) * 1000
    if len(words) > 800 and transition_density < 2.0:
        result.add(
            "coherence.transition_density",
            "Низкая плотность явных логических связок",
            severity="warning",
            path=path,
            details={"per_1000_words": round(transition_density, 2)},
        )

    if not re.search(r"^##\s+(?:Заключение|Заключение и подведение итогов)", markdown, re.MULTILINE | re.IGNORECASE):
        result.add("coherence.conclusion", "Итоговое заключение отсутствует", path=path)

    result.metrics = {
        "words": len(words),
        "sentences": len(sentences),
        "paragraphs": len(paragraphs),
        "sections": len(sections),
        "average_sentence_words": average_sentence,
        "transition_density_per_1000_words": round(transition_density, 2),
    }
    return result
