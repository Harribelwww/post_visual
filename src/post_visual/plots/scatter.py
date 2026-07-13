"""Scatter plot primitive for data-science result views."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import ceil
from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from scipy.stats import t as student_t

from post_visual.core.axes import style_axes
from post_visual.core.figure import get_fig_ax
from post_visual.style.contexts import style_context
from post_visual.style.palettes import RGB, resolve_colors
from post_visual.style.rc import DEFAULT_FIGSIZE_CM


@dataclass(frozen=True)
class _ScatterSeries:
    x: np.ndarray
    y: np.ndarray
    size: np.ndarray | float
    label: str | None = None


def scatter(
    data: Any | None = None,
    x: Any | None = None,
    y: Any | None = None,
    *,
    hue: str | None = None,
    size: str | Sequence[float] | float | None = None,
    label: str | None = None,
    fit_line: bool = False,
    fit_ci: float | None = None,
    nan_policy: str = "omit",
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    legend: bool | None = None,
    marker: str = "o",
    markers: Sequence[str] | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    scatter_kws: Mapping[str, Any] | None = None,
    fit_kws: Mapping[str, Any] | None = None,
    fit_band_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Draw a scatter plot and return `(fig, ax)`.

    Accepts array-like `x`/`y`, an `N x 2` matrix through `data`, or
    DataFrame-style `data`, `x`, `y`, and optional `hue` column names.
    """

    draw_args = dict(
        data=data,
        x=x,
        y=y,
        hue=hue,
        size=size,
        label=label,
        fit_line=fit_line,
        fit_ci=fit_ci,
        nan_policy=nan_policy,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        legend=legend,
        marker=marker,
        markers=markers,
        figsize_cm=figsize_cm,
        scatter_kws=scatter_kws,
        fit_kws=fit_kws,
        fit_band_kws=fit_band_kws,
        legend_kws=legend_kws,
    )

    if not style:
        return _draw_scatter(**draw_args)

    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_scatter(**draw_args)


def _draw_scatter(
    *,
    data: Any | None,
    x: Any | None,
    y: Any | None,
    hue: str | None,
    size: str | Sequence[float] | float | None,
    label: str | None,
    fit_line: bool,
    fit_ci: float | None,
    nan_policy: str,
    palette: str | int | Sequence[RGB],
    ax: Axes | None,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
    legend: bool | None,
    marker: str,
    markers: Sequence[str] | None,
    figsize_cm: tuple[float, float],
    scatter_kws: Mapping[str, Any] | None,
    fit_kws: Mapping[str, Any] | None,
    fit_band_kws: Mapping[str, Any] | None,
    legend_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    series = _normalize_input(data=data, x=x, y=y, hue=hue, size=size, label=label)
    series = _apply_nan_policy(series, nan_policy=nan_policy)
    if fit_ci is not None and not 0 < fit_ci < 1:
        raise ValueError("fit_ci must lie strictly between 0 and 1.")
    if markers is not None and len(markers) == 0:
        raise ValueError("markers must not be empty.")

    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    colors = resolve_colors(palette, n=len(series))

    base_scatter_kws = {
        "marker": marker,
        "linewidths": 1.2,
        "alpha": 0.95,
    }
    if scatter_kws:
        base_scatter_kws.update(scatter_kws)

    base_fit_kws = {
        "linestyle": "--",
        "linewidth": 1.2,
        "alpha": 0.85,
    }
    if fit_kws:
        base_fit_kws.update(fit_kws)
    base_band_kws = {"alpha": 0.16, "linewidth": 0.0}
    base_band_kws.update(fit_band_kws or {})

    for index, item in enumerate(series):
        color = colors[index]
        marker_value = marker if markers is None else markers[index % len(markers)]
        plot_ax.scatter(
            item.x,
            item.y,
            s=item.size,
            label=item.label,
            facecolors="white",
            edgecolors=color,
            **{**base_scatter_kws, "marker": marker_value},
        )
        if fit_line:
            _draw_fit_line(
                plot_ax,
                item=item,
                color=color,
                fit_ci=fit_ci,
                fit_kws=base_fit_kws,
                band_kws=base_band_kws,
            )

    plot_ax.margins(x=0.05, y=0.05)

    if title:
        plot_ax.set_title(title)
    if xlabel or isinstance(x, str):
        plot_ax.set_xlabel(xlabel or x)
    if ylabel or isinstance(y, str):
        plot_ax.set_ylabel(ylabel or y)

    _maybe_add_legend(plot_ax, series=series, legend=legend, legend_kws=legend_kws)
    return fig, plot_ax


def _normalize_input(
    *,
    data: Any | None,
    x: Any | None,
    y: Any | None,
    hue: str | None,
    size: str | Sequence[float] | float | None,
    label: str | None,
) -> list[_ScatterSeries]:
    if _is_dataframe_like(data) and isinstance(x, str):
        if not isinstance(y, str):
            raise ValueError("DataFrame-style input requires string column names for x and y.")
        return _normalize_dataframe(data=data, x=x, y=y, hue=hue, size=size, label=label)

    if data is not None and x is None and y is None:
        x_values, y_values = _xy_from_matrix(data)
        return [_make_series(x_values, y_values, size=size, label=label)]

    if data is not None and x is not None and y is None and not isinstance(x, str):
        return [_make_series(data, x, size=size, label=label)]

    if x is not None and y is not None:
        return [_make_series(x, y, size=size, label=label)]

    raise ValueError("Provide x/y arrays, an N x 2 `data` array, or DataFrame-style columns.")


def _normalize_dataframe(
    *,
    data: Any,
    x: str,
    y: str,
    hue: str | None,
    size: str | Sequence[float] | float | None,
    label: str | None,
) -> list[_ScatterSeries]:
    if hue is None:
        size_values = data[size] if isinstance(size, str) else size
        return [_make_series(data[x], data[y], size=size_values, label=label)]

    result = []
    for key, frame in data.groupby(hue, sort=False):
        size_values = frame[size] if isinstance(size, str) else size
        result.append(_make_series(frame[x], frame[y], size=size_values, label=str(key)))
    return result


def _make_series(
    x_values: Any,
    y_values: Any,
    *,
    size: str | Sequence[float] | float | None,
    label: str | None = None,
) -> _ScatterSeries:
    x_array = np.ravel(np.asarray(x_values))
    y_array = np.ravel(np.asarray(y_values))
    if x_array.size != y_array.size:
        raise ValueError("x and y must have the same length.")
    if x_array.size == 0:
        raise ValueError("Scatter data must contain at least one point.")

    size_values = _normalize_size(size=size, length=x_array.size)
    return _ScatterSeries(x=x_array, y=y_array, size=size_values, label=label)


def _normalize_size(size: str | Sequence[float] | float | None, *, length: int) -> np.ndarray | float:
    if size is None:
        return 36.0
    if isinstance(size, str):
        raise ValueError("String `size` is only valid for DataFrame-style input.")
    if np.isscalar(size):
        return float(size)

    size_array = np.ravel(np.asarray(size, dtype=float))
    if size_array.size != length:
        raise ValueError("size must be scalar or have the same length as x and y.")
    return size_array


def _xy_from_matrix(data: Any) -> tuple[np.ndarray, np.ndarray]:
    array = np.asarray(data)
    if array.ndim != 2 or array.shape[1] < 2:
        raise ValueError("`data` must be an N x 2 array when x/y are omitted.")
    return array[:, 0], array[:, 1]


def _is_dataframe_like(data: Any) -> bool:
    return data is not None and hasattr(data, "groupby") and hasattr(data, "__getitem__")


def _draw_fit_line(
    ax: Axes,
    *,
    item: _ScatterSeries,
    color: RGB,
    fit_ci: float | None,
    fit_kws: Mapping[str, Any],
    band_kws: Mapping[str, Any],
) -> None:
    mask = np.isfinite(item.x) & np.isfinite(item.y)
    if np.count_nonzero(mask) < 2:
        return

    slope, intercept = np.polyfit(item.x[mask], item.y[mask], deg=1)
    x_fit = np.linspace(np.min(item.x[mask]), np.max(item.x[mask]), 100)
    y_fit = slope * x_fit + intercept
    if fit_ci is not None and np.count_nonzero(mask) >= 3:
        x_values = item.x[mask].astype(float)
        y_values = item.y[mask].astype(float)
        residuals = y_values - (slope * x_values + intercept)
        dof = x_values.size - 2
        x_center = float(np.mean(x_values))
        denominator = float(np.sum((x_values - x_center) ** 2))
        if dof > 0 and denominator > 0:
            residual_scale = float(np.sqrt(np.sum(residuals**2) / dof))
            standard_error = residual_scale * np.sqrt(1 / x_values.size + (x_fit - x_center) ** 2 / denominator)
            critical = float(student_t.ppf((1 + fit_ci) / 2, dof))
            ax.fill_between(
                x_fit,
                y_fit - critical * standard_error,
                y_fit + critical * standard_error,
                color=color,
                **band_kws,
            )
    ax.plot(x_fit, y_fit, color=color, label=None, **fit_kws)


def _apply_nan_policy(
    series: Sequence[_ScatterSeries], *, nan_policy: str
) -> list[_ScatterSeries]:
    key = nan_policy.strip().lower()
    if key not in {"omit", "raise"}:
        raise ValueError("nan_policy must be 'omit' or 'raise'.")
    result = []
    for item in series:
        finite = np.isfinite(item.x) & np.isfinite(item.y)
        if isinstance(item.size, np.ndarray):
            finite &= np.isfinite(item.size)
        if key == "raise" and not np.all(finite):
            raise ValueError("scatter data contains non-finite values with nan_policy='raise'.")
        if not np.any(finite):
            raise ValueError("scatter data must retain at least one finite point.")
        size = item.size[finite] if isinstance(item.size, np.ndarray) else item.size
        result.append(_ScatterSeries(item.x[finite], item.y[finite], size, item.label))
    return result


def _maybe_add_legend(
    ax: Axes,
    *,
    series: Sequence[_ScatterSeries],
    legend: bool | None,
    legend_kws: Mapping[str, Any] | None,
) -> None:
    has_labels = any(item.label for item in series)
    if legend is False or (legend is None and not has_labels):
        return

    handles, labels = ax.get_legend_handles_labels()
    if not handles:
        return

    kwargs = {
        "loc": "best",
        "frameon": True,
        "fontsize": 13,
        "ncol": max(ceil(len(handles) / 5), 1),
    }
    if legend_kws:
        kwargs.update(legend_kws)
    legend_obj = ax.legend(handles, labels, **kwargs)
    legend_obj.get_frame().set_edgecolor("black")
    legend_obj.get_frame().set_facecolor("white")
