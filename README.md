# WorkLog OpsDev.NZ

**Status:** v0.0.1 — Planning / Staging

Configurable CLI tool for creating and managing dated development worklogs.
Generates Markdown entries with YAML frontmatter from per-project templates.

## Problem

Across multiple projects (outcome-engineering, opsdev.nz, floydwilde.studio) we
kept reinventing the same pattern: a script that creates a dated Markdown file
from a template, with frontmatter for date, author, tags, and draft status.
Each implementation had slightly different directory structures, section headers,
and filenames. The core concept was always the same.

## Solution

`worklog-opsdevnz` formalises this pattern into a single published module:

- **Per-project config** — `worklog.toml` controls directory structure, sections,
  author, tags, and filename patterns
- **Three structure modes** — `flat`, `year`, or `year-month` directory layouts
- **YAML frontmatter** — date, title, author, tags, draft status
- **Configurable sections** — each project defines its own section headers
- **Editor integration** — opens new entries in `$VISUAL` / `$EDITOR`
- **List existing entries** — browse worklogs with `--list`

## Quick Start

```bash
# Install (development)
uv pip install -e modules/worklog_opsdevnz

# Create today's worklog
worklog-opsdevnz create

# Create for a specific date with title
worklog-opsdevnz create -d 2026-04-28 -t "Module Scaffolding"

# List existing entries
worklog-opsdevnz list

# Scaffold a worklog.toml config
worklog-opsdevnz init
```

## Configuration

Each project gets a `worklog.toml` at its root:

```toml
worklog_dir = "docs/worklog"
structure = "flat"           # "flat", "year", or "year-month"
filename_pattern = "{date}-{slug}.md"
author = "OpsDev.nz Collective"
default_tags = ["worklog", "opsdevnz"]

[[sections]]
title = "🎯 Focus"
content = ""

[[sections]]
title = "✅ Completed"
content = ""

[[sections]]
title = "🧠 Notes"
content = ""

[[sections]]
title = "⏳ Next"
content = ""
```

## Scope

**WorkLog DOES:**
- Create dated Markdown worklog entries from templates
- Per-project configuration via `worklog.toml`
- List and browse existing entries
- Open entries in configured editor

**WorkLog DOES NOT (out of scope for 0.0.1):**
- Zensical blog integration (see design doc)
- Auto-generated index pages
- Retro template support (planned for 0.1.0)
- Time tracking / timesheet aggregation

## Requirements

- Python 3.12+
- See [pyproject.toml](pyproject.toml) for full dependencies

## Related

- [Functional Requirements](docs/specs/README.md)
- [Design Decisions](docs/design/README.md)
- [User Stories](docs/stories/README.md)

---

**Last Updated:** 2026-05-23
**Status:** Development (migrated to module template)
**Maintainer:** OpsDev.nz Collective
