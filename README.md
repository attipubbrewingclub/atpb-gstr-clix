# atpb-gstr-clix

atpb-gstr command-line utilities.

## Install

From the repo root:

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

**Windows:** use `venv\Scripts\activate` (cmd) or `venv\Scripts\Activate.ps1` (PowerShell) instead of `source`.

The `dev` extra adds **pytest** and **ruff** (lint + format). For a minimal editable install without those tools, use `pip install -e .`.

## Uninstall

```bash
pip uninstall atpb-gstr-clix
deactivate
```

Delete `venv` when done: `rm -rf venv` (Unix) or `Remove-Item -Recurse -Force .\venv` (PowerShell). To clear wheels/sdists from a local build, remove `dist`: `rm -rf dist` (Unix) or `Remove-Item -Recurse -Force .\dist` (PowerShell).

## Usage

Requires **Python 3.9+**. With the environment active, either run the installed script or the module:

```bash
atpb-gstr-clix --vrsn
# equivalent:
python -m atpb_gstr_clix --vrsn
```

`--vrsn`: version (Git + setuptools-scm, or fallback — see **Build**), `[dev]`/`[prod]`, and wheel build UTC time or `local` when editable.

Generate a 63-character S3 bucket GUID (single line on stdout). PRFX must match `--vldt` rules (lowercase `xxxx` groups separated by hyphens).

```bash
atpb-gstr-clix --s3bx --guid --newx PRFX
```

Validate one:

```bash
atpb-gstr-clix --s3bx --guid --vldt GUID
```

## Tests

With the `dev` extra installed:

```bash
pytest
```

From the repo root (with `dev` installed), optional checks:

```bash
ruff check .
ruff format --check .
```

Use `ruff format .` to apply formatting.

## Build

**Version:** setuptools-scm at `python -m build` time from Git tags (e.g. `git tag v0.2.0`); without Git, `fallback_version` in `pyproject.toml` (must match `PKG_VERSION_FALLBACK` in `atpb_gstr_clix/commands/constants.py`). **Timestamp:** `setup.py` writes UTC into the wheel.

1. `pytest` (and optionally `ruff check .` / `ruff format --check .`)
2. `python -m build` (after `pip install build` once). Output: `dist/`.

Smoke-test install (real path under `dist/`):

PowerShell:

```powershell
pip install (Get-Item dist\*.whl | Select-Object -First 1)
```

Bash (one wheel in `dist/`):

```bash
pip install dist/atpb_gstr_clix-*-py3-none-any.whl
```

CI without tags: set `SETUPTOOLS_SCM_PRETEND_VERSION` before `python -m build` ([setuptools-scm overrides](https://setuptools-scm.readthedocs.io/en/latest/overrides/)).

Publish (with `twine` installed): `twine check dist/*` then `twine upload dist/*`.
