# DOCX converter instructions

This directory is deterministic publishing code. Do not change lecture scientific content here.

Required properties:

- Pandoc output contains native editable OMML equations.
- `\tag{N.M}` is removed from the math expression before Pandoc and restored as a separate right-aligned number.
- A numbered equation is placed in a borderless three-column table with a centered formula.
- A4 size, 30/15/20/20 mm margins, Times New Roman, paragraph formatting and PAGE footer remain enforced.
- Technical `[[EQNO:...]]` markers must not survive in the final DOCX.

After changes run converter tests and `python scripts/validate_docx.py` on the smoke document. Never declare success when Pandoc is unavailable or structural validation fails.
