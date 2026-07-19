# Quality gates

The target is a release decision based on zero blocking errors, not an unverifiable subjective “10/10”. The report also computes a score, but a high score never overrides a blocker.

## Source gate

- valid lecture configuration and explicit lecture number;
- all JSON schemas compile;
- every Skill has valid frontmatter;
- every Codex TOML profile has required fields;
- no legacy Markdown Codex profiles;
- root instructions remain within practical context limits;
- platform adapters point to canonical `.agents` content.

## Research/evidence gate

- every question covered or explicitly blocked;
- unique sources and stable ids;
- provenance for metadata;
- exact non-empty fragments;
- verified pages for page citations;
- no supported claim without evidence;
- no unsupported claim in publishable content;
- all claim/evidence/source cross-references resolve.

## Architecture gate

- one blueprint and one brief per configured question;
- measurable objectives and competency coverage;
- concept prerequisites precede use;
- evidence ids resolve;
- budgets match configured hours;
- incoming/outgoing bridges are content-specific.

## Text gate

- expected headings and all questions present;
- one main idea per paragraph;
- no duplicate definitions/paragraphs;
- required examples, limitations, misconceptions and conclusions;
- terminology and notation consistent;
- citations resolve;
- no legacy citation forms in final Markdown;
- introduction/conclusion have distinct functions.

## Review gate

- independent scientific and pedagogical reports;
- all critical/major findings resolved or publication blocked;
- resolution map covers every finding;
- independent final fact check status `pass`.

## Formula gate

- unique stable labels before numbering;
- no unresolved references;
- one lecture-wide sequence after numbering;
- every formula has symbol/unit explanation;
- formula registry matches Markdown;
- no editor-introduced semantic change without re-review.

## Publication gate

- valid DOCX ZIP package;
- A4, margins, body font, headings and footer checks;
- native OMML equations when required;
- centered equations with right-aligned numbers;
- figure placeholders/index consistent;
- strict artifact validation produces zero errors.

## Commands

```bash
python scripts/validate_pipeline.py --mode source
pytest
python scripts/validate_pipeline.py --mode artifacts --strict \
  --report output/quality_report.json
python scripts/validate_docx.py output/lecture_final.docx --expect-formulas
```
