# Non-Functional Requirements

**Module:** worklog-opsdevnz  
**Spec Last Updated:** 2026-04-28 (from git history)  
**Status:** Draft  
**Created:** 2026-04-28

> The "Spec Last Updated" date is auto-generated from git history by `specmaint sync-metadata`.

---

## NFR-1: Configuration-Driven Design

### NFR-1.1: No Hardcoded Project Assumptions

**Requirement:** The tool MUST NOT assume any particular project structure, section headers,
or directory layout beyond what is specified in `worklog.toml`.

**Rationale:**
- Different projects have different worklog needs (opsdev.nz vs floydwilde.studio vs private ledgers)
- Hardcoded assumptions create maintenance burden and reduce reusability
- Configuration-driven approach enables any project to adopt the tool

**Correct Approach:**

```toml
# Each project defines its own sections
[[sections]]
title = "🎯 Focus"

[[sections]]
title = "✅ Completed"
```

```python
# GOOD: Config-driven
sections = config.get("sections", DEFAULT_SECTIONS)
```

---

## NFR-2: Code Quality

### NFR-2.1: Type Hints

**Requirement:** All public functions MUST have type hints.

```python
def resolve_path(config: dict[str, Any], iso_date: str, title_suffix: str | None = None) -> Path:
```

### NFR-2.2: Linting

**Requirement:** Code MUST pass `ruff` linting with the project's configured rules.

### NFR-2.3: CLI Framework

**Requirement:** The CLI MUST use Click (not argparse) for consistency with other
OpsDev.nz modules (specmaint, yalh, sprintmaint).

**Rationale:**
- Click provides subcommand groups, better help text, and consistent UX
- All other OpsDev.nz CLI tools use Click
- Reduces cognitive load for users familiar with the ecosystem

---

## NFR-3: Path Handling

### NFR-3.1: Relative to Project Root

**Requirement:** The `worklog_dir` in config is always relative to the directory
containing the `worklog.toml` file, NOT the current working directory.

**Rationale:**
- Users may run the command from a subdirectory (e.g., `cd docs/ && worklog-opsdevnz create`)
- The config file location anchors the path resolution

### NFR-3.2: Directory Creation

**Requirement:** Tool MUST create intermediate directories as needed (`mkdir -p` behaviour).

---

## NFR-4: Compatibility

### NFR-4.1: Python Version

**Requirement:** Tool MUST support Python 3.14+.

### NFR-4.2: Cross-Platform

**Requirement:** Tool MUST work on Linux and macOS. Windows support is not a
0.0.1 priority but the code SHOULD NOT actively break on Windows.

### NFR-4.3: Config Format

**Requirement:** Tool MUST support TOML as the primary config format.
YAML support is optional (via `pyyaml` dependency).

---

## NFR-5: Documentation

### NFR-5.1: CLI Help

**Requirement:** All commands and options MUST have descriptive help text
accessible via `--help`.

### NFR-5.2: Examples

**Requirement:** The `--help` output for `create` MUST include usage examples.

### NFR-5.3: Changelog

**Requirement:** All changes MUST be documented in `CHANGELOG.md` following
the Keep a Changelog format.

---

## NFR-6: Testing

### NFR-6.1: Unit Tests

**Requirement:** Core functionality (config loading, path resolution, frontmatter
generation) MUST have unit tests.

### NFR-6.2: No Filesystem Side Effects in Tests

**Requirement:** Tests MUST use `tmp_path` (pytest) or equivalent to avoid
modifying real files.

### NFR-6.3: No Network Dependencies

**Requirement:** Tests MUST NOT require network access.

---

## NFR-7: Migration from Prototype

### NFR-7.1: Backward Compatibility

**Requirement:** The module MUST be able to read worklog entries created by
the existing `scripts/worklog.py` in opsdev.nz without modification.

**Rationale:** Existing worklog entries in `public/opsdev.nz/docs/worklog/`
and `docs/worklog/` must remain valid.

### NFR-7.2: Config Compatibility

**Requirement:** The module MUST accept the same `worklog.toml` format as
the prototype, with no breaking changes to existing config files.

---

## Compliance Checklist

| Requirement | Status | Notes |
|-------------|--------|-------|
| No hardcoded project assumptions | 📋 Planned | Will be enforced in implementation |
| Type hints on public functions | 📋 Planned | mypy configured |
| Click CLI framework | 📋 Planned | Dependency declared |
| Relative path resolution | 📋 Planned | Will use config dir as anchor |
| Python 3.14+ | 📋 Planned | requires-python set |
| Cross-platform | 📋 Planned | pathlib for all paths |
| TOML config primary | 📋 Planned | tomllib (stdlib 3.14) |
| Unit tests | 📋 Planned | pytest configured |
| Backward compatible with prototype | 📋 Planned | Same config schema |

---

**Document:** NFR.md  
**Module:** worklog-opsdevnz  
**Module:** worklog-opsdevnz  
**Version:** see pyproject.toml
