# Evaluation fixtures

These three schema-valid configurations exercise distinct failure modes:

- scientific lecture with formulas and map interpretation;
- humanities lecture without formulas;
- long technical lecture with many independently authored sections.

For an A/B evaluation, generate complete artifacts from the same fixture on each platform, run `python evals/run_evals.py`, then compare reports with `--baseline`.
