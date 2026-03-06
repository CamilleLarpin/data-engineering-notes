.PHONY: tests lint format enrich quiz docker-build docker-run

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

docker-build:
	docker build -t data-engineering-notes-quiz .

docker-run:
	docker run --env-file .env data-engineering-notes-quiz