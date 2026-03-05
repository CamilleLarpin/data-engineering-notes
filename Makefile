.PHONY: tests lint format

tests:
	@echo "Running tests..."
	poetry run pytest -v

lint:
	poetry run ruff check .

format:
	poetry run ruff format .