# Setup Notes

This repository now contains the first `post_visual` Python package MVP with style primitives, figure/export helpers, line, scatter, grouped-bar, distribution, heatmap, and research-result recipe primitives.

## Expected Environment

- Python 3.10 or newer.
- Matplotlib-based local plotting environment.
- Optional LaTeX installation only when true `usetex=True` rendering is needed.

## Standard Local Install

Use a normal Python 3.10+ environment for development. On Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup-dev.ps1
```

Equivalent manual commands:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Use `python -m ...` commands from the same interpreter that installed the package:

```bash
python -m pytest
python examples/line_mvp.py
python examples/primitives_mvp.py
python examples/second_batch_mvp.py
python examples/recipes_mvp.py
python examples/comparison_recipes.py
python examples/interpretation_recipes.py
python examples/signal_recipes.py
```

Avoid calling a conda environment's `python.exe` directly from its filesystem path on Windows. Activate the environment or use `conda run -n <env> python ...` so native DLL search paths are configured correctly.

## Docker Test Path

Use Docker as the default build-stage dependency and test environment:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-docker.ps1
```

The script pulls `python:3.12-slim`, mounts the repository at `/workspace`, installs `.[dev]`, runs `pytest`, and generates the MVP example figures inside the mounted workspace.

For temporary figure generation with local host data mounted into a throwaway container, see `docs/setup/temporary-docker-plotting.md`.

Manual equivalent:

```bash
docker pull python:3.12-slim
docker run --rm -v "$PWD:/workspace" -w /workspace -e MPLBACKEND=Agg -e PIP_ROOT_USER_ACTION=ignore python:3.12-slim sh -lc "python -m pip install --upgrade pip && python -m pip install -e '.[dev]' && python -m pytest -p no:cacheprovider && python examples/line_mvp.py && python examples/primitives_mvp.py && python examples/second_batch_mvp.py && python examples/recipes_mvp.py && python examples/comparison_recipes.py && python examples/interpretation_recipes.py"
```

## Optional Extras

```bash
python -m pip install -e ".[signal]"
python -m pip install -e ".[image]"
python -m pip install -e ".[explain]"
python -m pip install -e ".[embedding]"
```

## Development Checks

- Unit tests: `python -m pytest`
- Example figure generation includes `examples/line_mvp.py`, `examples/primitives_mvp.py`, `examples/second_batch_mvp.py`, `examples/recipes_mvp.py`, `examples/comparison_recipes.py`, `examples/interpretation_recipes.py`, and `examples/signal_recipes.py`.
- Docker verification: `powershell -ExecutionPolicy Bypass -File scripts/test-docker.ps1`
- Temporary Docker plotting: `docs/setup/temporary-docker-plotting.md`
- Documentation path check: `powershell -ExecutionPolicy Bypass -File .codex/workflows/validate-doc-paths.ps1`
