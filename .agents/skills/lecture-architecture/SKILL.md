---
name: lecture-architecture
description: Design a coherent lecture blueprint and one evidence-backed section brief per configured question, including concept dependencies, learning objectives, bridges, examples, misconceptions, time and word budgets. Use after evidence curation and before section writing; do not write final lecture prose.
---

# Lecture architecture

## Inputs

- `input/lecture_config.md`
- `output/bibliography.json`
- `output/evidence_ledger.json`
- `output/literature_map.md`
- `output/key_concepts.md`
- `contracts/lecture-blueprint.schema.json`
- `contracts/section-brief.schema.json`

## Outputs

- `output/lecture_blueprint.json`
- `output/lecture_blueprint.md`
- `output/section_briefs/section_{N}.json`
- optional Gemini compatibility files `output/queries/query_{N}.md`

## Design method

1. State the lecture's central problem and one defensible thesis that answers it.
2. Translate configured competencies into observable learning outcomes. Cover knowledge, interpretation and application; do not merely repeat competency wording.
3. Build a directed concept graph. Every concept used in a section must either be a prerequisite or be introduced earlier in that section.
4. Preserve the configured question order unless the config explicitly permits reordering. When the order is pedagogically weak, record the issue and add prerequisite bridges rather than silently changing the plan.
5. Allocate time and words according to conceptual difficulty, not equally by default. Respect the configured total.
6. For every section define:
   - local question and contribution to the central thesis;
   - prerequisites and new terms;
   - required `claim_id` and `evidence_id` values;
   - formalism, examples and limitations;
   - likely misconceptions;
   - incoming and outgoing content-specific bridges;
   - micro-conclusion and assessment prompts.
7. Reserve introduction and conclusion functions at lecture level so section writers do not duplicate them.
8. Define a canonical terminology and notation table shared by all writers.

## Bridge quality

A bridge must name the established result and explain why the next question follows. Generic phrases such as «перейдём к следующему вопросу» are insufficient.

## Evidence gate

Do not place an unsupported claim in a brief. A partial claim may be used only when its limitation is made explicit. If a question lacks minimum evidence, mark the blueprint blocked and return the exact research gap.

## Verification

Validate the blueprint and each section brief against schemas. Check one brief per configured question, unique section numbers, complete claim references, total time/word budgets, acyclic concept dependencies and explicit adjacent bridges.
