# Decision 0002: Primitives Before Recipes

Date: 2026-07-13

## Decision

`post_visual` is primarily a library of small, composable scientific plotting primitives. Research and domain-specific functions remain supported as thin recipes built from those primitives.

Before adding more domain recipes, the project will complete a primitive-gap audit and move reusable drawing behavior out of recipes where appropriate.

## Layer Boundaries

### Core and Style

Own figure creation, axes treatment, palettes, annotations, validation, legends, colorbars, layouts, and export behavior.

### Plot Primitives

Own reusable visual marks and coordinate systems, including line, scatter, vertical/horizontal bars, distributions, error bars, interval bands, heatmaps, regular-grid color plots, image grids, and common annotations.

Primitives answer “how should this mark be drawn?” They should not assume EEG, model evaluation, diagnosis, SHAP, or another research domain.

### Recipes

Own input normalization and domain semantics for recurring research figures. Recipes should delegate drawing to primitives and preserve Matplotlib escape hatches.

Examples:

```text
heatmap + mask + centered colors   -> connectivity_matrix
horizontal_bar + sorting          -> feature_importance
line + offsets + event spans       -> signal_traces
grid color plot + colorbar         -> spectrogram
scatter + group summaries          -> embedding
```

### Test Infrastructure

Visual regression baselines validate stable appearance. They are not user-facing plot APIs.

## Inclusion Test for New Recipes

A new recipe is justified only when it:

1. represents a recurring research task rather than one paper’s fixed layout;
2. reuses existing primitives for most drawing behavior;
3. adds meaningful input normalization or domain semantics;
4. accepts `ax`, returns `(fig, ax)`, and exposes local overrides;
5. does not add heavy mandatory dependencies to the core package.

If a recipe needs substantial new drawing logic, the reusable part should be implemented as a primitive first.

## Consequences

- Existing recipes remain public and supported.
- `connectivity_matrix` remains a thin recipe over heatmap behavior.
- `feature_importance` should be refactored after a reusable horizontal/grouped bar primitive exists.
- Signal traces and spectrograms are paused until offset-line/event-span and regular-grid color primitives are available.
- Attention maps, convolution kernels, and activation views are deferred until image/grid primitives are mature.
- The next implementation stage is “primitive completion and recipe slimming,” not additional domain breadth.
