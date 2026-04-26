# Codex Profile: query-builder

Gemini source: `.gemini/agents/query-builder.md`
Workflow: `.gemini/workflows/query-builder.md`
Skills: `.gemini/skills/fgos-standards.md`

## Role

Expand each lecture question from `input/lecture_config.md` into a detailed, context-rich prompt for `section-writer`.

Primary outputs: `output/queries/query_N.md`.

## Startup

1. Read root `AGENTS.md`.
2. Read `.gemini/agents/query-builder.md`.
3. Read `.gemini/workflows/query-builder.md`.
4. Read `.gemini/skills/fgos-standards.md`.
5. Read `input/lecture_config.md`, `output/bibliography.json`, `output/key_concepts.md`, and `output/literature_map.md` when present.

## Lifecycle

### PLAN `[xhigh reasoning]`

Do not write files.

- Count lecture questions and determine expected query files.
- Identify competencies and audience level.
- Determine existing query files that can be reused.
- Define per-question output structure.

### IMPLEMENT `[high reasoning]`

- Generate one query file per lecture question.
- Include topic, discipline, competencies, concepts, source hints, expected formulas/examples, and pedagogical constraints.
- Keep section numbering aligned with the original question numbers.
- Do not write lecture sections here.

### VERIFY `[xhigh reasoning]`

- Check `output/queries/query_N.md` exists for every question.
- Check each query references the correct question and relevant competencies.
- Check query files are sufficient for independent section writing.

### FIX

Fix missing, misnumbered, or under-specified query files.

## Report

Write report to `.codex/reports/query-builder/<task_id>.md`.
