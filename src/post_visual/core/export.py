"""Figure export helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from matplotlib.figure import Figure


def save_figure(
    fig: Figure,
    path: str | Path,
    *,
    dpi: int = 300,
    bbox_inches: str | None = "tight",
    facecolor: str = "white",
    **savefig_kws: Any,
) -> Path:
    """Save a matplotlib figure with publication-oriented defaults."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        output_path,
        dpi=dpi,
        bbox_inches=bbox_inches,
        facecolor=facecolor,
        **savefig_kws,
    )
    return output_path

