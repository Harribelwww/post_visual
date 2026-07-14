"""Bar and grouped-bar plot primitives."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from math import ceil
from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from post_visual.core.axes import style_axes
from post_visual.core.figure import get_fig_ax
from post_visual.style.contexts import style_context
from post_visual.style.palettes import RGB, resolve_colors
from post_visual.style.rc import DEFAULT_FIGSIZE_CM


@dataclass(frozen=True)
class _BarData:
    categories: list[str]
    groups: list[str | None]
    values: np.ndarray


def grouped_bar(
    data: Any | None = None,
    x: Any | None = None,
    y: Any | None = None,
    *,
    hue: str | None = None,
    categories: Sequence[Any] | None = None,
    values: Any | None = None,
    groups: Sequence[Any] | None = None,
    errors: Any | None = None,
    estimator: str | Callable[[Any], float] = "mean",
    palette: str | int | Sequence[RGB] = "furina",
    colors: Sequence[Any] | None = None,
    orientation: str = "vertical",
    annotate: bool = False,
    fmt: str = ".3g",
    ax: Axes | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    legend: bool | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    bar_kws: Mapping[str, Any] | None = None,
    errorbar_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Draw simple or grouped bars and return `(fig, ax)`.

    Array inputs accept one-dimensional values for simple bars or a matrix
    shaped `(n_categories, n_groups)` for grouped bars. DataFrame-style input
    uses `x`, `y`, and optional `hue` column names. Set ``orientation`` to
    ``"horizontal"`` for horizontal bars.
    """

    draw_args = dict(
        data=data,
        x=x,
        y=y,
        hue=hue,
        categories=categories,
        values=values,
        groups=groups,
        errors=errors,
        estimator=estimator,
        palette=palette,
        colors=colors,
        orientation=orientation,
        annotate=annotate,
        fmt=fmt,
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
        return _draw_grouped_bar(**draw_args)

    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_grouped_bar(**draw_args)


bar = grouped_bar


def horizontal_bar(*args: Any, **kwargs: Any) -> tuple[Figure, Axes]:
    """Draw simple or grouped horizontal bars and return ``(fig, ax)``."""

    if "orientation" in kwargs:
        raise TypeError("horizontal_bar fixes orientation='horizontal'.")
    return grouped_bar(*args, orientation="horizontal", **kwargs)


def _draw_grouped_bar(
    *,
    data: Any | None,
    x: Any | None,
    y: Any | None,
    hue: str | None,
    categories: Sequence[Any] | None,
    values: Any | None,
    groups: Sequence[Any] | None,
    errors: Any | None,
    estimator: str | Callable[[Any], float],
    palette: str | int | Sequence[RGB],
    colors: Sequence[Any] | None,
    orientation: str,
    annotate: bool,
    fmt: str,
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
    bar_data = _normalize_input(
        data=data,
        x=x,
        y=y,
        hue=hue,
        categories=categories,
        values=values,
        groups=groups,
        estimator=estimator,
    )
    orientation = _normalize_orientation(orientation)
    error_values = _normalize_errors(errors, shape=bar_data.values.shape)

    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    category_axis = "x" if orientation == "vertical" else "y"
    value_axis = "y" if orientation == "vertical" else "x"
    plot_ax.grid(False, axis=category_axis)
    plot_ax.grid(True, axis=value_axis, linestyle="--", alpha=0.15, color="black")

    n_categories, n_groups = bar_data.values.shape
    x_positions = np.arange(n_categories)
    group_colors = resolve_colors(palette, n=n_groups)
    base_width = 0.65 if n_groups == 1 else 0.8 / n_groups

    base_bar_kws = {
        "edgecolor": "black",
        "linewidth": 0.8,
        "alpha": 0.95,
    }
    if bar_kws:
        base_bar_kws.update(bar_kws)
    base_error_kws = {
        "fmt": "none",
        "ecolor": "black",
        "elinewidth": 1.0,
        "capsize": 3,
    }
    if errorbar_kws:
        base_error_kws.update(errorbar_kws)

    for group_index, group_label in enumerate(bar_data.groups):
        offset = 0.0 if n_groups == 1 else (group_index - (n_groups - 1) / 2) * base_width
        positions = x_positions + offset
        group_values = bar_data.values[:, group_index]
        color = _resolve_bar_color(
            colors=colors,
            group_colors=group_colors,
            group_index=group_index,
            n_categories=n_categories,
            n_groups=n_groups,
        )
        if orientation == "vertical":
            draw_kws = {
                "width": base_width * 0.92,
                "color": color,
                "label": group_label,
                **base_bar_kws,
            }
            bars = plot_ax.bar(
                positions,
                group_values,
                **draw_kws,
            )
            if error_values is not None:
                plot_ax.errorbar(positions, group_values, yerr=error_values[:, group_index], **base_error_kws)
        else:
            draw_kws = {
                "height": base_width * 0.92,
                "color": color,
                "label": group_label,
                **base_bar_kws,
            }
            bars = plot_ax.barh(
                positions,
                group_values,
                **draw_kws,
            )
            if error_values is not None:
                plot_ax.errorbar(group_values, positions, xerr=error_values[:, group_index], **base_error_kws)
        if annotate:
            labels = [format(value, fmt) if np.isfinite(value) else "" for value in group_values]
            plot_ax.bar_label(bars, labels=labels, padding=3, fontsize=8)

    if orientation == "vertical":
        plot_ax.set_xticks(x_positions)
        plot_ax.set_xticklabels(bar_data.categories)
    else:
        plot_ax.set_yticks(x_positions)
        plot_ax.set_yticklabels(bar_data.categories)

    if title:
        plot_ax.set_title(title)
    if xlabel or (orientation == "vertical" and isinstance(x, str)) or (orientation == "horizontal" and isinstance(y, str)):
        plot_ax.set_xlabel(xlabel or (x if orientation == "vertical" else y))
    if ylabel or (orientation == "vertical" and isinstance(y, str)) or (orientation == "horizontal" and isinstance(x, str)):
        plot_ax.set_ylabel(ylabel or (y if orientation == "vertical" else x))

    _maybe_add_legend(
        plot_ax,
        groups=bar_data.groups,
        legend=legend,
        legend_kws=legend_kws,
    )
    return fig, plot_ax


def _normalize_input(
    *,
    data: Any | None,
    x: Any | None,
    y: Any | None,
    hue: str | None,
    categories: Sequence[Any] | None,
    values: Any | None,
    groups: Sequence[Any] | None,
    estimator: str | Callable[[Any], float],
) -> _BarData:
    if _is_dataframe_like(data) and isinstance(x, str):
        if not isinstance(y, str):
            raise ValueError("DataFrame-style input requires string column names for x and y.")
        return _normalize_dataframe(data=data, x=x, y=y, hue=hue, estimator=estimator)

    raw_values = values
    raw_categories = categories

    if raw_values is None and y is not None:
        raw_values = y
        if raw_categories is None:
            raw_categories = x
    elif raw_values is None and data is not None:
        raw_values = data

    if raw_values is None:
        raise ValueError("Provide bar `values`, y-values, array `data`, or DataFrame-style columns.")

    return _normalize_array_values(
        values=raw_values,
        categories=raw_categories,
        groups=groups,
    )


def _normalize_dataframe(
    *,
    data: Any,
    x: str,
    y: str,
    hue: str | None,
    estimator: str | Callable[[Any], float],
) -> _BarData:
    if hue is None:
        grouped = data.groupby(x, sort=False)[y].agg(estimator)
        values = np.asarray(grouped.to_numpy(dtype=float)).reshape(-1, 1)
        return _BarData(
            categories=[str(value) for value in grouped.index.tolist()],
            groups=[None],
            values=values,
        )

    categories = data[x].drop_duplicates().tolist()
    groups = data[hue].drop_duplicates().tolist()
    pivot = data.pivot_table(
        index=x,
        columns=hue,
        values=y,
        aggfunc=estimator,
        sort=False,
    )
    pivot = pivot.reindex(index=categories, columns=groups)
    return _BarData(
        categories=[str(value) for value in categories],
        groups=[str(value) for value in groups],
        values=np.asarray(pivot.to_numpy(dtype=float)),
    )


def _normalize_array_values(
    *,
    values: Any,
    categories: Sequence[Any] | None,
    groups: Sequence[Any] | None,
) -> _BarData:
    value_array = np.asarray(values, dtype=float)
    if value_array.ndim == 1:
        value_array = value_array.reshape(-1, 1)
        group_labels: list[str | None] = [None]
    elif value_array.ndim == 2:
        group_labels = _labels_or_default(groups, value_array.shape[1], prefix="Group")
    else:
        raise ValueError("Bar values must be one-dimensional or two-dimensional.")

    category_labels = _labels_or_default(categories, value_array.shape[0], prefix="Category")
    return _BarData(categories=category_labels, groups=group_labels, values=value_array)


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


def _is_dataframe_like(data: Any) -> bool:
    return data is not None and hasattr(data, "groupby") and hasattr(data, "__getitem__")


def _normalize_orientation(orientation: str) -> str:
    key = orientation.strip().lower()
    aliases = {"v": "vertical", "vertical": "vertical", "h": "horizontal", "horizontal": "horizontal"}
    if key not in aliases:
        raise ValueError("orientation must be 'vertical' or 'horizontal'.")
    return aliases[key]


def _normalize_errors(errors: Any | None, *, shape: tuple[int, int]) -> np.ndarray | None:
    if errors is None:
        return None
    result = np.asarray(errors, dtype=float)
    if result.ndim == 1 and shape[1] == 1:
        result = result.reshape(-1, 1)
    if result.shape != shape or np.any(result < 0):
        raise ValueError("errors must be non-negative and have the same shape as bar values.")
    return result


def _resolve_bar_color(
    *,
    colors: Sequence[Any] | None,
    group_colors: Sequence[Any],
    group_index: int,
    n_categories: int,
    n_groups: int,
) -> Any:
    if colors is None:
        return group_colors[group_index]
    resolved = list(colors)
    expected = n_categories if n_groups == 1 else n_groups
    if len(resolved) != expected:
        raise ValueError(f"colors must have length {expected}.")
    return resolved if n_groups == 1 else resolved[group_index]


def _maybe_add_legend(
    ax: Axes,
    *,
    groups: Sequence[str | None],
    legend: bool | None,
    legend_kws: Mapping[str, Any] | None,
) -> None:
    has_labels = any(group is not None for group in groups)
    if legend is False or (legend is None and not has_labels):
        return

    handles, labels = ax.get_legend_handles_labels()
    if not handles:
        return

    kwargs = {
        "loc": "upper left",
        "bbox_to_anchor": (1.01, 1.0),
        "borderaxespad": 0.0,
        "frameon": True,
        "fontsize": 9,
        "ncol": max(ceil(len(handles) / 5), 1),
    }
    if legend_kws:
        kwargs.update(legend_kws)
    legend_obj = ax.legend(handles, labels, **kwargs)
    legend_obj.get_frame().set_edgecolor("black")
    legend_obj.get_frame().set_facecolor("white")
