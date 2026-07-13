# Decision 0003: General Scientific Plotting Core Closure

Date: 2026-07-13

## Decision

The general scientific plotting core is complete after adding multi-panel layouts, image grids, general annotations, point-range summaries, distribution enhancements, Line/Scatter confidence support, and common axes helpers.

New work should normally compose these primitives. Domain-specific APIs remain justified only when they add recurring input normalization or semantics under the recipe inclusion test in Decision 0002.

## Completed Boundary

- Figure and axes lifecycle, export, multi-panel layouts, panel labels, shared legends, tick formatting, secondary axes, and inset axes.
- Lines, scatter, bars, distributions, point estimates, errors, intervals, categorical/continuous matrix colors, and grayscale/RGB(A) images.
- Text, arrows, significance brackets, event lines, thresholds, and highlighted spans.
- Confidence bands for single lines and confidence intervals for grouped linear fits.
- Explicit missing-data policies for Line and Scatter.
- Thin recipes for metrics, training, comparison, ablation, embedding, feature importance, calibration, and connectivity matrices.

## Deliberate Deferrals

- Swarm collision layout is not a separate core primitive. Deterministic-jitter `strip` provides raw-sample overlays without introducing a collision solver and unstable layout edge cases.
- Broken-axis support is not a core helper. Reliable broken axes require synchronized limits, spines, ticks, legends, annotations, and export layout across multiple axes; direct Matplotlib remains available.
- Signal traces, spectrograms, attention maps, kernels, and activations remain recipes or optional domain layers rather than core primitives.

## Consequences

- The primitive-completion phase is closed.
- Future core changes require a demonstrated recurring gap rather than a single-paper layout.
- Signal traces can compose line, offsets, and event annotations.
- Spectrograms can compose grid-color rendering and colorbar controls.
- Image and explainability views can compose image grids and multi-panel layouts without heavy mandatory dependencies.
