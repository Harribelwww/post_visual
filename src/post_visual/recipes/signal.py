"""Biosignal and connectivity visualization recipes."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
from matplotlib import colormaps
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from post_visual.plots.matrix import heatmap
from post_visual.style.rc import DEFAULT_FIGSIZE_CM


def connectivity_matrix(
    matrix: Any,
    *,
    labels: Sequence[Any] | None = None,
    triangle: str | None = None,
    include_diagonal: bool = True,
    symmetric: bool | None = None,
    center: float | None = None,
    cmap: str | None = None,
    mask_color: str = "#F7F7F7",
    annot: bool = False,
    fmt: str = ".2f",
    colorbar: bool = True,
    colorbar_label: str | None = "Connectivity",
    vmin: float | None = None,
    vmax: float | None = None,
    ax: Axes | None = None,
    title: str | None = "Connectivity Matrix",
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    imshow_kws: Mapping[str, Any] | None = None,
    colorbar_kws: Mapping[str, Any] | None = None,
    annot_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Plot a square connectivity or connectivity-difference matrix.

    ``triangle`` can hide the redundant half of a symmetric matrix. Set
    ``center=0`` for difference matrices to use a zero-centered color scale.
    """

    values, resolved_labels = _normalize_connectivity(matrix, labels=labels)
    if symmetric is True and not np.allclose(values, values.T, equal_nan=True):
        raise ValueError("matrix must be symmetric when symmetric=True.")
    masked = _apply_triangle_mask(
        values,
        triangle=triangle,
        include_diagonal=include_diagonal,
    )
    resolved_vmin, resolved_vmax = _resolve_color_limits(
        values,
        center=center,
        vmin=vmin,
        vmax=vmax,
    )
    resolved_cmap = cmap or ("RdBu_r" if center is not None else "viridis")
    cmap_obj = colormaps.get_cmap(resolved_cmap).with_extremes(bad=mask_color)
    image_options = {"cmap": cmap_obj}
    image_options.update(imshow_kws or {})
    colorbar_options = dict(colorbar_kws or {})
    if colorbar_label:
        colorbar_options.setdefault("label", colorbar_label)

    fig, plot_ax = heatmap(
        masked,
        xlabels=resolved_labels,
        ylabels=resolved_labels,
        annot=False,
        cmap=resolved_cmap,
        colorbar=colorbar,
        vmin=resolved_vmin,
        vmax=resolved_vmax,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        figsize_cm=figsize_cm,
        style=style,
        usetex=usetex,
        imshow_kws=image_options,
        colorbar_kws=colorbar_options,
    )
    if annot:
        _annotate_visible_cells(
            plot_ax,
            matrix=masked,
            fmt=fmt,
            annot_kws=annot_kws,
        )
    return fig, plot_ax


def _normalize_connectivity(
    matrix: Any,
    *,
    labels: Sequence[Any] | None,
) -> tuple[np.ndarray, list[str]]:
    if _is_dataframe_like(matrix):
        values = np.asarray(matrix.to_numpy(dtype=float))
        resolved_labels = [str(value) for value in (labels or matrix.columns.tolist())]
        if labels is None and list(matrix.index) != list(matrix.columns):
            raise ValueError("DataFrame connectivity index and columns must match.")
    else:
        values = np.asarray(matrix, dtype=float)
        resolved_labels = (
            [str(value) for value in labels]
            if labels is not None
            else [str(index + 1) for index in range(values.shape[0] if values.ndim else 0)]
        )
    if values.ndim != 2 or values.shape[0] == 0 or values.shape[0] != values.shape[1]:
        raise ValueError("connectivity matrix must be a non-empty square array.")
    if len(resolved_labels) != values.shape[0]:
        raise ValueError(f"labels must have length {values.shape[0]}.")
    return values, resolved_labels


def _apply_triangle_mask(
    values: np.ndarray,
    *,
    triangle: str | None,
    include_diagonal: bool,
) -> np.ndarray:
    result = values.astype(float, copy=True)
    if triangle is None:
        if not include_diagonal:
            np.fill_diagonal(result, np.nan)
        return result
    key = triangle.strip().lower()
    if key == "upper":
        result[np.tril_indices_from(result, k=-1 if include_diagonal else 0)] = np.nan
    elif key == "lower":
        result[np.triu_indices_from(result, k=1 if include_diagonal else 0)] = np.nan
    else:
        raise ValueError("triangle must be None, 'upper', or 'lower'.")
    return result


def _resolve_color_limits(
    values: np.ndarray,
    *,
    center: float | None,
    vmin: float | None,
    vmax: float | None,
) -> tuple[float | None, float | None]:
    if center is None:
        return vmin, vmax
    finite = values[np.isfinite(values)]
    if finite.size == 0:
        raise ValueError("matrix must contain at least one finite value.")
    if vmin is None and vmax is None:
        radius = float(np.max(np.abs(finite - center)))
        return center - radius, center + radius
    if vmin is None:
        return 2 * center - float(vmax), vmax
    if vmax is None:
        return vmin, 2 * center - float(vmin)
    if not np.isclose(center - vmin, vmax - center):
        raise ValueError("vmin and vmax must be symmetric around center.")
    return vmin, vmax


def _annotate_visible_cells(
    ax: Axes,
    *,
    matrix: np.ndarray,
    fmt: str,
    annot_kws: Mapping[str, Any] | None,
) -> None:
    image = ax.images[-1]
    options = {"ha": "center", "va": "center", "fontsize": 9}
    options.update(annot_kws or {})
    for row, col in np.argwhere(np.isfinite(matrix)):
        value = matrix[row, col]
        rgba = image.cmap(image.norm(value))
        luminance = 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]
        ax.text(
            col,
            row,
            format(value, fmt),
            color="white" if luminance < 0.45 else "black",
            **options,
        )


def _is_dataframe_like(data: Any) -> bool:
    return all(hasattr(data, attribute) for attribute in ("columns", "index", "to_numpy"))
