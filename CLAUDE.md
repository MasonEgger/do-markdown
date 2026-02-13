# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## First Step: Load the Python Skill

**Before writing any code**, load the `/python` skill. It contains critical rules (empty `__init__.py`, type hints, import style, docstring format, line-length) that override defaults. Failing to load it first will cause repeated corrections.

## Commands

```bash
just install          # uv sync
just test             # uv run pytest
just test-verbose     # uv run pytest -v
just lint             # uv run ruff check src/ tests/
just format           # uv run ruff format src/ tests/
just check            # Full verification: ruff check + ruff format --check + mypy --strict + pytest
```

Run a single test file: `uv run pytest tests/test_highlight.py -v`
Run a single test: `uv run pytest tests/test_highlight.py::TestInlineHighlight::test_basic_inline -v`

**`just check` must pass (all four steps) before any step is considered complete.**

## Project Overview

Python-Markdown extensions ported from DigitalOcean's `do-markdownit` (JavaScript/markdown-it). Used with MkDocs Material via `pymdownx.superfences` and `pymdownx.highlight`. The JS reference lives at `/home/mmegger/Code/MasonEgger/do-markdownit/`.

## Architecture

Each extension is a standalone Python-Markdown extension in `src/do_markdown/` with a `makeExtension(**kwargs)` entry point. Extensions are loaded by name (e.g., `do_markdown.highlight`).

**Two processor patterns:**

1. **Fence extension** (`fence.py`): Preprocessor (priority 40, runs *before* `pymdownx.superfences` at ~38) extracts directives from fence content, stores metadata as `<!-- do-fence:{JSON} -->` HTML comments. Postprocessor (priority 25) applies transformations to rendered HTML. All fence features (labels, environments, prefixes) share this single coordinated extension.

2. **Embed extensions** (youtube, codepen, twitter, instagram, slideshow, image_compare): Preprocessor (priority 20, runs *after* superfences) matches standalone `[name ...]` lines and replaces with raw HTML. Social embeds (codepen, twitter, instagram) add a Postprocessor (priority 15) for one-time script injection.

**Highlight extension** (`highlight.py`): InlineProcessor (priority 175) for regular text + Postprocessor (priority 25) for HTML-escaped `<^>` markers inside code blocks.

## Code Conventions

- `__init__.py` is **always empty** — never add anything to it
- Type hints on everything, no `Any` — mypy strict is enforced
- Absolute imports only (e.g., `from do_markdown._util import reduce_fraction`)
- RST docstrings (`:param:`, `:returns:`) on public interfaces
- `line-length = 120`, `target-version = "py314"`
- Every source file starts with a 2-line `# ABOUTME:` comment
- No trivial wrappers — call `html.escape()` directly, don't wrap stdlib functions
- HTML output must match the do-markdownit reference format (see `plan.md` HTML Output Contracts)

## Testing Approach

- TDD: write failing tests first (RED), implement (GREEN), then refactor
- Each extension has its own test file with a `_render(source)` helper that creates a `markdown.Markdown` instance with the extension loaded
- `tests/conftest.py` provides `md_with_superfences` fixture matching the real site stack
- Test **our extension logic only** — do not test Python-Markdown or pymdownx behavior
- Do not test trivial code; test behavior and outcomes

## Plan & Progress Tracking

- `plan.md`: Full implementation plan with detailed per-step prompts and HTML output contracts
- `todo.md`: Checklist tracking completion of each sub-step
- `.ai-sessions/`: Session summaries from previous work — read the most recent one for context
