# ABOUTME: Task runner for markwright development workflows.
# Provides the default help menu plus install, test, lint, docs, and check commands.

# Show this help menu (run `just` with no arguments)
default:
    @just --list

# Install dependencies
install:
    uv sync

# Run the unit suite with branch coverage, failing under 100% (excludes integration)
test:
    uv run pytest -m "not integration" --cov=markwright --cov-branch --cov-fail-under=100 --cov-report=term-missing

# Run the unit suite verbosely with branch coverage, failing under 100%
test-verbose:
    uv run pytest -v -m "not integration" --cov=markwright --cov-branch --cov-fail-under=100 --cov-report=term-missing

# Run the end-to-end integration tests (requires hugo on PATH)
test-integration:
    uv run pytest tests/integration -m integration -v

# Check lint and formatting
lint:
    uv run ruff check src/ tests/
    uv run ruff format --check src/ tests/

# Auto-format the code
format:
    uv run ruff format src/ tests/

# Type-check with mypy strict
typecheck:
    uv run mypy --strict src/

# Run tests, lint, and type-check
check: test lint typecheck

# Build the docs site (strict mode)
docs-build:
    uv run mkdocs build --strict

# Serve the docs site at localhost:8000
docs-serve:
    uv run mkdocs serve

# Serve the docs site on the Tailscale IP (reachable across your tailnet)
docs-serve-tailnet:
    uv run mkdocs serve -a $(tailscale ip -4):8000
