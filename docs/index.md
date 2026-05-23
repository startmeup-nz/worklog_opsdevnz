# worklog-opsdevnz

Configurable CLI tool for creating and managing dated development worklogs.

**Version:** see pyproject.toml  
**Status:** Development
**License:** Apache 2.0  
**Python:** 3.14+

## Overview

Across multiple projects, teams kept reinventing the same pattern: a script that
creates a dated Markdown file from a template, with YAML frontmatter for date,
author, tags, and draft status. Each implementation had slightly different
directory structures, section headers, and filenames — but the core concept was
always the same.

`worklog-opsdevnz` formalises this pattern into a single reusable module.
Install it once, configure it per project, and start logging.

## Quick Start

```bash
# Install (development)
uv pip install -e .

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
author = "Your Name"
default_tags = ["worklog", "log"]

[[sections]]
title = "🎯 Focus"

[[sections]]
title = "✅ Completed"

[[sections]]
title = "🧠 Notes"

[[sections]]
title = "⏳ Next"
```

## Directory Structure

The tool supports three directory layouts, configured per project:

| Mode | Layout | Best For |
|------|--------|----------|
| `flat` | `docs/worklog/2026-04-28-slug.md` | Occasional logging (< 20 entries) |
| `year` | `docs/worklog/2026/2026-04-28-slug.md` | Moderate logging (default) |
| `year-month` | `docs/worklog/2026/04/2026-04-28-slug.md` | Daily logging |

## Documentation

- **[Specification](specs/README.md)** — Functional requirements
- **[Non-Functional Requirements](specs/NFR.md)** — Code quality and design guidelines
- **[User Stories](stories/README.md)** — Persona-driven acceptance criteria
- **[Design Decisions](design/README.md)** — Architecture choices and rationale

## Scope

**In scope for 0.0.1 / 0.1.0:**
- Create, list, and init commands
- Per-project configuration via `worklog.toml`
- Three directory structure modes
- Editor integration (`$VISUAL` / `$EDITOR`)
- Template support (custom + retro templates)

**Out of scope (deferred):**
- Zensical blog integration — see [design decision](design/worklog-as-blog.md)
- RSS feed generation
- Auto-generated index pages (planned for 0.1.0)
- Time tracking / timesheet aggregation

## Development

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Run tests
uv run pytest

# Lint
uv run ruff check src/

# Serve documentation
uv run zensical serve
```

## Related

- [OpsDev.nz Collective](https://opsdev.nz) — Parent project
- [GitHub Repository](https://github.com/startmeup-nz/worklog-opsdevnz) — Source code
