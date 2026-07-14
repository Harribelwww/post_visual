# Decision 0001: Initial Toolkit Scope

Date: 2026-07-09

## Decision

Build `post_visual` as a data-science result visualization toolkit with a fixed scientific plotting style.

The toolkit should cover mainstream plots and research-result recipes before adding heavier domain-specific viewers.

## Rationale

The local paper set is centered on EEG, medical diagnosis, biosignals, and neural-network methods, but most result figures are standard data-science outputs:

- model performance comparisons
- confusion matrices
- training curves
- ablation and hyperparameter curves
- subject-wise distributions
- feature importance
- embeddings
- heatmaps, attention maps, and connectivity matrices
- raw signal and frequency-domain views

This argues for a lightweight matplotlib-first package with optional domain extensions instead of a specialized EEG or medical-image viewer as the base package.

## Style Policy

The style baseline is derived from `sci_plot.m`:

- fixed publication-oriented visual tone
- named palettes, starting with Furina and Nilou
- Times/serif text
- STIX/mathtext LaTeX-like formula rendering by default
- optional real LaTeX rendering
- white background, black axes, minor ticks, restrained grid
- consistent export defaults

## API Policy

Use `post_visual` as the package name and `pv` as the recommended import alias:

```python
import post_visual as pv
```

High-level functions should accept `ax` and return `fig, ax`. DataFrame-style inputs should be preferred while retaining ndarray support for common scientific workflows.
