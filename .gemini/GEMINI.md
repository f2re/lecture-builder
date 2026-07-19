# Lecture Builder Gemini compatibility adapter

The canonical instructions are root `AGENTS.md` and `.agents/`. Gemini agents and commands must not duplicate scientific or pedagogical policy.

Read `input/lecture_config.md`; `lecture_number` determines question `L.Q`, subsection `L.Q.S`, formula `L.N` and figure `L.N` numbering. The pipeline uses web and local sources for fact verification, creates theory/formulas/examples, methodical callouts, graphs, separate image prompts, reviews and DOCX. It does not reproduce experiments.

Full pipeline: `gemini build-lecture`.

Partial commands: `gemini search-literature`, `gemini write-section N`, `gemini enrich-lecture`, `gemini plan-visuals`, `gemini review-lecture`.
