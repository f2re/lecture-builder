---
name: gost-citation
description: Maintain stable source-id citations and format verified metadata for Russian academic materials without inventing fields or page locations. Use for «проверь ссылки и библиографию» during evidence curation, writing and publication.
---

# ГОСТ-oriented citation handling

Use `[@src_001]` for a source-level citation. Use `[@src_001, с. 45]` or a numeric range only when evidence for the adjacent claim contains the corresponding verified printed page_label. The physical PDF index, pages_total, page_ranges and a verified_pages boolean are insufficient. Every page in a cited range must be covered; do not add an unverified end page.

Keep source IDs canonical internally. Human-readable output may use a separately configured and actually executed bibliography renderer; do not imply that the current converter automatically supplies citeproc/CSL formatting when it has not done so. Specify the institutional formatting profile rather than promise universal ГОСТ conformity.

Format only observed fields. Unknown author, publisher, year, volume, issue, page extent, DOI or access date is null and omitted without inventing completeness. Preserve original title language and identifiers. Online access dates refer to actual known access, not an arbitrary current date.

Handle books, chapters, articles, proceedings, standards, reports, datasets, software documentation and web resources consistently. Deduplicate canonical DOI/URL/title records. Every in-text source ID resolves to bibliography.json; no invented aliases. A source's existence does not establish that it supports the claim.

## Gate
Validate bibliography schema and citation cross-references, exact fragment provenance and numeric page support. Migrate legacy author-year syntax to stable IDs before the final gate. When the printed location is unavailable, retain a truthful source-level citation rather than guess a page.

Apply .agents/references/integrity-contract.md and .agents/references/prompt-templates.md.
