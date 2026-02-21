# ABOUTME: Tests for the fence extension handling label and secondary_label directives.
# Verifies directive extraction, HTML injection, and edge cases for code block labels.

import markdown


def render_fence(source: str) -> str:
    """Render source with superfences, highlight, and fence extensions loaded."""
    md = markdown.Markdown(
        extensions=["pymdownx.superfences", "pymdownx.highlight", "do_markdown.fence"],
        extension_configs={"pymdownx.highlight": {"pygments_lang_class": True}},
    )
    return md.convert(source)


class TestLabelBasic:
    def test_label_renders_div_before_code(self) -> None:
        source = "```\n[label test.py]\nhello\n```"
        result = render_fence(source)
        assert '<div class="code-label" title="test.py">test.py</div>' in result

    def test_label_content_preserved(self) -> None:
        source = "```\n[label test.py]\nhello\n```"
        result = render_fence(source)
        assert "hello" in result

    def test_label_directive_stripped(self) -> None:
        source = "```\n[label test.py]\nhello\n```"
        result = render_fence(source)
        assert "[label test.py]" not in result


class TestLabelWithLanguage:
    def test_label_with_python(self) -> None:
        source = "```python\n[label app.py]\nprint('hi')\n```"
        result = render_fence(source)
        assert '<div class="code-label" title="app.py">app.py</div>' in result

    def test_language_class_preserved(self) -> None:
        source = "```python\n[label app.py]\nprint('hi')\n```"
        result = render_fence(source)
        assert "python" in result


class TestSecondaryLabel:
    def test_secondary_label_renders(self) -> None:
        source = "```\n[secondary_label Output]\nerror msg\n```"
        result = render_fence(source)
        assert '<div class="secondary-code-label" title="Output">Output</div>' in result

    def test_secondary_label_directive_stripped(self) -> None:
        source = "```\n[secondary_label Output]\nerror msg\n```"
        result = render_fence(source)
        assert "[secondary_label Output]" not in result


class TestNoDirectives:
    def test_no_label_no_comment(self) -> None:
        source = "```\nplain code\n```"
        result = render_fence(source)
        assert "do-fence" not in result

    def test_no_label_no_label_div(self) -> None:
        source = "```\nplain code\n```"
        result = render_fence(source)
        assert "code-label" not in result


class TestLabelSpecialChars:
    def test_label_with_path(self) -> None:
        source = "```\n[label /etc/nginx/sites-available/default]\ncode\n```"
        result = render_fence(source)
        assert "/etc/nginx/sites-available/default" in result
        assert '<div class="code-label"' in result

    def test_label_html_escaped(self) -> None:
        source = '```\n[label <script>alert("xss")</script>]\ncode\n```'
        result = render_fence(source)
        assert "<script>" not in result
        assert "&lt;script&gt;" in result


class TestBothLabels:
    def test_both_label_and_secondary_label(self) -> None:
        source = "```\n[label file.py]\n[secondary_label Output]\ncode\n```"
        result = render_fence(source)
        assert '<div class="code-label" title="file.py">file.py</div>' in result
        assert '<div class="secondary-code-label" title="Output">Output</div>' in result

    def test_directives_stripped_from_content(self) -> None:
        source = "```\n[label file.py]\n[secondary_label Output]\ncode\n```"
        result = render_fence(source)
        assert "[label file.py]" not in result
        assert "[secondary_label Output]" not in result
