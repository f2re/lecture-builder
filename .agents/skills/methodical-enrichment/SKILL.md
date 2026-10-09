---
name: methodical-enrichment
description: Design concise evidence-safe examples, mnemonics, formula-reading aids, misconception corrections and self-check callouts. Use for «добавь методические вставки» after section authoring; do not edit the sections or introduce unsupported science.
---

# Methodical enrichment

Read config, blueprint, briefs, complete sections, evidence ledger, key concepts and methodical-inserts schema. Write only output/methodical_inserts.json. The coherence editor inserts the approved material into the draft.

Available types are key_idea, mnemonic, thematic_example, formula_reading, common_mistake, self_check, comparison, professional_context and visual_cue. Select by a concrete learning function, not decoration. Follow configured min/max counts, required_functions and max_word_share. Do not put consecutive callouts, repeat the main example or fragment every paragraph. Suggestions to reduce configured density must go through review, not bypass validators.

A mnemonic must be short, unambiguous, reversible to the scientific concept and free of false causal/spatial/mathematical implications. A formula-reading aid supplements—not replaces—symbol definitions and assumptions. A self-check requires retrieval or transfer; provide answer criteria for the teacher without hidden new theory.

Factual inserts reference supported claim_id/evidence_id values. Hypothetical numbers require hypothetical=true and visible illustrative wording. Never portray invented numbers as observations, invent professional procedures or strengthen the original claim.

Each insert records stable section/question identity and an insertion strategy, preferably exact anchor text/hash. Render as a restrained blockquote with a hidden `<!-- methodical:... -->` marker. IDs remain traceable through editing and are hidden in DOCX.

## Gate
Validate schema, numbering, learning-function coverage, density, evidence, hypothetical labels and markers in draft/final. Scientific review verifies facts and simplifications; pedagogical review may reject distracting or redundant inserts. Counts alone do not demonstrate improved learning.

Apply .agents/references/integrity-contract.md and .agents/references/prompt-templates.md.
