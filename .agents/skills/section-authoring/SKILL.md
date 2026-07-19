---
name: section-authoring
description: Write exactly one numbered Russian university lecture question from a validated brief and verified evidence, with theory, definitions, formulas, examples, limitations, misconceptions, logical bridges and a micro-conclusion. Use after architecture; never assemble or edit other sections.
---

# Section authoring

## Inputs and output

Read one section brief, the blueprint, evidence ledger, bibliography, key concepts and config. Write exactly one `output/sections/section_{N}_{slug}.md`.

## Heading contract

For lecture 17 and the first question:

```markdown
## 17.1. Название вопроса

### 17.1.1. Первый подраздел

### 17.1.2. Второй подраздел
```

Use only the display numbers and subsection plan from the brief. Do not create local `1.1` numbering. Technical file names still use ordinal `section_1_...`.

## Required reasoning sequence

Connect to the previous result; state the local problem; define terms; explain theory/mechanism; introduce formulae after motivation; state units, assumptions and limits; work through the core evidence-backed example; correct the planned misconception; give a numbered micro-conclusion subsection; end with the planned bridge.

Use stable equation labels `\label{eq:...}` and `@eq:...` references. Never assign final formula numbers.

## Division of labor

The section author writes the essential scientific example needed to explain the theory. It does not add mnemonic boxes, self-check callouts or extra thematic mini-cases; those are designed by `methodical-enrichment` after all sections exist. It may identify a useful graph in prose but does not write image-generation prompts.

## Source discipline

Every factual, definitional, quantitative, causal and formula claim resolves to supported evidence and receives an adjacent `<!-- claim:claim_id -->` marker. Use stable source citations. Distinguish quotation, paraphrase, assumption, approximation and hypothetical worked example.

## Verification

Check output path, canonical headings, word budget, claims, citations, formula labels/symbols/units, core example, misconception, micro-conclusion and both bridges.
