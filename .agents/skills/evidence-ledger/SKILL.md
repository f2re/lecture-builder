---
name: evidence-ledger
description: Convert extracted source fragments into a verified bibliography, claim inventory and claim-to-evidence ledger without fabricating metadata. Use before lecture architecture and writing; do not write lecture prose or perform new web searches.
---

# Evidence ledger

## Inputs

- `output/lit/extracted_fragments.json`
- `output/lit/local_index.json`
- `output/lit/search_results.json`
- `input/lecture_config.md`
- `contracts/source-record.schema.json`
- `contracts/evidence-ledger.schema.json`

## Outputs

- `output/bibliography.json`
- `output/evidence_ledger.json`
- `output/literature_map.md`
- `output/key_concepts.md`

## Method

1. Group fragments by source and reconcile metadata only from verified provenance.
2. Assign stable `source_id` values. Preserve ids across reruns when the canonical source is unchanged.
3. Classify source category and authority using observable evidence, not reputation assumptions.
4. Build atomic claims for definitions, formulas, quantitative facts, mechanisms, limitations and interpretations required by the lecture questions.
5. Link every claim to exact fragments. Mark status:
   - `supported`: sufficient verified evidence;
   - `partial`: evidence supports only part or has material limitations;
   - `unsupported`: no adequate evidence;
   - `not_applicable`: pedagogical or organizational statement requiring no source.
6. Record assumptions and confidence. Conflicting sources remain visible; choose canonical terminology only with a stated rationale.
7. Build a question-to-source map and glossary from the highest-quality supporting evidence.

## Metadata rule

Unknown values are `null`. Page citations require page-aware extraction and `location_status: verified`. A title or year inferred from a filename remains unverified and cannot support a formal page citation.

## Coverage gate

Every configured question must have evidence for its core definition, central mechanism and required formula/example where applicable. Missing coverage is a blocking gap, not an invitation to synthesize from model memory.

## Verification

Validate both JSON files against their schemas. Run evidence cross-reference checks: unique ids, known sources, non-empty fragments, no `supported` claim without evidence and no `unsupported` claim entering section briefs.
