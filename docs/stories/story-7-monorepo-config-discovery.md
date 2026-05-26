# Story 7: Monorepo-Aware Config Discovery

**As a** developer working in a monorepo that contains multiple projects
(including git submodules), each with their own worklog configuration,

**I want** `worklog-opsdevnz` to discover the nearest `worklog.toml`
by checking the current directory first and then walking up,

**so that** each project can have its own worklog config while a
subproject without its own config can still inherit from its parent.

---

## Acceptance Criteria

### AC-7.1: Cwd-First Config Search

- [ ] When searching for `worklog.toml`, the tool checks the **current
      working directory first**, then walks up through parent directories.
- [ ] This fixes the current bug where parents are checked before cwd,
      causing global or home-directory configs to silently override
      project-level ones.

### AC-7.2: Nearest Config Wins

- [ ] The first config file found (closest to cwd) is used.
- [ ] If no config is found after walking to `/`, tool falls back to
      built-in defaults (unchanged from current behaviour).
- [ ] A standalone repo with a root `worklog.toml` works exactly as
      before — no change for the simple case.

### AC-7.3: Submodule Inheritance (Key Use Case)

- [ ] When cwd is inside a git submodule that does **not** have its own
      `worklog.toml`, the tool walks up past the submodule boundary and
      finds the parent repository's config.
- [ ] When cwd is inside a git submodule that **does** have its own
      `worklog.toml`, the submodule's config is used (cwd-first wins).

---

## Example

Given this monorepo layout:

```
my-monorepo/
├── worklog.toml                    # main project config
├── docs/worklogs/                  # main project worklogs
├── project-alpha/
│   ├── .git                        # git submodule
│   ├── worklog.toml                # alpha has its own config
│   └── docs/worklogs/              # alpha worklogs
└── vendor/
    └── octodns/
        ├── .git                    # git submodule, NO worklog.toml
        └── src/                    # vendored code
```

| cwd | Discovered config | Result |
|---|---|---|
| `project-alpha/` | `project-alpha/worklog.toml` | Alpha worklogs in `project-alpha/docs/worklogs/` |
| `vendor/octodns/` | `my-monorepo/worklog.toml` | Main project worklogs inherit ✅ |
| `my-monorepo/` | `my-monorepo/worklog.toml` | Main project worklogs |

---

## Priority

| Field | Value |
|-------|-------|
| **Priority** | High |
| **Version Target** | 0.1.1 |
| **Dependencies** | Story 2 (Per-Project Configuration) — this is an evolution of config discovery |
| **Spec Impact** | Requires update to FR-2.1.1 (fix search order) and FR-2.1.2 (clarify nearest wins) |

---

*Created: 2026-05-26*
