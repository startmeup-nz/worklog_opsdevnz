# Agents.md — worklog-opsdevnz

**Audience:** Contributors and AI assistants working on the worklog-opsdevnz module.

## IMPORTANT: No Autonomous Commits

AI assistants must NOT commit changes to this repository. Always stage changes
and describe what was done, then wait for human review and confirmation before
committing. This ensures all changes have human oversight.

## Module Scope

worklog-opsdevnz is a CLI tool for creating and managing dated development
worklogs. It generates Markdown entries with YAML frontmatter from per-project
configuration.

## Development Workflow

1. Install dependencies: `uv sync`
2. Run tests: `uv run python -m pytest`
3. Lint: `uv run ruff check src/ tests/`
4. Type check: `uv run mypy src/`

## Versioning

- **0.0.x** — Incubation phase, rapid iteration, breaking changes expected
- **0.1.0** — First public release, API stabilises
- **1.0.0** — Stable release, semantic versioning enforced

## Current Focus

- Keep the MVP narrow: create/open today's worklog, config discovery, editor integration
- Documentation must match actual implemented behaviour
- Spec and implementation status must stay in sync
- Defer bells and whistles (list, init, templates, blog integration) to 0.1.0+

## Related

- OpsDev.nz collaboration guide (see the parent repository for governance norms)
- Module lifecycle and standards (see the OpsDev.nz modules README)
