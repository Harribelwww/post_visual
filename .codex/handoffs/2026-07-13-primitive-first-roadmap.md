# Handoff: primitive-first roadmap adjustment

Date: 2026-07-13

## Goal

Realign `post_visual` with its original purpose: foundational plotting components first, advanced customization through composition, and thin domain recipes.

## Done

- Added Decision 0002 defining layer ownership and the inclusion test for recipes.
- Updated README, toolkit architecture, plot catalog, workspace overview, task capsule, manifest, docs index, and active handoff.
- Preserved all existing public APIs and the `33 passed` baseline.

## Decisions

- Do not add a new recipe merely because a paper contains a distinct figure.
- Move reusable drawing logic into `plots/` or `core/` first.
- Keep `connectivity_matrix` as a thin heatmap recipe.
- Add a horizontal/grouped-bar primitive and refactor `feature_importance` onto it.
- Pause new signal, spectrogram, attention, kernel, and activation APIs until primitive gaps are closed.
- Treat visual regression as verification infrastructure.

## In Progress

- Primitive-gap audit and recipe slimming.

## Verification

- Documentation and continuity validation must be rerun after this roadmap update.
- Code baseline remains the previously verified `33 passed` with 17 examples; no source code changed in this documentation-only update.

## Next Entry Point

Audit `src/post_visual/recipes/` against `src/post_visual/plots/`, then implement horizontal/grouped bars as the first missing primitive.
