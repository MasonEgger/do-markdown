# ABOUTME: Highlight extension converting <^>text<^> to <mark> tags.
# Works in regular text, inline code, and fenced code blocks.

import re
import xml.etree.ElementTree as etree

from markdown import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.postprocessors import Postprocessor

_HIGHLIGHT_PATTERN = r"<\^>(.*?)<\^>"
_ESCAPED_HIGHLIGHT_RE = re.compile(r"&lt;\^&gt;(.*?)&lt;\^&gt;")


class HighlightInlineProcessor(InlineProcessor):
    """Inline processor that converts ``<^>text<^>`` to ``<mark>text</mark>``.

    :param pattern: Regex pattern for matching highlight markers.
    :param md: The Markdown instance.
    """

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element, int, int]:  # type: ignore[override]
        """Create a ``<mark>`` element from the matched text.

        :param m: The regex match object.
        :param data: The full source string being processed.
        :returns: A tuple of (element, start, end).
        """
        el = etree.Element("mark")
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class HighlightPostprocessor(Postprocessor):
    """Postprocessor that replaces HTML-escaped ``<^>`` markers in rendered code blocks.

    Code blocks render ``<`` and ``>`` as ``&lt;`` and ``&gt;``, so the inline
    processor cannot reach them. This postprocessor catches those escaped markers
    in the final HTML and converts them to ``<mark>`` tags.
    """

    def run(self, text: str) -> str:
        """Replace escaped highlight markers with ``<mark>`` tags.

        :param text: The rendered HTML string.
        :returns: HTML with highlight markers replaced.
        """
        return _ESCAPED_HIGHLIGHT_RE.sub(r"<mark>\1</mark>", text)


class HighlightExtension(Extension):
    """Python-Markdown extension for ``<^>text<^>`` highlight syntax.

    Registers an :class:`HighlightInlineProcessor` for regular inline text and a
    :class:`HighlightPostprocessor` for code blocks where markers are HTML-escaped.
    """

    def extendMarkdown(self, md: Markdown) -> None:
        """Register the highlight processors with the Markdown instance.

        :param md: The Markdown instance to extend.
        """
        md.inlinePatterns.register(
            HighlightInlineProcessor(_HIGHLIGHT_PATTERN, md),
            "do_highlight_inline",
            175,
        )
        md.postprocessors.register(
            HighlightPostprocessor(md),
            "do_highlight_post",
            25,
        )


def makeExtension(**kwargs: str) -> HighlightExtension:
    """Entry point for Python-Markdown extension loading.

    :param kwargs: Extension configuration options.
    :returns: A configured HighlightExtension instance.
    """
    return HighlightExtension(**kwargs)
