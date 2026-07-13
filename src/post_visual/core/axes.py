"""Axes-level styling helpers."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

import numpy as np
from matplotlib import ticker
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.legend import Legend


def style_axes(
    ax: Axes,
    *,
    grid: bool = True,
    minor_ticks: bool = True,
) -> Axes:
    """Apply the fixed scientific axes treatment to an existing axes."""

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(0.8)

    ax.tick_params(axis="both", which="both", direction="in", colors="black")

    if minor_ticks:
        ax.minorticks_on()
    if grid:
        ax.grid(True, which="major", linestyle="--", alpha=0.15, color="black")

    ax.set_axisbelow(False)
    return ax


def format_axis(
    ax: Axes,
    *,
    axis: str = "y",
    style: str = "scientific",
    decimals: int = 1,
    scale: float = 100.0,
    scientific_limits: tuple[int, int] = (-3, 4),
) -> tuple[Figure, Axes]:
    """Apply percentage or scientific tick formatting to one axis."""

    axis_name = _normalize_axis(axis)
    key = style.strip().lower()
    target = ax.xaxis if axis_name == "x" else ax.yaxis
    if key in {"percent", "percentage"}:
        target.set_major_formatter(ticker.PercentFormatter(xmax=scale, decimals=decimals))
    elif key in {"scientific", "sci"}:
        formatter = ticker.ScalarFormatter(useMathText=True)
        formatter.set_powerlimits(scientific_limits)
        target.set_major_formatter(formatter)
    else:
        raise ValueError("style must be 'percent' or 'scientific'.")
    return ax.figure, ax


def shared_legend(
    axes: Any,
    *,
    fig: Figure | None = None,
    unique: bool = True,
    remove_axes_legends: bool = True,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Legend]:
    """Collect labeled artists from multiple axes into one figure legend."""

    axes_array = np.asarray(axes, dtype=object).ravel()
    valid_axes = [item for item in axes_array if isinstance(item, Axes) and item.get_visible()]
    if not valid_axes:
        raise ValueError("axes must contain at least one visible Axes.")
    resolved_fig = fig or valid_axes[0].figure
    if any(item.figure is not resolved_fig for item in valid_axes):
        raise ValueError("all axes must belong to the same figure.")
    handles: list[Any] = []
    labels: list[str] = []
    for item in valid_axes:
        local_handles, local_labels = item.get_legend_handles_labels()
        for handle, label in zip(local_handles, local_labels):
            if not label or label.startswith("_") or (unique and label in labels):
                continue
            handles.append(handle)
            labels.append(label)
    if not handles:
        raise ValueError("no labeled artists were found across the supplied axes.")
    kwargs = {"loc": "outside upper center", "ncol": max(1, len(handles)), "frameon": True}
    kwargs.update(legend_kws or {})
    legend = resolved_fig.legend(handles, labels, **kwargs)
    legend.get_frame().set_edgecolor("black")
    legend.get_frame().set_facecolor("white")
    if remove_axes_legends:
        for item in valid_axes:
            local_legend = item.get_legend()
            if local_legend is not None:
                local_legend.remove()
    return resolved_fig, legend


def secondary_axis(
    ax: Axes,
    *,
    axis: str = "x",
    location: str | float = "top",
    functions: tuple[Callable[[Any], Any], Callable[[Any], Any]] | None = None,
    label: str | None = None,
    axis_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Add a Matplotlib secondary x or y axis."""

    axis_name = _normalize_axis(axis)
    kwargs = dict(axis_kws or {})
    if functions is not None:
        kwargs["functions"] = functions
    secondary = (
        ax.secondary_xaxis(location, **kwargs)
        if axis_name == "x"
        else ax.secondary_yaxis(location, **kwargs)
    )
    if label:
        secondary.set_xlabel(label) if axis_name == "x" else secondary.set_ylabel(label)
    return ax.figure, secondary


def inset_axes(
    ax: Axes,
    bounds: Sequence[float],
    *,
    projection: str | None = None,
    inset_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Create an inset axes using parent-axes fractional bounds."""

    values = np.ravel(np.asarray(bounds, dtype=float))
    if values.size != 4 or not np.all(np.isfinite(values)):
        raise ValueError("bounds must contain four finite values: x, y, width, height.")
    if values[2] <= 0 or values[3] <= 0:
        raise ValueError("inset width and height must be positive.")
    kwargs = dict(inset_kws or {})
    if projection is not None:
        kwargs["projection"] = projection
    inset = ax.inset_axes(values.tolist(), **kwargs)
    return ax.figure, inset


def _normalize_axis(axis: str) -> str:
    key = axis.strip().lower()
    if key not in {"x", "y"}:
        raise ValueError("axis must be 'x' or 'y'.")
    return key
