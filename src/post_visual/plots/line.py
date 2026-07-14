"""Line plot primitive with the `sci_plot.m` scale aliases."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
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

DEFAULT_MARKERS = ("o", "s", "^", "d", "v", ">", "<", "p", "h")

_SCALE_ALIASES = {
    "p": ("linear", "linear"),
    "plot": ("linear", "linear"),
    "line": ("linear", "linear"),
    "linear": ("linear", "linear"),
    "sx": ("log", "linear"),
    "semilogx": ("log", "linear"),
    "sy": ("linear", "log"),
    "semilogy": ("linear", "log"),
    "ll": ("log", "log"),
    "loglog": ("log", "log"),
}


@dataclass(frozen=True)
class _LineSeries:
    x: np.ndarray
    y: np.ndarray
    label: str | None = None


def line(
    data: Any | None = None,
    x: Any | None = None,
    y: Any | None = None,
    *,
    series: Sequence[Any] | None = None,
    hue: str | None = None,
    label: str | None = None,
    lower: Any | None = None,
    upper: Any | None = None,
    nan_policy: str = "gap",
    plot_type: str = "p",
    scale: str | tuple[str, str] | None = None,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    legend: bool | None = None,
    marker: str | None = None,
    markers: Sequence[str] = DEFAULT_MARKERS,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    line_kws: Mapping[str, Any] | None = None,
    band_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Draw one or more 2D line series and return `(fig, ax)`.

    Inputs can be `(x, y)` arrays, an `N x 2` array via `data`, a sequence
    passed through `series`, or a DataFrame-like object with column names.
    The `plot_type` aliases mirror `sci_plot.m`: `p`, `sx`, `sy`, and `ll`.
    """

    draw_args = dict(
        data=data,
        x=x,
        y=y,
        series=series,
        hue=hue,
        label=label,
        lower=lower,
        upper=upper,
        nan_policy=nan_policy,
        plot_type=plot_type,
        scale=scale,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        legend=legend,
        marker=marker,
        markers=markers,
        figsize_cm=figsize_cm,
        line_kws=line_kws,
        band_kws=band_kws,
        legend_kws=legend_kws,
    )

    if not style:
        return _draw_line(**draw_args)

    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_line(**draw_args)


plot_line = line


def _draw_line(
    *,
    data: Any | None,
    x: Any | None,
    y: Any | None,
    series: Sequence[Any] | None,
    hue: str | None,
    label: str | None,
    lower: Any | None,
    upper: Any | None,
    nan_policy: str,
    plot_type: str,
    scale: str | tuple[str, str] | None,
    palette: str | int | Sequence[RGB],
    ax: Axes | None,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
    legend: bool | None,
    marker: str | None,
    markers: Sequence[str],
    figsize_cm: tuple[float, float],
    line_kws: Mapping[str, Any] | None,
    band_kws: Mapping[str, Any] | None,
    legend_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    line_series = _normalize_input(
        data=data,
        x=x,
        y=y,
        series=series,
        hue=hue,
        label=label,
    )
    band = _normalize_band(lower, upper, line_series=line_series, nan_policy=nan_policy)
    line_series, band = _apply_nan_policy(
        line_series,
        nan_policy=nan_policy,
        band=band,
    )
    xscale, yscale = _resolve_scales(plot_type=plot_type, scale=scale)
    _validate_log_data(line_series, xscale=xscale, yscale=yscale)

    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    plot_ax.set_xscale(xscale)
    plot_ax.set_yscale(yscale)

    colors = resolve_colors(palette, n=len(line_series))
    if marker is None and len(markers) == 0:
        raise ValueError("markers must not be empty when marker is not provided.")
    base_line_kws = {
        "linewidth": 1.5,
        "linestyle": "-",
        "markersize": 5,
        "markerfacecolor": "white",
    }
    if line_kws:
        base_line_kws.update(line_kws)
    base_band_kws = {"alpha": 0.2, "linewidth": 0.0}
    base_band_kws.update(band_kws or {})

    for index, item in enumerate(line_series):
        color = colors[index]
        marker_value = marker if marker is not None else markers[index % len(markers)]
        plot_kws = {
            "color": color,
            "marker": marker_value,
            "markeredgecolor": color,
            "label": item.label,
            **base_line_kws,
        }
        if band is not None and index == 0:
            lower_values, upper_values = band
            fill_kws = {"color": color, **base_band_kws}
            plot_ax.fill_between(item.x, lower_values, upper_values, **fill_kws)
        plot_ax.plot(item.x, item.y, **plot_kws)

    plot_ax.margins(x=0.05, y=0.05)

    if title:
        plot_ax.set_title(title)
    if xlabel or isinstance(x, str):
        plot_ax.set_xlabel(xlabel or x)
    if ylabel or isinstance(y, str):
        plot_ax.set_ylabel(ylabel or y)

    _maybe_add_legend(
        plot_ax,
        line_series=line_series,
        legend=legend,
        legend_kws=legend_kws,
    )
    return fig, plot_ax


def _normalize_input(
    *,
    data: Any | None,
    x: Any | None,
    y: Any | None,
    series: Sequence[Any] | None,
    hue: str | None,
    label: str | None,
) -> list[_LineSeries]:
    if series is not None:
        if any(value is not None for value in (data, x, y, hue)):
            raise ValueError("Use either `series` or (`data`, `x`, `y`, `hue`), not both.")
        return [_normalize_series_item(item) for item in series]

    if _is_dataframe_like(data) and isinstance(x, str):
        if not isinstance(y, str):
            raise ValueError("DataFrame-style input requires string column names for x and y.")
        return _normalize_dataframe(data=data, x=x, y=y, hue=hue, label=label)

    if data is not None and x is not None and y is None and not isinstance(x, str):
        return [_make_series(data, x, label=label)]

    if data is not None and x is None and y is None:
        x_values, y_values = _xy_from_matrix(data)
        return [_make_series(x_values, y_values, label=label)]

    if x is not None and y is not None:
        return [_make_series(x, y, label=label)]

    raise ValueError(
        "Provide x/y arrays, an N x 2 `data` array, DataFrame-style columns, "
        "or `series`."
    )


def _normalize_dataframe(
    *,
    data: Any,
    x: str,
    y: str,
    hue: str | None,
    label: str | None,
) -> list[_LineSeries]:
    if hue is None:
        return [_make_series(data[x], data[y], label=label)]

    result = []
    for key, frame in data.groupby(hue, sort=False):
        result.append(_make_series(frame[x], frame[y], label=str(key)))
    return result


def _normalize_series_item(item: Any) -> _LineSeries:
    if isinstance(item, Mapping):
        if "data" in item:
            x_values, y_values = _xy_from_matrix(item["data"])
            return _make_series(x_values, y_values, label=item.get("label"))
        return _make_series(item["x"], item["y"], label=item.get("label"))

    if not isinstance(item, Sequence) or isinstance(item, str):
        x_values, y_values = _xy_from_matrix(item)
        return _make_series(x_values, y_values)

    if len(item) == 2:
        first, second = item
        if isinstance(second, str):
            x_values, y_values = _xy_from_matrix(first)
            return _make_series(x_values, y_values, label=second)
        return _make_series(first, second)

    if len(item) == 3:
        first, second, label = item
        return _make_series(first, second, label=str(label))

    raise ValueError(
        "`series` items must be (x, y), (x, y, label), (N x 2 data, label), "
        "or mappings with x/y/label."
    )


def _make_series(x_values: Any, y_values: Any, *, label: str | None = None) -> _LineSeries:
    x_array = np.asarray(x_values)
    y_array = np.asarray(y_values)

    if x_array.ndim != 1:
        x_array = np.ravel(x_array)
    if y_array.ndim != 1:
        y_array = np.ravel(y_array)

    if x_array.size != y_array.size:
        raise ValueError("x and y must have the same length.")
    if x_array.size == 0:
        raise ValueError("Line data must contain at least one point.")

    return _LineSeries(x=x_array, y=y_array, label=label)


def _xy_from_matrix(data: Any) -> tuple[np.ndarray, np.ndarray]:
    array = np.asarray(data)
    if array.ndim != 2 or array.shape[1] < 2:
        raise ValueError("`data` must be an N x 2 array when x/y are omitted.")
    return array[:, 0], array[:, 1]


def _is_dataframe_like(data: Any) -> bool:
    return data is not None and hasattr(data, "groupby") and hasattr(data, "__getitem__")


def _resolve_scales(
    *,
    plot_type: str,
    scale: str | tuple[str, str] | None,
) -> tuple[str, str]:
    if isinstance(scale, tuple):
        if scale[0] not in {"linear", "log"} or scale[1] not in {"linear", "log"}:
            raise ValueError("scale tuple must contain only 'linear' or 'log'.")
        return scale

    alias = scale or plot_type
    key = str(alias).strip().lower()
    if key not in _SCALE_ALIASES:
        valid = ", ".join(sorted(_SCALE_ALIASES))
        raise ValueError(f"Unknown plot_type/scale {alias!r}. Valid aliases: {valid}.")
    return _SCALE_ALIASES[key]


def _validate_log_data(
    line_series: Sequence[_LineSeries],
    *,
    xscale: str,
    yscale: str,
) -> None:
    if xscale == "log":
        _validate_positive_values(line_series, axis="x")
    if yscale == "log":
        _validate_positive_values(line_series, axis="y")


def _validate_positive_values(line_series: Sequence[_LineSeries], *, axis: str) -> None:
    for item in line_series:
        values = item.x if axis == "x" else item.y
        finite_values = values[np.isfinite(values)]
        if finite_values.size and np.any(finite_values <= 0):
            label = f" for {item.label!r}" if item.label else ""
            raise ValueError(f"{axis} values must be positive for log-scale plots{label}.")


def _apply_nan_policy(
    line_series: Sequence[_LineSeries],
    *,
    nan_policy: str,
    band: tuple[np.ndarray, np.ndarray] | None,
) -> tuple[list[_LineSeries], tuple[np.ndarray, np.ndarray] | None]:
    key = nan_policy.strip().lower()
    if key not in {"gap", "omit", "raise"}:
        raise ValueError("nan_policy must be 'gap', 'omit', or 'raise'.")
    result = []
    resolved_band = band
    for index, item in enumerate(line_series):
        finite = np.isfinite(item.x) & np.isfinite(item.y)
        if band is not None and index == 0:
            lower_values, upper_values = band
            finite &= np.isfinite(lower_values) & np.isfinite(upper_values)
        if key == "raise" and not np.all(finite):
            raise ValueError("line or band data contains non-finite values with nan_policy='raise'.")
        if key == "omit":
            if not np.any(finite):
                raise ValueError("line data must retain at least one finite point after omission.")
            result.append(_LineSeries(x=item.x[finite], y=item.y[finite], label=item.label))
            if band is not None and index == 0:
                resolved_band = (lower_values[finite], upper_values[finite])
        elif key == "gap" and band is not None and index == 0:
            resolved_lower = lower_values.astype(float, copy=True)
            resolved_upper = upper_values.astype(float, copy=True)
            resolved_lower[~finite] = np.nan
            resolved_upper[~finite] = np.nan
            resolved_band = (resolved_lower, resolved_upper)
            result.append(item)
        else:
            result.append(item)
    return result, resolved_band


def _normalize_band(
    lower: Any | None,
    upper: Any | None,
    *,
    line_series: Sequence[_LineSeries],
    nan_policy: str,
) -> tuple[np.ndarray, np.ndarray] | None:
    if lower is None and upper is None:
        return None
    if lower is None or upper is None:
        raise ValueError("lower and upper must be provided together.")
    if len(line_series) != 1:
        raise ValueError("direct lower/upper bands are supported only for a single line series.")
    lower_values = np.ravel(np.asarray(lower, dtype=float))
    upper_values = np.ravel(np.asarray(upper, dtype=float))
    target = line_series[0].x.size
    if lower_values.size != target or upper_values.size != target:
        raise ValueError("lower and upper must match the plotted line length.")
    finite = np.isfinite(lower_values) & np.isfinite(upper_values)
    if nan_policy == "raise" and not np.all(finite):
        raise ValueError("band data contains non-finite values with nan_policy='raise'.")
    if np.any(lower_values[finite] > upper_values[finite]):
        raise ValueError("lower band values must not exceed upper values.")
    return lower_values, upper_values


def _maybe_add_legend(
    ax: Axes,
    *,
    line_series: Sequence[_LineSeries],
    legend: bool | None,
    legend_kws: Mapping[str, Any] | None,
) -> None:
    has_labels = any(item.label for item in line_series)
    if legend is False or (legend is None and not has_labels):
        return

    handles, labels = ax.get_legend_handles_labels()
    if not handles:
        return

    kwargs = {
        "loc": "best",
        "frameon": True,
        "fontsize": 9,
        "ncol": max(ceil(len(handles) / 5), 1),
    }
    if legend_kws:
        kwargs.update(legend_kws)

    legend_obj = ax.legend(handles, labels, **kwargs)
    legend_obj.get_frame().set_edgecolor("black")
    legend_obj.get_frame().set_facecolor("white")
