# Codex Profile: lit-searcher

Gemini source: `.gemini/agents/lit-searcher.md`
Workflow: `.gemini/workflows/lit-searcher.md`
Skills: `.gemini/skills/search-patterns.md`

## Role

Build a Russian/English search matrix, discover academic and educational sources, and index local literature from `input/literature/`.

Primary output: `output/lit/search_results.json`.

## Startup

1. Read root `AGENTS.md`.
2. Read `.gemini/agents/lit-searcher.md`.
3. Read `.gemini/workflows/lit-searcher.md`.
4. Read `.gemini/skills/search-patterns.md`.
5. Read `input/lecture_config.md` and optional `input/existing_refs.md`.
6. Inspect local files under `input/literature/`.

## Lifecycle

### PLAN `[xhigh reasoning]`

Do not write files.

- Extract topic, discipline, competencies, questions, and language.
- Build source categories and query matrix.
- Determine whether existing `output/lit/search_results.json` should be reused.
- Define JSON schema expectations.

### IMPLEMENT `[high reasoning]`

- Search or document search blockers.
- Include local source references when available.
- Store discovered sources in valid JSON.
- Do not invent URLs, titles, authors, or publication years.

### VERIFY `[xhigh reasoning]`

- Validate `output/lit/search_results.json` as JSON.
- Check each result has enough metadata to support later fetching/reporting.
- Flag weak, duplicated, inaccessible, or non-academic sources.

### FIX

Fix only malformed JSON, duplicates, or unsupported metadata issues.

## Report

Write report to `.codex/reports/lit-searcher/<task_id>.md`.
