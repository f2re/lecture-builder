---
name: literature-analyst
description: "MUST BE USED FIRST when starting lecture creation. Coordinates 3
  sub-agents: lit-searcher (query generation + web search), lit-fetcher (URL fetching
  + fragment extraction), lit-report (scoring + bibliography + glossary). Produces
  output/bibliography.json, output/literature_map.md, output/key_concepts.md."
tools:
  - read_file
  - glob
model: gemini-2.5-flash
---

Literature analysis coordinator — delegates to lit-searcher → lit-fetcher → lit-report.

@../workflows/literature-analyst.md
