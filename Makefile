.PHONY: install validate test numbering charts quality evals docx clean

install:
	python -m pip install -e '.[dev]'

validate:
	python scripts/validate_pipeline.py --mode source

test:
	pytest

numbering:
	python scripts/number_structure.py output/lecture_draft.md -o output/lecture_draft.md
	python scripts/validate_numbering.py output/lecture_draft.md

charts:
	python scripts/render_charts.py --spec output/chart_specs.json --figures output/figures_index.json

quality:
	python scripts/validate_pipeline.py --mode all --strict --report output/quality_report.json

evals:
	python evals/run_evals.py

docx:
	bash scripts/md2docx/run_md2docx.sh output/lecture_final.md -o output/lecture_final.docx
	python scripts/validate_docx.py output/lecture_final.docx --expect-formulas

clean:
	rm -rf .pytest_cache **/__pycache__ scripts/md2docx/venv
