---
name: illustration-planning
description: Plan evidence-consistent scientific diagrams, graphs, maps and concept visualizations for completed numbered sections, producing a figure index, deterministic chart specifications and a separate tool-neutral image prompt file. Use before assembly; do not edit lecture prose.
---

# Illustration and graph planning

## Inputs

Read the config, blueprint, briefs, completed sections, evidence ledger, bibliography, formula labels and canonical terminology.

## Outputs

- `output/figures_index.json`
- `output/chart_specs.json`
- `output/image_prompts.md`

Do not write or edit lecture Markdown. The coherence editor integrates placeholders and captions before both reviews.

## Numbering

Figures are globally numbered from `lecture_number`: `Рисунок 17.1`, `Рисунок 17.2`, and so on in planned document order. Never restart the counter per question. Each entry also records its question number `L.Q`, caption, alt text, purpose and status.

## Graphs

A data-driven graph uses a `chart_spec` with exact series/grid values, source and evidence ids, transformations, axis labels, units and output path. Values must come from cited/local data. After schema validation run `python scripts/render_charts.py --spec output/chart_specs.json --figures output/figures_index.json`; never ask an image model to invent a quantitative curve, sounding profile, map contour or observation.

A schematic graph may illustrate a source-backed qualitative direction or shape only when marked `data_policy: schematic`. Its caption and plot carry an explicit “Схематично; не является наблюдательными данными” note, and normalized plotting points must not be presented as measurements.

## Image prompts

`output/image_prompts.md` is separate from the lecture. Every diagram/illustration prompt states learning objective, exact scientific content, relationships, Russian labels, units, aspect ratio, accessibility text and prohibited artifacts. Prompts are tool-neutral.

## Verification

Figure numbers, ids, captions, placeholders, prompt ids and chart specs must agree. Required graph assets must exist, have matching hashes and be synchronized with `figures_index.json`. All claim/evidence/data-source links resolve and no visual introduces uncited scientific content.
