# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-05-25

### Added
- Automated release pipeline: Test PyPI gate + smoke test → real PyPI via
  OIDC Trusted Publishing (NFR-8)
- `docs/release-process.md` — step-by-step Trusted Publishing setup guide
- `docs/runbooks/module-promotion.md` — module incubation → published workflow
- Module promoted to published: submodule under `public/opsdev.nz/modules/`

### Changed
- CI: `test.yml` and `publish.yml` now use `uv` for dependency management
- Repo visibility: made public for Trusted Publishing

## [0.0.5] — 2026-05-25

### Added
- `--version` flag: prints installed version via `importlib.metadata` (#5)
- Spec FR-5.4: version reporting requirements documented
- Test for `--version` output (version-agnostic)

### Fixed
- `worklog_dir` now resolves relative to config file location, not CWD — running from any
  subdirectory creates files in the correct project-relative path (#4)
- Config discovery always anchored relative paths to the current working directory; now
  relative `worklog_dir` values are resolved against the config file's parent directory

### Added
- Spec FR-2.1.4: documents `worklog_dir` resolution rule
- Regression test: `test_get_config_worklog_dir_resolved_relative_to_config`

## [0.0.3] — 2026-05-24

### Changed
- Narrowed MVP scope: defer `list`, `init`, `create` subcommands to 0.1.0+
- Removed `-p` / `--previous` flag — current scope is create/open today's worklog only
- Removed unused `rich` dependency
- Cleaned up documentation to match actual implemented behaviour
- Spec cleaned up: removed stale requirements, renumbered FR sections, marked 0.1.0+ items

### Fixed
- README.md broken code block and stale `--list` reference
- docs/index.md references to non-existent commands (`create`, `list`, `init`, `-d`, `-t`)
- Spec implementation status updated to reflect reality

### Added
- Agents.md — minimal module-specific guidance, self-contained

## [0.0.2] — 2026-05-24

### Added
- Click CLI: bare command creates today's worklog, `-p` for yesterday, `-e` for editor
- Config discovery: walks up from cwd for `worklog.toml`/`worklog.yaml`, falls back to defaults
- Path resolution: three structure modes (flat, year, year-month)
- Frontmatter + body generation from config-driven sections
- Editor resolution: CLI override → `$VISUAL` → `$EDITOR`
- 17 tests covering config, paths, template, CLI (89% coverage)

### Changed
- Migrated from prototype script to Click-based module
- Removed hardcoded version strings from docs — DRY via pyproject.toml

### Fixed
- Linting issues (unused imports, missing `Path` import)
- Generated `site/` directory accidentally tracked — removed and gitignored

## [0.0.1] — Unreleased

### Added
- Initial module scaffold from template-opsdevnz
- Worklog specs, stories, and design docs ported from incubation
- pyproject.toml with Click, PyYAML dependencies
- GitHub Actions CI (test on push/PR) and PyPI publish (on tag)
- Dependabot weekly pip updates
