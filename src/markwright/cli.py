# ABOUTME: Command-line entry point for the mw markwright pipeline tool.
# Builds the argparse parser and dispatches the list subcommand; --version reports the package version.

from __future__ import annotations

import argparse
from importlib.metadata import version

from markwright import registry


def _package_version() -> str:
    """Return the installed markwright distribution version.

    :returns: The version string for the ``markwright`` distribution.
    """
    return version("markwright")


def build_parser() -> argparse.ArgumentParser:
    """Construct the ``mw`` argument parser with its subcommands.

    :returns: A parser exposing ``--version`` and the ``list`` subcommand.
    """
    parser = argparse.ArgumentParser(prog="mw", description="markwright Markdown pipeline CLI.")
    parser.add_argument("--version", action="version", version=f"mw {_package_version()}")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List registered extensions and the stages each provides.")
    return parser


def _run_list() -> int:
    """Print each registered extension and its available stages.

    :returns: Always ``0``.
    """
    for name, stages in registry.describe():
        print(f"{name}: {', '.join(stages)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse ``argv`` and dispatch to the selected subcommand.

    :param argv: Argument vector, or ``None`` to read from ``sys.argv``.
    :returns: Process exit code (``0`` success, ``2`` usage error).
    """
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exit_error:
        return exit_error.code if isinstance(exit_error.code, int) else 2
    if args.command == "list":
        return _run_list()
    parser.print_usage()
    return 2
