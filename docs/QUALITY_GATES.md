# Quality gates

A high score never overrides a blocker.

## Source and configuration

- valid config and explicit `lecture_number`;
- configured questions use `lecture_number.question` numbering;
- schemas compile, Skills have frontmatter and Codex TOML profiles are valid;
- Antigravity, Codex and Gemini adapters point to the same `.agents` layer;
- no experiment-reproduction stage or prompt/model manifest tracking is required.

## Research and evidence

- web and local source coverage for every question;
- exact fragments and metadata provenance;
- verified pages for page citations;
- no supported claim without evidence and no unsupported claim in publishable content.

## Architecture and numbering

- one blueprint section/brief per question;
- display numbers `L.Q`, subsections `L.Q.S`, sequential and matching config;
- concept prerequisites precede use;
- time/word budgets, competencies, methodical requirements and visual opportunities are complete.

## Text and methodical inserts

- coherent theory, definitions before use, formula interpretation and core examples;
- required methodical learning functions per question;
- mnemonics are accurate and reversible;
- thematic examples are source-backed or visibly hypothetical;
- insert density stays within config and required hidden markers occur in draft/final;
- no repeated definitions, boilerplate transitions or callout clutter.

## Visuals and graphs

- `figures_index.json`, `chart_specs.json` and separate `image_prompts.md` exist;
- figures use global `L.N` numbers and captions agree with index;
- graphs have axes, units, data policy and source ids when data-bound;
- schematic graphs are visibly labeled and contain no invented observational values;
- required graph assets are rendered, non-empty, hash-matched and synchronized with the figure index;
- prompts cannot invent quantitative curves, readings or map contours.

## Reviews

- independent scientific and pedagogical reports;
- callouts, examples, graphs and captions included in review scope;
- critical/major findings resolved;
- independent final fact check has status `pass`.

## Formulas and publication

- stable labels before numbering and one global `L.N` sequence after fact check;
- symbols, units, assumptions and references complete;
- DOCX contains native OMML, right-aligned numbers, numbered headings, captions and readable callouts;
- strict validation produces zero errors.

## Commands

```bash
python scripts/validate_pipeline.py --mode source
pytest
python scripts/number_structure.py output/lecture_final.md -o output/lecture_final.md
python scripts/validate_numbering.py output/lecture_final.md
python scripts/render_charts.py --spec output/chart_specs.json --figures output/figures_index.json
python scripts/validate_pipeline.py --mode artifacts --strict --report output/quality_report.json
python scripts/validate_docx.py output/lecture_final.docx --expect-formulas
```
