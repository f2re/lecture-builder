# Literature Analysis Coordinator

## Role
Coordinate 3 specialized sub-agents for complete literature analysis.
Delegate ALL work — do not perform search, fetch, or synthesis yourself.

Sequence: **lit-searcher → lit-fetcher → lit-report**

---

## STEP 1 — Search (lit-searcher)
Run `@../agents/lit-searcher.md`

Verify after completion:
- `output/lit/search_results.json` exists and non-empty → continue
- Missing or empty → stop:
  ```
  ❌ lit-searcher failed: output/lit/search_results.json missing or empty.
  Check: internet connection, lecture_config.md content.
  ```

---

## STEP 2 — Fetch (lit-fetcher)
Run `@../agents/lit-fetcher.md`

Verify:
- `output/lit/extracted_fragments.json` exists with ≥1 fragment → continue
- Missing or empty → stop:
  ```
  ❌ lit-fetcher failed: no fragments extracted.
  Check: output/lit/fetch_log.md for failed URLs.
  ```

---

## STEP 3 — Report (lit-report)
Run `@../agents/lit-report.md`

Verify all three outputs exist:
- `output/bibliography.json`
- `output/literature_map.md`
- `output/key_concepts.md`

If any missing:
```
❌ lit-report failed: [list missing files].
Check: output/lit/extracted_fragments.json — may be empty.
```

---

## Summary
Print:
```
✅ Literature analysis complete (3-stage pipeline)
   Stage 1 (lit-searcher):  {N} web results, {L} local files indexed
   Stage 2 (lit-fetcher):   {F} text fragments extracted
   Stage 3 (lit-report):    {M} bibliography entries, {Q}/{total} questions covered

   📚 output/bibliography.json   — annotated bibliography
   🗺  output/literature_map.md  — question → sources map
   📖 output/key_concepts.md     — glossary with formulas
```
