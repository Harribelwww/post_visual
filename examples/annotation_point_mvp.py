"""Generate general annotation and point-range examples."""

from __future__ import annotations

from pathlib import Path

import numpy as np

import post_visual as pv


def main() -> list[Path]:
    output_dir = Path(__file__).parent / "out"
    x = np.linspace(0, 1, 30)
    y = 0.55 + 0.25 * np.sin(np.pi * x)
    fig, ax = pv.line(x, y, title="General Annotation MVP", xlabel="Time", ylabel="Score")
    peak = int(np.argmax(y))
    pv.annotate_arrow("Peak response", (x[peak], y[peak]), (0.72, 0.72), ax=ax)
    pv.annotate_text(
        "Analysis window",
        (0.03, 0.95),
        coordinates="axes",
        ax=ax,
        text_kws={"ha": "left", "bbox": {"facecolor": "white", "edgecolor": "black", "alpha": 0.9}},
    )
    annotation_path = pv.save_figure(fig, output_dir / "general_annotations_mvp.png")

    estimates = np.array([0.82, 1.05, 1.28, 1.46])
    fig, ax = pv.forest_plot(
        estimates,
        estimates - np.array([0.14, 0.12, 0.16, 0.18]),
        estimates + np.array([0.16, 0.15, 0.20, 0.22]),
        categories=["Baseline", "Model A", "Model B", "Proposed"],
        reference=1.0,
        annotate=True,
        title="Point-range MVP",
        xlabel="Effect estimate (95% CI)",
    )
    forest_path = pv.save_figure(fig, output_dir / "point_range_mvp.png")
    return [annotation_path, forest_path]


if __name__ == "__main__":
    for path in main():
        print(path)
