# Design lecture architecture

Activate `lecture-architecture` and `fgos-competencies`.

Read the validated config, bibliography, evidence ledger, literature map and glossary. Produce a single macro-level argument for the lecture, a concept dependency graph, measurable learning objectives and one section plan per configured question. Each section must define prerequisites, introduced concepts, required claims/evidence, examples, misconceptions, word/time budget and concrete incoming/outgoing logical bridges.

Write:

- `output/lecture_blueprint.json`
- `output/lecture_blueprint.md`
- `output/section_briefs/section_{N}.json`
- compatibility prompts `output/queries/query_{N}.md` when Gemini workflows are used.

Validate every JSON file against its schema before completion.
