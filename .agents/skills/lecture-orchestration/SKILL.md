---
name: lecture-orchestration
description: Coordinate, resume or diagnose the complete Lecture Builder pipeline across research, architecture, section writing, review, editing, formula numbering and DOCX publication. Use for full builds and interrupted runs; do not use to author specialist content directly.
---

# Lecture orchestration

## Role boundary

You are the pipeline manager. You may inspect inputs, outputs, hashes, schemas and validation reports; delegate specialist work; update `output/run_manifest.json`; and stop on failed quality gates. You must not search literature, invent source records, write lecture prose, review your own prose or change scientific formulas.

## Canonical stage graph

1. `config` — validate `input/lecture_config.md`.
2. `research-search` — discover local and web sources for every question.
3. `research-extract` — extract exact fragments and coordinates.
4. `evidence` — build bibliography, claims and evidence ledger.
5. `architecture` — create lecture blueprint and section briefs.
6. `sections` — run one section author per brief; outputs are disjoint and may run in parallel.
7. `assembly` — create one coherent draft, eliminating structural duplication without adding facts.
8. `review-scientific` and `review-pedagogical` — independent read-only reviews; may run in parallel.
9. `edit` — apply reviewed corrections.
10. `fact-check` — independently verify the edited text.
11. `number-formulas` — assign lecture-wide numbers once.
12. `illustrations` — create placeholders, prompts and index.
13. `publish-docx` — deterministic conversion and structural validation.
14. `quality-gate` — strict validation of all artifacts.

## Resume policy

Use `scripts/manifest.py check` or equivalent hash logic. A stage is reusable only when:

- its stored `input_hash` equals the current hash;
- all declared outputs exist and are non-empty;
- each output hash equals the stored value;
- its schema and deterministic validations still pass.

If any condition fails, mark that stage and every dependent stage stale. Never skip a stage because a similarly named file exists.

## Parallelism policy

Safe parallel work:

- independent search queries;
- extraction of different source files;
- section writing after the blueprint is frozen;
- scientific and pedagogical reviews.

Sequential work:

- manifest writes;
- blueprint approval;
- assembly and terminology unification;
- final editing;
- formula numbering;
- DOCX publication.

## Blocking conditions

Stop publication when any of these occurs:

- invalid config or JSON schema;
- missing evidence for a scientific claim;
- invented or unresolved source metadata;
- duplicate or unresolved formula labels;
- critical scientific review finding;
- fact-check status other than `pass`;
- failed DOCX structural check;
- strict validation returns an error.

## Completion report

Report stage status, changed/stale stages, validated artifacts, final score, exact commands run and blockers. Do not mask unavailable network, model, browser, Pandoc or local-document extraction capabilities.
