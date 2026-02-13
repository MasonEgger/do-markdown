# ABOUTME: Task runner for do-markdown development workflows.
# Provides install, test, lint, format, and check commands.

install:
    uv sync

test:
    uv run pytest

test-verbose:
    uv run pytest -v

lint:
    uv run ruff check src/ tests/

format:
    uv run ruff format src/ tests/

check:
    uv run ruff check src/ tests/
    uv run ruff format --check src/ tests/
    uv run mypy --strict src/
    uv run pytest
