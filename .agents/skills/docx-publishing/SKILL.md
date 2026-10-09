---
name: docx-publishing
description: Convert the independently approved numbered Markdown into a ГОСТ-oriented DOCX and validate its structure. Use for «оформи лекцию в DOCX» after final reviews; do not change the approved scientific content or claim unperformed layout checks.
---

# DOCX publishing

Require the already numbered output/lecture_final.md, formula_registry.json, validated methodical/visual artifacts and passing final scientific, pedagogical and fact-check reports with current hashes. Independent resolved-finding rechecks must refer to the same final snapshot.

Do not normalize headings, renumber equations or edit prose after approval. Necessary changes return to the owning stage and invalidate final reviews. Read the Markdown and create output/lecture_final.docx with the existing wrapper.

Preserve L.Q/L.Q.S headings; native OMML formulas centered with right-aligned global (L.N) numbers; figure/table captions; typed callouts without hidden HTML markers; images/alt text where assets exist; A4, configured ГОСТ-oriented margins, Times New Roman, indentation, heading hierarchy, tables and page fields.

```bash
bash scripts/md2docx/run_md2docx.sh output/lecture_final.md \
  -o output/lecture_final.docx
python scripts/validate_docx.py output/lecture_final.docx --expect-formulas
```

Use --expect-formulas only when config requires formulas. Record actual publish-docx outputs in the manifest, then run:

```bash
python scripts/validate_pipeline.py --mode artifacts --strict \
  --report output/quality_report.json
```

The final quality gate does not hash itself or run_manifest.json as a stage output. Missing assets, unresolved references, stale approvals, invalid DOCX or any strict gate error blocks completion. File existence alone is not success.

Structural checks are not visual layout certification or scientific validation. Report unperformed visual/content-completeness/bibliographic-rendering checks explicitly; do not invent success for unavailable Pandoc or other tools.

Apply .agents/references/integrity-contract.md and .agents/references/prompt-templates.md.
