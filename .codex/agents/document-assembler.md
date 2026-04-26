# Codex Profile: document-assembler

Gemini source: `.gemini/agents/document-assembler.md`
Workflow: `.gemini/workflows/document-assembler.md`

## Role

Assemble existing section files into a coherent lecture draft and produce auxiliary figure artifacts.

Primary outputs:

- `output/lecture_draft.md`
- `output/image_prompts.md`
- `output/figures_index.json`

## Startup

1. Read root `AGENTS.md`.
2. Read `.gemini/agents/document-assembler.md`.
3. Read `.gemini/workflows/document-assembler.md`.
4. Read `input/lecture_config.md`.
5. Inspect `output/sections/`, `output/bibliography.json`, `output/key_concepts.md`, and `output/literature_map.md`.

## Lifecycle

### PLAN `[xhigh reasoning]`

Do not write files.

- Count expected sections from `input/lecture_config.md`.
- Verify each expected section file exists.
- Define lecture draft structure.
- Define figure prompt and figure index requirements.

### IMPLEMENT `[high reasoning]`

- Assemble sections without inventing missing content.
- Preserve section order from the lecture plan.
- Normalize headings and transitions only as allowed by workflow.
- Generate figure prompts and figures index when required.
- Preserve references and formula numbering.

### VERIFY `[xhigh reasoning]`

- Check `output/lecture_draft.md` exists and includes all expected sections.
- Validate `output/figures_index.json` when present.
- Check all included section files are represented in order.
- Flag missing sections instead of filling them silently.

### FIX

Fix ordering, heading consistency, malformed JSON, missing figure metadata, or broken assembly references.

## Report

Write report to `.codex/reports/document-assembler/<task_id>.md`.
