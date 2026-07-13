"""Generate embedding and feature-importance recipe examples."""

from __future__ import annotations

from pathlib import Path

import numpy as np

import post_visual as pv


def main() -> list[Path]:
    output_dir = Path(__file__).parent / "out"
    rng = np.random.default_rng(12)

    control = rng.normal(loc=[-1.0, 0.2, 0.0, -0.4, 0.3], scale=0.45, size=(35, 5))
    condition = rng.normal(loc=[1.0, -0.1, 0.5, 0.5, -0.2], scale=0.50, size=(35, 5))
    features = np.vstack([control, condition])
    labels = np.array(["Control"] * len(control) + ["Condition"] * len(condition))

    fig, ax = pv.embedding(
        features,
        labels=labels,
        method="pca",
        centers=True,
        confidence_ellipse=True,
        title="PCA Feature Embedding",
        palette="nilou",
    )
    embedding_path = pv.save_figure(fig, output_dir / "embedding_mvp.png")

    importance_values = np.array([0.08, -0.19, 0.14, 0.04, -0.11, 0.23, 0.06, -0.16])
    importance_names = [
        "Delta power",
        "Theta connectivity",
        "Alpha asymmetry",
        "Beta power",
        "Spectral entropy",
        "Temporal variance",
        "Coherence",
        "Complexity",
    ]
    fig, ax = pv.feature_importance(
        importance_values,
        names=importance_names,
        top_k=8,
        title="Signed Feature Importance",
        xlabel="Contribution to positive class",
    )
    importance_path = pv.save_figure(fig, output_dir / "feature_importance_mvp.png")

    return [embedding_path, importance_path]


if __name__ == "__main__":
    for path in main():
        print(path)
