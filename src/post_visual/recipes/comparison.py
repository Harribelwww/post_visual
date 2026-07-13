"""Model-comparison and ablation visualization recipes."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from matplotlib.figure import Figure

from post_visual.plots.bars import grouped_bar
from post_visual.style.contexts import style_context
from post_visual.style.palettes import RGB
from post_visual.style.rc import DEFAULT_FIGSIZE_CM


def model_comparison(
    values: Any,
    *,
    models: Sequence[Any] | None = None,
    metrics: Sequence[Any] | None = None,
    errors: Any | None = None,
    maximize: bool | Sequence[bool] = True,
    highlight_best: bool = True,
    annotate: bool = True,
    fmt: str = ".2f",
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = "Model Comparison",
    xlabel: str | None = None,
    ylabel: str | None = "Score",
    legend: bool | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    bar_kws: Mapping[str, Any] | None = None,
    errorbar_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Compare models across one or more metrics with grouped bars.

    ``values`` may be an array shaped ``(n_models, n_metrics)``, a
    DataFrame-like object, or a nested mapping of model to metric values.
    """

    data, model_labels, metric_labels = _normalize_comparison(
        values, models=models, metrics=metrics
    )
    error_values = _normalize_errors(errors, shape=data.shape)
    maximize_flags = _normalize_maximize(maximize, n_metrics=data.shape[1])

    draw_args = dict(
        data=data,
        model_labels=model_labels,
        metric_labels=metric_labels,
        errors=error_values,
        maximize=maximize_flags,
        highlight_best=highlight_best,
        annotate=annotate,
        fmt=fmt,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        legend=legend,
        figsize_cm=figsize_cm,
        bar_kws=bar_kws,
        errorbar_kws=errorbar_kws,
        legend_kws=legend_kws,
    )
    if not style:
        return _draw_model_comparison(**draw_args)

    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_model_comparison(**draw_args)


def ablation(
    values: Any,
    *,
    variants: Sequence[Any] | None = None,
    datasets: Sequence[Any] | None = None,
    errors: Any | None = None,
    reference: int | str = -1,
    relative: bool = False,
    palette: str | int | Sequence[RGB] = "nilou",
    ax: Axes | None = None,
    title: str | None = "Ablation Study",
    xlabel: str | None = None,
    ylabel: str | None = None,
    **comparison_kws: Any,
) -> tuple[Figure, Axes]:
    """Plot ablation variants, optionally as changes from a reference row."""

    data, variant_labels, dataset_labels = _normalize_comparison(
        values, models=variants, metrics=datasets
    )
    reference_index = _resolve_reference(reference, labels=variant_labels)
    plot_values = data - data[reference_index] if relative else data
    resolved_ylabel = ylabel or ("Change from reference" if relative else "Score")

    fig, plot_ax = model_comparison(
        plot_values,
        models=variant_labels,
        metrics=dataset_labels,
        errors=errors,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=resolved_ylabel,
        **comparison_kws,
    )
    if relative:
        plot_ax.axhline(0.0, color="0.25", linestyle="--", linewidth=1.0, zorder=1)
    return fig, plot_ax


def _draw_model_comparison(
    *,
    data: np.ndarray,
    model_labels: Sequence[str],
    metric_labels: Sequence[str],
    errors: np.ndarray | None,
    maximize: Sequence[bool],
    highlight_best: bool,
    annotate: bool,
    fmt: str,
    palette: str | int | Sequence[RGB],
    ax: Axes | None,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
    legend: bool | None,
    figsize_cm: tuple[float, float],
    bar_kws: Mapping[str, Any] | None,
    errorbar_kws: Mapping[str, Any] | None,
    legend_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    n_models, n_metrics = data.shape
    best_indices = [
        int(np.nanargmax(data[:, i]) if maximize[i] else np.nanargmin(data[:, i]))
        for i in range(n_metrics)
    ]
    base_bar_kws = {"alpha": 0.92, "edgecolor": "black", "linewidth": 0.8}
    base_bar_kws.update(bar_kws or {})
    fig, plot_ax = grouped_bar(
        values=data,
        categories=model_labels,
        groups=metric_labels if n_metrics > 1 else None,
        errors=errors,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        legend=legend if legend is not None else n_metrics > 1,
        figsize_cm=figsize_cm,
        style=False,
        bar_kws=base_bar_kws,
        errorbar_kws=errorbar_kws,
        legend_kws=legend_kws,
    )
    all_bars = [container for container in plot_ax.containers if isinstance(container, BarContainer)]
    if highlight_best:
        for metric_index, bars in enumerate(all_bars):
            best_bar = bars[best_indices[metric_index]]
            best_bar.set_linewidth(base_bar_kws["linewidth"])
            best_bar.set_edgecolor("#E64B35")

    if annotate:
        for metric_index, bars in enumerate(all_bars):
            labels = [
                format(value, fmt) if np.isfinite(value) and not np.isclose(value, 0.0) else ""
                for value in data[:, metric_index]
            ]
            plot_ax.bar_label(bars, labels=labels, padding=3, fontsize=9)

    return fig, plot_ax


def _normalize_comparison(
    values: Any,
    *,
    models: Sequence[Any] | None,
    metrics: Sequence[Any] | None,
) -> tuple[np.ndarray, list[str], list[str]]:
    if _is_dataframe_like(values):
        data = np.asarray(values.to_numpy(dtype=float))
        model_labels = [str(value) for value in (models or values.index.tolist())]
        metric_labels = [str(value) for value in (metrics or values.columns.tolist())]
    elif isinstance(values, Mapping):
        raw_models = list(models) if models is not None else list(values)
        model_labels = [str(value) for value in raw_models]
        first = values[raw_models[0]]
        if isinstance(first, Mapping):
            raw_metrics = list(metrics) if metrics is not None else list(first)
            metric_labels = [str(value) for value in raw_metrics]
            data = np.asarray(
                [[values[model][metric] for metric in raw_metrics] for model in raw_models],
                dtype=float,
            )
        else:
            metric_labels = [str(value) for value in (metrics or ["Score"])]
            data = np.asarray([values[model] for model in raw_models], dtype=float).reshape(-1, 1)
    else:
        data = np.asarray(values, dtype=float)
        if data.ndim == 1:
            data = data.reshape(-1, 1)
        if data.ndim != 2:
            raise ValueError("values must be one- or two-dimensional.")
        model_labels = _labels_or_default(models, data.shape[0], prefix="Model")
        metric_labels = _labels_or_default(metrics, data.shape[1], prefix="Metric")

    if data.ndim != 2 or data.size == 0:
        raise ValueError("values must contain a non-empty model-by-metric matrix.")
    if len(model_labels) != data.shape[0] or len(metric_labels) != data.shape[1]:
        raise ValueError("model and metric labels must match the value matrix shape.")
    if np.any(np.all(~np.isfinite(data), axis=0)):
        raise ValueError("each metric must contain at least one finite value.")
    return data, model_labels, metric_labels


def _normalize_errors(errors: Any | None, *, shape: tuple[int, int]) -> np.ndarray | None:
    if errors is None:
        return None
    result = np.asarray(errors, dtype=float)
    if result.ndim == 1 and shape[1] == 1:
        result = result.reshape(-1, 1)
    if result.shape != shape:
        raise ValueError("errors must have the same shape as values.")
    if np.any(result < 0):
        raise ValueError("errors must be non-negative.")
    return result


def _normalize_maximize(value: bool | Sequence[bool], *, n_metrics: int) -> list[bool]:
    if isinstance(value, bool):
        return [value] * n_metrics
    result = [bool(item) for item in value]
    if len(result) != n_metrics:
        raise ValueError("maximize must contain one flag per metric.")
    return result


def _resolve_reference(reference: int | str, *, labels: Sequence[str]) -> int:
    if isinstance(reference, str):
        if reference not in labels:
            raise ValueError(f"reference {reference!r} is not present in variants.")
        return labels.index(reference)
    index = reference if reference >= 0 else len(labels) + reference
    if index < 0 or index >= len(labels):
        raise ValueError("reference index is out of range.")
    return index


def _labels_or_default(
    labels: Sequence[Any] | None,
    length: int,
    *,
    prefix: str,
) -> list[str]:
    if labels is None:
        return [f"{prefix} {index + 1}" for index in range(length)]
    result = [str(label) for label in labels]
    if len(result) != length:
        raise ValueError(f"{prefix.lower()} labels must have length {length}.")
    return result


def _is_dataframe_like(values: Any) -> bool:
    return all(hasattr(values, attribute) for attribute in ("columns", "index", "to_numpy"))
