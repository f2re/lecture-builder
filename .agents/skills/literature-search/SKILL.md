---
name: literature-search
description: Discover academic, educational, normative and official sources for every configured lecture question, including local literature indexing and Russian/English query design. Use for «найди источники» before extraction; do not write lecture prose or fabricate metadata.
---

# Literature search

## Inputs and outputs
Read input/lecture_config.md, optional input/existing_refs.md, input/literature/ and contracts/source-record.schema.json. Write output/lit/local_index.json, search_results.json and search_log.md incrementally.

## Procedure
1. Validate configuration and enumerate every question; never stop at the first four.
2. Index local files first: path, media type, actual content hash, extractability and only observed metadata.
3. For each question identify missing definitions, mechanisms, derivations, limitations, examples, data and disagreements. Bind each query to question_id, gap_id, purpose and language.
4. Use accepted RU/EN terminology and variants. Choose source type by the claim: textbook/monograph for a foundational derivation; primary peer-reviewed work for a research result; official document for regulation; dataset and methodology for observations. Do not score solely by domain reputation.
5. Deduplicate by canonical URL, DOI and normalized title. Record query, timestamp, result rank and discovery method.
6. Mark metadata verified, partial or unverified based on observed provenance. A search snippet is not a read source and does not verify authorship, year or pages.

## Budgets and failure
Respect research.max_queries_per_question, max_results_per_query and extraction limits. Search remaining gaps, not arbitrary publication counts. Record unmet configured source categories. Missing network or inaccessible sources must be explicit; keep verified partial progress. Do not invent sources to satisfy a quota.

## Gate
Validate schemas, uniqueness, question coverage and provenance. Gaps may remain in discovery but cannot become unsupported lecture claims. Do not format the bibliography, synthesize definitions or read binary documents through a text-only tool.

Apply .agents/references/integrity-contract.md and the search template in .agents/references/prompt-templates.md.
