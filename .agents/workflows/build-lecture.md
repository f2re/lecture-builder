# Build a complete lecture

Run the complete Lecture Builder pipeline.

1. Read workspace rules and activate `lecture-orchestration` plus `document-numbering`.
2. Validate `input/lecture_config.md`; question prefixes must derive from `lecture_number`.
3. Initialize or inspect `output/run_manifest.json`; reuse stages only through existing content hashes and validations. Do not add prompt/model-version tracking.
4. Run literature discovery, local-source indexing, source extraction and evidence curation for every question.
5. Build the numbered blueprint and one brief per question.
6. Write section files independently, then normalize their question/subsection headings.
7. Run methodical enrichment and visual/graph planning in parallel. Produce `methodical_inserts.json`, `figures_index.json`, `chart_specs.json` and separate `image_prompts.md`.
8. Render required graph assets with `python scripts/render_charts.py --spec output/chart_specs.json --figures output/figures_index.json`.
9. Assemble a coherent draft that integrates typed inserts and visual placeholders without adding facts.
10. Run scientific and pedagogical reviews independently; both cover examples, mnemonics, graph specs and numbering.
11. Apply reviewed corrections and normalize structure again, then run independent source-based fact check.
12. Assign lecture-wide formula numbers with `scripts/number_formulas.py`.
13. Produce DOCX and run numbering, DOCX and strict artifact validation.
14. Finish only with zero blocking errors; report exact blockers otherwise.

This workflow does not reproduce scientific experiments. It verifies lecture content against sources and the local literature corpus.
