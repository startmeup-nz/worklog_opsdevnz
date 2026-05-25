# Release Process

This module uses **Trusted Publishing (OIDC)** to publish to PyPI.

## GitHub environments

In the repo **Settings → Environments**, there are two environments:

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

If the Test PyPI publish or smoke test fails, the real PyPI publish is
**aborted**.  This is the quality gate described in NFR-8.2.
