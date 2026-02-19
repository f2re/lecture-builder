---
name: lit-fetcher
description: "Document fetcher sub-agent. Reads output/lit/search_results.json from
  lit-searcher, fetches top-15 URLs via web_fetch, reads local files, and extracts
  text fragments (definitions, formulas, key passages) relevant to each lecture question.
  Output: output/lit/extracted_fragments.json. Run AFTER lit-searcher."
tools:
  - web_fetch
  - read_file
  - write_file
  - grep_search
model: gemini-2.5-flash
---

Document downloader and text fragment extractor for academic sources.

@../workflows/lit-fetcher.md
