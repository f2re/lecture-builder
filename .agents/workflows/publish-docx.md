# Publish final DOCX

1. Require `output/reviews/fact_check.json` with status `pass`.
2. Normalize and validate question/subsection headings with `scripts/number_structure.py` and `scripts/validate_numbering.py`.
3. Assign formulas once with `scripts/number_formulas.py`; figures already use validated global `L.N` numbers.
4. Confirm `image_prompts.md`, `figures_index.json`, `chart_specs.json` and methodical markers are consistent with the final lecture.
5. Convert with `scripts/md2docx/run_md2docx.sh`.
6. Validate DOCX and run `scripts/validate_pipeline.py --mode artifacts --strict`.
7. Do not publish on unresolved placeholders, missing charts required by config, invalid numbering or failed source/fact checks.
