"""Composable event-line and event-span annotation primitives."""

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


def annotate_text(
    text: str,
    xy: tuple[float, float],
    *,
    coordinates: str = "data",
    ax: Axes | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    text_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Add a text label in data or axes coordinates."""

    transform_name = _normalize_coordinates(coordinates)
    draw_args = dict(
        text=str(text),
        xy=_validate_xy_point(xy, name="xy"),
        coordinates=transform_name,
        ax=ax,
        figsize_cm=figsize_cm,
        text_kws=text_kws,
    )
    if not style:
        return _draw_text_annotation(**draw_args)
    with style_context(usetex=usetex):
        return _draw_text_annotation(**draw_args)


def annotate_arrow(
    text: str,
    xy: tuple[float, float],
    xytext: tuple[float, float],
    *,
    coordinates: str = "data",
    text_coordinates: str | None = None,
    ax: Axes | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    arrow_kws: Mapping[str, Any] | None = None,
    text_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Add a labeled arrow between two points."""

    xycoords = _normalize_coordinates(coordinates)
    textcoords = _normalize_coordinates(text_coordinates or coordinates)
    draw_args = dict(
        text=str(text),
        xy=_validate_xy_point(xy, name="xy"),
        xytext=_validate_xy_point(xytext, name="xytext"),
        coordinates=xycoords,
        text_coordinates=textcoords,
        ax=ax,
        figsize_cm=figsize_cm,
        arrow_kws=arrow_kws,
        text_kws=text_kws,
    )
    if not style:
        return _draw_arrow_annotation(**draw_args)
    with style_context(usetex=usetex):
        return _draw_arrow_annotation(**draw_args)


def significance_bracket(
    start: float,
    end: float,
    level: float,
    *,
    label: str = "*",
    orientation: str = "vertical",
    tip: float | None = None,
    ax: Axes | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    line_kws: Mapping[str, Any] | None = None,
    text_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Add a significance bracket between two category positions."""

    if not np.all(np.isfinite([start, end, level])) or start >= end:
        raise ValueError("start, end, and level must be finite with start < end.")
    orientation = _normalize_orientation(orientation)
    draw_args = dict(
        start=float(start),
        end=float(end),
        level=float(level),
        label=str(label),
        orientation=orientation,
        tip=tip,
        ax=ax,
        figsize_cm=figsize_cm,
        line_kws=line_kws,
        text_kws=text_kws,
    )
    if not style:
        return _draw_significance_bracket(**draw_args)
    with style_context(usetex=usetex):
        return _draw_significance_bracket(**draw_args)


def event_lines(
    positions: Any,
    *,
    labels: Sequence[Any] | None = None,
    orientation: str = "vertical",
    colors: Sequence[Any] | Any | None = None,
    palette: str | int | Sequence[RGB] = "furina",
    annotate: bool = True,
    legend: bool = False,
    ax: Axes | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    line_kws: Mapping[str, Any] | None = None,
    text_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Add vertical or horizontal event lines to an axes."""

    values = _normalize_positions(positions)
    resolved_labels = _normalize_labels(labels, length=values.size)
    orientation = _normalize_orientation(orientation)
    draw_args = dict(
        positions=values,
        labels=resolved_labels,
        orientation=orientation,
        colors=colors,
        palette=palette,
        annotate=annotate,
        legend=legend,
        ax=ax,
        figsize_cm=figsize_cm,
        line_kws=line_kws,
        text_kws=text_kws,
        legend_kws=legend_kws,
    )
    if not style:
        return _draw_event_lines(**draw_args)
    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_event_lines(**draw_args)


def event_spans(
    spans: Any,
    *,
    labels: Sequence[Any] | None = None,
    orientation: str = "vertical",
    colors: Sequence[Any] | Any | None = None,
    palette: str | int | Sequence[RGB] = "furina",
    annotate: bool = True,
    legend: bool = False,
    ax: Axes | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    span_kws: Mapping[str, Any] | None = None,
    text_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Add vertical or horizontal event intervals to an axes."""

    values = _normalize_spans(spans)
    resolved_labels = _normalize_labels(labels, length=values.shape[0])
    orientation = _normalize_orientation(orientation)
    draw_args = dict(
        spans=values,
        labels=resolved_labels,
        orientation=orientation,
        colors=colors,
        palette=palette,
        annotate=annotate,
        legend=legend,
        ax=ax,
        figsize_cm=figsize_cm,
        span_kws=span_kws,
        text_kws=text_kws,
        legend_kws=legend_kws,
    )
    if not style:
        return _draw_event_spans(**draw_args)
    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_event_spans(**draw_args)


def _draw_text_annotation(
    *,
    text: str,
    xy: tuple[float, float],
    coordinates: str,
    ax: Axes | None,
    figsize_cm: tuple[float, float],
    text_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    transform = plot_ax.transData if coordinates == "data" else plot_ax.transAxes
    kwargs = {"ha": "center", "va": "center", "fontsize": 10}
    kwargs.update(text_kws or {})
    plot_ax.text(*xy, text, transform=transform, **kwargs)
    return fig, plot_ax


def _draw_arrow_annotation(
    *,
    text: str,
    xy: tuple[float, float],
    xytext: tuple[float, float],
    coordinates: str,
    text_coordinates: str,
    ax: Axes | None,
    figsize_cm: tuple[float, float],
    arrow_kws: Mapping[str, Any] | None,
    text_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    kwargs = {"ha": "center", "va": "center", "fontsize": 10}
    kwargs.update(text_kws or {})
    arrowprops = {"arrowstyle": "->", "color": "black", "linewidth": 1.0}
    arrowprops.update(arrow_kws or {})
    plot_ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        xycoords=coordinates,
        textcoords=text_coordinates,
        arrowprops=arrowprops,
        **kwargs,
    )
    return fig, plot_ax


def _draw_significance_bracket(
    *,
    start: float,
    end: float,
    level: float,
    label: str,
    orientation: str,
    tip: float | None,
    ax: Axes | None,
    figsize_cm: tuple[float, float],
    line_kws: Mapping[str, Any] | None,
    text_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    line_options = {"color": "black", "linewidth": 1.0, "clip_on": False}
    line_options.update(line_kws or {})
    text_options = {"ha": "center", "va": "bottom", "fontsize": 10, "clip_on": False}
    text_options.update(text_kws or {})
    if orientation == "vertical":
        resolved_tip = _axis_tip(plot_ax.get_ylim(), tip)
        plot_ax.plot([start, start, end, end], [level - resolved_tip, level, level, level - resolved_tip], **line_options)
        plot_ax.text((start + end) / 2, level, label, **text_options)
    else:
        resolved_tip = _axis_tip(plot_ax.get_xlim(), tip)
        plot_ax.plot([level - resolved_tip, level, level, level - resolved_tip], [start, start, end, end], **line_options)
        horizontal_text = {**text_options, "ha": "left", "va": "center"}
        plot_ax.text(level, (start + end) / 2, label, **horizontal_text)
    return fig, plot_ax


def _draw_event_lines(
    *,
    positions: np.ndarray,
    labels: list[str | None],
    orientation: str,
    colors: Sequence[Any] | Any | None,
    palette: str | int | Sequence[RGB],
    annotate: bool,
    legend: bool,
    ax: Axes | None,
    figsize_cm: tuple[float, float],
    line_kws: Mapping[str, Any] | None,
    text_kws: Mapping[str, Any] | None,
    legend_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    resolved_colors = _resolve_annotation_colors(colors, palette=palette, length=positions.size)
    line_options = {"linestyle": "--", "linewidth": 1.0, "alpha": 0.9, "zorder": 3}
    line_options.update(line_kws or {})
    base_text_kws = _line_text_defaults(orientation)
    base_text_kws.update(text_kws or {})

    for position, label, color in zip(positions, labels, resolved_colors):
        artist_label = label if legend and label is not None else None
        draw_kws = {"color": color, "label": artist_label, **line_options}
        if orientation == "vertical":
            plot_ax.axvline(position, **draw_kws)
            if annotate and label is not None:
                plot_ax.text(position, 0.98, label, transform=plot_ax.get_xaxis_transform(), **base_text_kws)
        else:
            plot_ax.axhline(position, **draw_kws)
            if annotate and label is not None:
                plot_ax.text(0.98, position, label, transform=plot_ax.get_yaxis_transform(), **base_text_kws)
    _maybe_add_legend(plot_ax, show=legend, legend_kws=legend_kws)
    return fig, plot_ax


def _draw_event_spans(
    *,
    spans: np.ndarray,
    labels: list[str | None],
    orientation: str,
    colors: Sequence[Any] | Any | None,
    palette: str | int | Sequence[RGB],
    annotate: bool,
    legend: bool,
    ax: Axes | None,
    figsize_cm: tuple[float, float],
    span_kws: Mapping[str, Any] | None,
    text_kws: Mapping[str, Any] | None,
    legend_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    resolved_colors = _resolve_annotation_colors(colors, palette=palette, length=spans.shape[0])
    span_options = {"alpha": 0.16, "linewidth": 0.0, "zorder": 0}
    span_options.update(span_kws or {})
    base_text_kws = _span_text_defaults(orientation)
    base_text_kws.update(text_kws or {})

    for bounds, label, color in zip(spans, labels, resolved_colors):
        start, end = bounds
        midpoint = (start + end) / 2
        artist_label = label if legend and label is not None else None
        draw_kws = {"color": color, "label": artist_label, **span_options}
        if orientation == "vertical":
            plot_ax.axvspan(start, end, **draw_kws)
            if annotate and label is not None:
                plot_ax.text(midpoint, 0.98, label, transform=plot_ax.get_xaxis_transform(), **base_text_kws)
        else:
            plot_ax.axhspan(start, end, **draw_kws)
            if annotate and label is not None:
                plot_ax.text(0.98, midpoint, label, transform=plot_ax.get_yaxis_transform(), **base_text_kws)
    _maybe_add_legend(plot_ax, show=legend, legend_kws=legend_kws)
    return fig, plot_ax


def _normalize_positions(positions: Any) -> np.ndarray:
    values = np.ravel(np.asarray(positions, dtype=float))
    if values.size == 0 or not np.all(np.isfinite(values)):
        raise ValueError("positions must contain at least one finite value.")
    return values


def _normalize_coordinates(coordinates: str) -> str:
    key = coordinates.strip().lower()
    aliases = {"data": "data", "axes": "axes fraction", "axes fraction": "axes fraction"}
    if key not in aliases:
        raise ValueError("coordinates must be 'data' or 'axes'.")
    return aliases[key]


def _validate_xy_point(value: Any, *, name: str) -> tuple[float, float]:
    array = np.ravel(np.asarray(value, dtype=float))
    if array.size != 2 or not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain two finite coordinates.")
    return float(array[0]), float(array[1])


def _axis_tip(limits: tuple[float, float], tip: float | None) -> float:
    if tip is not None:
        if tip <= 0:
            raise ValueError("tip must be positive.")
        return tip
    span = abs(limits[1] - limits[0])
    return 0.02 * span if span > 0 else 0.02


def _normalize_spans(spans: Any) -> np.ndarray:
    values = np.asarray(spans, dtype=float)
    if values.ndim == 1 and values.size == 2:
        values = values.reshape(1, 2)
    if values.ndim != 2 or values.shape[0] == 0 or values.shape[1] != 2:
        raise ValueError("spans must have shape (n, 2).")
    if not np.all(np.isfinite(values)):
        raise ValueError("spans must contain only finite values.")
    if np.any(values[:, 0] >= values[:, 1]):
        raise ValueError("each span start must be less than its end.")
    return values


def _normalize_labels(labels: Sequence[Any] | None, *, length: int) -> list[str | None]:
    if labels is None:
        return [None] * length
    if isinstance(labels, str):
        result = [labels]
    else:
        result = [str(label) for label in labels]
    if len(result) != length:
        raise ValueError(f"labels must have length {length}.")
    return result


def _normalize_orientation(orientation: str) -> str:
    key = orientation.strip().lower()
    aliases = {"v": "vertical", "vertical": "vertical", "h": "horizontal", "horizontal": "horizontal"}
    if key not in aliases:
        raise ValueError("orientation must be 'vertical' or 'horizontal'.")
    return aliases[key]


def _resolve_annotation_colors(
    colors: Sequence[Any] | Any | None,
    *,
    palette: str | int | Sequence[RGB],
    length: int,
) -> list[Any]:
    if colors is None:
        return list(resolve_colors(palette, n=length))
    if isinstance(colors, str) or not isinstance(colors, Sequence):
        return [colors] * length
    resolved = list(colors)
    if len(resolved) in {3, 4} and all(isinstance(value, (int, float)) for value in resolved):
        return [colors] * length
    if len(resolved) != length:
        raise ValueError(f"colors must be a single color or have length {length}.")
    return resolved


def _line_text_defaults(orientation: str) -> dict[str, Any]:
    if orientation == "vertical":
        return {"ha": "right", "va": "top", "rotation": 90, "fontsize": 9}
    return {"ha": "right", "va": "bottom", "rotation": 0, "fontsize": 9}


def _span_text_defaults(orientation: str) -> dict[str, Any]:
    if orientation == "vertical":
        return {"ha": "center", "va": "top", "fontsize": 9}
    return {"ha": "right", "va": "center", "fontsize": 9}


def _maybe_add_legend(
    ax: Axes,
    *,
    show: bool,
    legend_kws: Mapping[str, Any] | None,
) -> None:
    if not show:
        return
    handles, labels = ax.get_legend_handles_labels()
    if not handles:
        return
    kwargs = {"loc": "best", "frameon": True, "fontsize": 9}
    kwargs.update(legend_kws or {})
    legend_obj = ax.legend(handles, labels, **kwargs)
    legend_obj.get_frame().set_edgecolor("black")
    legend_obj.get_frame().set_facecolor("white")
