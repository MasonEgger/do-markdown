# do-markdown

A Python port of DigitalOcean's [`do-markdownit`](https://github.com/digitalocean/do-markdownit) JavaScript library. These are [Python-Markdown](https://python-markdown.github.io/) extensions that can be used with any tool built on Python-Markdown, including [MkDocs](https://www.mkdocs.org/).

The original `do-markdownit` is licensed under the [Apache License 2.0](https://github.com/digitalocean/do-markdownit/blob/master/LICENSE). This port maintains compatibility with the original HTML output format.

## Features

- **Highlight** — `<^>text<^>` syntax for marking text, even inside code blocks
- **Fence** — Labels, secondary labels, environment classes, and line prefixes for code blocks
- **YouTube** — Responsive iframe embeds
- **CodePen** — Embedded pens with theme, tab, and layout options
- **Twitter** — Tweet embeds with theme and alignment options
- **Instagram** — Post embeds with caption and alignment options
- **Slideshow** — Image slideshows with navigation arrows
- **Image Compare** — Side-by-side image comparison with a slider

## Installation

```bash
uv add do-markdown
```

Or install from a local path:

```bash
uv add --editable ../do-markdown
```

!!! warning "MkDocs 2.0 Compatibility"
    MkDocs 2.0 removes the plugin system and rewrites the theming architecture, breaking all existing plugins and themes including Material for MkDocs. There is no migration path. This project pins **MkDocs 1.x** (`mkdocs>=1.6,<2`).

## Usage

### With MkDocs

Add the extensions to your `mkdocs.yml`:

```yaml
markdown_extensions:
  - pymdownx.superfences
  - pymdownx.highlight:
      pygments_lang_class: true
  - do_markdown.highlight
  - do_markdown.fence:
      allowed_environments:
        - local
        - second
        - third
        - fourth
        - fifth
  - do_markdown.youtube
  - do_markdown.codepen
  - do_markdown.twitter
  - do_markdown.instagram
  - do_markdown.slideshow
  - do_markdown.image_compare
```

Then use the custom syntax in your Markdown files. See each extension's documentation for syntax details and examples.

### Standalone (without MkDocs)

These extensions work with Python-Markdown directly. You can use them in any Python application — a Flask app, a CLI tool, a static site generator, or a simple script:

```python
import markdown

md = markdown.Markdown(extensions=[
    "pymdownx.superfences",
    "pymdownx.highlight",
    "do_markdown.highlight",
    "do_markdown.fence",
    "do_markdown.youtube",
    "do_markdown.codepen",
    "do_markdown.twitter",
    "do_markdown.instagram",
    "do_markdown.slideshow",
    "do_markdown.image_compare",
])

source = """
```command
[label deploy.sh]
ssh root@server
apt update
```
"""

html = md.convert(source)
print(html)
```

You can also load individual extensions if you only need specific features:

```python
import markdown

# Just the highlight extension
md = markdown.Markdown(extensions=["do_markdown.highlight"])
html = md.convert("This has a <^>highlighted word<^> in it.")

# Just YouTube embeds
md = markdown.Markdown(extensions=["do_markdown.youtube"])
html = md.convert("[youtube dQw4w9WgXcQ]")
```

!!! note
    The fence extension should be used alongside `pymdownx.superfences` and `pymdownx.highlight` for proper code block rendering. Without them, the fence preprocessor will still extract directives, but the code block HTML structure may differ from what the postprocessor expects.

## Architecture

Each extension is a standalone Python-Markdown extension loaded by name (e.g., `do_markdown.highlight`). The extensions use three processor patterns:

1. **Fence** — Preprocessor (priority 40) runs *before* `pymdownx.superfences` to extract directives. Postprocessor (priority 25) injects labels, classes, and prefix markup into rendered HTML.

2. **Embeds** — Preprocessors (priority 20) run *after* superfences, matching standalone `[name ...]` lines. Social embeds add a Postprocessor (priority 15) for one-time script injection.

3. **Highlight** — InlineProcessor (priority 175) for regular text, plus a Postprocessor (priority 25) for `<^>` markers inside code blocks where the delimiters are HTML-escaped.

## License

This project is a port of [do-markdownit](https://github.com/digitalocean/do-markdownit) by DigitalOcean, which is licensed under the Apache License 2.0. See the [NOTICE](https://github.com/MasonEgger/do-markdown/blob/main/NOTICE) file for attribution details.
