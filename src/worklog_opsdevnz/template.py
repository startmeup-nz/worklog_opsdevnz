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


def render_template(template_path: str, iso_date: str) -> str:
    """Render a custom Markdown template with placeholder substitution."""
    title = f"Work Log - {iso_date}"
    with open(template_path) as f:
        content = f.read()
    content = content.replace("{{DATE}}", iso_date)
    content = content.replace("{{TITLE}}", title)
    return content


def generate_content(
    config: dict[str, Any],
    iso_date: str,
) -> str:
    """Generate full worklog content.

    If a 'template' field is set in config, renders that file as the body.
    Otherwise uses the built-in sections-based body.
    Frontmatter is always generated regardless of template.
    """
    frontmatter = generate_frontmatter(config, iso_date)

    template_path = config.get("template")
    if template_path:
        body = render_template(template_path, iso_date)
    else:
        body = generate_body(config)

    return f"{frontmatter}\n{body}"
