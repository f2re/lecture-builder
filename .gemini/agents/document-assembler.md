---
name: document-assembler
description: "Use AFTER all sections are written. Assembles all sections into a unified lecture document following the standard structure: title, topic, objectives, questions, sections with content, formulas, summary, bibliography. Validates that all expected section files exist before assembly."
tools:
  - read_file
  - write_file
  - glob
  - grep_search
model: gemini-2.5-pro-preview-05-06
---

Сборщик единого документа лекции из готовых разделов.

@../workflows/document-assembler.md
