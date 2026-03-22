# atpb-gstr-clix

atpb-gstr command-line utilities.

Requires **Python 3.9+**.

## Install

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

**Windows:** `venv\Scripts\activate` (cmd) or `venv\Scripts\Activate.ps1` (PowerShell).

`[dev]` includes **pytest**, **ruff**, and **build**. For a slimmer editable install: `pip install -e .` (add `pip install build` if you need `python -m build`).

## Uninstall

```bash
pip uninstall atpb-gstr-clix
deactivate
```

Optional: remove `venv` or `dist` when you no longer need them (delete those folders).

```bash
rm -rf venv dist
```

**Windows:** `rmdir /s /q venv 2>nul & rmdir /s /q dist 2>nul` (cmd) or `Remove-Item -Recurse -Force .\venv, .\dist -ErrorAction SilentlyContinue` (PowerShell).

## Usage

```bash
atpb-gstr-clix --vrsn
python -m atpb_gstr_clix --vrsn   # same
```

`--vrsn` shows version (from Git via setuptools-scm, or fallback — see **Build**), install mode, and build timestamp (`local` when editable).

S3-style 63-character bucket GUID (stdout). Prefix must satisfy `--vldt` (lowercase `xxxx` groups, hyphens).

```bash
atpb-gstr-clix --s3bx --guid --newx PRFX
atpb-gstr-clix --s3bx --guid --vldt GUID
```

## Tests

```bash
pytest
ruff check .
ruff format --check .
```

`ruff format .` applies formatting. Needs `[dev]` (or install those tools yourself).

## Build

**Version:** setuptools-scm from Git tags at build time (e.g. `git tag v0.2.0`); with no Git, `fallback_version` in `pyproject.toml` — keep in sync with `PKG_VERSION_FALLBACK` in `atpb_gstr_clix/commands/constants.py`. **Timestamp:** `setup.py` writes UTC into wheels.

1. `pytest` (and optionally ruff, as above)
2. `python -m build` → `dist/`

**Smoke-test the wheel** (Bash expands `*`; PowerShell does not):

```powershell
pip install (Get-Item dist\*.whl | Select-Object -First 1)
```

```bash
pip install dist/atpb_gstr_clix-*-py3-none-any.whl
```

**CI without Git tags:** set `SETUPTOOLS_SCM_PRETEND_VERSION` before `python -m build` ([overrides](https://setuptools-scm.readthedocs.io/en/latest/overrides/)).

Not published to PyPI; use `dist/` locally or ship wheels however you prefer.
