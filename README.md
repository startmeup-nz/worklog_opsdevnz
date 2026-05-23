# OpsDev.nz Module Template

The standard starting point for every OpsDev.nz Python module — CI, automated
PyPI publishing, dependency scanning, and a clean project scaffold under
Apache-2.0. Clone it, rename the placeholders, and start building.

## Using this template

When creating a new module from this template, replace all `YOUR-MODULE` /
`YOUR_MODULE` / `template_opsdevnz` placeholders with the actual module name.

### Quick find-and-replace checklist

- [ ] `pyproject.toml`: name, description, keywords, URLs, entry point, coverage path
- [ ] `src/template_opsdevnz/` → rename to `src/<function>_opsdevnz/`
- [ ] `src/<module>/cli.py`: update version string
- [ ] `README.md`: replace with module-specific content
- [ ] `CHANGELOG.md`: reset to module-specific changelog

### After replacing placeholders

```bash
uv pip install -e ".[dev]"
uv run pytest
```

## Included in this template

- `pyproject.toml` — Apache-2.0, Python >= 3.12, Click, pytest/ruff/mypy dev deps
- `LICENSE` — Apache-2.0
- `SECURITY.md` — Reporting policy
- `CHANGELOG.md` — Keep a Changelog format
- `.github/workflows/test.yml` — CI on push/PR (py3.12-3.14)
- `.github/workflows/publish.yml` — PyPI publish on tag (Trusted Publishing)
- `.github/dependabot.yml` — Weekly pip updates
- `src/template_opsdevnz/cli.py` — Click CLI scaffold
- `tests/test_cli.py` — Click test example
