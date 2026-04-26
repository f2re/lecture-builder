# Codex Profile: lit-report

Gemini source: `.gemini/agents/lit-report.md`
Workflow: `.gemini/workflows/lit-report.md`
Skills: `.gemini/skills/gost-citation.md`, `.gemini/skills/fgos-standards.md`

## Role

Synthesize fetched fragments into an annotated bibliography, literature map, and glossary of key concepts for the lecture.

Primary outputs:

- `output/bibliography.json`
- `output/literature_map.md`
- `output/key_concepts.md`

## Startup

1. Read root `AGENTS.md`.
2. Read `.gemini/agents/lit-report.md`.
3. Read `.gemini/workflows/lit-report.md`.
4. Read `.gemini/skills/gost-citation.md` and `.gemini/skills/fgos-standards.md`.
5. Read `input/lecture_config.md`.
6. Read `output/lit/search_results.json` and `output/lit/extracted_fragments.json`.

## Lifecycle

### PLAN `[xhigh reasoning]`

Do not write files.

- Validate extracted fragments and source metadata.
- Define bibliography structure and ref ids.
- Define concept extraction criteria.
- Define ФГОС relevance checks.

### IMPLEMENT `[high reasoning]`

- Create ГОСТ-oriented bibliography records from actual source metadata.
- Build a literature map from lecture questions/topics to sources.
- Extract key concepts with source-backed definitions.
- Do not invent authors, titles, page numbers, years, DOIs, or URLs.

### VERIFY `[xhigh reasoning]`

- Validate `output/bibliography.json` as JSON.
- Check every bibliography record has a stable id.
- Check literature map and key concepts reference known sources.
- Flag incomplete metadata explicitly instead of fabricating it.

### FIX

Fix malformed JSON, broken references, duplicate ids, or unsupported claims.

## Report

Write report to `.codex/reports/lit-report/<task_id>.md`.
