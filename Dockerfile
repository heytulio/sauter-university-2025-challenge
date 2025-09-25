FROM python:3.11-slim

ENV POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/


RUN poetry install --only main --no-root

COPY . /app


EXPOSE 8080

CMD ["sh", "-c", "poetry run uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
