# ABOUTME: Tests for the fence extension handling label, secondary_label, and environment directives.
# Verifies directive extraction, HTML injection, environment classes, and edge cases for code blocks.

import markdown


def render_fence(source: str, allowed_environments: list[str] | None = None) -> str:
    """Render source with superfences, highlight, and fence extensions loaded."""
    extension_configs: dict[str, dict[str, object]] = {"pymdownx.highlight": {"pygments_lang_class": True}}
    if allowed_environments is not None:
        extension_configs["do_markdown.fence"] = {"allowed_environments": allowed_environments}
    md = markdown.Markdown(
        extensions=["pymdownx.superfences", "pymdownx.highlight", "do_markdown.fence"],
        extension_configs=extension_configs,
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


class TestEnvironmentBasic:
    def test_environment_class_on_pre(self) -> None:
        source = "```\n[environment local]\nssh root@server\n```"
        result = render_fence(source)
        assert "environment-local" in result

    def test_environment_directive_stripped(self) -> None:
        source = "```\n[environment local]\nssh root@server\n```"
        result = render_fence(source)
        assert "[environment local]" not in result


class TestEnvironmentAllowedList:
    def test_allowed_environment_applied(self) -> None:
        source = "```\n[environment local]\ncode\n```"
        result = render_fence(source, allowed_environments=["local", "staging", "production"])
        assert "environment-local" in result

    def test_disallowed_environment_not_applied(self) -> None:
        source = "```\n[environment unknown]\ncode\n```"
        result = render_fence(source, allowed_environments=["local", "staging", "production"])
        assert "environment-unknown" not in result
        assert "[environment unknown]" in result

    def test_empty_allowed_list_allows_all(self) -> None:
        source = "```\n[environment custom]\ncode\n```"
        result = render_fence(source, allowed_environments=[])
        assert "environment-custom" in result


class TestEnvironmentWithLabel:
    def test_environment_and_label_together(self) -> None:
        source = "```\n[environment local]\n[label server.sh]\ncode\n```"
        result = render_fence(source)
        assert "environment-local" in result
        assert '<div class="code-label" title="server.sh">server.sh</div>' in result

    def test_environment_and_secondary_label_together(self) -> None:
        source = "```\n[environment second]\n[secondary_label Output]\ncode\n```"
        result = render_fence(source)
        assert "environment-second" in result
        assert '<div class="secondary-code-label" title="Output">Output</div>' in result


class TestEnvironmentVariants:
    def test_second_environment(self) -> None:
        source = "```\n[environment second]\ncode\n```"
        result = render_fence(source)
        assert "environment-second" in result

    def test_third_environment(self) -> None:
        source = "```\n[environment third]\ncode\n```"
        result = render_fence(source)
        assert "environment-third" in result

    def test_directive_order_environment_after_label(self) -> None:
        source = "```\n[label server.sh]\n[environment local]\ncode\n```"
        result = render_fence(source)
        assert "environment-local" in result
        assert '<div class="code-label" title="server.sh">server.sh</div>' in result
