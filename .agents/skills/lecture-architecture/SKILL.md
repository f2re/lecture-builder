---
name: lecture-architecture
description: Design a coherent numbered lecture blueprint and one evidence-backed section brief per configured question, including concept dependencies, learning objectives, methodical requirements, visual opportunities, bridges, examples, misconceptions, time and word budgets. Use after evidence curation and before section writing.
---

# Lecture architecture

## Inputs

- `input/lecture_config.md`
- bibliography, evidence ledger, literature map and key concepts
- lecture blueprint and section brief schemas
- `document-numbering`, `fgos-competencies` and applicable domain skills

## Outputs

- `output/lecture_blueprint.json`
- `output/lecture_blueprint.md`
- `output/section_briefs/section_{N}.json`
- optional compatibility `output/queries/query_{N}.md`

## Design method

1. State the central problem and one defensible thesis.
2. Translate competencies into observable outcomes.
3. Build an acyclic concept graph and canonical terminology/notation table.
4. Derive every display number from `lecture_number`: question `L.Q`, subsection `L.Q.S`.
5. Preserve configured question order unless explicitly permitted otherwise.
6. Allocate time and words by conceptual difficulty.
7. For every question define purpose, prerequisites, introduced concepts, supported claim/evidence ids, formalism, examples, limitations, misconceptions, incoming/outgoing bridges and assessment prompts.
8. Create at least two logically meaningful numbered subsections, including a final numbered micro-conclusion subsection.
9. Define `methodical_requirements` for understanding, memory, application and self-check without writing the inserts themselves.
10. Identify `visual_opportunities` for diagrams, maps and source-bound graphs without generating prompts or figures.
11. Reserve introduction and conclusion functions at lecture level.

## Evidence and numbering gates

Unsupported claims never enter a brief. Partial claims retain explicit limitations. The blueprint and every brief must match lecture number, question order, subsection sequence, budgets and evidence cross-references.
