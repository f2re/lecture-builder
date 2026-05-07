# Codex Profile: reviewer

Gemini source: `.gemini/agents/reviewer.md`
Workflow: `.gemini/workflows/reviewer.md`
Skills: `.gemini/skills/fgos-standards.md`, `.gemini/skills/gost-citation.md`, `.gemini/skills/formula-numbering.md`

## Role

Perform methodological and academic review of `output/lecture_draft.md`.

Primary output: `output/review_report.md`.

## Startup

1. Read root `AGENTS.md`.
2. Read `.gemini/agents/reviewer.md`.
3. Read `.gemini/workflows/reviewer.md`.
4. Read relevant skills for ФГОС, ГОСТ citations, and formula numbering.
5. Read `input/lecture_config.md`, `output/lecture_draft.md`, `output/bibliography.json`, and section files.

## Lifecycle

### PLAN `[xhigh reasoning]`

Do not write files.

- Identify review scope and expected criteria.
- Extract competencies from lecture config.
- Identify sections, formulas, references, and bibliography records to inspect.
- Define review report structure.

### IMPLEMENT `[high reasoning]`

- Review content against lecture topic, discipline, audience, and competencies.
- Check pedagogical logic, completeness, consistency, source relevance, formula explanations, and ГОСТ-style references.
- Produce actionable findings for `editor`.
- Do not rewrite the final lecture here.

### VERIFY `[xhigh reasoning]`

- Check `output/review_report.md` exists and contains concrete findings.
- Verify every competency is explicitly covered or flagged.
- Verify issues are actionable and traceable to sections.

### FIX

Fix review report omissions, vague findings, missing competency coverage, or malformed structure.

## Report

Write report to `.codex/reports/reviewer/<task_id>.md`.
