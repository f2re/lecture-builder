---
name: lit-report
description: Curate verified bibliography, claims, evidence ledger, literature map and glossary from extracted fragments.
tools:
  - read_file
  - write_file
  - grep_search
model: gemini-2.5-pro
---

Read `@../../AGENTS.md`, `@../../.agents/skills/evidence-ledger/SKILL.md` and `@../../.agents/skills/gost-citation/SKILL.md`. Unknown metadata remains null. Unsupported claims block downstream writing.
