# Lecture Builder

Universal multi-agent system for automated creation of academic lecture materials
using Gemini CLI.

## 🚀 Features
- **3-stage literature pipeline** — search (Flash), fetch (Flash), synthesis (Pro), optimised for speed and cost.
- **Pedagogical design** — FGOS 3++-compliant query expansion and competency mapping.
- **Multi-agent architecture** — specialised roles for search, writing, review, and assembly.
- **LaTeX support** — correct formatting of mathematical and technical formulas.
- **GOST citations** — automatic bibliography formatting per GOST R 7.0.5-2008.

## 🛠 Installation
1. Install [Gemini CLI](https://github.com/google/gemini-cli).
2. Clone this repository.
3. Fill in `input/lecture_config.md`.

## 📖 Usage

```bash
gemini build-lecture        # Full pipeline
gemini search-literature    # Literature analysis only (3-stage)
gemini review-lecture       # Review an existing draft
```

### Available commands
- `/agents list` — verify all agents are available
- `gemini build-lecture` — full pipeline: literature → queries → writing → review → edit
- `gemini search-literature` — 3-stage literature sub-pipeline only
- `gemini review-lecture` — methodological review of an existing draft

---

## 🏗 Architecture

### Full pipeline
```
literature-analyst (coordinator, Flash)
  ├── lit-searcher  [Flash] → output/lit/search_results.json
  ├── lit-fetcher   [Flash] → output/lit/extracted_fragments.json
  └── lit-report    [Pro]  → output/bibliography.json
                              output/literature_map.md
                              output/key_concepts.md
query-builder       [Flash] → output/queries/query_{N}.md
section-writer ×N   [Pro]  → output/sections/section_{N}_*.md
document-assembler  [Flash] → output/lecture_draft.md
reviewer            [Pro]  → output/review_report.md
editor              [Pro]  → output/lecture_final.md
```

### Literature sub-pipeline (v2)

| Agent | Model | Responsibility |
|---|---|---|
| `lit-searcher` | gemini-2.5-flash | Build search matrix (RU+EN), run `google_web_search`, index local files |
| `lit-fetcher`  | gemini-2.5-flash | Fetch top-15 URLs via `web_fetch`, extract relevant text fragments |
| `lit-report`   | gemini-2.5-pro   | Score sources (FGOS), build bibliography, synthesise glossary |

**Why 3 agents?** Search and fetch are I/O-bound — Flash is 5–10× faster and cheaper.
Pro reasoning is needed only for the final synthesis step.

### Shared skills (`.gemini/skills/`)
- `search-patterns.md` — query templates for CyberLeninka, elibrary, arXiv, etc.
- `gost-citation.md` — GOST R 7.0.5-2008 citation format rules
- `fgos-standards.md` — FGOS 3++ competency framework

---

## 📁 Project structure
```
.gemini/
  agents/
    literature-analyst.md   # coordinator → calls lit-searcher, lit-fetcher, lit-report
    lit-searcher.md         # [Flash] web search + local file index
    lit-fetcher.md          # [Flash] URL fetching + fragment extraction
    lit-report.md           # [Pro]   scoring + bibliography + glossary
    query-builder.md
    section-writer.md
    document-assembler.md
    reviewer.md
    editor.md
  workflows/                # step-by-step instructions per agent
  commands/                 # CLI shortcuts (build-lecture, search-literature, …)
  skills/                   # shared reusable knowledge
input/
  lecture_config.md         # ← fill this first
  literature/               # optional: local PDFs / textbooks
output/
  lit/                      # intermediate stage files
  bibliography.json
  literature_map.md
  key_concepts.md
  lecture_final.md
  …
```

## 🤖 Models
| Task | Model |
|---|---|
| Literature search, fetch, query expansion, document assembly | `gemini-2.5-flash` |
| Bibliography synthesis, section writing, review, editing | `gemini-2.5-pro` |
