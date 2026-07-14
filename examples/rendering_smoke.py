"""Generate ordinary-container MathText and PDF export smoke artifacts."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import post_visual as pv


output_dir = Path(__file__).parent / "out"
output_dir.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(7)
x = rng.normal(size=8_000)
y = 0.6 * x + rng.normal(scale=0.7, size=x.size)

with pv.latex_context("mathtext"):
    fig, ax = pv.scatter(x=x, y=y, scatter_kws={"alpha": 0.35})
    ax.set_xlabel(r"Input $x$")
    ax.set_ylabel(r"Response $y = 0.6x + \epsilon$")
    pv.save_figure(fig, output_dir / "rendering_mathtext.png")
    pv.save_figure(fig, output_dir / "rendering_vector.pdf", pdf_mode="vector")
    pv.save_figure(
        fig,
        output_dir / "rendering_hybrid.pdf",
        pdf_mode="hybrid",
        raster_dpi=240,
        hybrid_kws={"scatter_threshold": 1_000},
    )
    plt.close(fig)
