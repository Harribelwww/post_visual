"""Generate MVP examples for research-result recipes."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import post_visual as pv


def main() -> list[Path]:
    output_dir = Path(__file__).parent / "out"

    y_true = np.array(["A", "A", "A", "B", "B", "B", "C", "C", "C", "C"])
    y_pred = np.array(["A", "A", "B", "B", "B", "C", "C", "C", "A", "C"])
    fig, ax = pv.confusion_matrix(
        y_true,
        y_pred,
        labels=["A", "B", "C"],
        title="Confusion Matrix MVP",
        cmap="magma",
    )
    confusion_path = pv.save_figure(fig, output_dir / "confusion_matrix_mvp.png")

    history = pd.DataFrame(
        {
            "epoch": np.arange(1, 7),
            "loss": [1.12, 0.86, 0.68, 0.53, 0.45, 0.39],
            "val_loss": [1.18, 0.94, 0.75, 0.62, 0.56, 0.51],
            "accuracy": [0.58, 0.66, 0.73, 0.79, 0.84, 0.87],
            "val_accuracy": [0.55, 0.62, 0.69, 0.74, 0.78, 0.81],
        }
    )
    fig, ax = pv.training_curves(
        history,
        metrics=["loss", "val_loss"],
        title="Training Curves MVP",
        ylabel="Loss",
        palette="furina",
    )
    training_path = pv.save_figure(fig, output_dir / "training_curves_mvp.png")

    return [confusion_path, training_path]


if __name__ == "__main__":
    for path in main():
        print(path)
