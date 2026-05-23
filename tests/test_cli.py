"""Tests for CLI entry point."""

from click.testing import CliRunner
from worklog_opsdevnz.cli import main


def test_hello():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "under development" in result.output
