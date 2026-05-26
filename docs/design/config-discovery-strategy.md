# Design Decision: Config Discovery Strategy

**Status:** Decision  
**Created:** 2026-05-26  
**Spec Reference:** FR-2.1, Story 7

---

## Problem

`worklog-opsdevnz` needs to find the right `worklog.toml` when invoked from
anywhere within a project tree. The config file determines which directory
worklogs go in, which section headers to use, who the author is, and more.

The existing prototype has a bug in its search order (it checks parent
directories *before* the current directory), and it does not handle
monorepo or submodule scenarios gracefully.

---

## Approaches Considered

### Approach 1: Current behavior (walk up from cwd, parents-first)

```python
candidates = list(start.parents) + [start]  # parents BEFORE cwd ❌
```

This checks `~/.config/` before `~/projects/my-project/`. If your global
dotfiles contain a `worklog.toml`, it silently overrides the project one.

**Problem:** The search order is wrong — parents should be checked *after*
cwd, not before. This actively breaks per-project configuration.

### Approach 2: `.git` boundary heuristic

Stop walking up at the nearest `.git` directory, treating it as a project
boundary marker. If cwd is inside a git submodule, the tool would never
see the parent repository's `worklog.toml`.

```python
candidates = [start] + list(start.parents)
# ... stop at .git boundary
```

**Problem:** A git submodule that does *not* have its own `worklog.toml`
cannot inherit its parent repository's config. If you're working in a
vendored submodule (e.g. `vendor/octodns/`) and want to log what you're
doing without adding a `worklog.toml` there, the `.git` boundary blocks
you and you get defaults instead.

This creates a guessing problem: the heuristic cannot distinguish between
"I want to be isolated" and "I have no config, please inherit from
upstream."

### Approach 3 (Chosen): cwd-first walk-up

```python
candidates = [start] + list(start.parents)  # cwd FIRST ✅
```

Simple, predictable, no heuristics:

1. Check the current directory first — nearest config wins.
2. Walk up through parents until a config is found or `/` is reached.
3. No boundary detection — the nearest `worklog.toml` is always the
   right one, regardless of whether you're in a submodule, a monorepo,
   or a standalone repo.

This is the same strategy as Docker's `.dockerignore`, ESLint's config
resolution, and Prettier's file discovery — all standard tools that handle
monorepos by looking for the nearest config file.

---

## Decision

**Use cwd-first walk-up.**

| Scenario | Before (parents-first) | After (cwd-first) |
|---|---|---|
| `cwd` has a `worklog.toml` | Works (by luck — no parent config exists) | ✅ Works — checked first |
| `cwd` has a config, parent also has one | ❌ Parent wins | ✅ Nearest (cwd) wins |
| Inside a submodule with no own config | ❌ Defaults (or finds wrong config) | ✅ Walks up to parent repo |

### Why not `.git`?

We deliberately chose *not* to use `.git` as a boundary marker because:

- **Flexibility:** A user working in a git submodule that has no
  `worklog.toml` of its own can still inherit the parent repo's config.
- **No guessing:** The tool does not need to infer intent when a
  submodule has no config — it simply walks up to the nearest one.
- **Simplicity:** No boundary detection logic, no sentinel files, no
  special-casing for different VCS tools (Mercurial, Fossil, etc.).
- **Predictability:** Nearest config wins, always. If isolation is
  desired, the user adds a `worklog.toml` to that directory.

---

## Changes Required

### `config.py::find_config()`

```python
# Before (buggy — parents first)
candidates = list(start.parents) + [start]

# After (cwd first)
candidates = [start] + list(start.parents)
```

### `config.py::get_config()`

No changes needed — it already calls `find_config(start=start)`. The
fix is entirely in `find_config()`.

### Spec update

FR-2.1.1 changes from:
> "starting from the current working directory and walking up to the
> filesystem root"

To:
> "starting from the current working directory, checking it first, then
> walking up through parent directories until a config file is found
> or the filesystem root is reached"

FR-2.1.2 is updated to clarify that the nearest config (closest to cwd)
wins.

---

## Related

- [Story 7: Monorepo-Aware Config Discovery](../stories/story-7-monorepo-config-discovery.md)
- [FR-2.1: Per-Project Configuration](../specs/functional-requirements.md) — Per-Project Configuration
- [Security: Config Trust Model](security-trust-model.md) — Editor validation, trust boundary, NFR-9
- [config.py](../../src/worklog_opsdevnz/config.py) — `find_config()` implementation
- [structure-modes.md](structure-modes.md) — Related design decision for worklog directory layout
