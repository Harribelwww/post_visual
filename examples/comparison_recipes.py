"""Generate paper-inspired model comparison, ablation, and calibration examples."""

from __future__ import annotations

from pathlib import Path

import numpy as np

import post_visual as pv


def main() -> list[Path]:
    output_dir = Path(__file__).parent / "out"

    comparison_values = np.array(
        [
            [0.79, 0.86, 0.91],
            [0.82, 0.88, 0.92],
            [0.84, 0.89, 0.94],
            [0.86, 0.91, 0.95],
        ]
    )
    comparison_errors = np.array(
        [
            [0.025, 0.020, 0.014],
            [0.020, 0.018, 0.012],
            [0.018, 0.015, 0.010],
            [0.015, 0.013, 0.009],
        ]
    )
    fig, ax = pv.model_comparison(
        comparison_values,
        models=["ConvNet", "EEGNet", "Conformer", "Proposed"],
        metrics=["Dataset A", "Dataset B", "Dataset C"],
        errors=comparison_errors,
        title="Cross-dataset Model Comparison",
        ylabel="Accuracy",
        fmt=".3f",
    )
    comparison_path = pv.save_figure(fig, output_dir / "model_comparison_mvp.png")

    ablation_values = np.array(
        [
            [0.79, 0.87, 0.93],
            [0.83, 0.88, 0.94],
            [0.82, 0.89, 0.94],
            [0.86, 0.91, 0.95],
        ]
    )
    fig, ax = pv.ablation(
        ablation_values,
        variants=["No data\naugmentation", "No\nattention", "No\nencoder", "Full\nmodel"],
        datasets=["Dataset A", "Dataset B", "Dataset C"],
        reference="Full\nmodel",
        relative=True,
        title="Ablation Relative to Full Model",
        fmt="+.3f",
        palette="nilou",
        figsize_cm=(20, 12),
        annotate=False,
    )
    ablation_path = pv.save_figure(fig, output_dir / "ablation_mvp.png")

    rng = np.random.default_rng(42)
    latent_probability = rng.uniform(0.03, 0.97, 300)
    y_true = rng.binomial(1, latent_probability)
    proposed = np.clip(latent_probability + rng.normal(0.0, 0.06, latent_probability.size), 0, 1)
    baseline = np.clip(0.5 + 1.35 * (latent_probability - 0.5), 0, 1)
    fig, ax = pv.calibration_curve(
        y_true,
        {"Proposed": proposed, "Baseline": baseline},
        n_bins=8,
        title="Reliability Diagram",
        palette="furina",
    )
    calibration_path = pv.save_figure(fig, output_dir / "calibration_mvp.png")

    return [comparison_path, ablation_path, calibration_path]


if __name__ == "__main__":
    for path in main():
        print(path)
