"""Matrix and heatmap plot primitives."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import TwoSlopeNorm
from matplotlib.figure import Figure

from post_visual.core.axes import style_axes
from post_visual.core.figure import get_fig_ax
from post_visual.style.contexts import style_context
from post_visual.style.rc import DEFAULT_FIGSIZE_CM


def heatmap(
    data: Any,
    *,
    xlabels: Sequence[Any] | None = None,
    ylabels: Sequence[Any] | None = None,
    annot: bool = False,
    fmt: str = ".2g",
    cmap: str = "viridis",
    colorbar: bool = True,
    vmin: float | None = None,
    vmax: float | None = None,
    ax: Axes | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    imshow_kws: Mapping[str, Any] | None = None,
    colorbar_kws: Mapping[str, Any] | None = None,
    annot_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Draw a heatmap for a 2D array or DataFrame and return `(fig, ax)`."""

    draw_args = dict(
        data=data,
        xlabels=xlabels,
        ylabels=ylabels,
        annot=annot,
        fmt=fmt,
        cmap=cmap,
        colorbar=colorbar,
        vmin=vmin,
        vmax=vmax,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        figsize_cm=figsize_cm,
        imshow_kws=imshow_kws,
        colorbar_kws=colorbar_kws,
        annot_kws=annot_kws,
    )

    if not style:
        return _draw_heatmap(**draw_args)
    with style_context(usetex=usetex):
        return _draw_heatmap(**draw_args)


def grid_color(
    data: Any,
    *,
    x: Any | None = None,
    y: Any | None = None,
    cmap: str = "viridis",
    colorbar: bool = True,
    colorbar_label: str | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    center: float | None = None,
    ax: Axes | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    mesh_kws: Mapping[str, Any] | None = None,
    colorbar_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Draw 2D values on a regular coordinate grid and return ``(fig, ax)``.

    ``x`` and ``y`` may contain cell centers or cell edges. When omitted,
    integer center coordinates are used. This primitive targets continuous
    coordinates such as time-frequency and spatial grids; use :func:`heatmap`
    for categorical matrix labels and cell annotations.
    """

    matrix, x_values, y_values = _normalize_grid(data=data, x=x, y=y)
    draw_args = dict(
        matrix=matrix,
        x=x_values,
        y=y_values,
        cmap=cmap,
        colorbar=colorbar,
        colorbar_label=colorbar_label,
        vmin=vmin,
        vmax=vmax,
        center=center,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        figsize_cm=figsize_cm,
        mesh_kws=mesh_kws,
        colorbar_kws=colorbar_kws,
    )
    if not style:
        return _draw_grid_color(**draw_args)
    with style_context(usetex=usetex):
        return _draw_grid_color(**draw_args)


def _draw_heatmap(
    *,
    data: Any,
    xlabels: Sequence[Any] | None,
    ylabels: Sequence[Any] | None,
    annot: bool,
    fmt: str,
    cmap: str,
    colorbar: bool,
    vmin: float | None,
    vmax: float | None,
    ax: Axes | None,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
    figsize_cm: tuple[float, float],
    imshow_kws: Mapping[str, Any] | None,
    colorbar_kws: Mapping[str, Any] | None,
    annot_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    matrix, resolved_xlabels, resolved_ylabels = _normalize_matrix(
        data=data,
        xlabels=xlabels,
        ylabels=ylabels,
    )

    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax, grid=False, minor_ticks=False)
    plot_ax.grid(False)

    base_imshow_kws = {
        "aspect": "auto",
        "interpolation": "nearest",
        "cmap": cmap,
        "vmin": vmin,
        "vmax": vmax,
    }
    if imshow_kws:
        base_imshow_kws.update(imshow_kws)

    image = plot_ax.imshow(matrix, **base_imshow_kws)
    _set_tick_labels(plot_ax, xlabels=resolved_xlabels, ylabels=resolved_ylabels)

    if annot:
        _annotate_cells(plot_ax, matrix=matrix, image=image, fmt=fmt, annot_kws=annot_kws)

    if colorbar:
        kwargs = {"fraction": 0.046, "pad": 0.04}
        if colorbar_kws:
            kwargs.update(colorbar_kws)
        fig.colorbar(image, ax=plot_ax, **kwargs)

    if title:
        plot_ax.set_title(title)
    if xlabel:
        plot_ax.set_xlabel(xlabel)
    if ylabel:
        plot_ax.set_ylabel(ylabel)
    return fig, plot_ax


def _draw_grid_color(
    *,
    matrix: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
    cmap: str,
    colorbar: bool,
    colorbar_label: str | None,
    vmin: float | None,
    vmax: float | None,
    center: float | None,
    ax: Axes | None,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
    figsize_cm: tuple[float, float],
    mesh_kws: Mapping[str, Any] | None,
    colorbar_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax, grid=False, minor_ticks=False)
    plot_ax.grid(False)
    kwargs: dict[str, Any] = {
        "cmap": cmap,
        "shading": "auto",
        "rasterized": True,
    }
    if center is None:
        kwargs.update(vmin=vmin, vmax=vmax)
    else:
        kwargs["norm"] = _centered_norm(matrix, center=center, vmin=vmin, vmax=vmax)
    kwargs.update(mesh_kws or {})
    mesh = plot_ax.pcolormesh(x, y, matrix, **kwargs)

    if colorbar:
        cbar_kwargs = {"fraction": 0.046, "pad": 0.04}
        cbar_kwargs.update(colorbar_kws or {})
        colorbar_obj = fig.colorbar(mesh, ax=plot_ax, **cbar_kwargs)
        if colorbar_label:
            colorbar_obj.set_label(colorbar_label)
    if title:
        plot_ax.set_title(title)
    if xlabel:
        plot_ax.set_xlabel(xlabel)
    if ylabel:
        plot_ax.set_ylabel(ylabel)
    return fig, plot_ax


def _normalize_matrix(
    *,
    data: Any,
    xlabels: Sequence[Any] | None,
    ylabels: Sequence[Any] | None,
) -> tuple[np.ndarray, list[str] | None, list[str] | None]:
    resolved_xlabels = _labels_to_list(xlabels)
    resolved_ylabels = _labels_to_list(ylabels)

    if _is_dataframe_like(data):
        if resolved_xlabels is None and hasattr(data, "columns"):
            resolved_xlabels = [str(value) for value in data.columns.tolist()]
        if resolved_ylabels is None and hasattr(data, "index"):
            resolved_ylabels = [str(value) for value in data.index.tolist()]
        matrix = np.asarray(data.to_numpy(dtype=float))
    else:
        matrix = np.asarray(data, dtype=float)

    if matrix.ndim != 2:
        raise ValueError("Heatmap data must be two-dimensional.")
    if matrix.shape[0] == 0 or matrix.shape[1] == 0:
        raise ValueError("Heatmap data must not be empty.")

    if resolved_xlabels is not None and len(resolved_xlabels) != matrix.shape[1]:
        raise ValueError(f"xlabels must have length {matrix.shape[1]}.")
    if resolved_ylabels is not None and len(resolved_ylabels) != matrix.shape[0]:
        raise ValueError(f"ylabels must have length {matrix.shape[0]}.")

    return matrix, resolved_xlabels, resolved_ylabels


def _normalize_grid(
    *, data: Any, x: Any | None, y: Any | None
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    matrix = np.asarray(data.to_numpy(dtype=float) if _is_dataframe_like(data) else data, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] == 0 or matrix.shape[1] == 0:
        raise ValueError("Grid-color data must be a non-empty two-dimensional array.")
    x_values = np.arange(matrix.shape[1], dtype=float) if x is None else np.ravel(np.asarray(x, dtype=float))
    y_values = np.arange(matrix.shape[0], dtype=float) if y is None else np.ravel(np.asarray(y, dtype=float))
    _validate_grid_axis(x_values, centers=matrix.shape[1], name="x")
    _validate_grid_axis(y_values, centers=matrix.shape[0], name="y")
    return matrix, x_values, y_values


def _validate_grid_axis(values: np.ndarray, *, centers: int, name: str) -> None:
    if values.size not in {centers, centers + 1}:
        raise ValueError(f"{name} must contain {centers} centers or {centers + 1} edges.")
    if not np.all(np.isfinite(values)) or np.any(np.diff(values) <= 0):
        raise ValueError(f"{name} coordinates must be finite and strictly increasing.")


def _centered_norm(
    matrix: np.ndarray,
    *,
    center: float,
    vmin: float | None,
    vmax: float | None,
) -> TwoSlopeNorm:
    finite = matrix[np.isfinite(matrix)]
    if finite.size == 0:
        raise ValueError("centered grid-color data must contain at least one finite value.")
    if vmin is None and vmax is None:
        radius = float(np.max(np.abs(finite - center)))
        if radius == 0:
            radius = 1.0
        vmin, vmax = center - radius, center + radius
    else:
        vmin = float(np.min(finite)) if vmin is None else vmin
        vmax = float(np.max(finite)) if vmax is None else vmax
    if not vmin < center < vmax:
        raise ValueError("center must lie strictly between vmin and vmax.")
    return TwoSlopeNorm(vmin=vmin, vcenter=center, vmax=vmax)


def _set_tick_labels(
    ax: Axes,
    *,
    xlabels: Sequence[str] | None,
    ylabels: Sequence[str] | None,
) -> None:
    if xlabels is not None:
        ax.set_xticks(np.arange(len(xlabels)))
        ax.set_xticklabels(xlabels)
    if ylabels is not None:
        ax.set_yticks(np.arange(len(ylabels)))
        ax.set_yticklabels(ylabels)


def _annotate_cells(
    ax: Axes,
    *,
    matrix: np.ndarray,
    image: Any,
    fmt: str,
    annot_kws: Mapping[str, Any] | None,
) -> None:
    kwargs = {"ha": "center", "va": "center", "fontsize": 11}
    if annot_kws:
        kwargs.update(annot_kws)

    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            value = matrix[row, col]
            if not np.isfinite(value):
                text = "nan"
                text_color = "black"
            else:
                text = format(value, fmt)
                rgba = image.cmap(image.norm(value))
                luminance = 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]
                text_color = "white" if luminance < 0.45 else "black"
            ax.text(col, row, text, color=text_color, **kwargs)


def _labels_to_list(labels: Sequence[Any] | None) -> list[str] | None:
    if labels is None:
        return None
    return [str(label) for label in labels]


def _is_dataframe_like(data: Any) -> bool:
    return data is not None and hasattr(data, "to_numpy") and hasattr(data, "__getitem__")
