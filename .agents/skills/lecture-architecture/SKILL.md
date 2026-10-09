---
name: lecture-architecture
description: Design a numbered evidence-backed lecture blueprint and one brief per question with concept dependencies, learning outcomes, examples, assessments and budgets. Use for «спроектируй структуру лекции» after evidence curation and before section authoring.
---

# Lecture architecture

Read configuration, bibliography, evidence ledger, literature map, key concepts and blueprint/brief schemas. Apply document-numbering and fgos-competencies. Write output/lecture_blueprint.json, lecture_blueprint.md and section_briefs/section_N.json; optional compatibility queries belong under output/queries/.

State the central problem and one defensible thesis. Translate configured competencies into observable outcomes. For each required outcome identify the assessment, answer criteria, practice and explanation that prepare the learner for it. Do not claim that exposure proves mastery.

Build an acyclic concept dependency graph and canonical terminology/notation. Preserve configured question order unless the user permits changes. Display numbers derive from lecture_number: L.Q and L.Q.S. Each question has at least two meaningful subsections, including a numbered micro-conclusion.

For every brief specify purpose, prerequisites, new concepts, supported/qualified claim and evidence IDs, allowed sources, formalism, core example, assumptions, misconception, incoming/outgoing bridges and assessment prompts. Allocate word and time budgets by difficulty; distinguish manuscript length from classroom delivery. Never silently assume hours means astronomical hours. Reserve lecture-level introduction and synthesis.

Specify methodical_requirements and visual_opportunities without authoring inserts or image prompts. Build a small evidence-scoped author packet through lecture_tools.context_packet.build_section_packet instead of sending unrelated literature to every author.

## Gate
Unsupported claims never enter a brief. Verify all configured questions, budgets, concept order, numbering, evidence links, assessment alignment and terminology. Return a targeted evidence_request when a required explanation lacks support.

Apply .agents/references/integrity-contract.md and .agents/references/prompt-templates.md.
