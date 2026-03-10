FROM python:3.12-slim

WORKDIR /app

# Install Poetry (pinned for reproducibility)
RUN pip install --no-cache-dir poetry==2.3.2Ok. 

# Install production dependencies only
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Copy project files
COPY src/ ./src/
COPY modules/ ./modules/
COPY errors-and-lessons/ ./errors-and-lessons/

CMD ["python", "src/scripts/quiz.py"]
