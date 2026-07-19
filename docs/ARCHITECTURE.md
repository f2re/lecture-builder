# Architecture

Lecture Builder separates generative judgment from deterministic assurance. Agents search, extract, design, write, enrich, visualize, review and edit; schemas and scripts enforce provenance, numbering, cross-references and publication structure.

The canonical layer is `.agents/`: rules, workflows and progressively loaded Skills. Antigravity consumes it directly; Codex adds TOML role/sandbox adapters; Gemini maps legacy commands to the same layer.

## Artifact graph

```text
lecture_config
├─→ local_index + search_results
│   └─→ extracted_fragments
│       └─→ bibliography + evidence_ledger + literature_map + glossary
│           └─→ numbered blueprint + numbered section briefs
│               └─→ section_N × N
│                   ├─→ methodical_inserts
│                   ├─→ figures_index + chart_specs + image_prompts
│                   │   └─→ generated chart assets
│                   └─→ lecture_draft
│                       ├─→ scientific_review
│                       └─→ pedagogical_review
│                           └─→ lecture_final + resolution
│                               └─→ fact_check
│                                   └─→ formula_registry + DOCX
└────────────────────────────────────────→ run_manifest + quality_report
```

## Trust boundaries

Search results are leads, not evidence. Extraction preserves exact fragments, hashes and locations. Evidence curation links atomic claims to verified fragments. The blueprint freezes concept order, `L.Q`/`L.Q.S` numbering, terminology, evidence requirements, methodical goals and visual opportunities.

Section writers own scientific exposition and the core worked example. The methodical enhancer owns only structured student-facing callouts. The visualization planner owns only figure metadata, chart specs and separate image prompts. The coherence editor integrates these artifacts but cannot add claims.

Scientific and pedagogical reviewers are read-only. Scientific review covers theory, formulas, examples, callouts, graph data provenance and captions. Pedagogical review covers progression, cognitive load, mnemonic quality, insert density and visual usefulness. The editor cannot approve its own changes; final fact check reopens evidence.

The system verifies lecture content against sources and the local corpus. Scientific experiment reproduction/replication is outside this architecture.

## Numbering

`lecture_number` determines all visible prefixes:

```text
question      L.Q
subsection    L.Q.S
formula       L.N (global formula counter)
figure        L.N (global figure counter)
table         L.N (global table counter)
```

Formula, figure and table sequences are independent global counters. Structure headings are normalized before review; formulas are numbered after fact check.

## Parallel execution

Safe: per-question search, per-source extraction, per-section authoring, methodical enrichment versus visual planning, and independent reviews.

Serialized: manifest writes, blueprint approval, structure normalization, chart rendering, assembly, editing, fact check, formula numbering and publication.
