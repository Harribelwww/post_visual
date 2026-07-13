"""Generate line and scatter enhancement examples."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import post_visual as pv


def main() -> list[Path]:
    output_dir = Path(__file__).parent / "out"
    x = np.linspace(0, 1, 40)
    center = 0.58 + 0.25 * np.sqrt(x)
    width = 0.07 - 0.03 * x
    fig, ax = pv.line(
        x,
        center,
        lower=center - width,
        upper=center + width,
        title="Line Confidence Band MVP",
        xlabel="Training progress",
        ylabel="Score",
    )
    line_path = pv.save_figure(fig, output_dir / "line_confidence_mvp.png")

    rng = np.random.default_rng(9)
    frame = pd.DataFrame(
        {
            "feature": np.r_[np.linspace(0, 1, 28), np.linspace(0, 1, 28)],
            "response": np.r_[
                0.45 + 0.38 * np.linspace(0, 1, 28) + rng.normal(0, 0.055, 28),
                0.52 + 0.25 * np.linspace(0, 1, 28) + rng.normal(0, 0.05, 28),
            ],
            "group": ["Proposed"] * 28 + ["Baseline"] * 28,
        }
    )
    fig, ax = pv.scatter(
        data=frame,
        x="feature",
        y="response",
        hue="group",
        fit_line=True,
        fit_ci=0.95,
        markers=["o", "s"],
        title="Scatter Regression CI MVP",
    )
    scatter_path = pv.save_figure(fig, output_dir / "scatter_regression_ci_mvp.png")
    return [line_path, scatter_path]


if __name__ == "__main__":
    for path in main():
        print(path)
