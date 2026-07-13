# Handoff: comparison, ablation, and calibration recipes

Date: 2026-07-12

## Goal

Implement the next research-result recipe set using visualization patterns from two user-provided EEG papers.

## Done

- Added `pv.model_comparison`, `pv.ablation`, and `pv.calibration_curve`.
- Added focused tests and paper-inspired synthetic examples.
- Generated and visually inspected all three new figures.
- Updated public documentation and continuity surfaces.
- Fixed Docker verification to propagate external-command failures.
- Refined best-result highlighting to a normal-width red border instead of a thick black outline.

## In Progress

- Nothing; this recipe stage is closed.

## Git State

Git commands remain unavailable because the workspace `.git` metadata is invalid.

## Blockers

None. Docker Desktop was started and the full verification completed.

## Verification

- Compile: passed.
- New recipe behavior assertions: passed.
- All five example groups: passed.
- Visual inspection: passed.
- Docker pytest: passed with `24 passed`; all 13 examples generated.

## Next Entry Point

Start the embedding and feature-importance stage while preserving the `24 passed` Docker baseline.
