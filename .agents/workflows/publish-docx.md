# Publish final DOCX

1. Require final, numbered lecture_final.md, formula registry and passing independent scientific, pedagogical and fact-check reports with matching hashes.
2. Validate numbering and chart/figure/methodical references without editing the final Markdown. Numbering and repairs must already be complete.
3. Convert using scripts/md2docx/run_md2docx.sh.
4. Validate DOCX, record publish-docx outputs, then run scripts/validate_pipeline.py --mode artifacts --strict.
5. Never report success for missing assets, stale approvals or skipped checks. Changing final text requires repeating final reviews. Structural DOCX validation alone is not visual layout certification.
