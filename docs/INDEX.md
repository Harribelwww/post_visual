# Documentation Index

## Start Here

- [Project landing page](../README.md)
- [Workspace overview](../.codex/WORKSPACE.md)
- [Active working context](../.codex/HANDOFF.md)

## Architecture

- [Architecture docs index](architecture/README.md)
- [Toolkit architecture](architecture/toolkit-architecture.md)
- [Plot catalog and prioritization](architecture/plot-catalog.md)

## Setup / Operations

- [Setup notes](setup/README.md)
- [Native WSL runtime](setup/wsl-native-runtime.md)
- [Completed WSL migration record](setup/wsl-migration.md)
- [Fixed LaTeX environment snapshot](setup/latex-test-environment.md)
- [Environment declaration](../environment.yml)
- [Locked linux-64 environment](../conda-lock.yml)
- [WSL bootstrap script](../scripts/bootstrap-wsl.sh)
- [Ordinary WSL verification](../scripts/test-wsl.sh)
- [External-LaTeX WSL verification](../scripts/test-latex-wsl.sh)

## Development / Testing

- [Implementation phases](architecture/toolkit-architecture.md)
- [Python package configuration](../pyproject.toml)
- [Line MVP example](../examples/line_mvp.py)
- [Scatter and grouped-bar examples](../examples/primitives_mvp.py)
- [Event-line and event-span example](../examples/annotation_mvp.py)
- [Distribution and heatmap examples](../examples/second_batch_mvp.py)
- [Multi-panel and image-grid examples](../examples/layout_image_mvp.py)
- [General annotation and point-range examples](../examples/annotation_point_mvp.py)
- [KDE, ECDF, and strip-overlay examples](../examples/distribution_enhancements.py)
- [Line/scatter confidence-interval examples](../examples/line_scatter_enhancements.py)
- [Axes-helper example](../examples/axes_helpers_mvp.py)
- [MathText/vector/hybrid export smoke example](../examples/rendering_smoke.py)
- [Real-LaTeX per-module gallery](../examples/usetex_module_gallery.py)
- [Research-result recipe examples](../examples/recipes_mvp.py)
- [Model comparison, ablation, and calibration examples](../examples/comparison_recipes.py)
- [Embedding and feature-importance examples](../examples/interpretation_recipes.py)
- [Connectivity examples](../examples/signal_recipes.py)
- [Documentation hygiene workflow](../.codex/workflows/docs-hygiene.md)
- [Continuity maintenance workflow](../.codex/workflows/continuity-maintenance.md)

## Decisions

- [Decisions index](decisions/README.md)
- [Initial toolkit scope and style policy](decisions/0001-initial-toolkit-scope.md)
- [Primitive-first architecture and recipe policy](decisions/0002-primitives-before-recipes.md)
- [General scientific plotting core closure](decisions/0003-general-core-closure.md)
- [Historical Docker-only runtime](decisions/0004-docker-only-runtime-and-texlive.md)
- [Native WSL micromamba and TeX Live runtime](decisions/0005-native-wsl-micromamba-texlive.md)

## Existing Sources

- [MATLAB style baseline](../sci_plot.m)

## Archives / Avoid By Default

- No archived docs.
