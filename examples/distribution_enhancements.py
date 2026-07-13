"""Generate enhanced distribution primitive examples."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import post_visual as pv


def main() -> list[Path]:
    output_dir = Path(__file__).parent / "out"
    rng = np.random.default_rng(21)
    frame = pd.DataFrame(
        {
            "score": np.r_[rng.normal(0.82, 0.04, 80), rng.normal(0.88, 0.03, 80)],
            "model": ["Baseline"] * 80 + ["Proposed"] * 80,
        }
    )
    fig, ax = pv.kde(data=frame, x="score", hue="model", fill=True, title="KDE MVP", xlabel="Score")
    kde_path = pv.save_figure(fig, output_dir / "kde_mvp.png")

    fig, ax = pv.ecdf(data=frame, x="score", hue="model", title="ECDF MVP", xlabel="Score")
    ecdf_path = pv.save_figure(fig, output_dir / "ecdf_mvp.png")

    matrix = np.column_stack([rng.normal(0.78, 0.05, 30), rng.normal(0.86, 0.04, 30)])
    fig, ax = pv.box(matrix, labels=["Baseline", "Proposed"], title="Box + Raw Samples MVP", ylabel="Score")
    pv.strip(matrix, labels=["Baseline", "Proposed"], ax=ax, seed=5)
    strip_path = pv.save_figure(fig, output_dir / "strip_overlay_mvp.png")
    return [kde_path, ecdf_path, strip_path]


if __name__ == "__main__":
    for path in main():
        print(path)
