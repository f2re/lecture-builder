# Lecture Builder — cross-platform agent policy

This repository generates Russian university lecture materials through a verified multi-agent pipeline. The canonical cross-platform instructions are under `.agents/`; Antigravity, Codex and the Gemini compatibility layer consume the same rules, skills and artifact contracts.

## Instruction precedence

1. System and user instructions.
2. The nearest applicable `AGENTS.md`.
3. `.agents/rules/*.md`.
4. The selected `.agents/workflows/*.md`.
5. The selected `.agents/skills/*/SKILL.md`.
6. Platform adapters under `.codex/` or `.gemini/`.
7. User-facing documentation.

When instructions conflict, follow the higher level and report the conflict. Scientific methodology must not be duplicated in platform adapters.

## Non-negotiable invariants

- Never invent authors, titles, years, publishers, DOI values, URLs, quotations, pages, source classifications or experimental data.
- Unknown metadata is `null` or explicitly unverified.
- Every substantive scientific claim must resolve through `output/evidence_ledger.json` to exact source evidence and be traceable in Markdown through `<!-- claim:claim_id -->`.
- Page citations are allowed only for page-aware verified extraction.
- `input/` is user-owned. Do not overwrite or delete it without an explicit request for that exact change.
- Generated artifacts belong in `output/`; prompts, rules, contracts, scripts and tests do not.
- Validate JSON against `contracts/` and use deterministic scripts before declaring a stage complete.
- File existence does not prove freshness. Use `output/run_manifest.json` and content hashes.
- The orchestrator coordinates; specialists search, extract, curate, design, write, review, edit and publish.
- Parallel workers may write only disjoint files.
- Any unsupported claim, unresolved citation, duplicate/unresolved equation label, critical review finding or failed DOCX check blocks publication.

## Canonical pipeline

1. Validate `input/lecture_config.md`.
2. Discover sources for every configured question.
3. Extract exact fragments with provenance and locations.
4. Build verified bibliography, claim inventory and evidence ledger.
5. Design one coherent lecture blueprint and one section brief per question.
6. Write one evidence-backed section per brief.
7. Assemble and coherence-edit the draft without adding facts.
8. Run independent scientific and pedagogical reviews.
9. Apply reviewed corrections in a separate final version.
10. Run an independent final fact check.
11. Assign lecture-wide equation numbers once.
12. Plan illustrations without inventing data.
13. Convert to DOCX and inspect native equation structure.
14. Run the strict quality gate and update the manifest.

## Required stage artifacts

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
output/lecture_draft.md
output/reviews/scientific.json
output/reviews/pedagogical.json
output/reviews/resolution.json
output/reviews/fact_check.json
output/review_report.md
output/lecture_final.md
output/formula_registry.json
output/image_prompts.md
output/figures_index.json
output/lecture_final.docx
output/quality_report.json
output/run_manifest.json
```

## Lecture quality contract

A lecture is one argument, not a concatenation of essays. Each section must connect to an established result, state a local question, define new terms, explain meaning, introduce formalism after motivation, state assumptions and limits, apply the model in an example, address a likely misconception, derive a micro-conclusion and create a content-specific bridge to the next question.

Use one main idea per paragraph. Do not use a concept before its prerequisite. Do not repeat definitions or generic transitions. Distinguish fact, interpretation, assumption, approximation, pedagogical simplification and worked example. Conclusions do not introduce new facts.

## Citation and evidence syntax

Use stable citations:

```text
[@src_001]
[@src_001, с. 45]
```

The second form requires verified page coordinates. Do not use unresolved author–year strings as the canonical representation.

## Formula syntax

Authors use stable labels and references, not final numbers:

```latex
$$
\Delta H = \frac{R\overline{T_v}}{g_0}\ln\frac{p_1}{p_2}
\label{eq:hypsometric}
$$

Из соотношения @eq:hypsometric следует ...
```

After final fact check, run the deterministic lecture-wide numbering pass. Do not restart equation counters per section and do not manually edit generated `\tag{lecture.counter}` values.

## Role boundaries

- `orchestrator`: manifest, dependencies, delegation and status only.
- `literature-searcher`: discovery/indexing only.
- `source-extractor`: exact extraction and provenance only.
- `evidence-curator`: bibliography, claims and evidence only.
- `lecture-architect`: blueprint and briefs only.
- `section-writer`: exactly one section file.
- `coherence-editor`: assembled draft only; no new claims.
- reviewers/fact-checker: read-only with machine-readable findings.
- `final-editor`: final Markdown and resolution log; no self-approval.
- `publisher`: numbering, illustrations, DOCX and strict validation.

## Parallelism

Safe: independent search queries, different source extraction jobs, disjoint section files after a frozen blueprint, and the two independent reviews.

Sequential: manifest updates, blueprint finalization, assembly, final editing, fact check, equation numbering and publication.

## Commands

```bash
python -m pip install -e '.[dev]'
python scripts/validate_pipeline.py --mode source
pytest
python scripts/number_formulas.py output/lecture_final.md \
  -o output/lecture_final.md --registry output/formula_registry.json
bash scripts/md2docx/run_md2docx.sh output/lecture_final.md \
  -o output/lecture_final.docx
python scripts/validate_docx.py output/lecture_final.docx --expect-formulas
python scripts/validate_pipeline.py --mode artifacts --strict \
  --report output/quality_report.json
```

If network, browser, document extraction, model access or Pandoc is unavailable, report the exact blocker. Never represent a skipped check as passed.
