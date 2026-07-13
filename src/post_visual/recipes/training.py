"""Training-history visualization recipes."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from post_visual.plots.line import line
from post_visual.style.palettes import RGB
from post_visual.style.rc import DEFAULT_FIGSIZE_CM


def training_curves(
    history: Any,
    *,
    x: str | Sequence[float] | None = "epoch",
    metrics: Sequence[str] | None = None,
    label_map: Mapping[str, str] | None = None,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = "Training Curves",
    xlabel: str | None = None,
    ylabel: str | None = None,
    legend: bool | None = True,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    line_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Plot training metrics from a dict-like object or DataFrame."""

    series, resolved_xlabel = _normalize_history(
        history=history,
        x=x,
        metrics=metrics,
        label_map=label_map,
    )
    return line(
        series=series,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel or resolved_xlabel,
        ylabel=ylabel,
        legend=legend,
        figsize_cm=figsize_cm,
        style=style,
        usetex=usetex,
        line_kws=line_kws,
        legend_kws=legend_kws,
    )


def _normalize_history(
    *,
    history: Any,
    x: str | Sequence[float] | None,
    metrics: Sequence[str] | None,
    label_map: Mapping[str, str] | None,
) -> tuple[list[tuple[np.ndarray, np.ndarray, str]], str]:
    if _is_dataframe_like(history):
        return _normalize_dataframe_history(
            history=history,
            x=x,
            metrics=metrics,
            label_map=label_map,
        )
    if isinstance(history, Mapping):
        return _normalize_mapping_history(
            history=history,
            x=x,
            metrics=metrics,
            label_map=label_map,
        )
    raise ValueError("history must be a DataFrame-like object or a mapping.")


def _normalize_dataframe_history(
    *,
    history: Any,
    x: str | Sequence[float] | None,
    metrics: Sequence[str] | None,
    label_map: Mapping[str, str] | None,
) -> tuple[list[tuple[np.ndarray, np.ndarray, str]], str]:
    columns = list(history.columns)
    metric_names = list(metrics) if metrics is not None else _numeric_columns(history, exclude=x)
    if not metric_names:
        raise ValueError("No numeric training metrics found.")

    x_values, xlabel = _resolve_x_values(
        length=len(history),
        x=x,
        source=history,
        source_keys=columns,
    )
    return _make_series(
        source=history,
        metric_names=metric_names,
        x_values=x_values,
        label_map=label_map,
    ), xlabel


def _normalize_mapping_history(
    *,
    history: Mapping[str, Any],
    x: str | Sequence[float] | None,
    metrics: Sequence[str] | None,
    label_map: Mapping[str, str] | None,
) -> tuple[list[tuple[np.ndarray, np.ndarray, str]], str]:
    keys = list(history)
    metric_names = list(metrics) if metrics is not None else [key for key in keys if key != x]
    if not metric_names:
        raise ValueError("No training metrics found.")

    first_metric = np.ravel(np.asarray(history[metric_names[0]]))
    x_values, xlabel = _resolve_x_values(
        length=first_metric.size,
        x=x,
        source=history,
        source_keys=keys,
    )
    return _make_series(
        source=history,
        metric_names=metric_names,
        x_values=x_values,
        label_map=label_map,
    ), xlabel


def _resolve_x_values(
    *,
    length: int,
    x: str | Sequence[float] | None,
    source: Any,
    source_keys: Sequence[str],
) -> tuple[np.ndarray, str]:
    if isinstance(x, str) and x in source_keys:
        return np.ravel(np.asarray(source[x])), x
    if x is not None and not isinstance(x, str):
        x_array = np.ravel(np.asarray(x))
        if x_array.size != length:
            raise ValueError("x must have the same length as each metric.")
        return x_array, "Epoch"
    return np.arange(1, length + 1), "Epoch"


def _make_series(
    *,
    source: Any,
    metric_names: Sequence[str],
    x_values: np.ndarray,
    label_map: Mapping[str, str] | None,
) -> list[tuple[np.ndarray, np.ndarray, str]]:
    result = []
    for metric in metric_names:
        if metric not in source:
            raise ValueError(f"Metric {metric!r} is not present in history.")
        y_values = np.ravel(np.asarray(source[metric], dtype=float))
        if y_values.size != x_values.size:
            raise ValueError(f"Metric {metric!r} must have the same length as x.")
        label = label_map.get(metric, metric) if label_map is not None else metric
        result.append((x_values, y_values, str(label)))
    return result


def _numeric_columns(history: Any, *, exclude: str | Sequence[float] | None) -> list[str]:
    excluded = {exclude} if isinstance(exclude, str) else set()
    result = []
    for column in history.columns:
        if column in excluded:
            continue
        values = np.asarray(history[column])
        if np.issubdtype(values.dtype, np.number):
            result.append(column)
    return result


def _is_dataframe_like(history: Any) -> bool:
    return history is not None and hasattr(history, "columns") and hasattr(history, "__getitem__")
