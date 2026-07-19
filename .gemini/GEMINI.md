# Lecture Builder 3.0 — Gemini compatibility gateway

The canonical project policy is `../AGENTS.md`. Canonical rules, workflows and Skills are under `../.agents/`. Read those files first. This `.gemini/` directory preserves legacy Gemini CLI entry points and role names; it must not become a second source of scientific or pedagogical truth.

## Full build

Use the legacy command `gemini build-lecture` or invoke `@agents/orchestrator.md`. The orchestrator follows `../.agents/workflows/build-lecture.md`, validates hashes and delegates specialist work.

## Input

Required: `../input/lecture_config.md`. Validate it with:

```bash
python scripts/validate_pipeline.py --mode source
```

## Core integrity

- never invent sources, metadata, pages or evidence;
- use source-id citations and verified evidence;
- design a lecture blueprint before sections;
- write one section per isolated call;
- number formulas only once after final fact check;
- run strict validation and DOCX inspection before success.
