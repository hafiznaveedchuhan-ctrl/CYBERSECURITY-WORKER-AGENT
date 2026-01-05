# MCP Server Dockerfile - Python 3.11 + FastMCP
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --only main

# Copy application code
COPY src ./src

# Create non-root user
RUN addgroup --system --gid 1001 python && \
    adduser --system --uid 1001 --gid 1001 python && \
    chown -R python:python /app

USER python

EXPOSE 8001

CMD ["python", "-m", "src.main"]
