# User Stories

This directory contains user stories for worklog-opsdevnz, organised by persona
and priority.

---

## Story 1: Daily Worklog Entry

**As a** developer working on a project,  
**I want to** create a dated worklog entry with my project's section headers,  
**so that** I can quickly capture what I did today without thinking about formatting.

**Acceptance Criteria:**
- [ ] Running `worklog-opsdevnz create` creates a file with today's date
- [ ] File contains YAML frontmatter with title, date, author, tags, draft
- [ ] File contains section headers from `worklog.toml`
- [ ] File opens in my configured editor
- [ ] Running again on the same day opens the existing file

---

## Story 2: Per-Project Configuration

**As a** developer working on multiple projects,  
**I want** each project to have its own worklog template and directory structure,  
**so that** my worklogs match each project's conventions without manual setup.

**Acceptance Criteria:**
- [ ] Each project has its own `worklog.toml`
- [ ] Tool finds config by walking up from current directory
- [ ] Different projects can use different structure modes (flat, year, year-month)
- [ ] Different projects can have different section headers

---

## Story 3: Browse Existing Entries

**As a** developer returning to a project after a break,  
**I want to** list my recent worklog entries,  
**so that** I can quickly find what I was working on last.

**Acceptance Criteria:**
- [ ] `worklog-opsdevnz list` shows all entries sorted newest-first
- [ ] Output shows relative paths from the worklog directory
- [ ] Excludes index.md and template files from listing

---

## Story 4: Standardise Across Projects

**As an** opsdev engineer maintaining multiple codebases,  
**I want to** install one tool that works across all my projects,  
**so that** I don't need to maintain separate worklog scripts for each.

**Acceptance Criteria:**
- [ ] Tool installable via `pip install worklog-opsdevnz`
- [ ] Works with existing `worklog.toml` format from prototype
- [ ] Compatible with entries created by the old `scripts/worklog.py`
- [ ] CLI uses Click for consistency with other OpsDev.nz tools

---

## Story 5: Retrospective Entries (0.1.0)

**As a** developer who runs retrospectives,  
**I want to** create a worklog entry from a retro template,  
**so that** my retros have a consistent structure different from daily logs.

**Acceptance Criteria:**
- [ ] `worklog-opsdevnz create --retro` uses the retro template
- [ ] Retro template is configurable per project
- [ ] Retro entries are distinguishable from daily logs (different filename or tag)

---

## Story 6: Auto-Generated Index (0.1.0)

**As a** reader of worklogs on a documentation site,  
**I want** an index page that lists entries in reverse-chronological order,  
**so that** I can browse worklogs without relying on alphabetical sidebar navigation.

**Acceptance Criteria:**
- [ ] `worklog-opsdevnz generate-index` creates/updates `index.md`
- [ ] Index lists entries newest-first with title, date, and tags
- [ ] Index is Markdown format compatible with Zensical/MkDocs

---

## Priority Order

| Story | Priority | Version Target |
|-------|----------|----------------|
| Story 1: Daily entry | High | 0.0.1 / 0.1.0 |
| Story 2: Per-project config | High | 0.0.1 / 0.1.0 |
| Story 3: Browse entries | High | 0.0.1 / 0.1.0 |
| Story 4: Standardise | High | 0.0.1 / 0.1.0 |
| Story 5: Retro entries | Medium | 0.1.0 |
| Story 6: Auto-generated index | Medium | 0.1.0 |
