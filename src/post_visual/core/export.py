"""Figure export helpers."""

from __future__ import annotations

from pathlib import Path
from collections.abc import Mapping
from typing import Any, Literal

from matplotlib.figure import Figure

from ..rendering.hybrid import HybridConfig, hybrid_rasterization


PdfMode = Literal["vector", "hybrid"]
SUPPORTED_EXPORT_FORMATS = frozenset({".png", ".pdf"})


def save_figure(
    fig: Figure,
    path: str | Path,
    *,
    dpi: int = 300,
    bbox_inches: str | None = "tight",
    facecolor: str = "white",
    pdf_mode: PdfMode = "vector",
    raster_dpi: int = 300,
    hybrid_kws: HybridConfig | Mapping[str, Any] | None = None,
    **savefig_kws: Any,
) -> Path:
    """Save a figure as PNG or vector/hybrid PDF with scientific defaults."""

    output_path = Path(path)
    suffix = output_path.suffix.lower()
    if suffix not in SUPPORTED_EXPORT_FORMATS:
        supported = ", ".join(sorted(SUPPORTED_EXPORT_FORMATS))
        raise ValueError(f"unsupported export format {suffix or '<none>'!r}; use {supported}")
    if pdf_mode not in {"vector", "hybrid"}:
        raise ValueError("pdf_mode must be 'vector' or 'hybrid'")
    if suffix != ".pdf" and pdf_mode != "vector":
        raise ValueError("pdf_mode='hybrid' is only valid for PDF output")
    if dpi < 1 or raster_dpi < 1:
        raise ValueError("dpi and raster_dpi must be positive")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    effective_dpi = raster_dpi if suffix == ".pdf" and pdf_mode == "hybrid" else dpi
    if suffix == ".pdf" and pdf_mode == "hybrid":
        with hybrid_rasterization(fig, hybrid_kws):
            fig.savefig(
                output_path,
                dpi=effective_dpi,
                bbox_inches=bbox_inches,
                facecolor=facecolor,
                **savefig_kws,
            )
    else:
        fig.savefig(
            output_path,
            dpi=effective_dpi,
            bbox_inches=bbox_inches,
            facecolor=facecolor,
            **savefig_kws,
        )
    return output_path
