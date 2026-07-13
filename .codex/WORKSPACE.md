# Workspace Overview

## Purpose

This workspace is for designing and implementing `post_visual`, a Python visualization toolkit for data-science research results with a consistent scientific style.

## Current State

- Existing style baseline: `sci_plot.m`.
- Durable documentation skeleton exists under `docs/`.
- Continuity skeleton exists under `.codex/`.
- Python package MVP exists under `src/post_visual/`.
- The implemented surface includes the completed general scientific plotting core, composition/layout helpers, and thin metric/training/comparison/interpretation/connectivity recipes.
- Standard local setup uses `scripts/setup-dev.ps1`.
- Default build-stage verification uses isolated Docker via `scripts/test-docker.ps1`.
- Current closed baseline includes 66 passing Docker tests and 31 generated example figures.

## Design Direction

The package should provide:

- a complete set of small, composable data-science plotting primitives
- thin research-result recipes built from those primitives
- consistent style templates
- flexible local overrides
- optional domain-specific extensions

Primitive-first is the governing architecture. The general core is closed; new domain recipes should compose existing primitives and pass the inclusion test. See `docs/decisions/0002-primitives-before-recipes.md` and `docs/decisions/0003-general-core-closure.md`.

The base style is derived from `sci_plot.m`: publication-style white background, serif fonts, LaTeX-like math rendering, restrained palettes, black axes, minor ticks, low-alpha grid, and consistent export defaults.

## Important Docs

- `README.md`: human landing page.
- `docs/INDEX.md`: canonical documentation route index.
- `docs/architecture/toolkit-architecture.md`: planned package architecture.
- `docs/architecture/plot-catalog.md`: supported plot types and priorities.
- `docs/decisions/0001-initial-toolkit-scope.md`: initial scope, naming, style, and API decisions.
- `docs/decisions/0002-primitives-before-recipes.md`: primitive-first layering and revised roadmap.
- `docs/decisions/0003-general-core-closure.md`: completed core boundary and deliberate deferrals.
- `.codex/HANDOFF.md`: current active working context.

## Environment Notes

- Workspace root: `C:\Users\HARRIBELWWW\Desktop\tmp\post_visual`
- Current source file: `sci_plot.m`
- Current date when skeleton was created: 2026-07-09
- This workspace may not be a git repository.

## Next Implementation Direction

1. Preserve the completed compositional core and the `66 passed` Docker baseline.
2. Add signal traces or spectrograms only as thin recipes when requested.
3. Keep heavy EEG, imaging, and explainability dependencies optional.
4. Add visual-regression baselines when stable appearance needs automated enforcement.
