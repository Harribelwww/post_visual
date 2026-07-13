"""Generate connectivity and later biosignal recipe examples."""

from __future__ import annotations

from pathlib import Path

import numpy as np

import post_visual as pv


def main() -> list[Path]:
    output_dir = Path(__file__).parent / "out"
    labels = ["F3", "F4", "C3", "C4", "P3", "P4"]
    connectivity = np.array(
        [
            [1.00, 0.64, 0.42, 0.28, 0.24, 0.18],
            [0.64, 1.00, 0.31, 0.58, 0.20, 0.37],
            [0.42, 0.31, 1.00, 0.73, 0.55, 0.34],
            [0.28, 0.58, 0.73, 1.00, 0.38, 0.61],
            [0.24, 0.20, 0.55, 0.38, 1.00, 0.69],
            [0.18, 0.37, 0.34, 0.61, 0.69, 1.00],
        ]
    )
    fig, ax = pv.connectivity_matrix(
        connectivity,
        labels=labels,
        triangle="upper",
        symmetric=True,
        annot=True,
        cmap="viridis",
        title="EEG Connectivity",
        colorbar_label="Coherence",
    )
    connectivity_path = pv.save_figure(fig, output_dir / "connectivity_matrix_mvp.png")

    difference = np.array(
        [
            [0.00, 0.12, -0.05, 0.03, -0.02, 0.01],
            [0.12, 0.00, -0.08, 0.09, -0.04, 0.06],
            [-0.05, -0.08, 0.00, 0.15, 0.07, -0.03],
            [0.03, 0.09, 0.15, 0.00, -0.06, 0.11],
            [-0.02, -0.04, 0.07, -0.06, 0.00, 0.13],
            [0.01, 0.06, -0.03, 0.11, 0.13, 0.00],
        ]
    )
    fig, ax = pv.connectivity_matrix(
        difference,
        labels=labels,
        triangle="lower",
        symmetric=True,
        center=0.0,
        annot=True,
        title="Connectivity Difference",
        colorbar_label="Condition - Control",
    )
    difference_path = pv.save_figure(fig, output_dir / "connectivity_difference_mvp.png")
    return [connectivity_path, difference_path]


if __name__ == "__main__":
    for path in main():
        print(path)
