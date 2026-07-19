---
name: final-editing
description: Apply approved scientific and pedagogical findings to produce final coherent Markdown while preserving evidence, lecture-derived numbering, methodical insert markers, visual references and formula semantics. Use before final fact check.
---

# Final editing

Read the draft, independent reviews, blueprint, evidence, bibliography, methodical inserts, figures/chart specs and config. Write only `output/lecture_final.md`, `output/edit_log.md` and `output/reviews/resolution.json`.

Resolve critical and major findings first. Preserve source ids, claim scope, caveats, stable formula labels, `L.Q`/`L.Q.S` headings, figure `L.N` captions and every retained `<!-- methodical:... -->` marker. Remove or rewrite a callout only when a review finding identifies a concrete problem, and record the decision.

Do not add source metadata, graph values or formula changes. Do not convert a hypothetical example into an observed fact. Normalize structure with `scripts/number_structure.py` before handing the result to the independent fact checker. Do not certify your own edits.
