# Design Decision: Directory Structure Modes

**Status:** Proposal  
**Created:** 2026-04-28  
**Spec Reference:** FR-3

---

## Problem

The existing prototype supports three directory structure modes: `flat`, `year`,
and `year-month`. Which should be the default? Which should we recommend for
new projects?

---

## Analysis of Existing Usage

| Project | Current Structure | Entry Count | Notes |
|---------|-------------------|-------------|-------|
| outcome-engineering | `year/YYYY-MM-DD-worklog.md` | ~50 entries (2025-2026) | Shell script, no config |
| public/opsdev.nz | `flat/YYYY-MM-DD-slug.md` | 2 entries | New, prototype config |
| floydwilde.studio | `year-month-name/YYYY-MM-DD-worklog.md` | ~10 entries | Hardcoded, month names |

---

## Mode Comparison

### Flat (`docs/worklog/2026-04-28-slug.md`)

**Best for:** Projects with < 20 entries, or projects that use a separate
index page for navigation.

**Pros:**
- Simplest structure
- Easy to `ls` and grep
- No nested directories to manage

**Cons:**
- Doesn't scale — 100+ entries in one directory is unwieldy
- File browsers and terminals become slow with many files
- No natural archive boundaries

### Year (`docs/worklog/2026/2026-04-28-slug.md`)

**Best for:** Projects with moderate entry counts (20-100/year).

**Pros:**
- Natural yearly archive boundaries
- Keeps directory sizes manageable
- Matches existing outcome-engineering pattern

**Cons:**
- Still potentially large directories (daily logging = 365 files/year)
- No monthly grouping for browsing

### Year-Month (`docs/worklog/2026/04/2026-04-28-slug.md`)

**Best for:** Projects with daily logging or high entry counts.

**Pros:**
- Most granular — 10-30 entries per directory
- Easy to browse archives by month
- Scales indefinitely
- Matches floydwilde.studio pattern (but with numeric months)

**Cons:**
- Deeper directory nesting
- Slightly more complex path resolution

---

## Decision

**Default: `year`** — Matches the most established pattern (outcome-engineering)
and is a reasonable middle ground.

**Recommended for daily logging: `year-month`** — If a project expects to log
most working days, this is the better choice.

**Recommended for occasional logging: `flat`** — If a project logs weekly or
less frequently, flat is simplest.

The tool supports all three; the choice is per-project via `worklog.toml`.

---

## Filename Pattern

The default pattern is `{date}-{slug}.md` where:
- `{date}` is the ISO date (`2026-04-28`)
- `{slug}` is derived from the title suffix (lowercase, hyphenated)

This ensures:
- Files sort chronologically when listed alphabetically
- Dates are machine-parseable from filenames
- Titles are human-readable in filenames

---

## Related

- [FR-3: Directory Structure Modes](../specs/functional-requirements.md) — Directory structure modes
- [worklog-as-blog.md](worklog-as-blog.md) — Zensical blog integration decision
