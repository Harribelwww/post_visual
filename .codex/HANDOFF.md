# Working Context

Last updated: 2026-07-13
Status: standby

## Current Goal

Preserve the completed general scientific plotting core and use it as the foundation for future thin domain recipes.

## Scope

- Primary workspace: `C:\Users\HARRIBELWWW\Desktop\tmp\post_visual`
- Editable area: current workspace only

## Current State

- General scientific plotting core is complete; see `docs/decisions/0003-general-core-closure.md`.
- The 10 public research recipes are cleanly closed: exports, tests, and 11 recipe example figures were audited on 2026-07-13.
- Added multi-panel layouts, panel labels, grayscale/RGB(A) image plots, and image grids.
- Added text/arrow/significance annotations and point-range/forest-style summaries.
- Added KDE, ECDF, and deterministic-jitter strip views.
- Added Line confidence bands, Scatter regression confidence intervals, marker mapping, and explicit missing-data policies.
- Added percentage/scientific formatting, shared legends, secondary axes, and inset axes.
- Refactored `model_comparison` to reuse `grouped_bar`; `feature_importance` already reuses bar primitives.
- Stable verification baseline: Docker `66 passed`; all 31 example figures generated.
- Ruff passes across `src`, `tests`, and `examples`.

## Required Reading

- `AGENTS.md`
- `.codex/WORKSPACE.md`
- `docs/INDEX.md`
- `.codex/tasks/post-visual-toolkit.md`
- `docs/architecture/toolkit-architecture.md`

## Changed Files

- `src/post_visual/core/__init__.py`: removed a duplicate import/`__all__` assignment and restored complete core exports.
- `tests/test_intervals.py`: removed an unused NumPy import found by the final Ruff audit.
- `src/post_visual/core/layout.py`, `core/axes.py`: panel and axes composition helpers.
- `src/post_visual/plots/image.py`: single-image and image-grid primitives.
- `src/post_visual/plots/annotations.py`, `intervals.py`, `distributions.py`: general annotation, point-range, KDE/ECDF/strip enhancements.
- `src/post_visual/plots/line.py`, `scatter.py`: confidence and missing-data enhancements.
- `src/post_visual/recipes/comparison.py`: grouped-bar reuse.
- `src/post_visual/__init__.py`, `plots/__init__.py`, `core/__init__.py`: public exports.
- `tests/`: focused coverage expanded to 66 passing tests.
- `examples/`: five new example groups; 31 generated figures total.
- `README.md`, `docs/INDEX.md`, architecture/catalog/decision docs: durable core-closure documentation.
- `.codex/WORKSPACE.md`, `.codex/tasks/post-visual-toolkit.md`, `.codex/manifest.yaml`: synchronized continuity and routing facts.

## Commands Run

- `ruff check src tests examples` in isolated Docker: passed.
- `python -m compileall -q src tests examples`: passed.
- Relevant example groups through `conda run -n pp`: passed.
- `scripts/test-docker.ps1`: `66 passed`; all 31 examples generated.
- Visual inspection: all new and materially changed examples passed.
- `.codex/workflows/validate-doc-paths.ps1`: passed after documentation updates.

## Verification State

- Passed: Ruff, compile, 66-test Docker suite, 31 example generators (including all 11 recipe figures), visual inspection, documentation path validation, continuity audit, and route-sync audit.
- Failed: none.
- Git: clean `main` tracking `origin/main` after the initial GitHub sync.

## Risks / Open Questions

- Swarm collision layout and broken axes are deliberately outside the core; see Decision 0003.
- Domain recipes such as signal traces and spectrograms remain optional follow-up work.

## Next Steps

1. Preserve the `66 passed / 31 examples` baseline.
2. Add signal traces or spectrograms only as thin recipes when requested.
3. Keep domain dependencies optional and promote new durable decisions to `docs/decisions/`.
