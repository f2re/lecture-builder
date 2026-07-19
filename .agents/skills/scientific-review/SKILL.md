---
name: scientific-review
description: Perform an independent read-only scientific audit of a lecture draft against verified evidence, formulas, units, assumptions, terminology and source fidelity. Use after assembly and after final editing for fact check; never edit the lecture being reviewed.
---

# Scientific review

## Inputs

- target lecture Markdown
- `output/evidence_ledger.json`
- `output/bibliography.json`
- `output/lecture_blueprint.json`
- `input/lecture_config.md`
- formula registry when available

## Output

Write a schema-valid report such as `output/reviews/scientific.json` or `output/reviews/fact_check.json`.

## Review dimensions

1. Claim fidelity: every scientific claim is supported by linked evidence and does not exceed the source.
2. Source integrity: citations resolve, page references are verified and quotations are exact.
3. Formula correctness: mathematical form, derivation, signs, variables, units, dimensions and applicability.
4. Terminology: accepted discipline-specific meanings, no silent synonym drift.
5. Causality: correlation, approximation and pedagogical simplification are not presented as universal causation.
6. Assumptions and limits: boundary conditions and known exceptions are visible where they affect interpretation.
7. Examples: arithmetic, units and conclusion are correct and do not imply unsupported generality.
8. Recency: time-sensitive statements use sufficiently current evidence or state their historical scope.

## Severity

- `critical`: false or unsupported central claim, invalid formula, fabricated source/location, unsafe instruction or contradiction that invalidates the lecture.
- `major`: materially misleading omission, terminology error, incomplete applicability limit or broken citation chain.
- `minor`: local precision or presentation issue with no material scientific effect.
- `note`: optional enhancement.

## Finding contract

Each finding names an id, severity, exact section/location, quoted target fragment, violated criterion, supporting source/evidence ids, required correction and whether publication is blocked.

## Independence

Do not rewrite the lecture and do not accept the editor's assertions as proof. Reopen evidence when an edit changes factual meaning. Status is `pass` only with no critical/major unresolved finding and no unsupported claim.
