.PHONY: install validate test quality evals docx clean

install:
	python -m pip install -e '.[dev]'

validate:
	python scripts/validate_pipeline.py --mode source

test:
	pytest

quality:
	python scripts/validate_pipeline.py --mode all --strict --report output/quality_report.json

evals:
	python evals/run_evals.py

docx:
	bash scripts/md2docx/run_md2docx.sh output/lecture_final.md -o output/lecture_final.docx
	python scripts/validate_docx.py output/lecture_final.docx --expect-formulas

clean:
	rm -rf .pytest_cache **/__pycache__ scripts/md2docx/venv
