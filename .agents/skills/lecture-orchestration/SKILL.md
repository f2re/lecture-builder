---
name: lecture-orchestration
description: Coordinate, resume or diagnose the complete Lecture Builder pipeline with verified sources, numbered sections, independent final reviews and bounded specialist repairs. Use for «собери лекцию», «продолжи сборку» or «проверь этапы»; do not author or self-review specialist content.
---

# Lecture orchestration

Read AGENTS.md, .agents/workflows/build-lecture.md and .agents/references/integrity-contract.md. The executable graph and output contract are in lecture_tools.stage_graph. Use scripts/manifest.py next; revalidate both current content and required semantic checks before reuse.

You coordinate dependencies, budgets, task packets and status. Specialists search, extract, curate evidence, design, write, enrich, visualize, review and publish. Do not fill missing scientific content yourself. No experimental replication and no prompt/model version tracking.

Dispatch one section per validated brief with a small evidence-scoped context packet. Use independent read-only contexts for scientific, pedagogical and final fact checks. Allow parallelism only for disjoint outputs; serialize manifest changes and document assembly.

Preserve immutable handoffs: visual plans under output/plans; draft reviews under output/reviews/draft; editor output lecture_edited.md; numbering produces lecture_final.md; final reports certify that numbered file; publication never edits it.

A reviewer returns structured findings with category. Run scripts/repair_plan.py --phase draft --cycle N, dispatch only status=ready, route to the owner and invalidate restart_stage/descendants after changes. A blocked plan or exhausted max_review_cycles stops dispatch. An editor cannot approve their own correction. Recheck changed material independently.

Completion requires all mandatory stages, valid output schemas and cross-references, source provenance, supported published claims, current complete final reviews, correct DOCX and zero strict gate errors. Do not mark missing capabilities or skipped checks as passed. Save useful partial work and report precise blockers.
