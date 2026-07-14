"""Multi-panel figure layout helpers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from string import ascii_lowercase
from typing import Any

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from post_visual.style.contexts import style_context
from post_visual.style.rc import cm_to_inches


def panel_grid(
    nrows: int,
    ncols: int,
    *,
    n_panels: int | None = None,
    sharex: bool | str = False,
    sharey: bool | str = False,
    panel_size_cm: tuple[float, float] = (7.0, 6.0),
    figsize_cm: tuple[float, float] | None = None,
    squeeze: bool = False,
    labels: bool | Sequence[Any] = False,
    label_prefix: str = "(",
    label_suffix: str = ")",
    suptitle: str | None = None,
    layout: str | None = "constrained",
    style: bool = True,
    usetex: bool = False,
    gridspec_kws: Mapping[str, Any] | None = None,
    subplot_kws: Mapping[str, Any] | None = None,
    adjust_kws: Mapping[str, Any] | None = None,
    label_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, np.ndarray]:
    """Create a regular panel layout and return ``(fig, axes)``.

    The returned axes are a two-dimensional object array unless ``squeeze``
    is explicitly requested. Extra axes beyond ``n_panels`` are hidden.
    """

    if nrows <= 0 or ncols <= 0:
        raise ValueError("nrows and ncols must be positive integers.")
    total = nrows * ncols
    visible = total if n_panels is None else n_panels
    if visible <= 0 or visible > total:
        raise ValueError("n_panels must be between 1 and nrows * ncols.")
    resolved_size = figsize_cm or (panel_size_cm[0] * ncols, panel_size_cm[1] * nrows)
    draw_args = dict(
        nrows=nrows,
        ncols=ncols,
        n_panels=visible,
        sharex=sharex,
        sharey=sharey,
        figsize_cm=resolved_size,
        squeeze=squeeze,
        labels=labels,
        label_prefix=label_prefix,
        label_suffix=label_suffix,
        suptitle=suptitle,
        layout=layout,
        gridspec_kws=gridspec_kws,
        subplot_kws=subplot_kws,
        adjust_kws=adjust_kws,
        label_kws=label_kws,
    )
    if not style:
        return _draw_panel_grid(**draw_args)
    with style_context(usetex=usetex):
        return _draw_panel_grid(**draw_args)


def label_panels(
    axes: Any,
    *,
    labels: Sequence[Any] | None = None,
    prefix: str = "(",
    suffix: str = ")",
    text_kws: Mapping[str, Any] | None = None,
) -> np.ndarray:
    """Add panel labels in axes coordinates and return the axes array."""

    axes_array = np.asarray(axes, dtype=object)
    flat_axes = [ax for ax in axes_array.ravel() if isinstance(ax, Axes) and ax.get_visible()]
    resolved_labels = _panel_labels(labels, length=len(flat_axes), prefix=prefix, suffix=suffix)
    kwargs = {
        "x": -0.08,
        "y": 1.04,
        "ha": "right",
        "va": "bottom",
        "fontsize": 10,
        "fontweight": "bold",
        "transform": None,
    }
    kwargs.update(text_kws or {})
    for ax, label in zip(flat_axes, resolved_labels):
        local = dict(kwargs)
        if local.get("transform") is None:
            local["transform"] = ax.transAxes
        x = local.pop("x")
        y = local.pop("y")
        ax.text(x, y, label, **local)
    return axes_array


def _draw_panel_grid(
    *,
    nrows: int,
    ncols: int,
    n_panels: int,
    sharex: bool | str,
    sharey: bool | str,
    figsize_cm: tuple[float, float],
    squeeze: bool,
    labels: bool | Sequence[Any],
    label_prefix: str,
    label_suffix: str,
    suptitle: str | None,
    layout: str | None,
    gridspec_kws: Mapping[str, Any] | None,
    subplot_kws: Mapping[str, Any] | None,
    adjust_kws: Mapping[str, Any] | None,
    label_kws: Mapping[str, Any] | None,
) -> tuple[Figure, np.ndarray]:
    fig, axes = plt.subplots(
        nrows,
        ncols,
        sharex=sharex,
        sharey=sharey,
        squeeze=squeeze,
        figsize=cm_to_inches(*figsize_cm),
        layout=layout if not adjust_kws else None,
        gridspec_kw=dict(gridspec_kws or {}),
        subplot_kw=dict(subplot_kws or {}),
    )
    axes_array = np.asarray(axes, dtype=object)
    for ax in axes_array.ravel()[n_panels:]:
        ax.set_visible(False)
    if labels:
        custom = None if labels is True else labels
        label_panels(
            axes_array,
            labels=custom,
            prefix=label_prefix,
            suffix=label_suffix,
            text_kws=label_kws,
        )
    if suptitle:
        fig.suptitle(suptitle)
    if adjust_kws:
        fig.subplots_adjust(**adjust_kws)
    return fig, axes_array


def _panel_labels(
    labels: Sequence[Any] | None,
    *,
    length: int,
    prefix: str,
    suffix: str,
) -> list[str]:
    if labels is None:
        if length > len(ascii_lowercase):
            raise ValueError("automatic panel labels support at most 26 visible panels.")
        return [f"{prefix}{ascii_lowercase[index]}{suffix}" for index in range(length)]
    result = [str(label) for label in labels]
    if len(result) != length:
        raise ValueError(f"panel labels must have length {length}.")
    return result
