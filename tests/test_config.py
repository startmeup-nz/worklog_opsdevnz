"""Tests for config discovery and loading."""

from pathlib import Path

from worklog_opsdevnz.config import find_config, get_config, merge_config


def test_find_config_toml(tmp_path: Path, tmp_path_factory: Path):
    """Search finds config in start dir; returns None from a path with no config above it."""
    empty = tmp_path_factory.mktemp("empty")
    assert find_config(start=empty) is None

    (tmp_path / "worklog.toml").write_text('author = "test-user"')
    found = find_config(start=tmp_path)
    assert found is not None
    assert found.name == "worklog.toml"


def test_find_config_walks_up(tmp_path: Path):
    (tmp_path / "worklog.toml").write_text('author = "test-user"')
    sub = tmp_path / "sub" / "deep"
    sub.mkdir(parents=True)

    found = find_config(start=sub)
    assert found is not None
    assert found.parent == tmp_path


def test_find_config_not_found(tmp_path: Path):
    assert find_config(start=tmp_path) is None


def test_merge_config_overrides():
    defaults = {"author": "unknown", "suffix": "worklog"}
    file_cfg = {"author": "john"}
    merged = merge_config(file_cfg, defaults)
    assert merged["author"] == "john"
    assert merged["suffix"] == "worklog"


def test_get_config_defaults(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config = get_config()
    assert config["structure"] == "year"
    assert config["suffix"] == "worklog"
    assert config["worklog_dir"] == "docs/worklog"
    assert len(config["sections"]) == 5


def test_get_config_from_file(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "worklog.toml").write_text('author = "Test Author"\nstructure = "flat"')
    config = get_config()
    assert config["author"] == "Test Author"
    assert config["structure"] == "flat"
    assert config["suffix"] == "worklog"  # default preserved
    # worklog_dir defaults to "docs/worklog" and should be resolved to absolute
    assert config["worklog_dir"] == str(tmp_path / "docs/worklog")


def test_get_config_worklog_dir_resolved_relative_to_config(tmp_path: Path, monkeypatch):
    """worklog_dir is resolved against config file directory, not CWD."""
    (tmp_path / "worklog.toml").write_text('worklog_dir = "my/logs"')
    sub = tmp_path / "sub" / "deep"
    sub.mkdir(parents=True)
    monkeypatch.chdir(sub)

    config = get_config()
    assert config["worklog_dir"] == str(tmp_path / "my/logs")
