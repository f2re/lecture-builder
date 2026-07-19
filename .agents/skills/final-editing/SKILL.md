---
name: final-editing
description: Apply approved scientific and pedagogical review findings to produce the final coherent Markdown, edit log and resolved-finding map while preserving evidence and formula semantics. Use after independent reviews and before final fact check.
---

# Final editing

## Inputs

- `output/lecture_draft.md`
- `output/reviews/scientific.json`
- `output/reviews/pedagogical.json`
- `output/lecture_blueprint.json`
- `output/evidence_ledger.json`
- `output/bibliography.json`
- `input/lecture_config.md`

## Outputs

- `output/lecture_final.md` before deterministic formula numbering
- `output/edit_log.md`
- `output/reviews/resolution.json`

## Editing procedure

1. Enumerate all blocking and non-blocking findings and map each to an explicit action.
2. Resolve critical and major findings first. A scientifically material correction must use existing evidence or return the task to research/section writing.
3. Improve logical flow, paragraph focus, terminology, notation, grammar and accessibility without changing supported meaning.
4. Preserve stable source ids, claim scope, caveats, formula labels and `@eq:*` references.
5. Remove repetition and generic transitions; replace them with relations derived from the blueprint.
6. Record each changed passage, finding id, action, rationale and evidence used.
7. Mark any deferred finding with a reason and publication consequence. Never claim it is resolved.

## Prohibitions

- no new source or page metadata;
- no formula-semantic change without scientific re-review;
- no deletion of limitation text merely for fluency;
- no editing of `lecture_draft.md` in place;
- no self-certification of fact-check status.

## Completion

Run deterministic checks, then hand the result to a separate scientific fact checker. The editor's work is not final until fact check passes.
