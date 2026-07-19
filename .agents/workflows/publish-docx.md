# Publish Markdown and DOCX

Activate `formula-governance`, `illustration-planning` and `docx-publishing`.

1. Confirm final fact check passed.
2. Assign deterministic formula numbers and resolve `@eq:*` references.
3. Validate citations, formula sequence, headings and JSON artifacts.
4. Run `bash scripts/md2docx/run_md2docx.sh output/lecture_final.md -o output/lecture_final.docx`.
5. Run `python scripts/validate_docx.py output/lecture_final.docx --expect-formulas` when formulas are required.
6. Run strict pipeline validation and record hashes in the run manifest.

Do not report success when Pandoc or DOCX validation fails.
