"""Generate MVP examples for scatter and grouped bars."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import post_visual as pv


def main() -> list[Path]:
    output_dir = Path(__file__).parent / "out"

    rng = np.random.default_rng(7)
    frame = pd.DataFrame(
        {
            "feature": np.r_[np.linspace(0, 1, 24), np.linspace(0, 1, 24)],
            "score": np.r_[
                0.58 + 0.28 * np.linspace(0, 1, 24) + rng.normal(0, 0.025, 24),
                0.52 + 0.22 * np.linspace(0, 1, 24) + rng.normal(0, 0.025, 24),
            ],
            "model": ["Proposed"] * 24 + ["Baseline"] * 24,
        }
    )

    fig, ax = pv.scatter(
        data=frame,
        x="feature",
        y="score",
        hue="model",
        fit_line=True,
        title="Scatter MVP",
        xlabel="Feature response",
        ylabel="Score",
        palette="nilou",
    )
    scatter_path = pv.save_figure(fig, output_dir / "scatter_mvp.png")

    bar_values = np.array(
        [
            [0.84, 0.88],
            [0.79, 0.85],
            [0.87, 0.91],
        ]
    )
    fig, ax = pv.grouped_bar(
        values=bar_values,
        categories=["Fold 1", "Fold 2", "Fold 3"],
        groups=["Baseline", "Proposed"],
        title="Grouped Bar MVP",
        ylabel="AUROC",
        palette="furina",
    )
    bar_path = pv.save_figure(fig, output_dir / "grouped_bar_mvp.png")

    x_values = np.arange(1, 7)
    estimates = np.array([0.62, 0.68, 0.71, 0.75, 0.78, 0.81])
    errors = np.array([0.05, 0.04, 0.045, 0.035, 0.03, 0.025])
    fig, ax = pv.errorbar(
        x_values,
        estimates,
        yerr=errors,
        label="Mean ± SD",
        title="Errorbar MVP",
        xlabel="Fold",
        ylabel="Score",
    )
    errorbar_path = pv.save_figure(fig, output_dir / "errorbar_mvp.png")

    center = 0.55 + 0.22 * np.linspace(0, 1, 30)
    interval = 0.06 - 0.02 * np.linspace(0, 1, 30)
    fig, ax = pv.interval_band(
        np.linspace(0, 1, 30),
        center - interval,
        center + interval,
        center=center,
        label="Mean and interval",
        title="Interval Band MVP",
        xlabel="Training progress",
        ylabel="Score",
        palette="nilou",
    )
    interval_path = pv.save_figure(fig, output_dir / "interval_band_mvp.png")

    return [scatter_path, bar_path, errorbar_path, interval_path]


if __name__ == "__main__":
    for path in main():
        print(path)
