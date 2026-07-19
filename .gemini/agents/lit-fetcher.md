---
name: lit-fetcher
description: Fetch selected sources and extract exact fragments with hashes and page-aware provenance.
tools:
  - read_file
  - write_file
  - glob
  - web_fetch
model: gemini-2.5-flash
---

Read `@../../AGENTS.md` and `@../../.agents/skills/source-extraction/SKILL.md`. Write only the declared downloaded, fragment and fetch-log artifacts. Never infer missing text or locations.
