# Functional Requirements Specification

**Module:** worklog-opsdevnz  
**Module Version:** see `pyproject.toml`  
**Spec Last Updated:** 2026-05-23 (from git history)  
**Status:** Draft

---

## Versioning Model

This spec follows the OpsDev.nz versioning model:

| Field | Source | Meaning |
|-------|--------|---------|
| Module Version | `pyproject.toml` | Version of the module being specified |
| Spec Last Updated | Git history | When this spec was last modified |

Use `specmaint sync-metadata` to sync both fields from their sources.

---

## Related Documents

- [Non-Functional Requirements](NFR.md) - Code quality, security, and design guidelines
- [Design Decisions](../design/README.md) - Architecture and integration decisions
- [User Stories](../stories/README.md) - Persona-driven narratives

---

## FR-1: Worklog Entry Creation

### FR-1.1: Basic Creation

- **FR-1.1.1**: Tool MUST create a new Markdown file with YAML frontmatter containing
  `title`, `date`, `author`, `tags`, and `draft` fields
- **FR-1.1.2**: Tool MUST default to today's date when no `-p` / `--previous` flag provided
- **FR-1.1.3**: Tool MUST use `-p` / `--previous` to open yesterday's worklog
- **FR-1.1.4**: Tool MUST NOT overwrite existing entries — if a file already exists for the
  given date, it MUST open the existing file instead

### FR-1.1.A: Frontmatter Format

- **FR-1.1.A.1**: Frontmatter MUST use YAML format delimited by `---` markers
- **FR-1.1.A.2**: `title` field MUST follow the pattern `"Work Log - {date}"`
- **FR-1.1.A.3**: `date` field MUST be ISO 8601 format (`YYYY-MM-DD`)
- **FR-1.1.A.4**: `author` field MUST come from `worklog.toml` config
- **FR-1.1.A.5**: `tags` field MUST be a YAML list from `default_tags` in config
- **FR-1.1.A.6**: `draft` field MUST default to `false`

### FR-1.1.B: Body Generation

- **FR-1.1.B.1**: Tool MUST generate section headers from the `sections` list in config
- **FR-1.1.B.2**: Each section MUST be an H2 heading (`## Title`)
- **FR-1.1.B.3**: Sections MUST appear in the order defined in config
- **FR-1.1.B.4**: A blank line MUST separate frontmatter from the first section heading

---

## FR-2: Per-Project Configuration

### FR-2.1: Config Discovery

- **FR-2.1.1**: Tool MUST search for `worklog.toml`, `worklog.yaml`, or `worklog.yml`
  starting from the current working directory and walking up to the filesystem root
- **FR-2.1.2**: Tool MUST use the first config file found
- **FR-2.1.3**: If no config file is found, tool MUST use built-in defaults

### FR-2.2: Configuration Schema

The `worklog.toml` file supports the following fields:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `worklog_dir` | string | No | `"docs/worklog"` | Base directory for worklog files |
| `structure` | string | No | `"year"` | Directory structure: `"flat"`, `"year"`, `"year-month"` |
| `filename_pattern` | string | No | `"{day}-{month}-{year}-{suffix}.md"` | Filename template. Default: `23-05-2026-worklog.md` |
| `filename_suffix` | string | No | `"worklog"` | Configurable suffix appended to the filename |
| `author` | string | No | `$USER` or `"unknown"` | Default author name |
| `default_tags` | list | No | `["internal", "log"]` | Default YAML tags |
| `sections` | list | No | (see defaults) | Ordered section headers |

### FR-2.3: Config Initialisation

- **FR-2.3.1**: `worklog-opsdevnz init` MUST create a `worklog.toml` in the current directory
- **FR-2.3.2**: Tool MUST NOT overwrite an existing config file
- **FR-2.3.3**: Generated config MUST include all default fields with commented explanations

---

## FR-3: Directory Structure Modes

### FR-3.1: Flat Mode (`structure = "flat"`)

- **FR-3.1.1**: All worklog files placed directly in `worklog_dir`
- **FR-3.1.2**: Filename: `YYYY-MM-DD-{suffix}.md` (year first to sort correctly)

### FR-3.2: Year Mode (`structure = "year"`) — default

- **FR-3.2.1**: Files placed in `worklog_dir/YYYY/`
- **FR-3.2.2**: Filename: `DD-MM-YYYY-{suffix}.md`
- **FR-3.2.3**: Example: `docs/worklog/2026/23-05-2026-worklog.md`

### FR-3.3: Year-Month Mode (`structure = "year-month"`)

- **FR-3.3.1**: Files placed in `worklog_dir/YYYY/MM/`
- **FR-3.3.2**: Filename: `DD-MM-YYYY-{suffix}.md`
- **FR-3.3.3**: Example: `docs/worklog/2026/05/23-05-2026-worklog.md`

---

## FR-4: Editor Integration

### FR-4.1: Editor Resolution

- **FR-4.1.1**: Tool MUST check for editor in this order:
  1. `-e` / `--editor` CLI argument
  2. `$VISUAL` environment variable
  3. `$EDITOR` environment variable
- **FR-4.1.2**: If no editor is configured, tool MUST print the file path and exit cleanly
- **FR-4.1.3**: Tool MUST resolve the editor command via `shutil.which()` and report
  if not found in PATH

### FR-4.2: File Opening

- **FR-4.2.1**: Tool MUST invoke the editor with the worklog file path as argument
- **FR-4.2.2**: Tool MUST wait for the editor process to complete before exiting

---

## FR-5: Entry Listing

### FR-5.1: List Command

- **FR-5.1.1**: `worklog-opsdevnz list` MUST find all `.md` files under `worklog_dir`
- **FR-5.1.2**: Tool MUST exclude `index.md`, `template.md`, and `retro-template.md`
  from listing
- **FR-5.1.3**: Entries MUST be sorted by date (newest first)
- **FR-5.1.4**: Output MUST show the relative path from `worklog_dir`

### FR-5.2: List Output (0.1.0+)

- **FR-5.2.1**: Tool SHOULD parse frontmatter to display title, date, and tags
- **FR-5.2.2**: Output SHOULD use Rich for formatted table display

---

## FR-6: CLI Interface

### FR-6.1: Command

`worklog-opsdevnz` — create or open today's worklog (default, no args required).
`list` and `init` subcommands are planned for future versions.

### FR-6.2: Global Options

| Option | Description |
|--------|-------------|
| `-p`, `--previous` | Open yesterday's worklog instead of today's |
| `-e`, `--editor` | Override editor command for this run |

### FR-6.3: Error Handling

- **FR-6.3.1**: Invalid date format MUST produce a clear error message and non-zero exit
- **FR-6.3.2**: Missing `worklog_dir` MUST produce a clear error message
- **FR-6.3.3**: All errors MUST write to stderr

---

## FR-7: Template Support (0.1.0)

### FR-7.1: Custom Templates

- **FR-7.1.1**: Tool MUST support a `template` field in config pointing to a Markdown file
- **FR-7.1.2**: Template files MUST support `{{DATE}}` and `{{TITLE}}` placeholders
- **FR-7.1.3**: If no template specified, tool MUST use the built-in default template

### FR-7.2: Retro Templates

- **FR-7.2.1**: Tool MUST support a separate `retro_template` field in config
- **FR-7.2.2**: `worklog-opsdevnz create --retro` MUST use the retro template

---

## Acceptance Criteria

### 0.0.1 Staging Complete When:

- [ ] Module directory structure created under `modules/worklog_opsdevnz/`
- [ ] `pyproject.toml` with correct metadata and dependencies
- [ ] Functional and non-functional requirements documented
- [ ] Design decision documented for Zensical blog integration (deferred)
- [ ] Prototype `scripts/worklog.py` from opsdev.nz reviewed and mapped to requirements
- [ ] Empty `src/worklog_opsdevnz/` package scaffolded
- [ ] Empty `tests/` directory scaffolded

### 0.0.2 MVP Complete When:

- [ ] `worklog-opsdevnz` (no args) creates today's worklog with YAML frontmatter and config-driven sections
- [ ] `-p` / `--previous` opens yesterday's worklog
- [ ] `-e` / `--editor` overrides the configured editor
- [ ] Config discovery walks up the tree, falls back to defaults
- [ ] Three structure modes work: flat, year, year-month
- [ ] Filename follows `DD-MM-YYYY-{suffix}.md` (year/month modes) or `YYYY-MM-DD-{suffix}.md` (flat)
- [ ] Tests cover config loading, path resolution, frontmatter generation

### 0.1.0 MVP Complete When:

- [ ] `create` command works with all three structure modes
- [ ] `list` command sorts by date and shows frontmatter metadata
- [ ] `init` command generates valid `worklog.toml`
- [ ] Editor integration works with `$VISUAL` / `$EDITOR`
- [ ] Template support (custom + retro) implemented
- [ ] Tests cover config loading, path resolution, frontmatter generation
- [ ] Published to PyPI as `worklog-opsdevnz`

---

## Implementation Status

### v0.0.1 (staging) — Complete

- [x] Module scaffolded with template
- [x] pyproject.toml with metadata and dependencies
- [x] Specs, stories, and design docs in place
- [x] GitHub Actions CI and Dependabot configured

### v0.0.2 (current)

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-1.1 | Basic creation with frontmatter + sections | ✅ Implemented | `template.py`, `cli.py` |
| FR-2.1 | Config discovery (TOML/YAML, walk-up, defaults) | ✅ Implemented | `config.py`, 6 tests |
| FR-3.1-3.3 | Structure modes (flat/year/year-month) | ✅ Implemented | `paths.py`, 4 tests |
| FR-4.1-4.2 | Editor integration | ✅ Implemented | `cli.py:_open_editor` |
| FR-6.1-6.3 | Click CLI with `-p` and `-e` flags | ✅ Implemented | `cli.py:main`, 4 tests |

---

**Document:** specs/README.md  
**Module:** worklog-opsdevnz  
**Version:** see pyproject.toml
