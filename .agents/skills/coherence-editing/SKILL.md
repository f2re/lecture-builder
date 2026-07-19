---
name: coherence-editing
description: Assemble validated section files into one logically continuous lecture draft, remove structural repetition, unify terminology and write evidence-neutral transitions without introducing new scientific claims. Use after all sections exist and before independent review.
---

# Coherence editing

## Inputs

- `output/lecture_blueprint.json`
- all expected `output/sections/section_*.md`
- `output/bibliography.json`
- `input/lecture_config.md`

## Output

- `output/lecture_draft.md`

## Assembly method

1. Verify exactly one non-empty section for every configured question and sort by numeric section id.
2. Build lecture metadata, measurable objectives, plan and literature sections from validated artifacts.
3. Write an introduction that establishes relevance, prerequisites, central problem, thesis and route through the questions. Do not summarize every section in advance.
4. Insert sections in blueprint order.
5. Reconcile adjacent bridges. Preserve content, but remove duplicate transition sentences and repeated definitions.
6. Enforce the canonical glossary and notation table. At first occurrence define an abbreviation; later use the canonical form consistently.
7. Consolidate repeated background into its earliest necessary position. Do not delete caveats, assumptions or source attributions.
8. Write a conclusion that synthesizes the central thesis, relates results across sections and maps outcomes to competencies without adding new facts.
9. Add control questions covering recall, interpretation and application.

## Edit boundary

You may improve connective prose, headings, ordering inside a section and duplicate explanatory material. You may not create unsupported facts, change a formula's semantics, invent references or conceal a missing section. Material scientific changes must return to the section author/evidence stage.

## Coherence checks

- each section follows from an explicit prior result;
- no undefined concept or abbreviation;
- no repeated paragraph or near-identical definition;
- examples follow the theory they apply;
- micro-conclusions support the final synthesis;
- introduction and conclusion have distinct functions;
- no boilerplate transition repeated across sections.

Run `python scripts/validate_pipeline.py --mode artifacts` when enough artifacts exist, and resolve coherence findings before review.
