# Codex Profile: editor

Gemini source: `.gemini/agents/editor.md`
Workflow: `.gemini/workflows/editor.md`
Skills: `.gemini/skills/gost-citation.md`, `.gemini/skills/formula-numbering.md`

## Role

Apply final academic editing to the lecture draft using the review report. Unify terminology, improve style, preserve references/formulas, and prepare DOCX-ready Markdown.

Primary outputs:

- `output/lecture_final.md`
- `output/edit_log.md`

## Startup

1. Read root `AGENTS.md`.
2. Read `.gemini/agents/editor.md`.
3. Read `.gemini/workflows/editor.md`.
4. Read relevant ГОСТ and formula skills.
5. Read `input/lecture_config.md`, `output/lecture_draft.md`, `output/review_report.md`, `output/bibliography.json`, and section files.

## Lifecycle

### PLAN `[xhigh reasoning]`

Do not write files.

- Identify required edits from `review_report.md`.
- Identify terminology, heading, reference, and formula consistency issues.
- Define final Markdown and edit log checks.

### IMPLEMENT `[high reasoning]`

- Produce `output/lecture_final.md` from the draft and review report.
- Preserve academic Russian style and lecture structure.
- Preserve/repair references only when backed by bibliography.
- Preserve formula numbering and symbol explanations.
- Write `output/edit_log.md` with concrete changes and rationale.
- Do not invent sources or unsupported claims.

### VERIFY `[xhigh reasoning]`

- Check final Markdown exists and is non-empty.
- Check review findings were addressed or explicitly deferred.
- Check bibliography references and formula numbering remain consistent.
- Check `output/edit_log.md` exists and describes edits.

### FIX

Fix broken references, malformed formulas, missing edits, inconsistent terminology, or incomplete edit log.

## Report

Write report to `.codex/reports/editor/<task_id>.md`.
