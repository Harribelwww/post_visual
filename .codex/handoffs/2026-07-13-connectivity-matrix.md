# Handoff: connectivity matrix

Date: 2026-07-13

## Goal

Start the biosignal stage with a reusable connectivity-matrix recipe.

## Done

- Added `pv.connectivity_matrix` with triangle masks, annotations, labels, symmetry checks, and zero-centered difference scales.
- Added four tests and two examples.
- Fixed the Matplotlib 3.11 colormap warning.
- Updated durable docs and active context.

## In Progress

- Signal traces and spectrogram recipes.

## Git State

Git status is unavailable because repository metadata is invalid.

## Verification

- Docker: `33 passed`, warning-free.
- Examples: all 17 generated.
- Visual inspection: passed.

## Next Entry Point

Continue in `src/post_visual/recipes/signal.py` with multi-channel signal traces, followed by spectrograms.
