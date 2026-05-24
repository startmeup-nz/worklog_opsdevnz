# Release Process

This module uses **Trusted Publishing (OIDC)** to publish to PyPI — no API tokens,
no rotating secrets. GitHub's OIDC identity is verified by PyPI at publish time.

## Setup (one-time per PyPI index)

### 1. Create the project on Test PyPI

Go to <https://test.pypi.org/manage/projects/> and create a new project named
`worklog-opsdevnz`. You only need to do this once — the workflow will push
subsequent versions to this project.

### 2. Configure Trusted Publishing on Test PyPI

1. Go to <https://test.pypi.org/manage/project/worklog-opsdevnz/settings/publishing/>
2. Fill in the pending publisher form:

   | Field | Value |
   |-------|-------|
   | Owner | `startmeup-nz` |
   | Repository name | `worklog-opsdevnz` |
   | Workflow name | `publish.yml` |
   | Environment name | `test-pypi` |

3. Click **Add**.

### 3. Create the project on real PyPI

Go to <https://pypi.org/manage/projects/> and create `worklog-opsdevnz`.

### 4. Configure Trusted Publishing on real PyPI

1. Go to <https://pypi.org/manage/project/worklog-opsdevnz/settings/publishing/>
2. Fill in:

   | Field | Value |
   |-------|-------|
   | Owner | `startmeup-nz` |
   | Repository name | `worklog-opsdevnz` |
   | Workflow name | `publish.yml` |
   | Environment name | `pypi` |

3. Click **Add**.

### 5. Create GitHub environments

In the repo **Settings → Environments**, create two environments if they don't
already exist:

- **`test-pypi`** — no secrets needed (OIDC handles it)
- **`pypi`** — no secrets needed (OIDC handles it)

The workflow already references these environments — they just need to exist.

## How a release works

1. Bump `version` in `pyproject.toml` and update `CHANGELOG.md`.
2. Merge to `main`.
3. Tag the release: `git tag v0.1.0 && git push origin v0.1.0`.
4. The `publish.yml` workflow fires:
   - **`test-pypi` job**: Builds wheel, publishes to Test PyPI, installs from Test PyPI
     in a clean venv, runs `worklog-opsdevnz --version` as a smoke test.
   - **`pypi` job** (depends on `test-pypi` passing): Builds wheel, publishes to real PyPI.

If the Test PyPI publish or smoke test fails, the real PyPI publish is **aborted**.
This is the quality gate described in NFR-8.2.

## First release checklist

Since this is the first publish:

- [ ] Project `worklog-opsdevnz` created on Test PyPI
- [ ] Project `worklog-opsdevnz` created on real PyPI
- [ ] Trusted Publishing configured on Test PyPI
- [ ] Trusted Publishing configured on real PyPI
- [ ] GitHub environments `test-pypi` and `pypi` exist
- [ ] Version bumped in `pyproject.toml`
- [ ] CHANGELOG.md updated
- [ ] Tag pushed
