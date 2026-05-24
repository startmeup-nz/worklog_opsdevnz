"""Tests for CLI entry point."""

from datetime import date

from click.testing import CliRunner

from worklog_opsdevnz.cli import main


def test_main_creates_file(tmp_path, monkeypatch):
    """Running with no args creates today's worklog in tmp_path."""
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Created" in result.output
    expected_leaf = (
        f"docs/worklog/{date.today().year}/{date.today():%d-%m-%Y}-worklog.md"
    )
    assert expected_leaf in result.output


def test_main_opens_existing(tmp_path, monkeypatch):
    """Running again opens the existing file."""
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main, [])
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Opening existing" in result.output


def test_main_help():
    """--help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "--editor" in result.output
