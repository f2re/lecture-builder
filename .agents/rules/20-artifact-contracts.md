# Artifact contracts

- Read the matching schema under `contracts/` before writing JSON.
- Write valid UTF-8 JSON, not Markdown code fences containing JSON.
- Use stable identifiers: `ref_*` or `src_*` for sources, `ev_*` for evidence, `claim_*` for claims and `eq:*` for formulas.
- `section-writer` writes exactly one `output/sections/section_{N}_{slug}.md` and no other stage artifact.
- Formula authors use `\label{eq:stable-id}` and references such as `@eq:stable-id`. Final numbers are assigned once, after assembly, by `scripts/number_formulas.py`.
- Reviews are machine-readable JSON under `output/reviews/`; the human-readable `output/review_report.md` is an assembled summary.
- `output/lecture_final.md` is produced from the draft plus reviewed corrections. Never edit `output/lecture_draft.md` in place.
- Use `python scripts/validate_pipeline.py --mode artifacts --strict` before declaring the lecture complete.
