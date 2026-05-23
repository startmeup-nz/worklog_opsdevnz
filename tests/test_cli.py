"""Tests for CLI entry point."""

from click.testing import CliRunner
from template_opsdevnz.cli import main


def test_hello():
    runner = CliRunner()
    result = runner.invoke(main, ["hello"])
    assert result.exit_code == 0
    assert "Hello" in result.output
