.PHONY: tests lint format enrich quiz

tests:
	@echo "Running tests..."
	poetry run pytest -v

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

enrich:
	poetry run python src/scripts/enrich.py $(dir)

quiz:
	poetry run python src/scripts/quiz.py