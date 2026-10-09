---
name: pedagogical-review
description: Independently review audience fit, learning progression, examples, assessments, timing and visual usefulness. Use for «проверь понятность лекции»; do not edit the lecture or certify its scientific accuracy.
---

# Pedagogical review

Read target Markdown, config, blueprint, methodical inserts and figures/chart specs. Use a read-only context independent of authors and the scientific reviewer. Initial reports belong under output/reviews/draft/pedagogical.json; repeat review after editing and numbering and save final approval at output/reviews/pedagogical.json for lecture_final.md.

Check every intended learning outcome against the explanation, practice, assessment and answer criteria. Determine whether a student with the stated prerequisites can solve the control task using the lecture. Check concept order, cognitive load, paragraph focus, motivated formalism, theory-to-example progression, misconception handling, micro-conclusions and content-specific bridges. Separate manuscript length from actual classroom timing.

Review thematic examples for added value rather than duplication. Mnemonics must be accurate, memorable and reversible to the concept. Formula-reading aids must support interpretation without replacing definitions or hiding conditions. Common-error callouts identify realistic learner mistakes; self-checks require retrieval or transfer and usable teacher criteria. Respect configured density and avoid fragmented prose.

Check visual purpose, readability, labels/units, captions and integration with the surrounding explanation. Request evidence-backed specialist revision whenever a pedagogical improvement needs new scientific content. Do not treat stylistic preference or insert counts as measured learning effectiveness.

## Required result
Return review-report JSON with reviewer_id, runtime-supplied artifact hashes, mandatory pedagogical REQUIRED_CHECKS, findings and explicit not-applicable reasons. Each concrete finding has severity, location, category and required_action. Final approval must match the numbered final text and current supporting artifacts. Do not self-edit, waive core checks or accept the editor's own approval of a correction.

Apply .agents/references/integrity-contract.md and .agents/references/prompt-templates.md.
