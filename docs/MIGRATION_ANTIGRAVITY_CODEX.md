# Cross-platform migration and 3.1 synchronization

## Canonical layer

`.agents/rules`, `.agents/workflows` and `.agents/skills` remain the single source of behavioral policy. Antigravity consumes them directly; Codex TOML profiles and Gemini compatibility files are narrow adapters.

## 3.1 role map

| Capability | Shared Skill | Codex profile | Gemini adapter |
|---|---|---|---|
| orchestration | `lecture-orchestration` | `lecture_orchestrator` | `orchestrator` |
| research/local corpus | `literature-search`, `source-extraction`, `evidence-ledger` | search/extract/curate profiles | lit-* adapters |
| structure | `lecture-architecture`, `document-numbering` | `lecture_architect` | `query-builder` |
| section generation | `section-authoring` | `section_writer` | `section-writer` |
| methodical inserts | `methodical-enrichment` | `methodical_enhancer` | `methodical-enhancer` |
| graphs/image prompts | `illustration-planning` | `visualization_planner` | `visualization-planner` |
| assembly | `coherence-editing` | `coherence_editor` | `document-assembler` |
| reviews/fact check | scientific + pedagogical Skills | reviewer profiles | `reviewer` |
| final editing | `final-editing` | `final_editor` | `editor` |
| formulas/DOCX | numbering, formula and DOCX Skills | `publisher` | orchestrated scripts |

## Numbering migration

`lecture_number` is authoritative. Legacy questions `1. ...`, `2. ...` are migrated to `L.1. ...`, `L.2. ...`. Generated headings use `L.Q` and `L.Q.S`; formula, figure and table counters are separate global `L.N` sequences.

Run:

```bash
python scripts/migrate_v2.py input/lecture_config.md -o input/lecture_config.v3.md
python scripts/number_structure.py output/lecture_draft.md -o output/lecture_draft.md
python scripts/validate_numbering.py output/lecture_draft.md
```

## Methodical and visual additions

The methodical enhancer produces typed JSON inserts rather than editing prose. The visualization planner produces a figure index, deterministic chart specs and a separate image prompt file. Required charts are rendered by `scripts/render_charts.py` before assembly and review.

The manifest remains content-hash based. It does not track prompt/model versions. Scientific experiment reproduction is deliberately outside the lecture-generation scope.
