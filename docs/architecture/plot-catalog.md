# Plot Catalog

This catalog records the figure types `post_visual` should support. It is based on common data-science practice and the research-paper figure set reviewed during the initial design.

Concept diagrams, model architecture cartoons, and workflow schematics are intentionally excluded from the core plotting target.

## Mainstream Data-Science Primitives

- Line plots, including linear, semilog-x, semilog-y, and log-log scales.
- Scatter plots with optional hue, size, marker, regression line, and confidence band.
- Bar and grouped bar plots.
- Errorbar plots and point estimates with confidence intervals. Implemented through `pv.errorbar` and `pv.interval_band`.
- Histogram and KDE plots.
- Box, violin, deterministic-jitter strip, KDE, and ECDF distribution plots.
- Heatmaps with annotations and colorbars.
- Regular-grid color plots with continuous coordinates and centered color normalization.
- Image grids and simple overlays, including shared/per-image colorbars.
- Regular multi-panel layouts with shared axes, panel labels, hidden extras, and constrained spacing.
- Annotation helpers for text, arrows, local callouts, thresholds, event spans, and significance brackets.
- Axes helpers for percentage/scientific formatting, shared legends, secondary axes, and insets.

## Research-Result Recipes

- Training curves: loss, accuracy, learning rate, and convergence comparison.
- Calibration and reliability plots.
- Confusion matrices, including normalized and unnormalized modes.
- Model comparison tables rendered as bars or point-range plots.
- Ablation and sensitivity plots.
- Hyperparameter curves.
- Subject-wise or fold-wise performance distributions.
- Computational cost plots: runtime, memory, FLOPs, parameters.

## EEG / Biosignal Result Views

- Multi-channel EEG, iEEG, ECG, or PSG traces.
- Event-highlighted signal windows.
- Time-frequency maps and spectrograms.
- FFT or frequency-domain comparison.
- Connectivity or adjacency matrices.
- Difference matrices across classes or conditions.

## Neural-Network Analysis Views

- Embedding plots: PCA, t-SNE, and UMAP.
- Feature importance bars, including SHAP-style summaries.
- Attention maps and self-attention matrices.
- Spatial and temporal convolution kernel visualizations.
- Feature maps and activation overlays.

## Priority Order

1. Preserve: current tested style, primitives, and public recipes.
2. Preserve the completed general scientific plotting core and its compositional APIs.
3. Keep recipes thin; `feature_importance` and `model_comparison` reuse bar primitives, while connectivity remains a heatmap specialization.
4. Next domain recipes when requested: signal traces and spectrograms over line/event/grid-color primitives.
5. Deferred from core: swarm collision layout and broken axes because they require substantially more layout state and edge-case policy.
6. Deferred domain work: attention maps, kernels, activations, and optional image/explainability integrations.

The catalog lists both primitives and possible recipes, but listing a domain view does not automatically authorize a new standalone API. Apply the inclusion test in `docs/decisions/0002-primitives-before-recipes.md` first.
