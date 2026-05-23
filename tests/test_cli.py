"""Tests for CLI entry point."""

from worklog_opsdevnz.cli import main


def test_main_runs():
    result = main()
    assert result is None  # main() returns None, prints to stdout


def test_version(capsys):
    from worklog_opsdevnz import __version__
    assert __version__ == "0.0.1"
