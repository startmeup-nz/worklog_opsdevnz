"""Frontmatter and body generation for worklog entries."""

from typing import Any


def generate_frontmatter(
    config: dict[str, Any],
    iso_date: str,
) -> str:
    """Generate YAML frontmatter."""
    title = f"Work Log - {iso_date}"
    tags = "\n".join(f"  - {t}" for t in config.get("default_tags", []))
    author = config.get("author", "unknown")

    return f"""---
title: "{title}"
date: {iso_date}
author: {author}
tags:
{tags}
draft: false
---
"""


def generate_body(config: dict[str, Any]) -> str:
    """Generate section headers from config."""
    sections = config.get("sections", [])
    lines = []
    for section in sections:
        title = section.get("title", "")
        content = section.get("content", "")
        lines.append(f"## {title}\n")
        if content:
            lines.append(f"{content}\n")
    return "\n".join(lines)


def generate_content(
    config: dict[str, Any],
    iso_date: str,
) -> str:
    """Generate full worklog content."""
    frontmatter = generate_frontmatter(config, iso_date)
    body = generate_body(config)
    return f"{frontmatter}\n{body}"
