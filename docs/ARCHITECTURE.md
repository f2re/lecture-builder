# Architecture

## Design principles

Lecture Builder separates generative judgment from deterministic assurance. Agents perform search, synthesis, pedagogy and editing; schemas and scripts enforce structure, provenance, freshness, cross-references, equation numbering and DOCX packaging.

The canonical layer is `.agents/`:

- `rules/` contains always-on invariants;
- `workflows/` contains user-invokable stage recipes;
- `skills/` contains progressively loaded domain and process knowledge.

Platform adapters are deliberately thin:

- Antigravity consumes `.agents` directly;
- Codex adds role/sandbox TOML under `.codex/agents`;
- Gemini maps legacy commands and agents to the same Skills.

## Artifact dependency graph

```text
lecture_config
├─→ local_index + search_results
│   └─→ extracted_fragments
│       └─→ bibliography + evidence_ledger + literature_map + glossary
│           └─→ lecture_blueprint + section_briefs
│               └─→ section_N × N
│                   └─→ lecture_draft
│                       ├─→ scientific_review
│                       └─→ pedagogical_review
│                           └─→ lecture_final + resolution
│                               └─→ fact_check
│                                   └─→ formula_registry + numbered Markdown
│                                       ├─→ figures artifacts
│                                       └─→ DOCX
└────────────────────────────────────────────→ run_manifest + quality_report
```

## Trust boundaries

### Research discovery

Search results are leads, not evidence. Snippets cannot establish authorship, date, page or factual claims.

### Extraction

An exact fragment plus source hash and location becomes potential evidence. Lost page mapping is represented as unavailable, not guessed.

### Evidence curation

Atomic claims are classified as supported, partial, unsupported or not applicable. Only supported claims enter normal section briefs; partial claims carry explicit limits.

### Architecture and writing

The blueprint freezes concept order, terminology, evidence requirements, logical bridges and budgets. Section writers operate on disjoint files and do not assign global equation numbers.

### Review and editing

Scientific and pedagogical reviewers are read-only and independent. The editor resolves findings but cannot approve its own changes. Final fact check reopens evidence after editing.

### Publication

Formula numbering, Markdown validation, DOCX conversion and document inspection are deterministic. The publisher cannot override a failed gate.

## Freshness

`run_manifest.json` stores stage input hashes and output hashes. A stage is fresh only when current inputs and outputs match stored values and validation still passes. A changed config invalidates all dependent stages; changed evidence invalidates architecture and downstream content.

## Parallel execution

Parallelism is limited to work with no shared output:

- per-question search;
- per-source extraction;
- per-section authoring after blueprint freeze;
- independent reviews.

Everything that creates a global ordering or shared state is serialized.
