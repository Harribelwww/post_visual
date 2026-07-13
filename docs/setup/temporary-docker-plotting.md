# Temporary Docker Plotting Guide

Use this guide when you want to make figures with `post_visual` in a temporary Docker container without creating a dedicated project image.

## Assumptions

- Run commands from the workspace root:

```powershell
C:\Users\HARRIBELWWW\Desktop\tmp\post_visual
```

- Docker Desktop is running.
- The container is non-interactive and headless, so scripts should save figures instead of calling `plt.show()`.

## Run An Existing Example

This mounts the current workspace into `/workspace`, installs the package, and runs one example script:

```powershell
docker run --rm `
  -v "${PWD}:/workspace" `
  -w /workspace `
  -e MPLBACKEND=Agg `
  -e PIP_ROOT_USER_ACTION=ignore `
  python:3.12-slim `
  sh -lc "python -m pip install --upgrade pip && python -m pip install -e . && python examples/recipes_mvp.py"
```

Generated figures are written back to the host under:

```text
examples/out/
```

## Run A Custom Plot Script

Create a script in the workspace, for example:

```text
scratch/my_plot.py
```

Example script:

```python
from pathlib import Path

import pandas as pd

import post_visual as pv

output_dir = Path("/workspace/scratch/out")
output_dir.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(
    {
        "epoch": [1, 2, 3, 4],
        "loss": [1.0, 0.7, 0.5, 0.4],
        "val_loss": [1.1, 0.8, 0.62, 0.55],
    }
)

fig, ax = pv.training_curves(df, metrics=["loss", "val_loss"], ylabel="Loss")
pv.save_figure(fig, output_dir / "training.png")
```

Run it:

```powershell
docker run --rm `
  -v "${PWD}:/workspace" `
  -w /workspace `
  -e MPLBACKEND=Agg `
  -e PIP_ROOT_USER_ACTION=ignore `
  python:3.12-slim `
  sh -lc "python -m pip install --upgrade pip && python -m pip install -e . && python scratch/my_plot.py"
```

The figure will appear on the host at:

```text
scratch/out/training.png
```

## Use Local Data

Mount any host data directory into the container with another `-v` argument.

Example host data directory:

```text
C:\Users\HARRIBELWWW\Desktop\data
```

Command:

```powershell
docker run --rm `
  -v "${PWD}:/workspace" `
  -v "C:\Users\HARRIBELWWW\Desktop\data:/data" `
  -w /workspace `
  -e MPLBACKEND=Agg `
  -e PIP_ROOT_USER_ACTION=ignore `
  python:3.12-slim `
  sh -lc "python -m pip install --upgrade pip && python -m pip install -e . && python scratch/my_plot.py"
```

Inside Python, read files through the container path:

```python
import pandas as pd

df = pd.read_csv("/data/results.csv")
```

Write outputs under `/workspace/...` if you want them to appear in the current repository on the host:

```python
pv.save_figure(fig, "/workspace/scratch/out/figure.png")
```

## Run With Dev Dependencies

Use this when your temporary script also needs test or development dependencies:

```powershell
docker run --rm `
  -v "${PWD}:/workspace" `
  -w /workspace `
  -e MPLBACKEND=Agg `
  -e PIP_ROOT_USER_ACTION=ignore `
  python:3.12-slim `
  sh -lc "python -m pip install --upgrade pip && python -m pip install -e '.[dev]' && python scratch/my_plot.py"
```

## Full Verification Container

To rerun the project verification path:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-docker.ps1
```

This installs dev dependencies, runs pytest, and generates all MVP examples.

## Notes

- The temporary container installs dependencies every run. Use a dedicated Dockerfile later if startup time becomes a problem.
- Use container paths in Python, such as `/workspace/...` and `/data/...`.
- Use `MPLBACKEND=Agg` for headless figure saving.
- Save figures as PNG, PDF, or SVG; do not rely on GUI display.
