# ABOUTME: Tests for the highlight extension converting <^>text<^> to <mark> tags.
# Covers inline text, inline code, fenced code blocks, and edge cases.

import markdown


def _render(source: str) -> str:
    """Render Markdown source with the highlight extension loaded."""
    md = markdown.Markdown(extensions=["do_markdown.highlight"])
    return md.convert(source)


def _render_with_superfences(source: str) -> str:
    """Render with highlight + superfences, matching the real site stack."""
    md = markdown.Markdown(
        extensions=["pymdownx.superfences", "pymdownx.highlight", "do_markdown.highlight"],
        extension_configs={"pymdownx.highlight": {"pygments_lang_class": True}},
    )
    return md.convert(source)


class TestInlineHighlight:
    """Test <^>...<^> in regular inline text."""

    def test_basic_inline(self) -> None:
        result = _render("This is a <^>variable<^>")
        assert "<mark>variable</mark>" in result

    def test_multiple_highlights_same_line(self) -> None:
        result = _render("<^>a<^> and <^>b<^>")
        assert "<mark>a</mark>" in result
        assert "<mark>b</mark>" in result

    def test_highlight_in_paragraph(self) -> None:
        result = _render("Before <^>middle<^> after")
        assert "<mark>middle</mark>" in result
        assert "Before" in result
        assert "after" in result


class TestInlineCodeHighlight:
    """Test <^>...<^> inside inline code spans."""

    def test_inline_code_highlight(self) -> None:
        result = _render("`code <^>var<^>`")
        assert "<mark>var</mark>" in result
        assert "<code>" in result


class TestFencedCodeHighlight:
    """Test <^>...<^> inside fenced code blocks."""

    def test_fenced_code_highlight(self) -> None:
        source = "```\nhello\n<^>highlighted<^>\n```"
        result = _render_with_superfences(source)
        assert "<mark>highlighted</mark>" in result
        assert "<pre" in result

    def test_fenced_code_with_language(self) -> None:
        source = "```python\nprint(<^>value<^>)\n```"
        result = _render_with_superfences(source)
        assert "<mark>" in result


class TestEdgeCases:
    """Test edge cases and non-matching inputs."""

    def test_unclosed_marker_no_match(self) -> None:
        result = _render("<^>unclosed")
        assert "<mark>" not in result

    def test_empty_highlight_produces_empty_mark(self) -> None:
        """The JS reference regex (.*?) matches empty, producing <mark></mark>."""
        result = _render("<^><^>")
        assert "<mark></mark>" in result

    def test_no_markers_passthrough(self) -> None:
        result = _render("plain text with no markers")
        assert "<mark>" not in result
        assert "plain text with no markers" in result
