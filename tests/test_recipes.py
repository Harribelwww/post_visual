from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

import post_visual as pv


def test_confusion_matrix_computes_and_plots_labels() -> None:
    y_true = ["A", "A", "B", "B", "B"]
    y_pred = ["A", "B", "B", "B", "A"]

    fig, ax = pv.confusion_matrix(y_true, y_pred, labels=["A", "B"])

    assert fig is ax.figure
    assert len(ax.images) == 1
    assert len(ax.texts) == 4
    assert [tick.get_text() for tick in ax.get_xticklabels()] == ["A", "B"]
    assert [tick.get_text() for tick in ax.get_yticklabels()] == ["A", "B"]
    assert ax.get_xlabel() == "Predicted label"
    assert ax.get_ylabel() == "True label"
    plt.close(fig)


def test_training_curves_accepts_dataframe_history() -> None:
    pd = pytest.importorskip("pandas")
    history = pd.DataFrame(
        {
            "epoch": [1, 2, 3],
            "loss": [0.9, 0.6, 0.4],
            "val_loss": [1.0, 0.7, 0.5],
            "note": ["warmup", "fit", "fit"],
        }
    )

    fig, ax = pv.training_curves(history)

    assert len(ax.lines) == 2
    assert [line.get_label() for line in ax.lines] == ["loss", "val_loss"]
    assert ax.get_xlabel() == "epoch"
    assert ax.get_legend() is not None
    plt.close(fig)


def test_training_curves_rejects_mismatched_metric_length() -> None:
    with pytest.raises(ValueError, match="same length"):
        pv.training_curves({"loss": [1.0, 0.8], "accuracy": [0.5]})


def test_model_comparison_adds_grouped_bars_errors_and_red_best_highlights() -> None:
    values = np.array([[0.81, 0.74], [0.85, 0.78], [0.83, 0.80]])
    errors = np.full_like(values, 0.01)

    fig, ax = pv.model_comparison(
        values,
        models=["CNN", "Transformer", "Hybrid"],
        metrics=["Dataset A", "Dataset B"],
        errors=errors,
    )

    assert fig is ax.figure
    assert len(ax.patches) == 6
    assert len(ax.texts) == 6
    assert [tick.get_text() for tick in ax.get_xticklabels()] == ["CNN", "Transformer", "Hybrid"]
    red_edges = [patch for patch in ax.patches if np.allclose(patch.get_edgecolor()[:3], (0.902, 0.294, 0.208), atol=0.002)]
    assert len(red_edges) == 2
    assert all(patch.get_linewidth() == 0.8 for patch in ax.patches)
    assert ax.get_legend() is not None
    plt.close(fig)


def test_ablation_can_plot_change_from_reference() -> None:
    values = np.array([[0.78, 0.86], [0.82, 0.88], [0.85, 0.90]])

    fig, ax = pv.ablation(
        values,
        variants=["No augmentation", "No attention", "Full model"],
        datasets=["Dataset A", "Dataset B"],
        reference="Full model",
        relative=True,
    )

    heights = np.array([patch.get_height() for patch in ax.patches]).reshape(2, 3).T
    assert np.allclose(heights[-1], 0.0)
    assert ax.get_ylabel() == "Change from reference"
    assert any(np.allclose(line.get_ydata(), [0.0, 0.0]) for line in ax.lines)
    plt.close(fig)


def test_calibration_curve_adds_ece_and_perfect_baseline() -> None:
    y_true = np.array([0, 0, 0, 1, 1, 1, 1, 0])
    y_prob = {
        "Calibrated": np.array([0.05, 0.15, 0.35, 0.62, 0.72, 0.88, 0.93, 0.22]),
        "Overconfident": np.array([0.01, 0.05, 0.78, 0.82, 0.91, 0.98, 0.99, 0.65]),
    }

    fig, ax = pv.calibration_curve(y_true, y_prob, n_bins=4)

    assert len(ax.lines) == 3
    labels = [text.get_text() for text in ax.get_legend().get_texts()]
    assert sum("ECE=" in label for label in labels) == 2
    assert "Perfect calibration" in labels
    assert ax.get_xlim() == (0.0, 1.0)
    assert ax.get_ylim() == (0.0, 1.0)
    plt.close(fig)


def test_calibration_curve_rejects_non_probability_values() -> None:
    with pytest.raises(ValueError, match="probabilities"):
        pv.calibration_curve([0, 1], [0.2, 1.2])
