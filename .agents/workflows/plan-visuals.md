# Plan lecture visuals and graphs

1. Read the blueprint, briefs, completed sections, evidence ledger and local source bibliography.
2. Activate `illustration-planning` and `document-numbering`.
3. Produce `output/figures_index.json`, `output/chart_specs.json` and the separate `output/image_prompts.md`.
4. Number figures globally as `lecture_number.ordinal`; never restart numbering per question.
5. For data-driven charts, use source-bound deterministic specifications with axis labels and units. Never ask an image model to invent quantitative data.
6. For diagrams and scientific illustrations, write tool-neutral generation prompts with exact content, labels, prohibited artifacts and accessibility text.
7. Validate schemas, then run `python scripts/render_charts.py --spec output/chart_specs.json --figures output/figures_index.json` for every non-omitted chart.
8. Do not edit lecture Markdown. The coherence editor inserts generated graph assets plus validated placeholders and captions before review.
