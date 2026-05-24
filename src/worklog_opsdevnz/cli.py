"""CLI entry point for worklog-opsdevnz."""

import shutil
import subprocess
from datetime import date
from pathlib import Path

import click

from worklog_opsdevnz.config import get_config
from worklog_opsdevnz.paths import resolve_path
from worklog_opsdevnz.template import generate_content


@click.command()
@click.option(
    "-e",
    "--editor",
    default=None,
    help="Override the editor command (default: $VISUAL or $EDITOR).",
)
def main(editor: str | None) -> None:
    """Create or open today's worklog entry."""
    entry_date = date.today()

    config = get_config()
    target = resolve_path(config, entry_date)
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        print(f"Opening existing worklog: {target}")
    else:
        content = generate_content(config, entry_date.isoformat())
        target.write_text(content)
        print(f"Created: {target}")

    _open_editor(target, editor)


def _open_editor(path: str | Path, override: str | None = None) -> None:
    """Open the file in the configured editor, or print the path."""
    editor = _resolve_editor(override)
    if editor:
        editor_cmd = shutil.which(editor)
        if editor_cmd:
            # fmt: off
            subprocess.run([editor_cmd, str(path)])
            # fmt: on
        else:
            print(f"Editor '{editor}' not found. Path: {path}")
    else:
        print(f"No editor configured. Path: {path}")


def _resolve_editor(override: str | None = None) -> str | None:
    """Resolve editor from CLI override, $VISUAL, or $EDITOR."""
    import os

    for candidate in (override, os.environ.get("VISUAL"), os.environ.get("EDITOR")):
        if candidate:
            return candidate
    return None


if __name__ == "__main__":
    main()
