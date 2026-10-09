# Build a complete lecture — 3.2

Read AGENTS.md, lecture-orchestration and .agents/references/integrity-contract.md. The executable dependency/output contract is lecture_tools.stage_graph.

1. Validate config; save the actual validation report as output/stages/config.json. Mark only validated outputs.
2. Search every question using gap-bound RU/EN queries; extract original bytes, exact normalized text and locations; curate bibliography and evidence.
3. Build the numbered blueprint and briefs. Build one evidence-scoped context packet per section.
4. Delegate section authors to disjoint files. Complete heading normalization before sections is marked complete. number-structure is read-only and saves its real validation report.
5. Run methodical enrichment and visual planning independently. Visual plans are immutable under output/plans/.
6. Copy chart/figure plans to the final JSON paths, render assets, validate and mark render-charts.
7. Assemble lecture_draft.md and run independent draft reviews to output/reviews/draft/.
8. Run scripts/repair_plan.py --phase draft --cycle N. Dispatch only status=ready requests to their owners. Invalidate restart_stage and descendants after changes. Respect max_review_cycles; never dispatch a blocked plan.
9. Final editor writes lecture_edited.md, edit_log.md and resolution.pending.json, not lecture_final.md.
10. Number formulas from edited to final; save formula_registry.json. No semantic changes are allowed in this pass.
11. Scientific and pedagogical reviewers independently recheck the exact numbered final text. Save final reports to output/reviews/ and independently verified resolution.json. Preserve draft reports.
12. A separate fact checker verifies that same final text, mandatory checks and claim coverage. Every final report records actual artifact hashes.
13. Convert final Markdown to DOCX without editing it; validate DOCX and mark publish-docx.
14. Run strict artifact validation. The quality-gate does not list its own report or manifest as stage outputs. Stop on any error.

Use scripts/manifest.py next for validated resume. A missing capability, source, check or exhausted correction budget is a blocker, never a synthetic success.
