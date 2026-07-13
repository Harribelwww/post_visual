"""Point-error and interval-band plot primitives."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from post_visual.core.axes import style_axes
from post_visual.core.figure import get_fig_ax
from post_visual.style.contexts import style_context
from post_visual.style.palettes import RGB, resolve_colors
from post_visual.style.rc import DEFAULT_FIGSIZE_CM


def errorbar(
    x: Any,
    y: Any,
    *,
    xerr: Any | None = None,
    yerr: Any | None = None,
    label: str | None = None,
    color: Any | None = None,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    legend: bool | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    errorbar_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Draw point estimates with optional x/y errors and return ``(fig, ax)``."""

    x_values, y_values = _validate_xy(x, y)
    x_errors = _validate_error(xerr, length=x_values.size, name="xerr")
    y_errors = _validate_error(yerr, length=y_values.size, name="yerr")
    draw_args = dict(
        x=x_values,
        y=y_values,
        xerr=x_errors,
        yerr=y_errors,
        label=label,
        color=color,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        legend=legend,
        figsize_cm=figsize_cm,
        errorbar_kws=errorbar_kws,
        legend_kws=legend_kws,
    )
    if not style:
        return _draw_errorbar(**draw_args)
    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_errorbar(**draw_args)


def interval_band(
    x: Any,
    lower: Any,
    upper: Any,
    *,
    center: Any | None = None,
    orientation: str = "vertical",
    label: str | None = None,
    color: Any | None = None,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    legend: bool | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    band_kws: Mapping[str, Any] | None = None,
    line_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Draw a vertical or horizontal interval band with an optional center line."""

    coordinates, lower_values, upper_values, center_values = _validate_interval(
        x=x, lower=lower, upper=upper, center=center
    )
    orientation = _normalize_orientation(orientation)
    draw_args = dict(
        coordinates=coordinates,
        lower=lower_values,
        upper=upper_values,
        center=center_values,
        orientation=orientation,
        label=label,
        color=color,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        legend=legend,
        figsize_cm=figsize_cm,
        band_kws=band_kws,
        line_kws=line_kws,
        legend_kws=legend_kws,
    )
    if not style:
        return _draw_interval_band(**draw_args)
    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_interval_band(**draw_args)


def point_range(
    estimates: Any,
    lower: Any,
    upper: Any,
    *,
    categories: Sequence[Any] | None = None,
    orientation: str = "horizontal",
    reference: float | None = None,
    annotate: bool = False,
    fmt: str = ".3g",
    color: Any | None = None,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    errorbar_kws: Mapping[str, Any] | None = None,
    reference_kws: Mapping[str, Any] | None = None,
    text_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Draw categorical point estimates with lower and upper interval bounds."""

    values, lower_values, upper_values = _validate_point_range(estimates, lower, upper)
    labels = _category_labels(categories, length=values.size)
    orientation = _normalize_orientation(orientation)
    draw_args = dict(
        estimates=values,
        lower=lower_values,
        upper=upper_values,
        categories=labels,
        orientation=orientation,
        reference=reference,
        annotate=annotate,
        fmt=fmt,
        color=color,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        figsize_cm=figsize_cm,
        errorbar_kws=errorbar_kws,
        reference_kws=reference_kws,
        text_kws=text_kws,
    )
    if not style:
        return _draw_point_range(**draw_args)
    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_point_range(**draw_args)


def forest_plot(*args: Any, **kwargs: Any) -> tuple[Figure, Axes]:
    """Draw a horizontal point-range plot suitable for forest-style summaries."""

    if "orientation" in kwargs:
        raise TypeError("forest_plot fixes orientation='horizontal'.")
    return point_range(*args, orientation="horizontal", **kwargs)


def _draw_errorbar(
    *,
    x: np.ndarray,
    y: np.ndarray,
    xerr: np.ndarray | None,
    yerr: np.ndarray | None,
    label: str | None,
    color: Any | None,
    palette: str | int | Sequence[RGB],
    ax: Axes | None,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
    legend: bool | None,
    figsize_cm: tuple[float, float],
    errorbar_kws: Mapping[str, Any] | None,
    legend_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    resolved_color = color if color is not None else resolve_colors(palette, n=1)[0]
    kwargs = {
        "fmt": "o",
        "linestyle": "none",
        "markersize": 5,
        "markerfacecolor": "white",
        "capsize": 3,
        "elinewidth": 1.0,
        "linewidth": 1.0,
    }
    kwargs.update(errorbar_kws or {})
    plot_ax.errorbar(x, y, xerr=xerr, yerr=yerr, label=label, color=resolved_color, **kwargs)
    _finish_axes(plot_ax, title=title, xlabel=xlabel, ylabel=ylabel)
    _maybe_add_legend(plot_ax, label=label, legend=legend, legend_kws=legend_kws)
    return fig, plot_ax


def _draw_point_range(
    *,
    estimates: np.ndarray,
    lower: np.ndarray,
    upper: np.ndarray,
    categories: list[str],
    orientation: str,
    reference: float | None,
    annotate: bool,
    fmt: str,
    color: Any | None,
    palette: str | int | Sequence[RGB],
    ax: Axes | None,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
    figsize_cm: tuple[float, float],
    errorbar_kws: Mapping[str, Any] | None,
    reference_kws: Mapping[str, Any] | None,
    text_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    positions = np.arange(estimates.size)
    resolved_color = color if color is not None else resolve_colors(palette, n=1)[0]
    errors = np.vstack([estimates - lower, upper - estimates])
    kwargs = {
        "fmt": "o",
        "linestyle": "none",
        "markersize": 5,
        "markerfacecolor": "white",
        "capsize": 3,
        "elinewidth": 1.2,
        "color": resolved_color,
    }
    kwargs.update(errorbar_kws or {})
    if orientation == "horizontal":
        plot_ax.errorbar(estimates, positions, xerr=errors, **kwargs)
        plot_ax.set_yticks(positions)
        plot_ax.set_yticklabels(categories)
        plot_ax.grid(False, axis="y")
    else:
        plot_ax.errorbar(positions, estimates, yerr=errors, **kwargs)
        plot_ax.set_xticks(positions)
        plot_ax.set_xticklabels(categories)
        plot_ax.grid(False, axis="x")
    if reference is not None:
        reference_options = {"color": "0.35", "linestyle": "--", "linewidth": 1.0}
        reference_options.update(reference_kws or {})
        if orientation == "horizontal":
            plot_ax.axvline(reference, **reference_options)
        else:
            plot_ax.axhline(reference, **reference_options)
    if annotate:
        options = {"fontsize": 8, "va": "center", "ha": "left"}
        options.update(text_kws or {})
        for position, estimate in zip(positions, estimates):
            if orientation == "horizontal":
                plot_ax.annotate(format(estimate, fmt), (estimate, position), xytext=(5, 0), textcoords="offset points", **options)
            else:
                vertical_options = {"fontsize": 8, "va": "bottom", "ha": "center", **(text_kws or {})}
                plot_ax.annotate(format(estimate, fmt), (position, estimate), xytext=(0, 5), textcoords="offset points", **vertical_options)
    _finish_axes(plot_ax, title=title, xlabel=xlabel, ylabel=ylabel)
    return fig, plot_ax


def _draw_interval_band(
    *,
    coordinates: np.ndarray,
    lower: np.ndarray,
    upper: np.ndarray,
    center: np.ndarray | None,
    orientation: str,
    label: str | None,
    color: Any | None,
    palette: str | int | Sequence[RGB],
    ax: Axes | None,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
    legend: bool | None,
    figsize_cm: tuple[float, float],
    band_kws: Mapping[str, Any] | None,
    line_kws: Mapping[str, Any] | None,
    legend_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    resolved_color = color if color is not None else resolve_colors(palette, n=1)[0]
    fill_kws = {"alpha": 0.2, "linewidth": 0.0, "color": resolved_color}
    fill_kws.update(band_kws or {})
    line_options = {"linewidth": 1.5, "color": resolved_color}
    line_options.update(line_kws or {})
    band_label = label if center is None else None
    if orientation == "vertical":
        plot_ax.fill_between(coordinates, lower, upper, label=band_label, **fill_kws)
        if center is not None:
            plot_ax.plot(coordinates, center, label=label, **line_options)
    else:
        plot_ax.fill_betweenx(coordinates, lower, upper, label=band_label, **fill_kws)
        if center is not None:
            plot_ax.plot(center, coordinates, label=label, **line_options)
    _finish_axes(plot_ax, title=title, xlabel=xlabel, ylabel=ylabel)
    _maybe_add_legend(plot_ax, label=label, legend=legend, legend_kws=legend_kws)
    return fig, plot_ax


def _validate_xy(x: Any, y: Any) -> tuple[np.ndarray, np.ndarray]:
    x_values = np.ravel(np.asarray(x, dtype=float))
    y_values = np.ravel(np.asarray(y, dtype=float))
    if x_values.size == 0 or x_values.size != y_values.size:
        raise ValueError("x and y must be non-empty and have the same length.")
    if not np.all(np.isfinite(x_values)) or not np.all(np.isfinite(y_values)):
        raise ValueError("x and y must contain only finite values.")
    return x_values, y_values


def _validate_point_range(
    estimates: Any, lower: Any, upper: Any
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    values = np.ravel(np.asarray(estimates, dtype=float))
    lower_values = np.ravel(np.asarray(lower, dtype=float))
    upper_values = np.ravel(np.asarray(upper, dtype=float))
    if values.size == 0 or lower_values.size != values.size or upper_values.size != values.size:
        raise ValueError("estimates, lower, and upper must be non-empty and have matching lengths.")
    if not all(np.all(np.isfinite(item)) for item in (values, lower_values, upper_values)):
        raise ValueError("point-range values must be finite.")
    if np.any(lower_values > values) or np.any(values > upper_values):
        raise ValueError("each estimate must lie between its lower and upper bounds.")
    return values, lower_values, upper_values


def _category_labels(categories: Sequence[Any] | None, *, length: int) -> list[str]:
    if categories is None:
        return [f"Category {index + 1}" for index in range(length)]
    result = [str(value) for value in categories]
    if len(result) != length:
        raise ValueError(f"categories must have length {length}.")
    return result


def _validate_error(error: Any | None, *, length: int, name: str) -> np.ndarray | None:
    if error is None:
        return None
    values = np.asarray(error, dtype=float)
    if values.ndim == 1 and values.size == length:
        pass
    elif values.ndim == 2 and values.shape == (2, length):
        pass
    else:
        raise ValueError(f"{name} must have shape ({length},) or (2, {length}).")
    if not np.all(np.isfinite(values)) or np.any(values < 0):
        raise ValueError(f"{name} must contain finite non-negative values.")
    return values


def _validate_interval(
    *, x: Any, lower: Any, upper: Any, center: Any | None
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray | None]:
    coordinates = np.ravel(np.asarray(x, dtype=float))
    lower_values = np.ravel(np.asarray(lower, dtype=float))
    upper_values = np.ravel(np.asarray(upper, dtype=float))
    arrays = [coordinates, lower_values, upper_values]
    center_values = None if center is None else np.ravel(np.asarray(center, dtype=float))
    if center_values is not None:
        arrays.append(center_values)
    if coordinates.size == 0 or any(values.size != coordinates.size for values in arrays):
        raise ValueError("x, lower, upper, and center must be non-empty and have matching lengths.")
    if any(not np.all(np.isfinite(values)) for values in arrays):
        raise ValueError("interval values must be finite.")
    if np.any(lower_values > upper_values):
        raise ValueError("lower values must not exceed upper values.")
    if center_values is not None and (
        np.any(center_values < lower_values) or np.any(center_values > upper_values)
    ):
        raise ValueError("center values must lie within the interval.")
    return coordinates, lower_values, upper_values, center_values


def _normalize_orientation(orientation: str) -> str:
    key = orientation.strip().lower()
    aliases = {"v": "vertical", "vertical": "vertical", "h": "horizontal", "horizontal": "horizontal"}
    if key not in aliases:
        raise ValueError("orientation must be 'vertical' or 'horizontal'.")
    return aliases[key]


def _finish_axes(ax: Axes, *, title: str | None, xlabel: str | None, ylabel: str | None) -> None:
    ax.margins(0.05)
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)


def _maybe_add_legend(
    ax: Axes,
    *,
    label: str | None,
    legend: bool | None,
    legend_kws: Mapping[str, Any] | None,
) -> None:
    show = legend if legend is not None else label is not None
    if not show:
        return
    kwargs = {"loc": "best", "frameon": True, "fontsize": 11}
    kwargs.update(legend_kws or {})
    legend_obj = ax.legend(**kwargs)
    legend_obj.get_frame().set_edgecolor("black")
    legend_obj.get_frame().set_facecolor("white")
