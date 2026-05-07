# Codex Profile: lit-fetcher

Gemini source: `.gemini/agents/lit-fetcher.md`
Workflow: `.gemini/workflows/lit-fetcher.md`

## Role

Fetch selected sources from `output/lit/search_results.json` and extract relevant fragments for the lecture topic and questions.

Primary output: `output/lit/extracted_fragments.json`.

## Startup

1. Read root `AGENTS.md`.
2. Read `.gemini/agents/lit-fetcher.md`.
3. Read `.gemini/workflows/lit-fetcher.md`.
4. Read `input/lecture_config.md`.
5. Read `output/lit/search_results.json`.

## Lifecycle

### PLAN `[xhigh reasoning]`

Do not write files.

- Validate search results JSON.
- Select top sources according to workflow criteria.
- Identify network/fetch limitations.
- Define extracted fragment schema.

### IMPLEMENT `[high reasoning]`

- Fetch or read available sources.
- Extract relevant fragments with source provenance.
- Preserve source ids from search results.
- Do not fabricate text fragments, page numbers, or source content.

### VERIFY `[xhigh reasoning]`

- Validate `output/lit/extracted_fragments.json` as JSON.
- Check each fragment references an existing search result/source id.
- Check fragments are relevant to topic/questions and contain enough context for reporting.

### FIX

Fix malformed JSON, broken source links, duplicates, or missing provenance.

## Report

Write report to `.codex/reports/lit-fetcher/<task_id>.md`.
