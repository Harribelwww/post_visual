# post_visual

`post_visual` is a Python visualization toolkit for data-science research results with a fixed scientific plotting style.

The first style baseline comes from `sci_plot.m`: serif typography, LaTeX-like math rendering, white figure background, clean black axes, restrained grid lines, reusable palettes, and publication-oriented export defaults.

## Current Scope

- Provide common plotting primitives for mainstream data science figures.
- Provide thin research-result recipes composed from those primitives.
- Keep visual style consistent while allowing data, grouping, statistics, labels, annotations, and axes to be customized.
- Keep domain-specific dependencies optional. EEG, medical imaging, and explainability plots should build on the core toolkit without making the base package heavy.

## Architecture Direction

The package is primitive-first. Reusable marks and layout behavior belong under `plots/` or `core/`; domain semantics and input normalization belong under `recipes/`.

The general scientific plotting core is complete. Existing recipes remain supported as thin conveniences; future domain work should compose the completed primitives. See `docs/decisions/0002-primitives-before-recipes.md` and `docs/decisions/0003-general-core-closure.md`.

## Import Style

```python
import post_visual as pv
```

## Development And Verification

The supported runtime is native WSL2. micromamba manages an isolated Python 3.12
environment named `post-visual`, and a user-owned TeX Live 2026 tree provides optional
external LaTeX. Docker and Windows Python are not supported paths.

```bash
scripts/bootstrap-wsl.sh
scripts/test-wsl.sh
scripts/test-latex-wsl.sh
```

The environment declaration is `environment.yml`; `conda-lock.yml` records the exact
linux-64 resolution. The validated paths, versions, TeX package snapshot, and maintenance
rules are documented in the
[native WSL runtime guide](docs/setup/wsl-native-runtime.md).

## Text Rendering And Export

MathText is the project default in `post_visual.toml`. External LaTeX is explicit and
strict by default:

```python
import post_visual as pv

with pv.latex_context("mathtext"):
    fig, ax = pv.line([0, 1], [0, 1], xlabel=r"$x$", ylabel=r"$y$")

pv.save_figure(fig, "figure.png")
pv.save_figure(fig, "figure-vector.pdf", pdf_mode="vector")
pv.save_figure(
    fig,
    "figure-hybrid.pdf",
    pdf_mode="hybrid",
    raster_dpi=300,
    hybrid_kws={"scatter_threshold": 5000},
)
```

Only PNG and PDF are supported. Hybrid PDF keeps text, formulas, axes, lines, bars,
legends, and annotations vector while rasterizing selected high-density scatter, mesh,
or filled-contour artists. Run project configuration and diagnostics in the
`post-visual` environment:

```text
post-visual configure --engine usetex
post-visual doctor --latex --output-dir artifacts/latex-doctor
```

## Core APIs

Single-axes plot functions accept `ax` and return `(fig, ax)`. Multi-panel and image-grid helpers return `(fig, axes)`.

- `pv.line(...)`: multi-series/DataFrame input, log aliases, confidence bands, and explicit NaN policy.
- `pv.scatter(...)`: hue/size/marker mappings, regression lines, confidence intervals, and explicit NaN policy.
- `pv.grouped_bar(...)` / `pv.bar(...)`: vertical or horizontal simple/grouped bars with optional errors and annotations.
- `pv.horizontal_bar(...)`: convenience entry point for horizontal simple or grouped bars.
- `pv.errorbar(...)`: point estimates with symmetric or asymmetric x/y errors.
- `pv.interval_band(...)`: vertical or horizontal bounds with an optional center line.
- `pv.point_range(...)` / `pv.forest_plot(...)`: categorical estimates with interval bounds and reference lines.
- `pv.event_lines(...)`: composable vertical or horizontal event/threshold lines with labels.
- `pv.event_spans(...)`: composable vertical or horizontal highlighted intervals with labels.
- `pv.annotate_text(...)`, `pv.annotate_arrow(...)`, `pv.significance_bracket(...)`: text, arrows, callouts, and significance marks.
- `pv.hist(...)`: array values or DataFrame `x` with optional `hue`.
- `pv.kde(...)`, `pv.ecdf(...)`, `pv.strip(...)`: density, cumulative-distribution, and raw-sample views.
- `pv.box(...)`: array, matrix, or DataFrame grouped distributions.
- `pv.violin(...)`: array, matrix, or DataFrame grouped distributions.
- `pv.heatmap(...)`: 2D arrays or DataFrames with optional annotations and colorbar.
- `pv.grid_color(...)`: continuous-coordinate regular grids with colorbars and optional centered normalization.
- `pv.image(...)` / `pv.image_grid(...)`: grayscale/RGB(A) images with shared limits and colorbars.
- `pv.panel_grid(...)` / `pv.label_panels(...)`: constrained multi-panel layouts and panel labels.
- `pv.format_axis(...)`, `pv.shared_legend(...)`, `pv.secondary_axis(...)`, `pv.inset_axes(...)`: axes and figure composition helpers.
- `pv.confusion_matrix(...)`: labels or precomputed matrices with optional normalization.
- `pv.training_curves(...)`: dict or DataFrame training histories.
- `pv.model_comparison(...)`: grouped cross-model/cross-dataset comparisons with error bars and best-result highlighting.
- `pv.ablation(...)`: absolute ablation scores or changes relative to a full/reference model.
- `pv.calibration_curve(...)`: binary reliability curves with local binning and ECE labels.
- `pv.embedding(...)`: precomputed 2D coordinates or lightweight PCA with class centers and confidence ellipses.
- `pv.feature_importance(...)`: signed or grouped feature importance with sorting, Top-K, annotations, and error bars.
- `pv.connectivity_matrix(...)`: connectivity and difference matrices with triangular masks, annotations, and zero-centered color scales.

```python
import post_visual as pv

pv.line(...)
pv.scatter(...)
pv.grouped_bar(...)
pv.bar(...)
pv.horizontal_bar(...)
pv.errorbar(...)
pv.interval_band(...)
pv.point_range(...)
pv.forest_plot(...)
pv.event_lines(...)
pv.event_spans(...)
pv.annotate_text(...)
pv.annotate_arrow(...)
pv.significance_bracket(...)
pv.hist(...)
pv.kde(...)
pv.ecdf(...)
pv.strip(...)
pv.box(...)
pv.violin(...)
pv.heatmap(...)
pv.grid_color(...)
pv.image(...)
pv.image_grid(...)
fig, axes = pv.panel_grid(2, 2, labels=True)
pv.shared_legend(axes)
pv.confusion_matrix(...)
pv.training_curves(...)
pv.model_comparison(...)
pv.ablation(...)
pv.calibration_curve(...)
pv.embedding(...)
pv.feature_importance(...)
pv.connectivity_matrix(...)
```

## Repository Layout

- `src/post_visual/`: package source.
- `tests/`: behavior tests run by native WSL verification.
- `examples/`: MVP example figure generators.
- `examples/usetex_module_gallery.py`: one real-LaTeX PNG for each public plotting and recipe module.
- `environment.yml` / `conda-lock.yml`: readable and locked micromamba environment definitions.
- `scripts/`: native WSL bootstrap and verification entry points.
- `docs/`: durable architecture, setup, plot catalog, and decision docs.
- `.codex/`: workspace continuity and handoff state.

## Documentation

- [Documentation index](docs/INDEX.md)
- [Architecture docs index](docs/architecture/README.md)
- [Toolkit architecture](docs/architecture/toolkit-architecture.md)
- [Plot catalog](docs/architecture/plot-catalog.md)
- [Setup notes](docs/setup/README.md)
- [Native WSL runtime](docs/setup/wsl-native-runtime.md)
- [Completed WSL migration](docs/setup/wsl-migration.md)
- [Fixed LaTeX test environment](docs/setup/latex-test-environment.md)
- [Decisions index](docs/decisions/README.md)
- [Initial design decisions](docs/decisions/0001-initial-toolkit-scope.md)
- [Primitive-first architecture decision](docs/decisions/0002-primitives-before-recipes.md)
- [General core closure decision](docs/decisions/0003-general-core-closure.md)
- [Historical Docker-only runtime decision](docs/decisions/0004-docker-only-runtime-and-texlive.md)
- [Native WSL runtime decision](docs/decisions/0005-native-wsl-micromamba-texlive.md)

## Codex Bootstrap

For Codex sessions, read `AGENTS.md`, `.codex/WORKSPACE.md`, `.codex/HANDOFF.md` when active, and `docs/INDEX.md`.
