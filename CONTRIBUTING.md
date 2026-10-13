# Contributing to ai-color-palette-generator

Thanks for wanting to mash some new taters into the palette pot. This repo
is a modular toolkit — feature modules live under `palette_gen/`, shared
primitives under `palette_gen/utils/`, and every extension point is a
handler or a service.

## Dev setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

## Project layout

- `palette_gen/handlers/` — CLI and file-format handlers (one class per format)
- `palette_gen/services/` — orchestration services (extraction, harmony, scoring)
- `palette_gen/models/` — dataclasses and typed schema for palettes, swatches, config
- `palette_gen/utils/` — color math, image loading, logging, caching
- `palette_gen/config/` — TOML defaults and schema validation

## Adding a new export format

1. Drop a handler in `palette_gen/handlers/` subclassing `BaseExportHandler`.
2. Register it in `palette_gen/handlers/__init__.py`.
3. Add a fixture under `tests/fixtures/`.
4. Run `pytest -q` and `ruff check`.

## Style

- `ruff` and `black` are the law. Line length 100.
- Type hints everywhere. `mypy --strict` must pass on `palette_gen/`.
- No silent `except Exception`. Log and re-raise, or handle narrowly.
- Name things after what they hold. `data` is not a name, it is a cry for help.

## Commit messages

`scope: short imperative summary` — e.g. `harmony: add tetradic generator`.

## PR checklist

- [ ] Tests added or updated
- [ ] `pytest -q` green
- [ ] `ruff check` and `mypy` clean
- [ ] No new hard-coded paths
- [ ] Changelog entry under `## Unreleased`