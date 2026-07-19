---
name: section-authoring
description: Write exactly one Russian university lecture section from a validated section brief and verified evidence, with definitions, explanation, formulas, examples, limitations, misconceptions, logical bridges and a micro-conclusion. Use after lecture architecture; never assemble or edit other sections.
---

# Section authoring

## Inputs

- one `output/section_briefs/section_{N}.json`
- `output/lecture_blueprint.json`
- `output/evidence_ledger.json`
- `output/bibliography.json`
- `output/key_concepts.md`
- `input/lecture_config.md`

## Output boundary

Write exactly one file `output/sections/section_{N}_{slug}.md`. Do not write queries, reviews, the draft, the final lecture, the formula registry or the manifest.

## Required reasoning sequence

1. Use the brief's incoming bridge to connect to the precise result already established.
2. State the local problem and why it matters for the lecture thesis.
3. Define every new term before analytical use.
4. Explain the scientific or physical mechanism in prose.
5. Introduce formalism after motivation. Use stable formula labels `\label{eq:...}` and references `@eq:...`; do not assign numbers.
6. State assumptions, units and applicability limits.
7. Work through an example whose steps visibly use the introduced concepts or formula.
8. Address the misconception identified in the brief.
9. Give a 3–5 point micro-conclusion derived only from the section.
10. End with the brief's content-specific outgoing bridge.

## Source discipline

- Every factual, definitional, quantitative, causal and formula claim must resolve to supported claim/evidence entries. Add `<!-- claim:claim_id -->` immediately after the sentence or paragraph that uses the claim.
- Cite sources using `[@source_id]` or a verified page form.
- Never cite model memory, a search snippet or an unverified filename inference.
- Distinguish quotation, paraphrase, interpretation, assumption and worked example.

## Readability

Use one main idea per paragraph, varied but precise transitions, concrete verbs and explicit logical relations. Prefer explanation over enumerating statements. Avoid bureaucratic nominalizations, conversational fillers, repetitive openings and paragraphs that exceed roughly 180 words without a structural reason.

## Verification

Check the exact output path, section heading, word budget, required claims, citations, formula labels, symbol explanations, example, misconception, micro-conclusion and both bridges. Run deterministic citation and formula checks where possible.
