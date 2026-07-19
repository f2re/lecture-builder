# Evaluation fixtures

The fixtures exercise three lecture modes with canonical lecture-derived numbering:

- scientific lecture with formulas, source-bound/schematic graphs and methodical inserts;
- humanities lecture without formulas but with mnemonics, examples and self-checks;
- long technical lecture with many independently authored `L.Q` sections.

Every question is numbered from `lecture_number`; for example lecture 17 uses `17.1`, `17.2`, while generated subsections use `17.1.1`, `17.1.2`. Formula and figure counters remain global to the lecture.

For an A/B evaluation, generate complete artifacts from the same fixture on each platform, run `python evals/run_evals.py`, then compare reports with `--baseline`.
