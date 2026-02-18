---
name: orchestrator
description: "ENTRY POINT. Runs the full lecture generation pipeline automatically: validates input, calls each agent in sequence, checks outputs, and stops on error. Use this instead of calling agents manually."
tools:
  - read_file
  - write_file
  - glob
  - grep_search
model: gemini-2.5-pro-preview-05-06
---

Оркестратор полного пайплайна генерации лекции.

@../workflows/orchestrator.md
