# Toolkit Architecture

## Purpose

`post_visual` is a data-science visualization toolkit for research outputs. It should cover common plotting needs first, then add research-specific recipes for EEG, medical diagnosis, neural-network evaluation, and related workflows.

The package should not become a heavy domain viewer. EEG, medical imaging, and neural-network explainability support should remain optional modules layered on top of a lightweight plotting core.

## Design Constraints

- Fixed visual style by default.
- Flexible data and result customization.
- Matplotlib-first implementation.
- DataFrame-friendly APIs for data-science workflows.
- Every high-level plot should accept an existing `ax` and return `fig, ax`.
- Keep escape hatches through `plot_kws`, `legend_kws`, `colorbar_kws`, `save_kws`, or equivalent keyword dictionaries.
- Avoid one giant universal plotting function. Use small primitives and task-focused recipes.
- Implement reusable drawing behavior as primitives before adding new domain recipes.
- Keep recipes thin: normalize inputs, attach domain semantics, and delegate rendering.

## Layer Ownership

| Layer | Owns | Must avoid |
| --- | --- | --- |
| `style/` | palettes, fonts, rcParams, style contexts | domain-specific plot logic |
| `core/` | figure/axes lifecycle, annotations, validation, layouts, export | full plot recipes |
| `plots/` | reusable visual marks and coordinate systems | EEG, diagnosis, SHAP, or model-specific assumptions |
| `recipes/` | recurring research semantics and input normalization | duplicating reusable drawing implementations |

Recipes are valid public conveniences, but they are not evidence that every research figure needs a new API. Before a recipe grows, identify whether its drawing behavior belongs in a reusable primitive.

## Layered API

```text
post_visual/
  style/          # palettes, rcParams, style contexts, export defaults
  core/           # figure/axes helpers, validation, annotations, saving
  plots/          # mainstream plotting primitives
  recipes/        # research-result plotting recipes
  data/           # light adapters and example data helpers
```

## Template Model

```text
style template   -> palette, fonts, mathtext, axes, legend, grid, export
figure template  -> single-panel, multi-panel, paper, slide, square
plot recipe      -> ROC, confusion matrix, training curve, ablation, etc.
local override   -> labels, data grouping, colors, markers, ax, annotations
```

This keeps plots template-driven while preserving matplotlib-level control.

## Proposed Package Layout

```text
src/post_visual/
  __init__.py
  style/
    __init__.py
    palettes.py
    rc.py
    contexts.py
  core/
    __init__.py
    figure.py
    axes.py
    layout.py
    export.py
  plots/
    __init__.py
    line.py
    scatter.py
    bars.py
    distributions.py
    matrix.py
    image.py
    intervals.py
    annotations.py
  recipes/
    __init__.py
    metrics.py
    training.py
    comparison.py
    ablation.py
    embedding.py
    signal.py
    explainability.py
```

## Implemented MVP

The current package implements the plotting foundation:

- `style/`: named Furina/Nilou palettes, scientific rcParams, and scoped style contexts.
- `core/`: figure/axes lifecycle, panel layouts and labels, formatting, shared legends, secondary/inset axes, and saving.
- `plots/line.py`: scale aliases, confidence bands, multi-series input, and gap/omit/raise NaN policies.
- `plots/scatter.py`: hue/size/marker mappings, regression confidence intervals, and omit/raise NaN policies.
- `plots/bars.py`: `pv.grouped_bar`, `pv.bar`, and `pv.horizontal_bar` for vertical/horizontal simple or grouped bars, errors, and annotations.
- `plots/intervals.py`: errors, interval bands, categorical point ranges, and forest-style summaries.
- `plots/annotations.py`: text, arrows, significance brackets, events, thresholds, and highlighted windows.
- `plots/distributions.py`: histograms, KDE, ECDF, box, violin, and jittered raw-sample strips.
- `plots/matrix.py`: `pv.heatmap` for categorical matrices and `pv.grid_color` for continuous-coordinate regular grids.
- `plots/image.py`: grayscale/RGB(A) images and image grids with shared or per-image colorbars.
- `recipes/metrics.py`: `pv.confusion_matrix`, `pv.roc_curve`, and `pv.pr_curve`.
- `recipes/training.py`: `pv.training_curves` for dict and DataFrame training histories.
- `recipes/comparison.py`: `pv.model_comparison` and `pv.ablation` for cross-dataset comparisons and component studies.
- `recipes/metrics.py`: also provides `pv.calibration_curve` with reliability bins and ECE labels.
- `recipes/interpretation.py`: `pv.embedding` and `pv.feature_importance` with NumPy-only PCA and precomputed-coordinate support.
- `recipes/signal.py`: `pv.connectivity_matrix` for symmetric, directed, triangular, and zero-centered difference matrices.

All high-level plotting functions accept `ax` and return `(fig, ax)`.
Build-stage verification is Docker-first through `scripts/test-docker.ps1`.

## Style Baseline From `sci_plot.m`

- White figure background.
- Figure size near `16 x 12 cm` for standard plots.
- Serif text, with Times-like font preference.
- STIX/mathtext-style formula rendering by default.
- Optional real LaTeX rendering through `usetex=True`.
- Black axes, visible box, minor ticks.
- Restrained dashed grid with low alpha.
- Line width around `1.5`.
- Hollow markers with white fill.
- Furina and Nilou palettes as first named palettes.

## Dependency Policy

Core dependencies should stay lightweight:

```toml
dependencies = [
  "numpy",
  "pandas",
  "scipy",
  "matplotlib",
  "seaborn",
  "scikit-learn",
]
```

Optional extras:

```toml
[project.optional-dependencies]
signal = ["mne"]
image = ["scikit-image", "nibabel", "pydicom"]
explain = ["captum", "shap"]
embedding = ["umap-learn"]
dev = ["pytest", "pytest-mpl", "ruff"]
```

## Implementation Phases

1. Done: build style layer, export helpers, and line plot MVP.
2. Done: add scatter and grouped-bar primitives.
3. Done: add distributions and heatmaps.
4. Done: add confusion matrix, ROC/PR, and training curves.
5. Done: add ablation, model comparison, and calibration recipes.
6. Done: add embedding and feature-importance recipes.
7. Done: connectivity-matrix recipe as a thin heatmap specialization.
8. Done: close primitive gaps with bars, intervals, annotations, continuous grid colors, image grids, and multi-panel layouts.
9. Done: add point ranges, KDE/ECDF/strip views, Line/Scatter confidence support, and axes helpers.
10. Done: slim `feature_importance` and `model_comparison` onto shared bar primitives; keep connectivity as a heatmap specialization.
11. Next: implement signal traces and spectrograms as thin recipes when requested.
12. Deferred: swarm collision layout, broken axes, attention maps, kernels, activations, and broader optional integrations.

The layering decision is recorded in `docs/decisions/0002-primitives-before-recipes.md`; the completed core boundary and deliberate deferrals are recorded in `docs/decisions/0003-general-core-closure.md`.
