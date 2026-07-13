# Handoff: embedding and feature importance

Date: 2026-07-12

## Goal

Add lightweight embedding and feature-importance visualization recipes.

## Done

- Added `pv.embedding` with precomputed-coordinate and NumPy PCA modes.
- Added centers, confidence ellipses, explained variance, and DataFrame support.
- Added `pv.feature_importance` with signed colors, grouped values, sorting, Top-K, error bars, and annotations.
- Added five tests and two example figures.
- Updated public docs, setup commands, task state, and active handoff.

## In Progress

- Nothing; the stage is closed.

## Git State

Git status is unavailable because the workspace metadata is invalid.

## Verification

- Docker: `29 passed`.
- Examples: all 15 generated.
- Visual inspection: passed.

## Next Entry Point

Implement signal traces, spectrograms, and connectivity matrices while preserving the current lightweight dependency policy.
