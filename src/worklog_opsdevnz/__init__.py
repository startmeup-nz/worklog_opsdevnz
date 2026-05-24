"""worklog-opsdevnz — Configurable worklog management CLI."""

from importlib import metadata

try:
    __version__ = metadata.version("worklog-opsdevnz")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0+local"
