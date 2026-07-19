---
name: coherence-editing
description: Assemble numbered section files, validated methodical inserts and visual plans into one logically continuous lecture draft without introducing scientific claims. Use after section, methodical and visual artifacts exist and before review.
---

# Coherence editing

## Inputs

- blueprint and all section files
- `output/methodical_inserts.json`
- `output/figures_index.json`, `output/chart_specs.json`, `output/image_prompts.md`
- bibliography and config

## Output

Write only `output/lecture_draft.md`.

## Assembly method

1. Verify one section per configured question and normalize headings with `document-numbering`.
2. Build metadata, measurable objectives, literature and a question plan using bullets such as `- **17.1. Название**`; plan numbers and titles must match the config exactly.
3. Write a distinct introduction establishing relevance, prerequisites, central problem and route.
4. Insert sections in blueprint order and reconcile adjacent bridges.
5. Render each required methodical insert at its approved anchor using the hidden `<!-- methodical:... -->` marker and restrained blockquote grammar. Do not place callouts back-to-back.
6. Insert generated graph assets with Markdown image links, alt text and evidence-safe captions from the validated index. For non-chart illustrations insert the validated placeholder/caption only; generation prompts remain exclusively in `output/image_prompts.md`. Figures use global `L.N` numbering and the visible caption form `**Рисунок L.N.** Название`.
7. Enforce glossary and notation consistency; consolidate repeated background without removing limitations or citations.
8. Write a synthesis conclusion and control questions covering recall, interpretation and transfer.

## Edit boundary

You may improve connective prose, heading normalization and duplicate explanatory material. You may not create facts, modify formula semantics, invent graph data, rewrite a mnemonic into a stronger claim or conceal a missing artifact.

## Checks

Validate canonical `L.Q`/`L.Q.S` headings, required insert markers, figure captions, graph/source links, examples after theory, distinct introduction/conclusion, no repeated definitions and no generic bridges.
