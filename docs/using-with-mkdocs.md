# Using with MkDocs

do-markdown is a set of Python-Markdown extensions, so it works in any Python-Markdown consumer.
This page covers the MkDocs case. Each extension page shows the plain Python-Markdown usage.

To use the extensions in a MkDocs site, add them under `markdown_extensions` in `mkdocs.yml`.
List only the ones you need.

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

The fence extension expects `pymdownx.superfences` and `pymdownx.highlight` to be loaded too.
Without them the fence preprocessor still extracts directives, but the code-block HTML may not match what the postprocessor rewrites.

!!! warning "MkDocs 2.0 Compatibility"
    MkDocs 2.0 removes the plugin system and rewrites the theming architecture, breaking all existing plugins and themes including Material for MkDocs. There is no migration path. This project pins **MkDocs 1.x** (`mkdocs>=1.6,<2`).
