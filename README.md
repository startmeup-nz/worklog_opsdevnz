# WorkLog OpsDev.NZ

**Status:** Development — see pyproject.toml for version

Configurable CLI tool for creating and managing dated development worklogs.
Generates Markdown entries with YAML frontmatter from per-project templates.

## Problem

Across multiple projects we kept reinventing the same pattern: a script that
creates a dated Markdown file from a template, with frontmatter for date,
author, tags, and draft status.  Each implementation had slightly different
directory structures, section headers, and filenames. The core concept was
always the same.

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
# Create today's worklog
worklog-opsdevnz

# Create yesterday's worklog
worklog-opsdevnz --previous

# Override the editor for this run
worklog-opsdevnz --editor nvim
```

## Configuration

Each project gets a `worklog.toml` at its root:

```toml
worklog_dir = "docs/worklog"
structure = "year"           # "flat", "year", or "year-month"
author = "Your Name"
default_tags = ["worklog", "log"]

[[sections]]
title = "Focus for Today"

[[sections]]
title = "Completed"

[[sections]]
title = "Notes"

[[sections]]
title = "Next"
```

## Scope

**WorkLog DOES:**
- Create dated Markdown worklog entries with YAML frontmatter
- Per-project configuration via `worklog.toml`
- Open entries in configured editor (`$VISUAL` / `$EDITOR`)
- Three directory structure modes: flat, year, year-month

**WorkLog DOES NOT (out of scope for 0.0.2):**
- Zensical blog integration (see design doc)
- Auto-generated index pages
- Retro template support (planned for 0.1.0)
- Time tracking / timesheet aggregation
- `list`, `init`, or `create` subcommands (planned for 0.1.0)

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
