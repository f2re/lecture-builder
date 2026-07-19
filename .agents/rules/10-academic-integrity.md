# Academic integrity and source fidelity

- Never invent authors, titles, years, publishers, DOI values, URLs, page numbers, quotations or source classifications.
- Unknown source metadata is `null` or explicitly marked `unverified`; it is never reconstructed from plausibility.
- Every factual, definitional, quantitative or formula claim must have a `claim_id` linked to one or more verified `evidence_id` values in `output/evidence_ledger.json`. Mark its exact use in Markdown with `<!-- claim:claim_id -->`; comments are removed during DOCX conversion.
- Use stable citations `[@source_id]` or `[@source_id, с. 45]`. A page may be cited only when its location is verified.
- Quotations must preserve exact wording and location. Paraphrases must not be formatted as quotations.
- Separate established fact, interpretation, model assumption, pedagogical simplification and worked example.
- State applicability limits, assumptions and units for scientific models and formulas.
- Any `unsupported` claim, unresolved citation or critical scientific finding blocks publication.
