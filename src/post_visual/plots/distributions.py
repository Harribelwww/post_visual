"""Distribution plot primitives."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from scipy.stats import gaussian_kde

from post_visual.core.axes import style_axes
from post_visual.core.figure import get_fig_ax
from post_visual.style.contexts import style_context
from post_visual.style.palettes import RGB, resolve_colors
from post_visual.style.rc import DEFAULT_FIGSIZE_CM


@dataclass(frozen=True)
class _DistributionGroup:
    values: np.ndarray
    label: str | None = None


def hist(
    data: Any | None = None,
    x: Any | None = None,
    *,
    hue: str | None = None,
    bins: int | Sequence[float] | str = "auto",
    density: bool = False,
    stacked: bool = False,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    legend: bool | None = None,
    alpha: float = 0.35,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    hist_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Draw one or more histograms and return `(fig, ax)`."""

    draw_args = dict(
        data=data,
        x=x,
        hue=hue,
        bins=bins,
        density=density,
        stacked=stacked,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        legend=legend,
        alpha=alpha,
        figsize_cm=figsize_cm,
        hist_kws=hist_kws,
        legend_kws=legend_kws,
    )

    if not style:
        return _draw_hist(**draw_args)

    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_hist(**draw_args)


def box(
    data: Any | None = None,
    x: Any | None = None,
    y: Any | None = None,
    *,
    hue: str | None = None,
    labels: Sequence[Any] | None = None,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    box_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Draw a box plot for array or DataFrame-style groups."""

    draw_args = dict(
        data=data,
        x=x,
        y=y,
        hue=hue,
        labels=labels,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        figsize_cm=figsize_cm,
        box_kws=box_kws,
    )

    if not style:
        return _draw_box(**draw_args)

    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_box(**draw_args)


def violin(
    data: Any | None = None,
    x: Any | None = None,
    y: Any | None = None,
    *,
    hue: str | None = None,
    labels: Sequence[Any] | None = None,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    violin_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Draw a violin plot for array or DataFrame-style groups."""

    draw_args = dict(
        data=data,
        x=x,
        y=y,
        hue=hue,
        labels=labels,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        figsize_cm=figsize_cm,
        violin_kws=violin_kws,
    )

    if not style:
        return _draw_violin(**draw_args)
    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_violin(**draw_args)


def kde(
    data: Any | None = None,
    x: Any | None = None,
    *,
    hue: str | None = None,
    bw_method: str | float | None = None,
    gridsize: int = 200,
    cut: float = 3.0,
    fill: bool = False,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = "Density",
    legend: bool | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    line_kws: Mapping[str, Any] | None = None,
    fill_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Draw one-dimensional Gaussian kernel density estimates."""

    if gridsize < 2 or cut < 0:
        raise ValueError("gridsize must be at least 2 and cut must be non-negative.")
    groups = _normalize_hist_input(data=data, x=x, hue=hue)
    draw_args = dict(
        groups=groups,
        bw_method=bw_method,
        gridsize=gridsize,
        cut=cut,
        fill=fill,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel or (x if isinstance(x, str) else None),
        ylabel=ylabel,
        legend=legend,
        figsize_cm=figsize_cm,
        line_kws=line_kws,
        fill_kws=fill_kws,
        legend_kws=legend_kws,
    )
    if not style:
        return _draw_kde(**draw_args)
    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_kde(**draw_args)


def ecdf(
    data: Any | None = None,
    x: Any | None = None,
    *,
    hue: str | None = None,
    complementary: bool = False,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    legend: bool | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    line_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Draw empirical cumulative distribution functions."""

    groups = _normalize_hist_input(data=data, x=x, hue=hue)
    draw_args = dict(
        groups=groups,
        complementary=complementary,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel or (x if isinstance(x, str) else None),
        ylabel=ylabel or ("Survival probability" if complementary else "Cumulative probability"),
        legend=legend,
        figsize_cm=figsize_cm,
        line_kws=line_kws,
        legend_kws=legend_kws,
    )
    if not style:
        return _draw_ecdf(**draw_args)
    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_ecdf(**draw_args)


def strip(
    data: Any | None = None,
    x: Any | None = None,
    y: Any | None = None,
    *,
    hue: str | None = None,
    labels: Sequence[Any] | None = None,
    orientation: str = "vertical",
    jitter: float = 0.12,
    seed: int | None = 0,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    scatter_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Draw jittered raw observations for one or more categories."""

    if jitter < 0:
        raise ValueError("jitter must be non-negative.")
    orientation = _normalize_orientation(orientation)
    groups = _normalize_grouped_input(data=data, x=x, y=y, hue=hue, labels=labels)
    draw_args = dict(
        groups=groups,
        orientation=orientation,
        jitter=jitter,
        seed=seed,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel or (x if isinstance(x, str) else None),
        ylabel=ylabel or (y if isinstance(y, str) else None),
        figsize_cm=figsize_cm,
        scatter_kws=scatter_kws,
    )
    if not style:
        return _draw_strip(**draw_args)
    style_palette: str | int = palette if isinstance(palette, str | int) else "furina"
    with style_context(palette=style_palette, usetex=usetex):
        return _draw_strip(**draw_args)

def _draw_hist(
    *,
    data: Any | None,
    x: Any | None,
    hue: str | None,
    bins: int | Sequence[float] | str,
    density: bool,
    stacked: bool,
    palette: str | int | Sequence[RGB],
    ax: Axes | None,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
    legend: bool | None,
    alpha: float,
    figsize_cm: tuple[float, float],
    hist_kws: Mapping[str, Any] | None,
    legend_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    groups = _normalize_hist_input(data=data, x=x, hue=hue)

    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    colors = resolve_colors(palette, n=len(groups))

    base_hist_kws = {
        "bins": bins,
        "density": density,
        "alpha": alpha,
        "edgecolor": "black",
        "linewidth": 0.8,
    }
    if hist_kws:
        base_hist_kws.update(hist_kws)

    if stacked and len(groups) > 1:
        draw_kws = {
            "label": [group.label for group in groups],
            "color": colors,
            "stacked": True,
            **base_hist_kws,
        }
        plot_ax.hist(
            [group.values for group in groups],
            **draw_kws,
        )
    else:
        for index, group in enumerate(groups):
            draw_kws = {
                "label": group.label,
                "color": colors[index],
                **base_hist_kws,
            }
            plot_ax.hist(
                group.values,
                **draw_kws,
            )

    if title:
        plot_ax.set_title(title)
    if xlabel or isinstance(x, str):
        plot_ax.set_xlabel(xlabel or x)
    plot_ax.set_ylabel(ylabel or ("Density" if density else "Count"))

    _maybe_add_legend(plot_ax, groups=groups, legend=legend, legend_kws=legend_kws)
    return fig, plot_ax


def _draw_kde(
    *,
    groups: Sequence[_DistributionGroup],
    bw_method: str | float | None,
    gridsize: int,
    cut: float,
    fill: bool,
    palette: str | int | Sequence[RGB],
    ax: Axes | None,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
    legend: bool | None,
    figsize_cm: tuple[float, float],
    line_kws: Mapping[str, Any] | None,
    fill_kws: Mapping[str, Any] | None,
    legend_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    colors = resolve_colors(palette, n=len(groups))
    line_options = {"linewidth": 1.5}
    line_options.update(line_kws or {})
    fill_options = {"alpha": 0.2, "linewidth": 0.0}
    fill_options.update(fill_kws or {})
    for group, color in zip(groups, colors):
        if group.values.size < 2 or np.unique(group.values).size < 2:
            raise ValueError("KDE groups must contain at least two distinct finite values.")
        estimator = gaussian_kde(group.values, bw_method=bw_method)
        bandwidth = float(np.sqrt(estimator.covariance[0, 0]))
        grid = np.linspace(group.values.min() - cut * bandwidth, group.values.max() + cut * bandwidth, gridsize)
        density = estimator(grid)
        plot_ax.plot(grid, density, color=color, label=group.label, **line_options)
        if fill:
            plot_ax.fill_between(grid, 0, density, color=color, **fill_options)
    _finish_distribution_axes(plot_ax, title=title, xlabel=xlabel, ylabel=ylabel)
    _maybe_add_legend(plot_ax, groups=groups, legend=legend, legend_kws=legend_kws)
    return fig, plot_ax


def _draw_ecdf(
    *,
    groups: Sequence[_DistributionGroup],
    complementary: bool,
    palette: str | int | Sequence[RGB],
    ax: Axes | None,
    title: str | None,
    xlabel: str | None,
    ylabel: str,
    legend: bool | None,
    figsize_cm: tuple[float, float],
    line_kws: Mapping[str, Any] | None,
    legend_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    colors = resolve_colors(palette, n=len(groups))
    options = {"where": "post", "linewidth": 1.5}
    options.update(line_kws or {})
    for group, color in zip(groups, colors):
        values = np.sort(group.values)
        probabilities = np.arange(1, values.size + 1) / values.size
        if complementary:
            probabilities = 1 - probabilities
        plot_ax.step(values, probabilities, color=color, label=group.label, **options)
    plot_ax.set_ylim(-0.02, 1.02)
    _finish_distribution_axes(plot_ax, title=title, xlabel=xlabel, ylabel=ylabel)
    _maybe_add_legend(plot_ax, groups=groups, legend=legend, legend_kws=legend_kws)
    return fig, plot_ax


def _draw_strip(
    *,
    groups: Sequence[_DistributionGroup],
    orientation: str,
    jitter: float,
    seed: int | None,
    palette: str | int | Sequence[RGB],
    ax: Axes | None,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
    figsize_cm: tuple[float, float],
    scatter_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    colors = resolve_colors(palette, n=len(groups))
    rng = np.random.default_rng(seed)
    options = {"s": 24, "alpha": 0.7, "edgecolors": "black", "linewidths": 0.4, "zorder": 3}
    options.update(scatter_kws or {})
    positions = np.arange(1, len(groups) + 1)
    for position, group, color in zip(positions, groups, colors):
        offsets = rng.uniform(-jitter, jitter, group.values.size) if jitter else np.zeros(group.values.size)
        if orientation == "vertical":
            plot_ax.scatter(position + offsets, group.values, color=color, **options)
        else:
            plot_ax.scatter(group.values, position + offsets, color=color, **options)
    labels = [group.label for group in groups]
    if orientation == "vertical":
        plot_ax.set_xticks(positions)
        plot_ax.set_xticklabels(labels)
        plot_ax.grid(False, axis="x")
    else:
        plot_ax.set_yticks(positions)
        plot_ax.set_yticklabels(labels)
        plot_ax.grid(False, axis="y")
    _finish_distribution_axes(plot_ax, title=title, xlabel=xlabel, ylabel=ylabel)
    return fig, plot_ax


def _draw_box(
    *,
    data: Any | None,
    x: Any | None,
    y: Any | None,
    hue: str | None,
    labels: Sequence[Any] | None,
    palette: str | int | Sequence[RGB],
    ax: Axes | None,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
    figsize_cm: tuple[float, float],
    box_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    groups = _normalize_grouped_input(data=data, x=x, y=y, hue=hue, labels=labels)

    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    plot_ax.grid(False, axis="x")
    plot_ax.grid(True, axis="y", linestyle="--", alpha=0.15, color="black")

    positions = np.arange(1, len(groups) + 1)
    base_box_kws = {
        "patch_artist": True,
        "showfliers": False,
        "medianprops": {"color": "black", "linewidth": 1.2},
        "boxprops": {"edgecolor": "black", "linewidth": 0.8},
        "whiskerprops": {"color": "black", "linewidth": 0.8},
        "capprops": {"color": "black", "linewidth": 0.8},
    }
    if box_kws:
        base_box_kws.update(box_kws)

    result = plot_ax.boxplot(
        [group.values for group in groups],
        positions=positions,
        **base_box_kws,
    )
    plot_ax.set_xticks(positions)
    plot_ax.set_xticklabels([group.label for group in groups])
    colors = resolve_colors(palette, n=len(groups))
    for patch, color in zip(result["boxes"], colors, strict=True):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)

    if title:
        plot_ax.set_title(title)
    if xlabel or isinstance(x, str):
        plot_ax.set_xlabel(xlabel or x)
    if ylabel or isinstance(y, str):
        plot_ax.set_ylabel(ylabel or y)
    return fig, plot_ax


def _draw_violin(
    *,
    data: Any | None,
    x: Any | None,
    y: Any | None,
    hue: str | None,
    labels: Sequence[Any] | None,
    palette: str | int | Sequence[RGB],
    ax: Axes | None,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
    figsize_cm: tuple[float, float],
    violin_kws: Mapping[str, Any] | None,
) -> tuple[Figure, Axes]:
    groups = _normalize_grouped_input(data=data, x=x, y=y, hue=hue, labels=labels)

    fig, plot_ax = get_fig_ax(ax=ax, figsize_cm=figsize_cm)
    style_axes(plot_ax)
    plot_ax.grid(False, axis="x")
    plot_ax.grid(True, axis="y", linestyle="--", alpha=0.15, color="black")

    positions = np.arange(1, len(groups) + 1)
    base_violin_kws = {
        "showmeans": False,
        "showmedians": True,
        "showextrema": True,
    }
    if violin_kws:
        base_violin_kws.update(violin_kws)

    result = plot_ax.violinplot(
        [group.values for group in groups],
        positions=positions,
        **base_violin_kws,
    )
    colors = resolve_colors(palette, n=len(groups))
    for body, color in zip(result["bodies"], colors, strict=True):
        body.set_facecolor(color)
        body.set_edgecolor("black")
        body.set_alpha(0.75)

    for key in ("cbars", "cmins", "cmaxes", "cmedians"):
        artist = result.get(key)
        if artist is not None:
            artist.set_color("black")
            artist.set_linewidth(0.8)

    plot_ax.set_xticks(positions)
    plot_ax.set_xticklabels([group.label for group in groups])

    if title:
        plot_ax.set_title(title)
    if xlabel or isinstance(x, str):
        plot_ax.set_xlabel(xlabel or x)
    if ylabel or isinstance(y, str):
        plot_ax.set_ylabel(ylabel or y)
    return fig, plot_ax


def _normalize_hist_input(
    *,
    data: Any | None,
    x: Any | None,
    hue: str | None,
) -> list[_DistributionGroup]:
    if _is_dataframe_like(data) and isinstance(x, str):
        if hue is None:
            return [_make_group(data[x], label=None)]
        return [_make_group(frame[x], label=str(key)) for key, frame in data.groupby(hue, sort=False)]

    values = data if x is None else x
    if values is None:
        raise ValueError("Provide histogram values through `data`, `x`, or DataFrame-style columns.")
    return [_make_group(values, label=None)]


def _normalize_grouped_input(
    *,
    data: Any | None,
    x: Any | None,
    y: Any | None,
    hue: str | None,
    labels: Sequence[Any] | None,
) -> list[_DistributionGroup]:
    if _is_dataframe_like(data):
        if isinstance(y, str) and isinstance(x, str):
            return _groups_from_dataframe(data=data, x=x, y=y, hue=hue)
        if isinstance(y, str) and x is None:
            return [_make_group(data[y], label=y)]
        if isinstance(x, str) and y is None:
            return [_make_group(data[x], label=x)]

    values = data if data is not None else y if y is not None else x
    if values is None:
        raise ValueError("Provide distribution values through `data`, `x`, `y`, or DataFrame-style columns.")
    return _groups_from_array(values, labels=labels)


def _groups_from_dataframe(
    *,
    data: Any,
    x: str,
    y: str,
    hue: str | None,
) -> list[_DistributionGroup]:
    group_cols = [x] if hue is None else [x, hue]
    groups = []
    for key, frame in data.groupby(group_cols, sort=False):
        if isinstance(key, tuple):
            label = " | ".join(str(part) for part in key)
        else:
            label = str(key)
        groups.append(_make_group(frame[y], label=label))
    return groups


def _groups_from_array(values: Any, labels: Sequence[Any] | None) -> list[_DistributionGroup]:
    array = np.asarray(values, dtype=float)
    if array.ndim == 1:
        label = str(labels[0]) if labels is not None and len(labels) > 0 else None
        return [_make_group(array, label=label)]
    if array.ndim != 2:
        raise ValueError("Distribution values must be one-dimensional or two-dimensional.")

    if labels is not None and len(labels) != array.shape[1]:
        raise ValueError(f"labels must have length {array.shape[1]}.")
    result = []
    for index in range(array.shape[1]):
        label = str(labels[index]) if labels is not None else f"Group {index + 1}"
        result.append(_make_group(array[:, index], label=label))
    return result


def _make_group(values: Any, *, label: str | None) -> _DistributionGroup:
    array = np.ravel(np.asarray(values, dtype=float))
    array = array[np.isfinite(array)]
    if array.size == 0:
        raise ValueError("Distribution data must contain at least one finite value.")
    return _DistributionGroup(values=array, label=label)


def _is_dataframe_like(data: Any) -> bool:
    return data is not None and hasattr(data, "groupby") and hasattr(data, "__getitem__")


def _normalize_orientation(orientation: str) -> str:
    key = orientation.strip().lower()
    aliases = {"v": "vertical", "vertical": "vertical", "h": "horizontal", "horizontal": "horizontal"}
    if key not in aliases:
        raise ValueError("orientation must be 'vertical' or 'horizontal'.")
    return aliases[key]


def _finish_distribution_axes(
    ax: Axes, *, title: str | None, xlabel: str | None, ylabel: str | None
) -> None:
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)


def _maybe_add_legend(
    ax: Axes,
    *,
    groups: Sequence[_DistributionGroup],
    legend: bool | None,
    legend_kws: Mapping[str, Any] | None,
) -> None:
    has_labels = any(group.label for group in groups)
    if legend is False or (legend is None and not has_labels):
        return

    handles, labels = ax.get_legend_handles_labels()
    if not handles:
        return

    kwargs = {"loc": "best", "frameon": True, "fontsize": 9}
    if legend_kws:
        kwargs.update(legend_kws)
    legend_obj = ax.legend(handles, labels, **kwargs)
    legend_obj.get_frame().set_edgecolor("black")
    legend_obj.get_frame().set_facecolor("white")
