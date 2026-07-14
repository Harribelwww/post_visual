"""Single-image and image-grid plot primitives."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from math import ceil
from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from post_visual.core.figure import get_fig_ax
from post_visual.core.layout import panel_grid
from post_visual.style.contexts import style_context
from post_visual.style.rc import DEFAULT_FIGSIZE_CM


def image(
    data: Any,
    *,
    cmap: str = "gray",
    vmin: float | None = None,
    vmax: float | None = None,
    colorbar: bool = False,
    colorbar_label: str | None = None,
    axis: bool = False,
    ax: Axes | None = None,
    title: str | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    image_kws: Mapping[str, Any] | None = None,
    colorbar_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Display a grayscale, RGB, or RGBA image and return ``(fig, ax)``."""

    array = _validate_image(data)
    draw_args = dict(
        data=array,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        colorbar=colorbar,
        colorbar_label=colorbar_label,
        axis=axis,
        ax=ax,
        title=title,
        figsize_cm=figsize_cm,
        image_kws=image_kws,
        colorbar_kws=colorbar_kws,
    )
    if not style:
        return _draw_image(**draw_args)
    with style_context(usetex=usetex):
        return _draw_image(**draw_args)


def image_grid(
    images: Sequence[Any],
    *,
    titles: Sequence[Any] | None = None,
    ncols: int = 3,
    cmap: str = "gray",
    shared_limits: bool = True,
    vmin: float | None = None,
    vmax: float | None = None,
    colorbar: bool | str = False,
    colorbar_label: str | None = None,
    axis: bool = False,
    axes: Any | None = None,
    panel_size_cm: tuple[float, float] = (6.0, 5.5),
    style: bool = True,
    usetex: bool = False,
    image_kws: Mapping[str, Any] | None = None,
    colorbar_kws: Mapping[str, Any] | None = None,
    layout_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, np.ndarray]:
    """Display multiple images in a regular grid and return ``(fig, axes)``.

    ``colorbar`` accepts ``False``, ``"shared"``, or ``"each"``. Shared
    limits apply only to scalar images; RGB/RGBA images retain native colors.
    """

    arrays = [_validate_image(item) for item in images]
    if not arrays:
        raise ValueError("images must contain at least one image.")
    resolved_titles = _normalize_titles(titles, length=len(arrays))
    mode = _normalize_colorbar_mode(colorbar)
    if mode == "shared" and not shared_limits:
        raise ValueError("A shared colorbar requires shared_limits=True.")
    if ncols <= 0:
        raise ValueError("ncols must be positive.")
    draw_args = dict(
        images=arrays,
        titles=resolved_titles,
        ncols=ncols,
        cmap=cmap,
        shared_limits=shared_limits,
        vmin=vmin,
        vmax=vmax,
        colorbar_mode=mode,
        colorbar_label=colorbar_label,
        axis=axis,
        axes=axes,
        panel_size_cm=panel_size_cm,
        image_kws=image_kws,
        colorbar_kws=colorbar_kws,
        layout_kws=layout_kws,
    )
    if not style:
        return _draw_image_grid(**draw_args)
    with style_context(usetex=usetex):
        return _draw_image_grid(**draw_args)


def _draw_image(
    *,
    data: np.ndarray,
    cmap: str,
    vmin: float | None,
    vmax: float | None,
    colorbar: bool,
    colorbar_label: str | None,
    axis: bool,
    ax: Axes | None,
    title: str | None,
    figsize_cm: tuple[float, float],
    image_kws: Mapping[str, Any] | None,
    colorbar_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    artist = _imshow(plot_ax, data, cmap=cmap, vmin=vmin, vmax=vmax, image_kws=image_kws)
    if not axis:
        plot_ax.set_axis_off()
    if title:
        plot_ax.set_title(title)
    if colorbar and data.ndim == 2:
        cbar = fig.colorbar(artist, ax=plot_ax, **dict(colorbar_kws or {}))
        if colorbar_label:
            cbar.set_label(colorbar_label)
    return fig, plot_ax


def _draw_image_grid(
    *,
    images: list[np.ndarray],
    titles: list[str | None],
    ncols: int,
    cmap: str,
    shared_limits: bool,
    vmin: float | None,
    vmax: float | None,
    colorbar_mode: str,
    colorbar_label: str | None,
    axis: bool,
    axes: Any | None,
    panel_size_cm: tuple[float, float],
    image_kws: Mapping[str, Any] | None,
    colorbar_kws: Mapping[str, Any] | None,
    layout_kws: Mapping[str, Any] | None,
) -> tuple[Figure, np.ndarray]:
    nrows = ceil(len(images) / ncols)
    if axes is None:
        options = dict(layout_kws or {})
        fig, axes_array = panel_grid(
            nrows,
            ncols,
            n_panels=len(images),
            panel_size_cm=panel_size_cm,
            style=False,
            **options,
        )
    else:
        axes_array = np.asarray(axes, dtype=object)
        flat = axes_array.ravel()
        if flat.size < len(images) or not all(isinstance(item, Axes) for item in flat):
            raise ValueError("axes must contain at least one Axes per image.")
        fig = flat[0].figure
        if any(item.figure is not fig for item in flat):
            raise ValueError("all axes must belong to the same figure.")
        for extra in flat[len(images):]:
            extra.set_visible(False)

    scalar_images = [item for item in images if item.ndim == 2]
    resolved_vmin, resolved_vmax = vmin, vmax
    if shared_limits and scalar_images:
        finite = np.concatenate([item[np.isfinite(item)] for item in scalar_images])
        if finite.size:
            resolved_vmin = float(np.min(finite)) if vmin is None else vmin
            resolved_vmax = float(np.max(finite)) if vmax is None else vmax

    artists = []
    scalar_artists = []
    for plot_ax, data, title in zip(axes_array.ravel(), images, titles):
        local_vmin = resolved_vmin if shared_limits else vmin
        local_vmax = resolved_vmax if shared_limits else vmax
        artist = _imshow(
            plot_ax,
            data,
            cmap=cmap,
            vmin=local_vmin,
            vmax=local_vmax,
            image_kws=image_kws,
        )
        artists.append(artist)
        if data.ndim == 2:
            scalar_artists.append((plot_ax, artist))
        if not axis:
            plot_ax.set_axis_off()
        if title:
            plot_ax.set_title(title)

    cbar_options = dict(colorbar_kws or {})
    if colorbar_mode == "shared" and scalar_artists:
        cbar = fig.colorbar(
            scalar_artists[0][1],
            ax=[item[0] for item in scalar_artists],
            **cbar_options,
        )
        if colorbar_label:
            cbar.set_label(colorbar_label)
    elif colorbar_mode == "each":
        for plot_ax, artist in scalar_artists:
            cbar = fig.colorbar(artist, ax=plot_ax, **cbar_options)
            if colorbar_label:
                cbar.set_label(colorbar_label)
    return fig, axes_array


def _imshow(
    ax: Axes,
    data: np.ndarray,
    *,
    cmap: str,
    vmin: float | None,
    vmax: float | None,
    image_kws: Mapping[str, Any] | None,
) -> Any:
    kwargs = {"interpolation": "nearest", "aspect": "equal"}
    if data.ndim == 2:
        kwargs.update(cmap=cmap, vmin=vmin, vmax=vmax)
    kwargs.update(image_kws or {})
    return ax.imshow(data, **kwargs)


def _validate_image(data: Any) -> np.ndarray:
    array = np.asarray(data)
    valid = array.ndim == 2 or (array.ndim == 3 and array.shape[2] in {3, 4})
    if not valid or array.shape[0] == 0 or array.shape[1] == 0:
        raise ValueError("image data must have shape (H, W), (H, W, 3), or (H, W, 4).")
    return array


def _normalize_titles(titles: Sequence[Any] | None, *, length: int) -> list[str | None]:
    if titles is None:
        return [None] * length
    result = [str(title) for title in titles]
    if len(result) != length:
        raise ValueError(f"titles must have length {length}.")
    return result


def _normalize_colorbar_mode(colorbar: bool | str) -> str:
    if colorbar is False:
        return "none"
    if colorbar is True:
        return "shared"
    key = colorbar.strip().lower()
    if key not in {"shared", "each", "none"}:
        raise ValueError("colorbar must be False, True, 'shared', 'each', or 'none'.")
    return key
