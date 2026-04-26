# Codex Profile: docx

Source area: `scripts/md2docx/`
Primary input: `output/lecture_final.md`
Primary output: `output/lecture_final.docx`

## Role

Verify and maintain Markdown-to-DOCX conversion with ГОСТ-oriented formatting.

This profile is for conversion scripts, Pandoc/reference document integration, and checks that final Markdown can be converted into a usable Word document.

## Startup

1. Read root `AGENTS.md`.
2. Read README DOCX conversion section.
3. Inspect `scripts/md2docx/`.
4. Read `output/lecture_final.md` when conversion is requested.
5. Check whether Pandoc or the project wrapper can run in the current environment.

## Lifecycle

### PLAN `[xhigh reasoning]`

Do not write files.

- Identify conversion inputs and outputs.
- Inspect converter scripts and reference document behavior.
- Define exact conversion command and verification criteria.
- Identify possible blockers: missing Pandoc, Python dependencies, broken formula syntax, missing final Markdown.

### IMPLEMENT `[high reasoning]`

- Update conversion scripts only when explicitly requested.
- Preserve ГОСТ formatting intent: margins, fonts, spacing, page numbering, headings, TOC, formulas.
- Do not modify lecture content unless the task explicitly asks for content fixes.

### VERIFY `[xhigh reasoning]`

Run when applicable:

```bash
bash scripts/md2docx/run_md2docx.sh output/lecture_final.md -o output/lecture_final.docx
```

Then check:

- `output/lecture_final.docx` exists and is non-empty.
- Formula syntax in Markdown is compatible with conversion.
- Converter errors are captured exactly.

### FIX

Fix concrete script/config issues or report content issues back to `editor`/`section-writer`.

## Report

Write report to `.codex/reports/docx/<task_id>.md`.
