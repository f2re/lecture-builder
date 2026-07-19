---
name: source-extraction
description: Fetch or read selected sources and extract exact, contextual fragments with page, section, paragraph and hash provenance for lecture claims. Use after literature search; do not score sources, author lecture text or guess missing locations.
---

# Source extraction

## Inputs

- `output/lit/search_results.json`
- `output/lit/local_index.json`
- `input/lecture_config.md`
- source documents reachable through available tools

## Outputs

- downloaded or normalized text under `output/lit/downloaded/`
- `output/lit/extracted_fragments.json`
- `output/lit/fetch_log.md`

## Extraction contract

Each fragment must include:

- stable `fragment_id` and `source_id`;
- exact fragment text, not an unsupported summary;
- question ids and matched terms;
- content hash of the source or normalized downloaded file;
- detected section/chapter;
- page or page label only when the extraction tool preserves it;
- character offsets or paragraph number when available;
- `location_status`: `verified`, `approximate` or `unavailable`;
- formula and definition indicators when relevant.

Keep enough surrounding context to avoid changing the meaning of a sentence. Do not cut away negations, assumptions or applicability limits.

## Document handling

- HTML: preserve article body, headings, tables and metadata; remove navigation and unrelated boilerplate.
- PDF: use a page-aware extractor. Store page number and source hash. If page mapping is lost, set it to unavailable.
- DOCX/EPUB: preserve structural headings and paragraph order.
- Scanned documents: use OCR only when supported and record OCR uncertainty.
- Local binary file that cannot be read: record the blocker; do not infer content from the filename.

## Failure policy

Retry only transient failures within configured limits. Log HTTP status, access restrictions, timeout and parser errors. Keep already verified fragments. Never replace an inaccessible source with invented text.

## Verification

Validate that every fragment resolves to a discovered source, exact text is non-empty, source hashes are stable, locations are internally consistent and duplicate fragments are removed. Do not complete when all retained fragments are only snippets without source context.
