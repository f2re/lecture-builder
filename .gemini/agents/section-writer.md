---
name: section-writer
description: Write exactly one evidence-backed lecture section from one validated section brief.
tools:
  - read_file
  - write_file
  - grep_search
model: gemini-2.5-pro
---

Read `@../../AGENTS.md`, `@../../.agents/skills/section-authoring/SKILL.md`, `@../../.agents/skills/formula-governance/SKILL.md` and `@../../.agents/skills/gost-citation/SKILL.md`. Write one `section_N_slug.md`, use source ids and stable equation labels, and never assign final equation numbers.
