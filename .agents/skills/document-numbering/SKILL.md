---
name: document-numbering
description: Apply and verify lecture-derived numbering for questions, subsections, equations, figures and tables. Use for «исправь нумерацию» during architecture and authoring; validate immutable final content without silently rewriting it.
---

# Document numbering

lecture_number in input/lecture_config.md is the single numbering root. Lecture 17 uses question 17.1; subsections 17.1.1 and 17.1.2; optional deeper 17.1.1.1; global formula (17.1), figure Рисунок 17.1 and table Таблица 17.1. Counters are separate namespaces. Technical files retain local ordinal section_1_... so a lecture number change does not rename intermediate files.

Use exact configuration/brief titles and display numbers. The visible question plan uses bullets such as `- **17.1. Название вопроса**`, not a second independent enumerated list. Headings use `## 17.1. ...`, `### 17.1.1. ...`. Methodical callouts are typed but not visibly numbered.

Authors normalize headings before marking section outputs complete. The later number-structure stage only checks these frozen files and records output/stages/number_structure.json. Do not mutate completed upstream outputs to make their hashes appear fresh.

Normalize the editor's lecture_edited.md before final equation numbering. Formula-governance creates lecture_final.md and formula_registry.json. Only then do final reviewers and fact checker approve that exact snapshot.

```bash
python scripts/validate_numbering.py output/lecture_final.md
```

This final command is a check, not permission to modify approved text. A late correction invalidates relevant downstream stages and requires reapproval. Verify canonical section hierarchy and globally sequential figure/table/formula captions; never restart their counters per question.

Apply .agents/references/integrity-contract.md and .agents/references/prompt-templates.md.
