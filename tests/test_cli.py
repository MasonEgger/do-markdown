# ABOUTME: Tests for the mw CLI entry point: --version, list, and usage errors.
# Drives main() with explicit argv and captures stdout/stderr via capsys.

from __future__ import annotations

from importlib.metadata import version as package_version

import pytest

from markwright.cli import main


class TestCliVersion:
    """Tests for the top-level --version action."""

    def test_version_returns_zero_and_prints_package_version(self, capsys: pytest.CaptureFixture[str]) -> None:
        exit_code = main(["--version"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert package_version("markwright") in captured.out


class TestCliList:
    """Tests for the list subcommand."""

    def test_list_returns_zero_and_reports_each_extension_with_stages(self, capsys: pytest.CaptureFixture[str]) -> None:
        exit_code = main(["list"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert "youtube" in captured.out
        assert "fence" in captured.out
        # A pre-only extension and a pre+post extension are labeled differently.
        assert "youtube: pre" in captured.out
        assert "youtube: pre, post" not in captured.out
        assert "fence: pre, post" in captured.out


class TestCliUsageError:
    """Tests for argparse usage errors."""

    def test_unknown_subcommand_returns_two(self, capsys: pytest.CaptureFixture[str]) -> None:
        exit_code = main(["bogus"])
        assert exit_code == 2
