---
name: lit-searcher
description: "Fast search sub-agent. Reads lecture_config.md, builds a search matrix
  (4–5 queries per question in RU+EN), runs google_web_search across CyberLeninka /
  elibrary / RSHU / arXiv, and indexes local literature files. Output:
  output/lit/search_results.json + output/lit/local_index.json. Uses Flash for speed."
tools:
  - google_web_search
  - read_file
  - write_file
  - glob
model: gemini-2.5-flash
---

Fast academic literature searcher — query generation and web search only.

@../workflows/lit-searcher.md
