# Review a lecture draft

Run two independent read-only reviews:

1. `scientific-review`: evidence fidelity, factual accuracy, formulas, units, assumptions, terminology and applicability.
2. `pedagogical-review`: progression, audience fit, competencies, readability, examples, misconceptions, transitions and assessment questions.

Write machine-readable reports to `output/reviews/scientific.json` and `output/reviews/pedagogical.json`, then assemble `output/review_report.md`. Do not edit the lecture during review. A critical unsupported claim, invalid formula or unresolved citation sets status to `block`.
