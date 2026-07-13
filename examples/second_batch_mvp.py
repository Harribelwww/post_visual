"""Generate MVP examples for distributions and heatmaps."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import post_visual as pv


def main() -> list[Path]:
    output_dir = Path(__file__).parent / "out"
    rng = np.random.default_rng(11)

    scores = pd.DataFrame(
        {
            "AUROC": np.r_[
                rng.normal(0.88, 0.025, 36),
                rng.normal(0.82, 0.035, 36),
            ],
            "model": ["Proposed"] * 36 + ["Baseline"] * 36,
        }
    )
    fig, ax = pv.hist(
        data=scores,
        x="AUROC",
        hue="model",
        bins=10,
        title="Histogram MVP",
        xlabel="AUROC",
        palette="nilou",
    )
    hist_path = pv.save_figure(fig, output_dir / "hist_mvp.png")

    fold_scores = pd.DataFrame(
        {
            "fold": ["Fold 1"] * 20 + ["Fold 2"] * 20 + ["Fold 3"] * 20,
            "score": np.r_[
                rng.normal(0.83, 0.03, 20),
                rng.normal(0.86, 0.025, 20),
                rng.normal(0.89, 0.02, 20),
            ],
        }
    )
    fig, ax = pv.box(
        data=fold_scores,
        x="fold",
        y="score",
        title="Box MVP",
        ylabel="Score",
        palette="furina",
    )
    box_path = pv.save_figure(fig, output_dir / "box_mvp.png")

    matrix = pd.DataFrame(
        [[36, 4, 2], [5, 31, 6], [1, 7, 34]],
        index=["Class A", "Class B", "Class C"],
        columns=["Pred A", "Pred B", "Pred C"],
    )
    fig, ax = pv.heatmap(
        matrix,
        annot=True,
        title="Heatmap MVP",
        xlabel="Prediction",
        ylabel="Reference",
        cmap="magma",
    )
    heatmap_path = pv.save_figure(fig, output_dir / "heatmap_mvp.png")

    time = np.linspace(0, 2.0, 120)
    frequency = np.linspace(1, 40, 64)
    power = np.exp(-((frequency[:, None] - (8 + 7 * time[None, :])) ** 2) / 18)
    power += 0.55 * np.exp(-((frequency[:, None] - 24) ** 2) / 30) * np.exp(-((time[None, :] - 1.2) ** 2) / 0.08)
    fig, ax = pv.grid_color(
        power,
        x=time,
        y=frequency,
        title="Regular Grid Color MVP",
        xlabel="Time (s)",
        ylabel="Frequency (Hz)",
        colorbar_label="Normalized power",
        cmap="magma",
    )
    grid_path = pv.save_figure(fig, output_dir / "grid_color_mvp.png")

    return [hist_path, box_path, heatmap_path, grid_path]


if __name__ == "__main__":
    for path in main():
        print(path)
