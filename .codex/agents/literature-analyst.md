# Codex Profile: literature-analyst

Gemini source: `.gemini/agents/literature-analyst.md`
Workflow: `.gemini/workflows/literature-analyst.md`

## Role

Coordinate the literature sub-pipeline: search, fetch, source extraction, annotated bibliography, literature map, and key concepts.

This profile delegates detailed work to `lit-searcher`, `lit-fetcher`, and `lit-report`.

## Startup

1. Read root `AGENTS.md`.
2. Read `.gemini/agents/literature-analyst.md`.
3. Read `.gemini/workflows/literature-analyst.md`.
4. Read relevant skills: `.gemini/skills/search-patterns.md`, `.gemini/skills/gost-citation.md`, `.gemini/skills/fgos-standards.md`.
5. Inspect `input/lecture_config.md`, `input/existing_refs.md`, `input/literature/`, and `output/lit/`.

## Lifecycle

### PLAN `[xhigh reasoning]`

Do not write files.

- Identify literature artifacts already present.
- Decide which subprofiles must run or be skipped.
- Define source quality criteria and expected outputs.
- Define JSON validation and bibliography checks.

### IMPLEMENT `[high reasoning]`

- Coordinate search → fetch → report sequence.
- Preserve existing literature artifacts unless regeneration is requested.
- Do not invent sources, bibliographic metadata, page numbers, or URLs.

### VERIFY `[xhigh reasoning]`

- Validate `output/lit/search_results.json` and `output/lit/extracted_fragments.json` when present.
- Verify `output/bibliography.json`, `output/literature_map.md`, and `output/key_concepts.md` exist for completed literature stage.
- Check that inline reference formats can be mapped to bibliography records where applicable.

### FIX

Fix orchestration defects or route source/fetch/report issues to the appropriate subprofile.

## Report

Write report to `.codex/reports/literature-analyst/<task_id>.md`.
