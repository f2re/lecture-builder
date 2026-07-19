# Artifact contracts

JSON Schema under this directory define every machine-readable pipeline artifact. Source validation compiles all schemas; artifact validation checks instances and cross-file references.

Core contracts cover config, local/search/extraction source data, bibliography, evidence ledger, numbered lecture blueprint, section briefs, reviews, formulas, figures, manifest and publication artifacts.

Methodical and visual extensions:

- `methodical-inserts.schema.json` — typed examples, mnemonics, formula-reading aids, common errors and self-checks;
- `chart-specs.schema.json` — source-bound or explicitly schematic graph specifications;
- `figures-index.schema.json` — global `lecture_number.ordinal` numbering, captions, alt text and links to prompts/chart specs.

Question/subsection display numbers derive from `lecture_number`; formulas, figures and tables use separate global counters with the same lecture prefix.
