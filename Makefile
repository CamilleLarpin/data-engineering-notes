.PHONY: tests lint format enrich

tests:
	@echo "Running tests..."
	poetry run pytest -v

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

enrich:
	poetry run python src/scripts/enrich.py $(dir)