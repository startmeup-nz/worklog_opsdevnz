"""Tests for frontmatter and body generation."""

import pytest

from worklog_opsdevnz.template import (
    generate_frontmatter,
    generate_body,
    generate_content,
    render_template,
)


def test_generate_frontmatter():
    config = {
        "author": "Test Author",
        "default_tags": ["internal", "test"],
    }
    fm = generate_frontmatter(config, "2026-05-23")
    assert "title: " in fm
    assert "Work Log - 2026-05-23" in fm
    assert "date: 2026-05-23" in fm
    assert "author: Test Author" in fm
    assert "  - internal" in fm
    assert "  - test" in fm
    assert "draft: false" in fm
    assert fm.startswith("---")
    assert fm.strip().endswith("---")


def test_generate_body_with_sections():
    config = {
        "sections": [
            {"title": "Focus", "content": ""},
            {"title": "Notes", "content": "some note"},
        ]
    }
    body = generate_body(config)
    assert "## Focus" in body
    assert "## Notes" in body
    assert "some note" in body


def test_generate_content_full():
    config = {
        "author": "opsdev",
        "default_tags": ["log"],
        "sections": [{"title": "Today", "content": ""}],
    }
    content = generate_content(config, "2026-05-23")
    assert content.startswith("---")
    assert "Work Log - 2026-05-23" in content
    assert "## Today" in content


def test_render_template_with_placeholders(tmp_path):
    template = tmp_path / "my-template.md"
    template.write_text("# {{TITLE}}\n\nDate: {{DATE}}\n\nFree-form notes.")

    result = render_template(str(template), "2026-05-26")
    assert "# Work Log - 2026-05-26" in result
    assert "Date: 2026-05-26" in result
    assert "Free-form notes." in result
    assert "{{DATE}}" not in result
    assert "{{TITLE}}" not in result


def test_render_template_file_not_found():
    with pytest.raises(FileNotFoundError):
        render_template("/nonexistent/template.md", "2026-05-26")


def test_generate_content_with_template(tmp_path):
    template = tmp_path / "my-template.md"
    template.write_text("# {{TITLE}}\n\nDate: {{DATE}}")

    config = {
        "author": "opsdev",
        "default_tags": ["log"],
        "template": str(template),
    }
    content = generate_content(config, "2026-05-26")
    assert content.startswith("---")
    assert "Work Log - 2026-05-26" in content
    assert "author: opsdev" in content
    assert "# Work Log - 2026-05-26" in content
    assert "Date: 2026-05-26" in content
    # Frontmatter generated, body from template — not sections
    assert "## " not in content.split("---\n")[2] if "---\n" in content else True


def test_generate_content_without_template():
    """No template field → built-in sections body, unchanged behaviour."""
    config = {
        "author": "opsdev",
        "default_tags": ["log"],
        "sections": [{"title": "Today", "content": ""}],
    }
    content = generate_content(config, "2026-05-26")
    assert "## Today" in content
