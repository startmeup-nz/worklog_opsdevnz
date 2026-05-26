# Non-Functional Requirements

**Module:** worklog-opsdevnz  
**Spec Last Updated:** 2026-04-28 (from git history)  
**Status:** Draft  
**Created:** 2026-04-28

> The "Spec Last Updated" date reflects the most recent change to this document.

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

**Requirement:** The CLI MUST use Click (not argparse) for consistency with other OpsDev.nz modules.

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

## NFR-8: Release Process

### NFR-8.1: Automated CI/CD Pipeline

**Requirement:** The module MUST have an automated CI/CD pipeline for release
publishing. The release flow must be triggered by a push of a version tag
(e.g. `v0.1.0`) to the primary branch, and must execute in an isolated
runner environment with access to only the PyPI credentials it needs.

**Rationale:** Manual releases are error-prone and inconsistent. An
automated pipeline ensures every release follows the same reproducible
process regardless of the CI platform.

### NFR-8.2: Test PyPI Gate *(Optional)*

**Requirement:** The release workflow MAY publish to Test PyPI as a quality
gate before the real PyPI publish. When used, the Test PyPI package must
be installable and functional before the real publish proceeds.

**Rationale:** A broken release on real PyPI is hard to fix and confusing
to users. Test PyPI provides a safe environment to validate the package
end-to-end before it reaches the public index. Mature modules with
established pipelines may skip this step.

### NFR-8.3: Single Source of Truth for Version

**Requirement:** The version number MUST be sourced from a single place
(`pyproject.toml`), read via `importlib.metadata.version()`. No version
string duplication across files.

**Rationale:** Duplicated version strings drift over time and create
confusion about which value is authoritative.

### NFR-8.4: Dry-Run Safety

**Requirement:** The release workflow MUST support a dry-run mode (e.g.
publish to Test PyPI only, without tagging or real PyPI) for pipeline
validation before cutting a real release.

### NFR-8.5: Smoketest Verification

**Requirement:** After publishing to Test PyPI, the workflow MUST install
the published wheel from Test PyPI in a clean virtual environment and run
`worklog-opsdevnz --version` to confirm the version string matches the
release tag and the package is functional.

---

## NFR-9: Security & Config Trust *(new — 2026-05-26)*

### NFR-9.1: Config Trust Model

**Requirement:** The tool MUST operate on the assumption that config files
in the project tree are trusted. This is the same model used by `make`,
`npm`, `eslint`, and other CLI tools that discover configuration by
walking up the directory tree.

**Rationale:** Filesystem-based trust is the standard security model for
developer tooling. Adding authentication, sandboxing, or prompts would
create friction without meaningfully improving security — an attacker
with filesystem access can already place malicious `.bashrc`,
`Makefile`, or `package.json` files.

### NFR-9.2: Editor Path Warning

**Requirement:** If the `editor` value in `worklog.toml` contains a path
separator (`/`), the tool MUST print a warning to stderr before invoking
the editor. The warning must be informational only — it must not block
execution.

**Rationale:** An attacker who places a malicious `worklog.toml` in a
shared or writable directory could set `editor = "/tmp/malware.sh"`. The
warning draws attention to non-command-name editor values — the most
realistic injection vector — while allowing legitimate use of custom
editor scripts and absolute paths.

### NFR-9.3: Config Discovery Transparency *(verbose mode)*

**Requirement:** When `--verbose` is passed, the tool MUST print the
config file path and its resolved `worklog_dir` to stderr before
creating or opening an entry.

**Rationale:** Transparent config discovery lets users verify which
config file was selected. This helps debug unexpected behaviour and
makes it visible if a config from an unexpected location is being used.

### NFR-9.4: File Write Safety *(future)*

**Requirement:** The tool SHOULD verify that the resolved worklog file
path stays within the intended `worklog_dir`. If path traversal is
detected (e.g. `worklog_dir = "../"`), the tool SHOULD refuse to
write.

**Note:** Aspirational for 0.1.1. Not implemented yet.

---

## Compliance Checklist

| Requirement | Status | Notes |
|-------------|--------|-------|
| No hardcoded project assumptions | ✅ Complete | Config-driven sections, tags, author, structure |
| Type hints on public functions | ✅ Complete | mypy configured, all public functions typed |
| Click CLI framework | ✅ Complete | Click 8.x, `@click.command`, `@click.option`, `@click.version_option` |
| Relative path resolution | ✅ Complete | Resolved against config file directory (FR-2.1.4) |
| Python 3.14+ | ✅ Complete | `requires-python = ">=3.12"` |
| Cross-platform | ✅ Complete | pathlib for all paths |
| TOML config primary | ✅ Complete | tomllib (stdlib 3.14) |
| Unit tests | ✅ Complete | 18 tests, 88% coverage |
| Backward compatible with prototype | ✅ Complete | Same config schema, same worklog format |
| Automated CI/CD pipeline | 📋 Planned | Tag-triggered publish to PyPI |
| Test PyPI gate | 📋 Planned (optional) | Validate on Test PyPI before real publish |
| Single source of truth for version | ✅ Complete | `importlib.metadata.version()` in `__init__.py` |
| Dry-run safety | 📋 Planned | Test PyPI-only publish for validation |
| Smoketest verification | 📋 Planned | Install from Test PyPI, run `--version` |
| Config trust model (NFR-9.1) | 📋 Documented | `docs/design/security-trust-model.md` |
| Editor path warning (NFR-9.2) | 📋 In design | `docs/design/security-trust-model.md` |
| Config discovery transparency (NFR-9.3) | 📋 In design | `--verbose` flag planned |
| File write safety (NFR-9.4) | 🔮 Future | Path traversal guard — aspirational |

---

**Document:** NFR.md  
**Module:** worklog-opsdevnz  
**Module:** worklog-opsdevnz  
**Version:** see pyproject.toml
