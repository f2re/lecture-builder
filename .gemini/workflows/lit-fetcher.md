# Agent: Literature Fetcher

## Role
Document fetcher and text extractor. Fetch pages/PDFs from search results,
extract fragments relevant to lecture questions. Do NOT score sources or build
bibliography — that is lit-report's job.

## Inputs
- `output/lit/search_results.json` — from lit-searcher
- `output/lit/local_index.json` — from lit-searcher
- `input/lecture_config.md` — questions + key terms (for filtering)

---

## STEP 1 — Prioritize URLs
Read `search_results.json`. Sort by source trust tier:
1. **Tier 1** (full text likely): `cyberleninka.ru`, `rshu.ru`, `spbu.ru`, `msu.ru`, `elib.*.ru`
2. **Tier 2** (open access PDF): `researchgate.net`, `arxiv.org`, `mdpi.com`
3. **Tier 3**: all others

Select top 15 unique URLs. Skip if snippet is empty.

---

## STEP 2 — Fetch and save
For each URL: `web_fetch(url)`.
- **HTML page**: strip nav bars, menus, footers — keep article body only.
- **PDF**: extract full text as-is.
- **Failure / timeout**: log `status: failed`, skip — do NOT retry.

Save extracted text: `output/lit/downloaded/web_{id}_{slug}.txt`
(slug = domain name, ≤30 chars, alphanumeric only)

Also read each local file from `local_index.json` via `read_file`.

---

## STEP 3 — Extract relevant fragments
Load `input/lecture_config.md` — all questions and key terms per question.

For each document (fetched + local): scan paragraphs.
Keep a paragraph if it contains ≥2 key terms from any single question.

For each matching paragraph:
```json
{
  "source_id": "web_003",
  "source_url": "https://...",
  "question_ids": [1, 2],
  "fragment": "paragraph text, up to 400 words",
  "section": "chapter or section heading if detectable",
  "has_formula": true,
  "formula_text": "ΔH = RT/g · ln(p₁/p₂)",
  "has_definition": true,
  "definition_term": "абсолютная топография"
}
```
Collect all fragments. No scoring at this stage — keep everything.

---

## STEP 4 — Output
Write `output/lit/extracted_fragments.json` — array of all fragment records.
Write `output/lit/fetch_log.md`:
```markdown
# Fetch Log
Date: {ISO date}
| Source | Status | Fragments extracted |
|---|---|---|
| cyberleninka.ru/... | fetched | 5 |
| elibrary.ru/...    | failed  | 0 |
| local: book.pdf    | read    | 12 |
```

Print:
```
✅ lit-fetcher complete
   Fetched: {N}/{M} URLs | Local files: {K} | Fragments extracted: {F}
   → output/lit/extracted_fragments.json
```
