"""Tests for frontmatter and body generation."""

from worklog_opsdevnz.template import generate_frontmatter, generate_body, generate_content


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
