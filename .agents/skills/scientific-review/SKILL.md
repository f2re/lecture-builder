---
name: scientific-review
description: Independently audit source fidelity, theory, formulas, arithmetic, examples and scientific visuals without editing them. Use for «проверь научную корректность» on the draft or numbered final snapshot; do not issue unsupported approval.
---

# Scientific review

Read the target Markdown, exact extracted sources/evidence, bibliography, blueprint, methodical inserts, chart specs and formula/figure artifacts. Use an independent read-only context. Return machine-readable findings; the runtime saves the response without changing its conclusion.

Draft-phase output belongs at output/reviews/draft/scientific.json. After editing and numbering, independently recheck lecture_final.md and return output/reviews/scientific.json. A separate fact-check context uses the same skill for output/reviews/fact_check.json. Final reports certify the exact same numbered snapshot.

Independently identify substantive statements, including statements without markers. Check that the source supports the actual wording, not merely its topic or claim_id. Preserve negations, assumptions, causal direction, uncertainty and scope. Verify printed-page provenance, time-sensitive claims, accepted terminology, formula signs/indices/constants/units, worked-example arithmetic and limiting behavior. Check graph data, transformations, axes, captions and source consistency.

Mnemonics, analogies and other factual methodical inserts are scientific content. Reject a simplification that distorts causality, dimensional meaning or applicability. Hypothetical values must remain visibly illustrative. This is source-based verification, not experimental replication.

## Required result
Use review-report schema and role-specific REQUIRED_CHECKS in lecture_tools.review_integrity. Include reviewer_id, actual reviewed_artifacts hashes supplied by runtime, status, checks, findings and applicable reasons for not_applicable. A finding identifies location/fragment, severity, category, claim/evidence IDs and a testable required_action. Core checks cannot be waived. Fact-check coverage.claim_ids must cover all required and actually marked final claims, with a separate check for unmarked additions.

Do not set pass with unsupported claims, invalid formulae, invented data or critical/major findings. An editor's resolved flag is not approval: independently recheck the current final hash, retain editor/reviewer separation and report real gaps or unavailable capabilities.

Apply .agents/references/integrity-contract.md and .agents/references/prompt-templates.md.
