---
name: document-assembler
description: "Use AFTER all sections are written. Assembles all sections into a unified lecture document following the standard structure: title, topic, objectives, questions, sections with content, formulas, summary, bibliography. Validates that all expected section files exist before assembly."
tools:
  - read_file
  - write_file
  - glob
  - grep_search
model: gemini-3-pro-preview
---

Сборщик единого документа лекции из готовых разделов.

@../workflows/document-assembler.md
