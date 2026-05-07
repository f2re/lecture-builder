# Codex Profile: section-writer

Gemini source: `.gemini/agents/section-writer.md`
Workflow: `.gemini/workflows/section-writer.md`
Skills: `.gemini/skills/formula-numbering.md`

## Role

Write or revise one lecture section in Russian academic and pedagogical style.

Primary outputs: `output/sections/section_{N}_{slug}.md`.

## Startup

1. Read root `AGENTS.md`.
2. Read `.gemini/agents/section-writer.md`.
3. Read `.gemini/workflows/section-writer.md`.
4. Read `.gemini/skills/formula-numbering.md` when formulas are required.
5. Read `input/lecture_config.md`.
6. Read the relevant `output/queries/query_N.md`.
7. Read `output/bibliography.json`, `output/key_concepts.md`, and relevant literature artifacts when present.

## Lifecycle

### PLAN `[xhigh reasoning]`

Do not write files.

- Identify the target section number N.
- Validate the matching query file exists.
- Determine expected formulas, examples, definitions, and references.
- Define output filename and verification checks.

### IMPLEMENT `[high reasoning]`

- Write only the requested section.
- Use Russian academic style appropriate for the configured audience.
- Use ГОСТ formula numbering with `\tag{N.M}` when formulas are required.
- Explain symbols after each block formula.
- Use only source-backed references from bibliography/literature artifacts.
- Do not assemble the full lecture.

### VERIFY `[xhigh reasoning]`

- Check section file name follows `output/sections/section_{N}_{slug}.md`.
- Check headings, definitions, examples, formulas, and references.
- Verify formulas are numbered consistently and symbol explanations are present.
- Verify references resolve to bibliography records where applicable.

### FIX

Fix missing structure, malformed formulas, broken references, or naming issues.

## Report

Write report to `.codex/reports/section-writer/<task_id>.md`.
