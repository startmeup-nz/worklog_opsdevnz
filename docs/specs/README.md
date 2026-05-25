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
- **FR-1.1.2**: Tool MUST target today's date by default
- **FR-1.1.3**: Tool MUST NOT overwrite existing entries — if a file already exists for the
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
- **FR-2.1.4**: Relative `worklog_dir` paths MUST be resolved against the config file's
  parent directory, not the current working directory

### FR-2.2: Configuration Schema

The `worklog.toml` file supports the following fields:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `worklog_dir` | string | No | `"docs/worklog"` | Base directory for worklog files (relative paths resolved against config file's parent directory) |
| `structure` | string | No | `"year"` | Directory structure: `"flat"`, `"year"`, `"year-month"` |
| `suffix` | string | No | `"worklog"` | Filename suffix (e.g. `23-05-2026-worklog.md`) |
| `author` | string | No | `$USER` or `"unknown"` | Default author name |
| `default_tags` | list | No | `["internal", "log"]` | Default YAML tags |
| `editor` | string | No | (unset) | Preferred editor command (e.g. `"nvim"`, `"code"`). Overridden by `-e`/`--editor` CLI flag and `$VISUAL`/`$EDITOR` env vars |
| `template` | string | No | (unset) | Path to a custom Markdown template (supports `{{DATE}}`, `{{TITLE}}` placeholders) |
| `sections` | list | No | (see defaults) | Ordered section headers |

### FR-2.3: Config Initialisation *(0.1.0+)*

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
  2. `editor` field in `worklog.toml` config
  3. `$VISUAL` environment variable
  4. `$EDITOR` environment variable
- **FR-4.1.2**: If no editor is configured, tool MUST print the file path and exit cleanly
- **FR-4.1.3**: Tool MUST resolve the editor command via `shutil.which()` and report
  if not found in PATH

### FR-4.2: File Opening

- **FR-4.2.1**: Tool MUST invoke the editor with the worklog file path as argument
- **FR-4.2.2**: Tool MUST wait for the editor process to complete before exiting

---

## FR-5: CLI Interface

### FR-5.1: Command

`worklog-opsdevnz` — create or open today's worklog (default, no args required).

### FR-5.2: Global Options

| Option | Description |
|--------|-------------|
| `-e`, `--editor` | Override editor command for this run |
| `--version` | Print the installed version and exit |

### FR-5.3: Error Handling

- **FR-5.3.1**: File write failures MUST produce a clear error message and non-zero exit
- **FR-5.3.2**: All errors MUST write to stderr

### FR-5.4: Version Reporting

- **FR-5.4.1**: `--version` MUST print the installed version to stdout and exit with code 0
- **FR-5.4.2**: Version MUST be read from installed package metadata via
  `importlib.metadata.version()` to avoid duplicating the version string across files
- **FR-5.4.3**: If package metadata is unavailable (e.g. local editable install), the tool
  MUST fall back to a `"0.0.0+local"` placeholder

---

## FR-6: Custom Template *(future)*

### FR-6.1: Template Configuration

- **FR-6.1.1**: Tool SHOULD support a `template` field in `worklog.toml` pointing to a
  Markdown file. When set, the template replaces the built-in section-based body
  generation for the worklog entry.
- **FR-6.1.2**: Template files MAY use `{{DATE}}` and `{{TITLE}}` placeholders, which the
  tool replaces with the current date and a title derived from the entry date.
- **FR-6.1.3**: If no `template` field is configured, the tool MUST use the built-in
  default (config-driven sections from the `sections` list).

**Example:**

`worklog.toml`:
```toml
template = "my-worklog-template.md"
```

`my-worklog-template.md`:
```markdown
# {{TITLE}}

Date: {{DATE}}

Write whatever you want here — no predefined sections.
```

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
- [ ] `-e` / `--editor` overrides the configured editor
- [ ] Config discovery walks up the tree, falls back to defaults
- [ ] Three structure modes work: flat, year, year-month
- [ ] Filename follows `DD-MM-YYYY-{suffix}.md` (year/month modes) or `YYYY-MM-DD-{suffix}.md` (flat)
- [ ] Tests cover config loading, path resolution, frontmatter generation

### 0.1.0 MVP Complete When:

- [x] `init` command generates valid `worklog.toml` (deferred)
- [x] Published to PyPI as `worklog-opsdevnz`
- [x] Published to `public/opsdev.nz/modules/` as 4th submodule
- [x] Automated release pipeline with Test PyPI gate (NFR-8)

---

## Implementation Status

### v0.0.1 (staging) — Complete

- [x] Module scaffolded with template
- [x] pyproject.toml with metadata and dependencies
- [x] Specs, stories, and design docs in place
- [x] GitHub Actions CI and Dependabot configured

### v0.0.2 — Complete

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-1.1 | Basic creation with frontmatter + sections | ✅ Implemented | `template.py`, `cli.py` |
| FR-2.1 | Config discovery (TOML/YAML, walk-up, defaults) | ✅ Implemented | `config.py`, 6 tests |
| FR-3.1-3.3 | Structure modes (flat/year/year-month) | ✅ Implemented | `paths.py`, 4 tests |
| FR-4.1-4.2 | Editor integration | ✅ Implemented | `cli.py:_open_editor` |
| FR-5.1-5.3 | Click CLI with `-e` flag | ✅ Implemented | `cli.py:main`, 4 tests |

### v0.0.5 (current)

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-2.1.4 | Config-relative `worklog_dir` resolution | ✅ Implemented | `config.py:get_config` |
| FR-5.4 | `--version` flag with `importlib.metadata` | ✅ Implemented | `cli.py:main`, `__init__.py` |

---

**Document:** specs/README.md  
**Module:** worklog-opsdevnz  
**Version:** see pyproject.toml
