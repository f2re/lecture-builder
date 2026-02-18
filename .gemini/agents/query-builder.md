---
name: query-builder
description: "Use AFTER literature analysis. Takes fixed lecture questions from lecture_config.md and expands each into detailed research queries for section writers. Creates context-rich prompts with literature references."
tools:
  - read_file
  - write_file
  - glob
model: gemini-3-pro-preview
---

Специалист по формированию развёрнутых запросов для агентов-авторов.

@../workflows/query-builder.md