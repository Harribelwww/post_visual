"""Matplotlib rcParams for the fixed scientific style."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import matplotlib as mpl
from cycler import cycler

from .palettes import get_palette

CM_TO_INCH = 1 / 2.54
DEFAULT_FIGSIZE_CM = (16.0, 12.0)
DEFAULT_SERIF_FONTS = (
    "Times New Roman",
    "Times",
    "STIXGeneral",
    "DejaVu Serif",
)


def cm_to_inches(width_cm: float, height_cm: float) -> tuple[float, float]:
    """Convert a figure size from centimeters to inches."""

    return width_cm * CM_TO_INCH, height_cm * CM_TO_INCH


def scientific_rc(
    palette: str | int = "furina",
    *,
    usetex: bool = False,
    font_serif: Sequence[str] = DEFAULT_SERIF_FONTS,
) -> dict[str, Any]:
    """Build rcParams for the `post_visual` scientific plotting style."""

    colors = get_palette(palette)
    figsize = cm_to_inches(*DEFAULT_FIGSIZE_CM)

    return {
        "figure.figsize": figsize,
        "figure.facecolor": "white",
        "figure.dpi": 120,
        "savefig.facecolor": "white",
        "savefig.edgecolor": "white",
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "font.family": "serif",
        "font.serif": list(font_serif),
        "font.size": 10,
        "font.weight": "normal",
        "mathtext.fontset": "stix",
        "text.usetex": bool(usetex),
        "axes.facecolor": "white",
        "axes.edgecolor": "black",
        "axes.linewidth": 0.8,
        "axes.labelsize": 10,
        "axes.labelweight": "normal",
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.grid": True,
        "axes.axisbelow": "line",
        "axes.prop_cycle": cycler(color=colors),
        "grid.color": "black",
        "grid.alpha": 0.15,
        "grid.linestyle": "--",
        "grid.linewidth": 0.8,
        "lines.linewidth": 1.5,
        "lines.markersize": 5,
        "xtick.color": "black",
        "ytick.color": "black",
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.minor.visible": True,
        "ytick.minor.visible": True,
        "legend.fontsize": 9,
        "legend.frameon": True,
        "legend.edgecolor": "black",
        "legend.facecolor": "white",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }


def apply_style(
    palette: str | int = "furina",
    *,
    usetex: bool = False,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Apply the scientific style globally and return the rcParams used."""

    rc = scientific_rc(palette=palette, usetex=usetex)
    if extra:
        rc.update(extra)
    mpl.rcParams.update(rc)
    return rc
