---
name: evidence-ledger
description: Build verified bibliography and atomic claim-to-fragment evidence from extracted sources. Use for «свяжи тезисы с источниками» before architecture; do not search the web, invent metadata or write lecture prose.
---

# Evidence ledger

Read extracted_fragments.json, local_index.json, search_results.json, config and source/evidence schemas. Write output/bibliography.json, evidence_ledger.json, literature_map.md and key_concepts.md.

Reconcile only observed metadata. Keep stable source_ids across reruns; unknown fields are null. Preserve fragment_id, source_id, document_hash, exact_fragment and verified locations from extraction. supports_claims must agree with claims' evidence_ids. Do not replace a source fragment with an agent's summary.

Build atomic definitions, formulas, quantitative facts, mechanisms, limits, examples and interpretations needed by each question. Distinguish supported, partial, unsupported and not_applicable. Partial support retains explicit limitations. A pedagogical/organizational statement that truly needs no source may be not_applicable; factual statements cannot use this label to evade verification.

Conflicting evidence stays visible. Explain the terminology choice and each source's scope; do not erase disagreement. A citation identifier alone never proves the claim's meaning.

## Coverage gate
Each required question needs grounds for its central definition, mechanism and required formula/example. Unsupported research hypotheses may remain in the ledger, but not in the brief or published text. Missing grounds create an evidence_request, not a claim from model memory.

Validate schema, unique IDs, source/fragment cross-references, nonempty exact excerpts and bidirectional claim links. Invoke source provenance validation. Numeric citations require printed page_label linked to the adjacent claim; pages_total, page_ranges and verified_pages do not verify locations.

Apply .agents/references/integrity-contract.md and .agents/references/prompt-templates.md.
