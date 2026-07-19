---
name: lecture-orchestration
description: Coordinate, resume or diagnose the complete Lecture Builder pipeline across research, architecture, numbered section writing, methodical enrichment, visual planning, review, editing, formula numbering and DOCX publication. Use for full builds and interrupted runs; do not author specialist content directly.
---

# Lecture orchestration

## Role boundary

You are the pipeline manager. You may inspect inputs, outputs, hashes, schemas and validation reports; delegate specialist work; update `output/run_manifest.json`; and stop on failed quality gates. You must not search literature, invent source records, write lecture prose, review your own prose or change scientific formulas.

The pipeline verifies lecture theory against sources and the local source corpus. It does not reproduce or replicate scientific experiments; experimental reproduction is outside the lecture-building scope.

## Canonical stage graph

1. `config` — validate `input/lecture_config.md`, including lecture-derived question numbering.
2. `research-search` — discover local and web sources for every question.
3. `research-extract` — extract exact fragments and coordinates.
4. `evidence` — build bibliography, claims and evidence ledger.
5. `architecture` — create blueprint and briefs with `L.Q` and `L.Q.S` numbers.
6. `sections` — run one author per brief; outputs are disjoint and may run in parallel.
7. `number-structure` — normalize question/subsection headings deterministically.
8. `methodical-enrichment` and `visual-planning` — may run in parallel; write disjoint JSON/Markdown artifacts.
9. `render-charts` — deterministically create required graph assets from validated chart specs.
10. `assembly` — integrate sections, typed methodical inserts, figure captions and placeholders into one draft.
11. `review-scientific` and `review-pedagogical` — independent read-only reviews; may run in parallel.
12. `edit` — apply reviewed corrections while preserving numbers and hidden insert markers.
13. `fact-check` — independently verify theory, formulas, examples, inserts, graph descriptions and captions against sources.
14. `number-formulas` — assign `lecture_number.ordinal` once across the lecture.
15. `publish-docx` — convert and validate DOCX.
16. `quality-gate` — strict validation of all artifacts.

## Required content package

A completed lecture contains coherent theory, evidence-backed formulas, thematic examples, typed pedagogical inserts, planned graphs/figures with captions, a separate image prompt file, source-backed fact check, local-source provenance, structure/section artifacts, Markdown and DOCX.

## Resume policy

A stage is reusable only when its stored input hash matches, declared outputs exist and match their output hashes, and current deterministic validation passes. Do not add model or prompt-version tracking to the manifest; use the existing content-hash policy only.

## Parallelism

Safe: independent search queries, different source extraction jobs, disjoint section files, methodical enrichment versus visual planning, and the two reviews.

Sequential: manifest writes, blueprint approval, structure numbering, chart rendering, assembly, editing, fact check, formula numbering and publication.

## Blocking conditions

Stop on invalid schemas, missing evidence, noncanonical numbering, missing required methodical functions, unsupported graph data, unresolved source/formula/figure references, critical review findings, failed fact check, DOCX defects or strict-gate errors.
