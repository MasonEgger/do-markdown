# ABOUTME: Task runner for do-markdown development workflows.
# Provides install, test, lint, format, typecheck, and check commands.

install:
    uv sync

test:
    uv run pytest --cov=do_markdown --cov-report=term-missing

test-verbose:
    uv run pytest -v --cov=do_markdown --cov-report=term-missing

lint:
    uv run ruff check src/ tests/
    uv run ruff format --check src/ tests/

format:
    uv run ruff format src/ tests/

typecheck:
    uv run mypy --strict src/

check: test lint typecheck
