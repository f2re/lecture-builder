---
name: methodical-enrichment
description: Design concise, evidence-safe thematic examples, mnemonics, formula-reading aids, common-error warnings and self-check callouts for completed lecture sections. Use after section authoring and before assembly; do not edit section files or introduce new scientific claims.
---

# Methodical enrichment

## Inputs

- `input/lecture_config.md`
- `output/lecture_blueprint.json`
- all `output/section_briefs/section_*.json`
- all `output/sections/section_*.md`
- `output/evidence_ledger.json`
- `output/key_concepts.md`
- `contracts/methodical-inserts.schema.json`

## Output

Write only `output/methodical_inserts.json`. The coherence editor renders and inserts the approved callouts into `output/lecture_draft.md`; this agent never edits section files or the lecture directly.

## Insert types

Use the smallest useful set for each question:

- `key_idea` — one-sentence conceptual anchor;
- `mnemonic` — a short memory device that preserves the scientific meaning;
- `thematic_example` — a discipline-specific mini-case tied to the current concept;
- `formula_reading` — how to read a formula conceptually, including sign, direction and limiting behavior;
- `common_mistake` — likely error and its correction;
- `self_check` — one retrieval or transfer question with no hidden new theory;
- `comparison` — a compact distinction between easily confused concepts;
- `professional_context` — how the concept is used in the configured specialty;
- `visual_cue` — a verbal spatial image that supports, but does not replace, a scientific figure.

## Coverage and restraint

Follow `methodical` settings from the configuration. Normally each question should cover the functions `understand`, `remember`, `apply` and `self_check` using four or five inserts. Keep the combined insert text below the configured word share. Do not place two callouts consecutively, repeat the main prose or decorate every paragraph.

A mnemonic is acceptable only when it is:

- short enough to recall;
- unambiguous for the target audience;
- reversible back to the correct concept;
- free from false causal, spatial or mathematical implications.

## Scientific integrity

Factual inserts must reference supported `claim_id` or `evidence_id` values. A made-up numerical scenario is allowed only with `hypothetical: true` and must be visibly described as illustrative. Never invent observational values, source metadata, formula behavior or professional procedures.

## Placement

Each insert identifies a stable section, question number and insertion strategy. Prefer placement after the concept or formula it clarifies. Use an exact anchor text or hash when available. The visible rendering is a restrained Markdown blockquote, for example:

```markdown
<!-- methodical:ins:q1:mnemonic:1 -->
> **Мнемоника: «выше — меньше давления».** Используйте её только для запоминания направления изменения давления с высотой; количественная связь задаётся уравнением гидростатики.
```

The insert id remains hidden in DOCX and supports deterministic validation.

## Verification

Validate JSON Schema, section/question numbering, type density, learning-function coverage, claim/evidence references, hypothetical labeling and required markers in the assembled draft and final lecture. Pedagogical review may reject an insert that is distracting, misleading or redundant; scientific review checks every fact-bearing insert.
