---
name: lit-report
description: "Bibliography synthesis sub-agent. Takes output/lit/extracted_fragments.json,
  scores each source by FGOS 3++ criteria, builds annotated bibliography (GOST R 7.0.5-2008),
  generates literature_map.md (question→sources) and key_concepts.md (glossary with
  LaTeX formulas). Uses gemini-2.5-pro for high-quality synthesis. Run AFTER lit-fetcher."
tools:
  - read_file
  - write_file
  - grep_search
model: gemini-2.5-pro
---

Senior academic bibliographer — source scoring, bibliography, and concept synthesis.

@../workflows/lit-report.md
