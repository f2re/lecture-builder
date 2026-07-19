# Machine-readable artifact contracts

All generated JSON must be UTF-8 JSON, validate against the matching Draft 2020-12 schema, and use stable cross-file identifiers.

| Schema | Artifact |
|---|---|
| `lecture-config` | `input/lecture_config.md` parsed as YAML |
| `local-index` | `output/lit/local_index.json` |
| `search-results` | `output/lit/search_results.json` |
| `extracted-fragments` | `output/lit/extracted_fragments.json` |
| `source-record` | normalized individual source records |
| `bibliography` | `output/bibliography.json` |
| `evidence-ledger` | `output/evidence_ledger.json` |
| `lecture-blueprint` | `output/lecture_blueprint.json` |
| `section-brief` | `output/section_briefs/section_N.json` |
| `review-report` | scientific, pedagogical and fact-check reports |
| `review-resolution` | `output/reviews/resolution.json` |
| `formula-registry` | `output/formula_registry.json` |
| `figures-index` | `output/figures_index.json` |
| `run-manifest` | `output/run_manifest.json` |

Schemas establish shape; Python validators enforce cross-file relationships, freshness, evidence support, review resolution, equation sequence and DOCX structure.
