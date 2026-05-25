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


def test_main_version():
    """--version prints the installed version."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "worklog-opsdevnz, version" in result.output
    # Extract and verify it's a non-empty version string
    version_str = result.output.strip().split(", version ")[-1]
    assert version_str


def test_main_editor_from_config(tmp_path, monkeypatch):
    """Editor in worklog.toml is resolved before $VISUAL/$EDITOR."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "worklog.toml").write_text('editor = "fake-editor-test"\n')
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    # config-based editor picked up but not found in PATH
    assert "Editor 'fake-editor-test' not found" in result.output


def test_main_editor_cli_overrides_config(tmp_path, monkeypatch):
    """-e flag overrides the editor set in worklog.toml."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "worklog.toml").write_text('editor = "fake-editor-test"\n')
    runner = CliRunner()
    result = runner.invoke(main, ["-e", "override-editor-test"])
    assert result.exit_code == 0
    # CLI override takes priority over config
    assert "Editor 'override-editor-test' not found" in result.output
