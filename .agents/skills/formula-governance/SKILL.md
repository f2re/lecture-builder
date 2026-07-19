---
name: formula-governance
description: Govern scientific notation, stable equation labels, lecture-wide deterministic numbering, symbol and unit explanations, references and DOCX-safe rendering. Use whenever formulas are required; authors must not assign final numbers manually.
---

# Formula governance

## Authoring contract

Write display equations with a stable semantic label:

```latex
$$
\Delta H = \frac{R\overline{T_v}}{g_0}\ln\frac{p_1}{p_2}
\label{eq:hypsometric}
$$
```

Refer to it as `@eq:hypsometric`. Inline expressions use `\(...\)` and are not numbered.

## Global numbering

After assembly and final fact check, run:

```bash
python scripts/number_formulas.py output/lecture_final.md \
  -o output/lecture_final.md \
  --registry output/formula_registry.json
```

The deterministic pass traverses equations once in document order, replaces stable references and inserts `\tag{lecture_number.counter}`. It rejects duplicate labels, unresolved references and conflicting manual tags.

## Scientific requirements

After every display formula:

- define each newly introduced symbol;
- state units in the configured unit system;
- explain the physical or methodological meaning;
- name assumptions and applicability limits;
- cite evidence for the formula or derivation;
- use canonical notation from the blueprint.

## Editing rule

A prose editor may repair formatting or wording but may not change signs, exponents, indices, variables, constants or derivation logic without scientific review.

## Verification

Validate unique labels, complete references, sequential lecture-wide numbers, lecture number consistency, symbol explanations and DOCX OMML/table structure. Numbering is never restarted per section.
