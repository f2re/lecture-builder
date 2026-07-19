---
name: gost-citation
description: Format verified bibliography metadata for Russian academic lecture materials and enforce stable source-id citations without inventing missing fields or page locations. Use during evidence curation, writing and publication.
---

# ГОСТ-oriented citation handling

## Canonical in-text form

Use machine-resolvable source identifiers:

- `[@src_001]` for a source-level citation;
- `[@src_001, с. 45]` or `[@src_001, с. 45–47]` only when the page location is verified.

Human-facing author–year rendering may be produced during publication, but source ids remain the canonical internal representation.

## Metadata policy

Format only observed and verified fields. Unknown author, publisher, year, issue, page extent, DOI or access date is `null` and omitted from the rendered citation. Never manufacture punctuation around missing data in a way that implies completeness.

## Source classes

Support books, chapters, journal articles, conference papers, standards, reports, datasets, software/documentation and web resources. Preserve original title language and identifiers. Record electronic access dates only when the source is genuinely accessed online and the date is known.

## Consistency

- one stable `source_id` per canonical source;
- identical source metadata everywhere;
- all in-text references resolve to `bibliography.json`;
- no bibliography entry is cited by an invented alias;
- quotations include verified location where available;
- duplicate DOI/URL/title records are reconciled before formatting.

## Verification

Run schema and citation cross-reference validation. Page-specific references without page-aware evidence are blocking errors. Legacy `[Автор, год]` forms should be migrated to source ids before final publication.
