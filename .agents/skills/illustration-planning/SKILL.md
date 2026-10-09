---
name: illustration-planning
description: Plan source-consistent scientific diagrams, graphs and maps with deterministic chart specifications and separate image prompts. Use for «подготовь графики и схемы» after section writing; do not edit lecture prose or invent observational data.
---

# Illustration and graph planning

Read config, blueprint, briefs, completed sections, evidence, bibliography, formula labels and terminology. Write immutable output/plans/figures_index.json, output/plans/chart_specs.json and output/image_prompts.md. The rendering stage copies plans to output/figures_index.json and output/chart_specs.json, then modifies only those copies and declared assets.

Number figures globally from lecture_number in document order: Рисунок 17.1, Рисунок 17.2. Each entry records figure_id, L.Q question, purpose, caption, alt text, status and placeholder. For each figure state what the student should see and which misleading interpretation must be avoided.

Quantitative chart specifications contain exact series/grid values, source/evidence IDs, transformations, axis labels, units and output path. Values must come from cited/local data. After schema validation, the renderer runs `python scripts/render_charts.py --spec output/chart_specs.json --figures output/figures_index.json`. Never ask an image model to create an observational curve, sounding or map contour without data.

A qualitative schematic uses data_policy=schematic and an explicit caption/plot note: «Схематично; не является наблюдательными данными». Normalized plotting points are not measurements.

Image prompts stay separate from student-facing prose. Include learning objective, exact scientific content/relationships, Russian labels, units, aspect ratio, alt text and prohibited artifacts. Remain tool-neutral; generated imagery does not certify scientific correctness.

## Gate
Verify figure numbering/IDs, captions, references, prompt IDs, sources and chart specs. Required assets must exist, match recorded hashes and agree with the rendered index. No figure introduces an unsupported fact. The coherence editor places assets or permitted placeholders; both reviewers check their integration.

Apply .agents/references/integrity-contract.md and .agents/references/prompt-templates.md.
