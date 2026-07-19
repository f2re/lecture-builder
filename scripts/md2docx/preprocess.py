from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

FENCED_CODE_RE = re.compile(r"(```.*?```|~~~.*?~~~)", re.DOTALL)
FRONT_MATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
BRACKET_INLINE_RE = re.compile(r"\\\(\s*(.*?)\s*\\\)", re.DOTALL)
BRACKET_DISPLAY_RE = re.compile(r"\\\[\s*(.*?)\s*\\\]", re.DOTALL)
TAGGED_DISPLAY_RE = re.compile(
    r"\$\$\s*(?P<expression>.*?)\s*\\tag\{(?P<number>\d+\.\d+)\}\s*\$\$",
    re.DOTALL,
)


def _outside_code_segments(text: str) -> Iterable[tuple[bool, str]]:
    for index, part in enumerate(FENCED_CODE_RE.split(text)):
        yield index % 2 == 0, part


def preprocess_markdown(source: Path) -> tuple[str, list[str]]:
    """Normalize Markdown and move equation tags outside math for Pandoc."""

    text = source.read_text(encoding="utf-8")
    text = FRONT_MATTER_RE.sub("", text)
    text = HTML_COMMENT_RE.sub("", text)
    numbers: list[str] = []

    def process(segment: str) -> str:
        segment = BRACKET_INLINE_RE.sub(lambda m: f"${m.group(1).strip()}$", segment)
        segment = BRACKET_DISPLAY_RE.sub(lambda m: f"$$\n{m.group(1).strip()}\n$$", segment)

        def move_tag(match: re.Match[str]) -> str:
            number = match.group("number")
            numbers.append(number)
            expression = match.group("expression").strip()
            return f"$$\n{expression}\n$$\n\n[[EQNO:{number}]]"

        return TAGGED_DISPLAY_RE.sub(move_tag, segment)

    normalized = "".join(process(part) if is_text else part for is_text, part in _outside_code_segments(text))
    normalized = re.sub(r"\n{4,}", "\n\n\n", normalized).strip() + "\n"
    return normalized, numbers
