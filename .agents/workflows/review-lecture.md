# Review lecture

1. Validate source provenance, numbering, citations, claim markers, inserts and visuals.
2. Run scientific and pedagogical reviewers in separate read-only contexts. Draft phase reads lecture_draft.md and saves results under output/reviews/draft/.
3. Require concrete checks, findings with category, reviewer_id and artifact hashes fixed by the runtime, not guessed by the model.
4. Build bounded specialist-owned requests with scripts/repair_plan.py --phase draft --cycle N. An editor cannot certify their own correction.
5. After corrections and formula numbering, independently recheck lecture_final.md in both roles; write final reports at output/reviews/scientific.json and pedagogical.json plus verified resolution.json.
6. Run a separate fact checker over that exact final snapshot. Check marked and unmarked claims, formulae, arithmetic, scope, negations, graph data and pedagogical simplifications.
7. A missing check, stale hash, uncovered claim or unverified correction blocks release. Assemble the human-readable report without altering machine conclusions.
