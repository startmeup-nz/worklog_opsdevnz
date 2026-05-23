"""Path resolution for worklog files."""

from datetime import date
from pathlib import Path
from typing import Any


def resolve_path(
    config: dict[str, Any],
    entry_date: date,
) -> Path:
    """Compute the target file path based on config structure."""
    base = Path(config.get("worklog_dir", "docs/worklog"))
    structure = config.get("structure", "year")
    suffix = config.get("suffix", "worklog")

    if structure == "flat":
        filename = f"{entry_date.isoformat()}-{suffix}.md"
        return base / filename
    elif structure == "year-month":
        year = entry_date.strftime("%Y")
        month = entry_date.strftime("%m")
        filename = f"{entry_date.strftime('%d-%m-%Y')}-{suffix}.md"
        return base / year / month / filename
    else:  # "year" (default)
        year = entry_date.strftime("%Y")
        filename = f"{entry_date.strftime('%d-%m-%Y')}-{suffix}.md"
        return base / year / filename
