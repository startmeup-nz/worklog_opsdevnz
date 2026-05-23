"""Tests for path resolution."""

from datetime import date

from worklog_opsdevnz.paths import resolve_path


def test_resolve_path_flat():
    config = {"worklog_dir": "docs/worklog", "structure": "flat", "suffix": "worklog"}
    path = resolve_path(config, date(2026, 5, 23))
    assert str(path) == "docs/worklog/2026-05-23-worklog.md"


def test_resolve_path_year():
    config = {"worklog_dir": "logs", "structure": "year", "suffix": "log"}
    path = resolve_path(config, date(2026, 5, 23))
    assert str(path) == "logs/2026/23-05-2026-log.md"


def test_resolve_path_year_month():
    config = {"worklog_dir": "logs", "structure": "year-month", "suffix": "ops"}
    path = resolve_path(config, date(2026, 5, 23))
    assert str(path) == "logs/2026/05/23-05-2026-ops.md"


def test_resolve_path_custom_suffix():
    config = {"structure": "year", "suffix": "retro"}
    path = resolve_path(config, date(2026, 1, 1))
    assert str(path).endswith("-retro.md")
