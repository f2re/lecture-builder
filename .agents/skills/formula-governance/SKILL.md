---
name: formula-governance
description: Govern scientific notation, stable equation labels, lecture-wide deterministic numbering, symbol and unit explanations, references and DOCX-safe rendering. Use whenever formulas are required; authors must not assign final numbers manually.
---

# Formula governance

Write display equations with stable semantic labels and cite them as `@eq:...`. Inline expressions are unnumbered.

After final fact check, `scripts/number_formulas.py` traverses the complete lecture once and assigns `(lecture_number.ordinal)`: for lecture 17, `(17.1)`, `(17.2)`, `(17.3)`. This counter is independent of question/subsection numbers and never restarts per question.

After every display formula define newly introduced symbols, state units, explain scientific meaning, name assumptions/limits and cite evidence. A `formula_reading` methodical insert may translate the relation into a memory-friendly interpretation, but it must not replace symbol definitions or alter signs, exponents, indices, constants or scope.

Validate unique labels, resolved references, global sequence, lecture prefix, symbol explanations and native OMML/right-aligned DOCX numbering.
