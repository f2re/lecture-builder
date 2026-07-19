# Research literature

Activate `literature-search`, `source-extraction`, `evidence-ledger` and `gost-citation`.

Cover every question from `input/lecture_config.md`. Respect the configured query/result limits, but do not silently omit later questions. Prefer primary, peer-reviewed, normative and official sources. Index local literature first. Preserve source metadata provenance and exact fragment locations. Do not infer missing pages or bibliographic fields.

Required outputs:

- `output/lit/local_index.json`
- `output/lit/search_results.json`
- `output/lit/search_log.md`
- `output/lit/extracted_fragments.json`
- `output/lit/fetch_log.md`
- `output/bibliography.json`
- `output/evidence_ledger.json`
- `output/literature_map.md`
- `output/key_concepts.md`

Validate JSON and resolve all source identifiers before completion.
