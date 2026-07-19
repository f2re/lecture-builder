---
name: docx-publishing
description: Convert the fully reviewed and numbered Markdown into a ГОСТ-oriented DOCX with native equations, readable numbered headings, figures, typed callouts, margins, fonts and structural smoke checks.
---

# DOCX publishing

Require a passing fact check, canonical question/subsection numbering, final formula numbers, validated figure/chart artifacts and separate image prompts.

Run the Markdown-to-DOCX wrapper, preserving:

- question headings `L.Q` and subsection headings `L.Q.S`;
- native OMML equations centered with right-aligned `(L.N)` numbers;
- figure/table captions `L.N`;
- methodical blockquotes with consistent labels and without hidden HTML markers;
- charts/images and alt text when assets exist;
- A4, ГОСТ-oriented margins, Times New Roman, paragraph indentation, heading hierarchy, tables and page field.

Run DOCX and strict artifact validation. Never report publication success from file existence alone.
