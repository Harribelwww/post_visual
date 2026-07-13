"""Figure and axes construction helpers."""

from __future__ import annotations

from typing import Any

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from post_visual.style.rc import DEFAULT_FIGSIZE_CM, cm_to_inches


def get_fig_ax(
    ax: Axes | None = None,
    *,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    **subplot_kws: Any,
) -> tuple[Figure, Axes]:
    """Return `(fig, ax)`, creating a figure when `ax` is not supplied."""

    if ax is not None:
        return ax.figure, ax

    fig, new_ax = plt.subplots(figsize=cm_to_inches(*figsize_cm), **subplot_kws)
    return fig, new_ax

