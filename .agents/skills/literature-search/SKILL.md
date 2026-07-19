---
name: literature-search
description: Discover academic, educational, normative and official sources for every configured lecture question, including local literature indexing and Russian/English query design. Use before source extraction; do not synthesize claims or fabricate bibliographic metadata.
---

# Literature search

## Inputs

- `input/lecture_config.md`
- optional `input/existing_refs.md`
- optional files under `input/literature/`
- `contracts/source-record.schema.json`

## Outputs

- `output/lit/local_index.json`
- `output/lit/search_results.json`
- `output/lit/search_log.md`

Write incrementally so partial progress survives tool or network failures.

## Procedure

1. Validate config and enumerate every question. Do not limit the search to the first four questions.
2. Index local files first. Record path, media type, content hash, extractability and only metadata actually observed in the document or file system.
3. Build a compact search matrix for each question in the configured languages. Use term variants, accepted English terminology and discipline context.
4. Prefer source classes in this order:
   - normative and official scientific organizations;
   - peer-reviewed journals and proceedings;
   - current university textbooks and monographs;
   - institutional repositories;
   - reputable datasets and technical documentation;
   - other web sources only when primary material is unavailable.
5. Deduplicate by canonical URL, DOI and normalized title.
6. Record search provenance: query, question, timestamp, result rank and discovery method.
7. Mark metadata as `verified`, `partial` or `unverified`. A snippet is not proof of authorship, year or page count.

## Query discipline

Respect `research.max_queries_per_question` and `max_results_per_query`. These are cost controls, not permission to omit questions. When coverage is insufficient, record the gap rather than generating synthetic sources.

## Minimum quality

For each question, aim for the configured minimum textbooks, peer-reviewed sources and normative documents. Flag any unmet category explicitly in the log.

## Prohibitions

- no invented DOI, URL, author, title, year or publisher;
- no source scoring based solely on domain reputation;
- no bibliography formatting at this stage;
- no claims, definitions or lecture prose;
- no reading binary documents through text-only tools that cannot preserve pages.

## Verification

Validate JSON, uniqueness, question coverage and source provenance. A successful degraded run may contain gaps, but the gaps must be explicit and must prevent unsupported downstream claims.
