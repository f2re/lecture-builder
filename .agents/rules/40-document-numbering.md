# Lecture-derived document numbering

`lecture_number` in `input/lecture_config.md` is the single visible numbering root.

For lecture 17:

- questions are `17.1`, `17.2`, ...;
- subsections of question 17.1 are `17.1.1`, `17.1.2`, ...;
- deeper headings may use `17.1.1.1` only when the hierarchy genuinely requires it;
- formulas are numbered globally `(17.1)`, `(17.2)`, ... in document order;
- figures are numbered globally `Рисунок 17.1`, `Рисунок 17.2`, ...;
- tables are numbered globally `Таблица 17.1`, `Таблица 17.2`, ...;
- formula, figure and table counters never restart inside a question.

Technical file paths keep local ordinals such as `section_1_...` and `section_2_...`. Methodical callouts are visibly typed but unnumbered. Generated Markdown must pass `scripts/validate_numbering.py`.
