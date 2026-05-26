"""Configuration discovery and loading for worklog-opsdevnz."""

import os
import sys
import tomllib
from pathlib import Path
from typing import Any

DEFAULT_CONFIG: dict[str, Any] = {
    "worklog_dir": "docs/worklog",
    "structure": "year",
    "suffix": "worklog",
    "author": os.environ.get("USER", "unknown"),
    "default_tags": ["internal", "log"],
    "sections": [
        {"title": "Focus for Today", "content": ""},
        {"title": "Completed", "content": ""},
        {"title": "Notes & Reflections", "content": ""},
        {"title": "Related", "content": ""},
        {"title": "Next", "content": ""},
    ],
}


def find_config(start: Path | None = None) -> Path | None:
    """Search for worklog.toml or worklog.yaml from start up to root."""
    if start is None:
        start = Path.cwd()
    candidates = [start] + list(start.parents)
    for candidate in candidates:
        for name in ("worklog.toml", "worklog.yaml", "worklog.yml"):
            path = candidate / name
            if path.exists():
                return path
    return None


def load_config(path: Path) -> dict[str, Any]:
    """Load config from TOML or YAML file."""
    if path.suffix == ".toml":
        with open(path, "rb") as f:
            return tomllib.load(f)
    else:
        try:
            import yaml  # type: ignore[import-untyped]
        except ImportError:
            print("Error: PyYAML required for .yaml config", file=sys.stderr)
            sys.exit(1)
        with open(path) as f:
            return yaml.safe_load(f) or {}


def merge_config(
    file_config: dict[str, Any], defaults: dict[str, Any]
) -> dict[str, Any]:
    """Merge file config over defaults."""
    merged = dict(defaults)
    merged.update(file_config)
    return merged


def get_config() -> dict[str, Any]:
    """Discover and load config, falling back to defaults."""
    config_path = find_config()
    if config_path:
        merged = merge_config(load_config(config_path), DEFAULT_CONFIG)
        worklog_dir = merged["worklog_dir"]
        if not Path(worklog_dir).is_absolute():
            merged["worklog_dir"] = str(config_path.parent / worklog_dir)
        return merged
    return dict(DEFAULT_CONFIG)
