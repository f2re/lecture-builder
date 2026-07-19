---
name: docx-publishing
description: Convert validated final Markdown into a ГОСТ-oriented, readable DOCX with native Word equations, right-aligned equation numbers, styles, margins, page numbering and structural smoke checks. Use only after fact check and deterministic formula numbering.
---

# DOCX publishing

## Inputs

- numbered `output/lecture_final.md`
- `output/formula_registry.json`
- `input/lecture_config.md`
- converter under `scripts/md2docx/`

## Output

- `output/lecture_final.docx`

## Procedure

1. Confirm strict Markdown/JSON validation has no errors.
2. Run `bash scripts/md2docx/run_md2docx.sh output/lecture_final.md -o output/lecture_final.docx`.
3. The converter must preserve native OMML equations and place each numbered display equation in a borderless three-column row: spacer, centered equation, right-aligned number.
4. Apply A4 page size, configured ГОСТ-oriented margins, Times New Roman body text, consistent headings, paragraph indents, line spacing, table/caption styles and page numbering.
5. Keep hyperlinks, lists, tables, Cyrillic symbols and mathematical indices intact.
6. Run `python scripts/validate_docx.py output/lecture_final.docx --expect-formulas` when formulas are required.

## Blocking checks

- DOCX missing or empty;
- no native OMML for a lecture requiring formulas;
- equation numbers missing or mismatched with registry;
- invalid page margins/font/footer;
- unresolved image placeholders when final publication requires embedded figures;
- Pandoc or dependency failure.

Never report successful DOCX publication from file existence alone.
