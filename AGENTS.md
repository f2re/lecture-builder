# Lecture Builder — cross-platform agent policy

Lecture Builder generates Russian university lectures through one verified multi-agent pipeline. Canonical instructions live in `.agents/`; Antigravity, Codex and the Gemini compatibility layer consume the same rules, Skills, workflows and contracts.

## Instruction precedence

1. System and user instructions.
2. Nearest applicable `AGENTS.md`.
3. `.agents/rules/*.md`.
4. Selected `.agents/workflows/*.md`.
5. Selected `.agents/skills/*/SKILL.md`.
6. Platform adapters under `.codex/` or `.gemini/`.
7. User-facing documentation.

Scientific/methodical behavior must not be duplicated in platform adapters.

## Non-negotiable invariants

- Never invent source metadata, quotations, page numbers, observations, graph values or experimental data.
- Unknown metadata is `null` or explicitly unverified.
- Every substantive scientific claim resolves through `output/evidence_ledger.json` and is marked in Markdown with `<!-- claim:claim_id -->`.
- Page citations require page-aware verified extraction.
- `input/` is user-owned; generated artifacts belong under `output/`.
- Validate JSON against `contracts/`; a file's existence does not prove freshness or correctness.
- Use the existing manifest content hashes only. Do not add prompt-version or model-version tracking.
- The pipeline verifies theory against sources and the local corpus. It does not reproduce or replicate scientific experiments.
- The orchestrator coordinates; specialists search, extract, curate, design, write, enrich, visualize, review, edit and publish.
- Parallel workers may write only disjoint files.
- Unsupported claims, invalid numbering, misleading methodical inserts, invented graph data, unresolved formula/figure references, critical review findings or DOCX failures block publication.

## Canonical pipeline

1. Validate `input/lecture_config.md`.
2. Search web and local literature for every question.
3. Extract exact fragments with provenance and locations.
4. Build bibliography, claim inventory, evidence ledger, literature map and glossary.
5. Design one numbered blueprint and one numbered brief per question.
6. Write one evidence-backed section per brief.
7. Normalize question/subsection headings.
8. Run methodical enrichment and visual/graph planning in parallel.
9. Render validated graph assets deterministically.
10. Assemble one coherent draft with typed inserts, figure captions and placeholders.
11. Run independent scientific and pedagogical reviews.
12. Apply corrections to a separate final version.
13. Run independent source-based fact check.
14. Assign lecture-wide formula numbers once.
15. Convert to DOCX and run strict validation.

## Required artifacts

```text
output/lit/local_index.json
output/lit/search_results.json
output/lit/search_log.md
output/lit/extracted_fragments.json
output/lit/fetch_log.md
output/bibliography.json
output/evidence_ledger.json
output/literature_map.md
output/key_concepts.md
output/lecture_blueprint.json
output/lecture_blueprint.md
output/section_briefs/section_N.json
output/sections/section_N_slug.md
output/methodical_inserts.json
output/figures_index.json
output/chart_specs.json
output/image_prompts.md
output/lecture_draft.md
output/reviews/scientific.json
output/reviews/pedagogical.json
output/reviews/resolution.json
output/reviews/fact_check.json
output/review_report.md
output/lecture_final.md
output/edit_log.md
output/formula_registry.json
output/lecture_final.docx
output/quality_report.json
output/run_manifest.json
```

## Numbering contract

`lecture_number` is the single numbering root. For lecture 17:

- question headings: `## 17.1. ...`, `## 17.2. ...`;
- subsection headings: `### 17.1.1. ...`, `### 17.1.2. ...`;
- optional deeper headings: `#### 17.1.1.1. ...`;
- formula numbers: `(17.1)`, `(17.2)`, `(17.3)` globally;
- figure numbers: `Рисунок 17.1`, `Рисунок 17.2` globally;
- table numbers: `Таблица 17.1`, `Таблица 17.2` globally.

Question, formula, figure and table counters are separate namespaces. Technical file names retain local ordinals such as `section_1_...`.

## Lecture quality contract

A lecture is one argument, not a stack of essays. Each question connects to prior knowledge, states a problem, defines terms, explains theory, introduces formalism after motivation, states limits, applies the model, corrects a misconception, derives a micro-conclusion and creates a specific bridge.

Methodical callouts are restrained student-facing inserts: key idea, mnemonic, thematic example, formula reading, common error, self-check, comparison, professional context or visual cue. They are visibly typed but unnumbered, so they do not compete with the scientific hierarchy. Factual inserts require evidence; hypothetical values are labeled.

Graphs use source-bound deterministic specifications with axes and units, or are explicitly schematic. Image-generation prompts remain in the separate `output/image_prompts.md` file.

## Role boundaries

- `orchestrator`: manifest, dependencies, delegation and status only.
- `literature-searcher`: discovery/local indexing only.
- `source-extractor`: exact extraction and provenance only.
- `evidence-curator`: bibliography, claims and evidence only.
- `lecture-architect`: blueprint/briefs and numbering plan only.
- `section-writer`: exactly one section file.
- `methodical-enhancer`: methodical insert JSON only.
- `visualization-planner`: figure index, chart specs, separate image prompts and declared deterministic chart assets only.
- `coherence-editor`: assembled draft only; no new claims.
- reviewers/fact-checker: read-only machine-readable findings.
- `final-editor`: final Markdown and resolution log; no self-approval.
- `publisher`: deterministic numbering, DOCX and strict validation.

## Parallelism

Safe: independent search/extraction, disjoint section files, methodical versus visual planning, and independent reviews.

Sequential: manifest writes, blueprint finalization, structure normalization, chart rendering, assembly, editing, fact check, formula numbering and publication.

## Commands

```bash
python -m pip install -e '.[dev]'
python scripts/validate_pipeline.py --mode source
pytest
python scripts/number_structure.py output/lecture_final.md -o output/lecture_final.md
python scripts/validate_numbering.py output/lecture_final.md
python scripts/render_charts.py --spec output/chart_specs.json --figures output/figures_index.json
python scripts/number_formulas.py output/lecture_final.md -o output/lecture_final.md --registry output/formula_registry.json
bash scripts/md2docx/run_md2docx.sh output/lecture_final.md -o output/lecture_final.docx
python scripts/validate_docx.py output/lecture_final.docx --expect-formulas
python scripts/validate_pipeline.py --mode artifacts --strict --report output/quality_report.json
```

Report unavailable network, model, extraction or Pandoc capabilities exactly; never represent a skipped check as passed.
