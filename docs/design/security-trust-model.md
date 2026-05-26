# Security Design: Config Trust Model

**Status:** Decision  
**Created:** 2026-05-26  
**Spec Reference:** FR-2.1, Story 7

---

## Problem

`worklog-opsdevnz` discovers `worklog.toml` by walking up the directory
tree from the current working directory. This raises a trust question:

> What if a malicious `worklog.toml` exists somewhere in the search path?

Unlike a fixed config path (e.g. `~/.config/worklog/worklog.toml`), the
walk-up approach means the tool will use *any* `worklog.toml` it
encounters — including one planted by an attacker in a shared directory,
a cloned repository, or a compromised dependency.

---

## Risk Analysis

### Attack Surface

The tool reads these fields from `worklog.toml`:

| Field | Type | Risk Level | Concern |
|-------|------|------------|---------|
| `worklog_dir` | Path | Low | Redirect file writes to another directory |
| `structure` | Enum (`flat`/`year`/`year-month`) | None | Deterministic, validated options |
| `suffix` | String | Low | Affects filename only |
| `author` | String | Low | Affects YAML frontmatter only |
| `editor` | String (command) | **High** | **Potential code execution** |
| `template` | Path | Medium | File read from arbitrary path |
| `default_tags` | List | None | Affects YAML frontmatter only |
| `sections` | List | None | Affects template generation only |

The **editor field** is the primary concern. If a malicious config sets
`editor = "/tmp/malware.sh"`, the tool will attempt to execute it.

### Threat Scenarios

| Scenario | Likelihood | Impact | Notes |
|---|---|---|---|
| Malicious config in `/tmp/` | Low | Medium | User would need to run tool in `/tmp/` |
| Malicious config in cloned repo | Low-Medium | Medium | Same risk as `Makefile`, `package.json`, `.eslintrc` |
| Malicious config planted by compromised dependency | Low | High | Supply-chain attack, not specific to this tool |
| Accidental misconfiguration (wrong `editor`) | Medium | Low | Tool error, not security breach |

### Comparison to Industry Norm

| Tool | Config Discovery | Editor/Command Risk | Safeguards |
|------|-----------------|-------------------|------------|
| **ESLint** | Walk-up to root | `.eslintrc` can specify formatter plugins | Plugin sandboxing (limited) |
| **Prettier** | Walk-up to root | No command execution | — |
| **Black** | Walk-up to root (pyproject.toml) | No command execution | — |
| **Docker** | Walk-up (compose.yml) | Compose can mount volumes, run commands | Root-owned config warning |
| **Make** | Fixed (Makefile) | Full shell execution | User awareness, decades of precedent |
| **npm** | Walk-up (package.json) | `scripts` run arbitrary commands | Pre-flight audit (`npm audit`) |

`worklog-opsdevnz` is no worse than any of these. Editor-path injection
is the only real risk, and it requires the attacker to place a config
file in a directory you then run the tool from.

---

## Decision

### Trust Assumption

> This tool trusts the `worklog.toml` files in your project tree. You are
> responsible for the directories you run the tool from. Config files
> from untrusted sources (e.g. cloned repositories) should be reviewed
> before use, just as you would review a `Makefile` or `package.json`.

This matches the standard security model of CLI tools: **the filesystem
is your sandbox.** The tool does not attempt to guess whether a config
file is trustworthy — that is the user's responsibility.

### Editor Path Validation (Mitigation)

While we do not sandbox the config, we add a lightweight check for the
highest-risk field:

```python
if config_editor and ("/" in config_editor):
    click.echo(
        f"Warning: editor '{config_editor}' contains a path separator.\n"
        f"  If this is not a simple command name, review your worklog.toml.",
        err=True,
    )
```

This catches absolute paths (`/usr/bin/malware`) and relative paths
(`./scripts/hook`) while allowing straightforward command names
(`nvim`, `code`, `vim`). It does not block — it warns. A user who
deliberately sets `editor = "/usr/local/bin/my-editor"` can ignore
the warning.

### Config Discovery Transparency (Mitigation)

When `--verbose` is passed, the tool prints which config file it found
and where it resolves `worklog_dir` to:

```
$ worklog-opsdevnz --verbose
Using config: /home/john/projects/my-project/worklog.toml
Worklog dir:  /home/john/projects/my-project/docs/worklogs
```

This has two benefits:

1. **Debugging** — if the wrong config is being picked up, verbose
   output makes it obvious immediately.
2. **Awareness** — if a config from an unexpected location is in play
   (e.g. `/tmp/worklog.toml`), the user sees it before the editor opens.

### What We Are Not Doing

| Safeguard Considered | Rejected Because |
|---|---|
| **Ownership check** (config must be owned by current user) | Breaks shared project directories, CI runners, and team repos |
| **Permission check** (config must not be world-writable) | OS already enforces this for the running user |
| **Config hash allowlist** (trust only known configs) | Unmaintainable, breaks every new project setup |
| **Sandboxed editor execution** | Disproportionate for a tool that writes Markdown files |
| **Prompt on config load** ("use this config? Y/N") | Annoying for legitimate daily use, trains users to reflexively approve |
| **Block absolute editor paths** | Legitimate use case: custom editor scripts, CI wrappers |
| **Block root-level config** (`/worklog.toml`) | Valid container use case — a tool running in a container may have its config at `/` |

### Why Not Hard-Block Root-Level Configs?

In a typical workstation setup, you'd never put a config at `/`. But in a
container, `/` *is* the project root. A Dockerfile might COPY a
`worklog.toml` to the container root, making `/worklog.toml` the correct
and expected config location. Hard-blocking root configs would break this
legitimate use case for no security gain — if an attacker has write access
to `/`, you have bigger problems than a worklog tool.

### Documentation

The trust assumption is codified in the specification:

- [NFR-9: Security & Config Trust](../specs/NFR.md) — Config trust model,
  editor path warning, config discovery transparency, file write safety

---

## Related

- [Design: Config Discovery Strategy](config-discovery-strategy.md) — Config file discovery approach
- [Spec: FR-2.1](../specs/functional-requirements.md) — Per-Project Configuration
- [Spec: NFR-9](../specs/NFR.md) — Security non-functional requirements
- [Story 7: Monorepo-Aware Config Discovery](../stories/story-7-monorepo-config-discovery.md) — User story
