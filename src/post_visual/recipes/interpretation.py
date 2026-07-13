"""Embedding and feature-importance visualization recipes."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse

from post_visual.core.axes import style_axes
from post_visual.core.figure import get_fig_ax
from post_visual.plots.bars import grouped_bar
from post_visual.style.contexts import style_context
from post_visual.style.palettes import RGB, resolve_colors
from post_visual.style.rc import DEFAULT_FIGSIZE_CM


def embedding(
    data: Any,
    *,
    labels: Any | None = None,
    x: int | str = 0,
    y: int | str = 1,
    features: Sequence[str] | None = None,
    method: str = "precomputed",
    centers: bool = False,
    confidence_ellipse: bool = False,
    ellipse_n_std: float = 2.0,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = "Embedding",
    xlabel: str | None = None,
    ylabel: str | None = None,
    legend: bool | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    scatter_kws: Mapping[str, Any] | None = None,
    center_kws: Mapping[str, Any] | None = None,
    ellipse_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Plot precomputed 2D coordinates or a lightweight PCA projection."""

    coords, label_values, resolved_xlabel, resolved_ylabel = _resolve_embedding(
        data=data,
        labels=labels,
        x=x,
        y=y,
        features=features,
        method=method,
    )
    draw_args = dict(
        coords=coords,
        labels=label_values,
        centers=centers,
        confidence_ellipse=confidence_ellipse,
        ellipse_n_std=ellipse_n_std,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel or resolved_xlabel,
        ylabel=ylabel or resolved_ylabel,
        legend=legend,
        figsize_cm=figsize_cm,
        scatter_kws=scatter_kws,
        center_kws=center_kws,
        ellipse_kws=ellipse_kws,
        legend_kws=legend_kws,
    )
    if not style:
        return _draw_embedding(**draw_args)
    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_embedding(**draw_args)


def feature_importance(
    values: Any,
    *,
    names: Sequence[Any] | None = None,
    groups: Sequence[Any] | None = None,
    errors: Any | None = None,
    top_k: int | None = 15,
    sort: bool = True,
    absolute_sort: bool = True,
    annotate: bool = True,
    fmt: str = ".3f",
    positive_color: RGB | str = "#E64B35",
    negative_color: RGB | str = "#4C78A8",
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = "Feature Importance",
    xlabel: str | None = "Importance",
    ylabel: str | None = None,
    legend: bool | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    bar_kws: Mapping[str, Any] | None = None,
    errorbar_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Plot sorted single- or multi-group feature importances."""

    data, feature_names, group_names = _normalize_importance(values, names=names, groups=groups)
    error_values = _normalize_importance_errors(errors, shape=data.shape)
    order = _importance_order(data, sort=sort, absolute_sort=absolute_sort, top_k=top_k)
    data = data[order]
    feature_names = [feature_names[index] for index in order]
    if error_values is not None:
        error_values = error_values[order]

    draw_args = dict(
        data=data,
        feature_names=feature_names,
        group_names=group_names,
        errors=error_values,
        annotate=annotate,
        fmt=fmt,
        positive_color=positive_color,
        negative_color=negative_color,
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
        return _draw_feature_importance(**draw_args)
    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_feature_importance(**draw_args)


def _draw_embedding(
    *,
    coords: np.ndarray,
    labels: np.ndarray | None,
    centers: bool,
    confidence_ellipse: bool,
    ellipse_n_std: float,
    palette: str | int | Sequence[RGB],
    ax: Axes | None,
    title: str | None,
    xlabel: str,
    ylabel: str,
    legend: bool | None,
    figsize_cm: tuple[float, float],
    scatter_kws: Mapping[str, Any] | None,
    center_kws: Mapping[str, Any] | None,
    ellipse_kws: Mapping[str, Any] | None,
    legend_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    if ellipse_n_std <= 0:
        raise ValueError("ellipse_n_std must be positive.")
    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    class_values = _unique_in_order(labels) if labels is not None else [None]
    colors = resolve_colors(palette, n=len(class_values))
    point_kws = {"s": 34, "alpha": 0.82, "linewidths": 0.5}
    point_kws.update(scatter_kws or {})
    centroid_kws = {"marker": "X", "s": 95, "edgecolors": "black", "linewidths": 0.8, "zorder": 4}
    centroid_kws.update(center_kws or {})
    patch_kws = {"fill": True, "alpha": 0.12, "linewidth": 1.2, "zorder": 1}
    patch_kws.update(ellipse_kws or {})

    for index, class_value in enumerate(class_values):
        mask = np.ones(coords.shape[0], dtype=bool) if labels is None else labels == class_value
        subset = coords[mask]
        color = colors[index]
        plot_ax.scatter(
            subset[:, 0],
            subset[:, 1],
            color=color,
            label=None if class_value is None else str(class_value),
            **point_kws,
        )
        if confidence_ellipse and subset.shape[0] >= 3:
            ellipse = _make_confidence_ellipse(subset, n_std=ellipse_n_std, color=color, kws=patch_kws)
            plot_ax.add_patch(ellipse)
        if centers:
            center = np.mean(subset, axis=0)
            plot_ax.scatter(center[0], center[1], color=color, **centroid_kws)

    plot_ax.margins(0.08)
    if title:
        plot_ax.set_title(title)
    plot_ax.set_xlabel(xlabel)
    plot_ax.set_ylabel(ylabel)
    show_legend = legend if legend is not None else labels is not None
    if show_legend:
        kwargs = {"loc": "best", "frameon": True, "fontsize": 11}
        kwargs.update(legend_kws or {})
        plot_ax.legend(**kwargs)
    return fig, plot_ax


def _draw_feature_importance(
    *,
    data: np.ndarray,
    feature_names: Sequence[str],
    group_names: Sequence[str | None],
    errors: np.ndarray | None,
    annotate: bool,
    fmt: str,
    positive_color: RGB | str,
    negative_color: RGB | str,
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
    n_groups = data.shape[1]
    colors = [positive_color if value >= 0 else negative_color for value in data[:, 0]] if n_groups == 1 else None
    fig, plot_ax = grouped_bar(
        values=data,
        categories=feature_names,
        groups=group_names,
        errors=errors,
        palette=palette,
        colors=colors,
        orientation="horizontal",
        annotate=annotate,
        fmt=fmt,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        legend=legend if legend is not None else n_groups > 1,
        figsize_cm=figsize_cm,
        style=False,
        bar_kws=bar_kws,
        errorbar_kws=errorbar_kws,
        legend_kws=legend_kws,
    )
    plot_ax.axvline(0.0, color="0.25", linewidth=0.8)
    plot_ax.margins(x=0.15)
    return fig, plot_ax


def _resolve_embedding(
    *,
    data: Any,
    labels: Any | None,
    x: int | str,
    y: int | str,
    features: Sequence[str] | None,
    method: str,
) -> tuple[np.ndarray, np.ndarray | None, str, str]:
    key = method.strip().lower()
    resolved_labels = _resolve_labels(data, labels)
    if key == "precomputed":
        if _is_dataframe_like(data) and isinstance(x, str) and isinstance(y, str):
            coords = np.column_stack([np.asarray(data[x], dtype=float), np.asarray(data[y], dtype=float)])
            return _validate_embedding(coords, resolved_labels), resolved_labels, x, y
        array = np.asarray(data, dtype=float)
        if array.ndim != 2:
            raise ValueError("precomputed embedding data must be two-dimensional.")
        coords = array[:, [int(x), int(y)]]
        return _validate_embedding(coords, resolved_labels), resolved_labels, f"Dimension {int(x) + 1}", f"Dimension {int(y) + 1}"
    if key != "pca":
        raise ValueError("method must be 'precomputed' or 'pca'.")

    if _is_dataframe_like(data):
        label_column = labels if isinstance(labels, str) else None
        feature_names = list(features) if features is not None else [
            column
            for column in data.columns
            if column != label_column and np.issubdtype(np.asarray(data[column]).dtype, np.number)
        ]
        matrix = np.asarray(data[feature_names], dtype=float)
    else:
        matrix = np.asarray(data, dtype=float)
    coords, explained = _pca_projection(matrix)
    coords = _validate_embedding(coords, resolved_labels)
    return coords, resolved_labels, f"PC1 ({explained[0] * 100:.1f}%)", f"PC2 ({explained[1] * 100:.1f}%)"


def _pca_projection(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if matrix.ndim != 2 or matrix.shape[0] < 2 or matrix.shape[1] < 2:
        raise ValueError("PCA requires at least two samples and two features.")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("PCA data must contain only finite values.")
    centered = matrix - np.mean(matrix, axis=0, keepdims=True)
    _, singular_values, vt = np.linalg.svd(centered, full_matrices=False)
    coords = centered @ vt[:2].T
    variances = singular_values**2
    explained = variances[:2] / np.sum(variances) if np.sum(variances) else np.zeros(2)
    return coords, explained


def _validate_embedding(coords: np.ndarray, labels: np.ndarray | None) -> np.ndarray:
    if coords.shape[0] == 0 or coords.shape[1] != 2 or not np.all(np.isfinite(coords)):
        raise ValueError("embedding coordinates must be a non-empty finite N x 2 array.")
    if labels is not None and labels.size != coords.shape[0]:
        raise ValueError("labels must have the same length as embedding data.")
    return coords


def _resolve_labels(data: Any, labels: Any | None) -> np.ndarray | None:
    if labels is None:
        return None
    values = data[labels] if isinstance(labels, str) and _is_dataframe_like(data) else labels
    return np.ravel(np.asarray(values))


def _make_confidence_ellipse(
    points: np.ndarray,
    *,
    n_std: float,
    color: Any,
    kws: Mapping[str, Any],
) -> Ellipse:
    covariance = np.cov(points, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]
    width, height = 2 * n_std * np.sqrt(np.maximum(eigenvalues, 0))
    angle = float(np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0])))
    center = np.mean(points, axis=0)
    return Ellipse(center, width=width, height=height, angle=angle, facecolor=color, edgecolor=color, **kws)


def _normalize_importance(
    values: Any,
    *,
    names: Sequence[Any] | None,
    groups: Sequence[Any] | None,
) -> tuple[np.ndarray, list[str], list[str | None]]:
    if isinstance(values, Mapping):
        raw_names = list(names) if names is not None else list(values)
        feature_names = [str(value) for value in raw_names]
        data = np.asarray([values[name] for name in raw_names], dtype=float)
    elif _is_dataframe_like(values):
        data = np.asarray(values.to_numpy(dtype=float))
        feature_names = [str(value) for value in (names or values.index.tolist())]
        if groups is None:
            groups = values.columns.tolist()
    else:
        data = np.asarray(values, dtype=float)
        feature_names = _labels_or_default(names, data.shape[0] if data.ndim else 0, prefix="Feature")
    if data.ndim == 1:
        data = data.reshape(-1, 1)
    if data.ndim != 2 or data.size == 0:
        raise ValueError("importance values must be a non-empty one- or two-dimensional array.")
    if len(feature_names) != data.shape[0]:
        raise ValueError("feature names must match the number of rows in values.")
    group_names = [None] if data.shape[1] == 1 else _labels_or_default(groups, data.shape[1], prefix="Group")
    return data, feature_names, group_names


def _normalize_importance_errors(errors: Any | None, *, shape: tuple[int, int]) -> np.ndarray | None:
    if errors is None:
        return None
    result = np.asarray(errors, dtype=float)
    if result.ndim == 1 and shape[1] == 1:
        result = result.reshape(-1, 1)
    if result.shape != shape or np.any(result < 0):
        raise ValueError("errors must be non-negative and have the same shape as values.")
    return result


def _importance_order(
    data: np.ndarray,
    *,
    sort: bool,
    absolute_sort: bool,
    top_k: int | None,
) -> np.ndarray:
    scores = np.nanmax(np.abs(data), axis=1) if absolute_sort else np.nanmax(data, axis=1)
    order = np.argsort(scores) if sort else np.arange(data.shape[0])
    if top_k is not None:
        if top_k <= 0:
            raise ValueError("top_k must be positive or None.")
        order = order[-top_k:] if sort else order[:top_k]
    return order


def _unique_in_order(values: np.ndarray) -> list[Any]:
    result = []
    for value in values:
        if not any(value == existing for existing in result):
            result.append(value)
    return result


def _labels_or_default(labels: Sequence[Any] | None, length: int, *, prefix: str) -> list[str]:
    if labels is None:
        return [f"{prefix} {index + 1}" for index in range(length)]
    result = [str(value) for value in labels]
    if len(result) != length:
        raise ValueError(f"{prefix.lower()} labels must have length {length}.")
    return result


def _is_dataframe_like(data: Any) -> bool:
    return all(hasattr(data, attribute) for attribute in ("columns", "__getitem__", "to_numpy"))
