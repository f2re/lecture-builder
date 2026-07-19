# Build a complete lecture

Run the complete Lecture Builder 3.0 pipeline.

1. Read all workspace rules and activate `lecture-orchestration`.
2. Validate `input/lecture_config.md` with `python scripts/validate_pipeline.py --mode source`.
3. Initialize or inspect `output/run_manifest.json`; reuse a stage only when its input and output hashes are fresh.
4. Run literature discovery, source extraction and evidence curation for every lecture question.
5. Build and validate `output/lecture_blueprint.json`, then create one section brief per question.
6. Write sections independently from their briefs. Parallelize only section files with disjoint outputs.
7. Assemble and coherence-edit the draft. Do not add unsupported facts during assembly.
8. Run scientific and pedagogical reviews independently. Block on critical scientific findings.
9. Apply reviewed corrections, then run an independent fact check.
10. Assign lecture-wide formula numbers with `scripts/number_formulas.py`.
11. Produce final illustration artifacts and DOCX.
12. Run `python scripts/validate_pipeline.py --mode artifacts --strict --report output/quality_report.json`.
13. Finish only when validation returns zero errors. Report exact blockers otherwise.
