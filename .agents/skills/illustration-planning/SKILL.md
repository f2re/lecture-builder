---
name: illustration-planning
description: Plan evidence-consistent scientific diagrams, charts, maps and concept visualizations for a completed lecture, producing neutral tool-agnostic prompts, placeholders and an index. Use after factual content is stable; do not generate or alter scientific claims.
---

# Illustration planning

## Inputs

- fact-checked `output/lecture_final.md`
- `output/lecture_blueprint.json`
- formula registry and canonical terminology
- `input/lecture_config.md`

## Outputs

- `output/image_prompts.md`
- `output/figures_index.json`
- figure placeholders in final Markdown when requested

## Selection criteria

Use a figure when it reduces cognitive load for spatial structure, multi-stage process, comparison, quantitative relation, map interpretation, geometry of a formula or concept dependency. Do not add decorative images or duplicate prose as an infographic.

## Prompt contract

Every prompt specifies learning objective, exact scientific content, relationships, labels, units, aspect ratio, accessibility constraints, prohibited artifacts and the source section. Prompts are tool-neutral; optional adapters may target a particular image system without making it canonical.

## Integrity

Do not ask an image model to invent observational data, map contours, instrument readings or quantitative curves. Data-driven charts must be produced from a cited dataset by deterministic plotting code. Scientific labels and units must match the lecture.

## Verification

Figure ids, numbers, titles, placeholders and index entries must agree. Every figure has a purpose, source section, priority and status. Cross-references resolve and no figure introduces uncited factual content.
