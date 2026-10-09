---
name: formula-governance
description: Govern equation notation, stable labels, units, deterministic global numbering and DOCX-safe rendering. Use for «проверь формулы и обозначения» whenever formulas are required; authors never assign final equation numbers.
---

# Formula governance

Use stable semantic `\label{eq:...}` labels in display equations and `@eq:...` references. Inline expressions remain unnumbered. Explain newly introduced symbols, units, scientific meaning, assumptions and limitations after each display equation and connect its claim to evidence.

A formula_reading methodical insert may explain a relation conceptually but must not replace symbol definitions or change signs, indices, exponents, constants or scope. Scientific changes belong to the section author and require independent recheck. Recalculate illustrative arithmetic; do not mistake algebraic equivalence for physical applicability.

## Final numbering
After the editor completes output/lecture_edited.md and before final reviews, run:

```bash
python scripts/number_formulas.py output/lecture_edited.md \
  -o output/lecture_final.md --registry output/formula_registry.json
```

Traverse the entire lecture once. For lecture 17 assign (17.1), (17.2), (17.3) without restarting per question. Formula numbering is independent of question/figure/table namespaces. This pass may change labels/references deterministically but not scientific meaning.

Final scientific/pedagogical reviews and fact check inspect the numbered final snapshot. Do not renumber or edit it after approval; a change requires renewed checks.

Validate label uniqueness, resolved references, prefix/sequence, registry agreement, symbol definitions and native OMML with right-aligned numbers in DOCX. Publishing reads the approved Markdown without changing it.

Apply .agents/references/integrity-contract.md and .agents/references/prompt-templates.md.
