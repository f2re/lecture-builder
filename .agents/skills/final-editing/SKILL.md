---
name: final-editing
description: Apply reviewed editorial corrections while preserving evidence, meaning, numbering and visual links. Use for «внеси замечания рецензентов»; scientific corrections go to their specialist owners and editors cannot approve their own fixes.
---

# Final editing

Read lecture_draft.md, independent draft reviews, blueprint, evidence, bibliography, methodical inserts, figures/chart specs and config. Write only output/lecture_edited.md, output/edit_log.md and output/reviews/resolution.pending.json. Do not overwrite lecture_final.md or issue final resolution approvals.

Prioritize critical and major findings. Use typed change_requests from scripts/repair_plan.py; scientific formulas/examples require the section author, source changes require extraction/evidence owners, and visuals require the planner. Do not repair scientific content by stylistic intuition. Return an evidence_request if a correction lacks grounds.

Apply minimal approved changes while preserving source IDs, claim scope, caveats, stable equation labels, canonical L.Q/L.Q.S headings, global figure captions and retained methodical markers. A callout is removed or rewritten only for a concrete finding and the decision is logged. Never promote a hypothetical example to an observed fact or invent source metadata and graph values.

Record finding_id, reviewer role, what changed, editor_id and the remaining recheck requirement. Marking an edit completed is not independent confirmation. Respect max_review_cycles; do not hide unresolved findings after the budget is exhausted.

Normalize edited structure before the deterministic formula-numbering pass. That pass creates lecture_final.md. Independent final reviewers then verify the exact numbered result and publish verified resolution.json with recheck verdicts and current hashes. The editor never certifies their own edits.

Apply .agents/references/integrity-contract.md and .agents/references/prompt-templates.md.
