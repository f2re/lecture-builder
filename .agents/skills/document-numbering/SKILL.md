---
name: document-numbering
description: Apply and verify lecture-derived numbering for questions, subsections, formulas, figures and tables. Use during architecture, section authoring, assembly, editing and publication whenever lecture_number is present.
---

# Document numbering

`lecture_number` in `input/lecture_config.md` is the single numbering root. For lecture 17:

- questions: `17.1`, `17.2`, `17.3`;
- subsections of the first question: `17.1.1`, `17.1.2`;
- deeper subsection when needed: `17.1.1.1`;
- formulas: `(17.1)`, `(17.2)`, `(17.3)` in document order;
- figures: `Рисунок 17.1`, `Рисунок 17.2` in document order;
- tables: `Таблица 17.1`, `Таблица 17.2` in document order.

Technical file names continue to use the local ordinal (`section_1_...`, `section_2_...`) so changing the lecture number does not rename intermediate paths.

## Canonical Markdown

```markdown
## 17.1. Первый учебный вопрос

### 17.1.1. Первое логическое звено

### 17.1.2. Второе логическое звено
```

Question titles in the configuration and the visible lecture plan use the same display form; the plan uses bullet entries such as `- **17.1. Первый учебный вопрос**`. Legacy `1. ...` items may be migrated, but generated lecture headings must always use `lecture_number.question`.

## Deterministic operations

Normalize headings before review:

```bash
python scripts/number_structure.py output/lecture_draft.md -o output/lecture_draft.md
```

Validate headings, figures and tables:

```bash
python scripts/validate_numbering.py output/lecture_final.md
```

Formula numbering remains a separate deterministic pass after fact check. Never restart formula or figure counters inside a question. Methodical callouts are typed but visibly unnumbered so they do not compete with the scientific hierarchy.
