# Task Capsule: post_visual toolkit

## Goal

Maintain `post_visual` as a Matplotlib-first, primitive-first visualization toolkit with a completed general core and thin research recipes.

## Done When

- Core style, plotting primitives, and research-result recipes cover the priority plot catalog.
- Reusable drawing behavior lives in `plots/` or `core/`; recipes remain thin and compositional.
- High-level plotting functions accept `ax` and return `(fig, ax)`.
- Docker verification passes.
- Durable docs and continuity files are current.

## Relevant Files

- `src/post_visual/`
- `tests/`
- `examples/`
- `scripts/test-docker.ps1`
- `README.md`
- `docs/INDEX.md`
- `docs/architecture/toolkit-architecture.md`
- `docs/architecture/plot-catalog.md`
- `docs/setup/README.md`
- `.codex/WORKSPACE.md`
- `.codex/HANDOFF.md`

## Relevant Docs

- `docs/architecture/toolkit-architecture.md`
- `docs/architecture/plot-catalog.md`
- `docs/decisions/0001-initial-toolkit-scope.md`
- `docs/decisions/0002-primitives-before-recipes.md`
- `docs/decisions/0003-general-core-closure.md`
- `docs/setup/README.md`

## Decisions Already Made

- Package name: `post_visual`.
- Recommended import alias: `pv`.
- Build-stage verification: Docker-first through `scripts/test-docker.ps1`.
- Local Python install is retained through `scripts/setup-dev.ps1` for interactive work.
- Core dependencies stay lightweight; EEG, imaging, explainability, and embedding dependencies stay optional.
- `sci_plot.m` is a style baseline, not production Python code.
- New domain recipes require a recurring task, meaningful semantics, primitive reuse, Matplotlib escape hatches, and no heavy mandatory dependency.
- The general core is complete; swarm collision layout and broken-axis orchestration are deliberately deferred.

## Known Dead Ends

- The active default Python environment lacks matplotlib, so local `python -m pytest` is not useful until dependencies are installed.
- Directly invoking a conda environment's `python.exe` by filesystem path on Windows can miss native DLL search paths. Use Docker, activated conda, or `conda run`.

## Phase Plan

1. Done: style layer, export helpers, line plot, scatter plot, grouped bars, distributions, heatmaps, confusion matrix, ROC/PR, training curves, tests, and examples.
2. Done: ablation, model comparison, and calibration.
3. Done: embeddings and feature importance.
4. Done: connectivity matrix as a thin heatmap specialization.
5. Done: primitive-gap audit, image/image-grid support, multi-panel layouts, point-range summaries, distribution enhancements, Line/Scatter confidence support, and axes helpers.
6. Done: recipe audit and `model_comparison` refactor onto `grouped_bar`.
7. Deferred until requested: signal traces, spectrograms, attention maps, activation views, and kernel visualizations.

## Current Phase

The general scientific plotting core and the 10 existing public recipes closed cleanly on 2026-07-13. The verified baseline is Ruff-clean with `66 passed`, 31 total example figures, and 11 recipe example figures.

## Current Verification Baseline

- Ruff passes across `src`, `tests`, and `examples`.
- Docker verification through `scripts/test-docker.ps1` passed with `66 passed`.
- The Docker path generated all 31 core and recipe example figures.
- Documentation and continuity audits are clean; `main` is synchronized with the GitHub origin.

## Next Step

Preserve the completed core baseline. Add a thin signal-trace or spectrogram recipe only when a concrete user task requests it.
