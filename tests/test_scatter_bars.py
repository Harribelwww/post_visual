from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

import post_visual as pv


def test_scatter_accepts_dataframe_hue_and_fit_line() -> None:
    pd = pytest.importorskip("pandas")
    frame = pd.DataFrame(
        {
            "feature": [1, 2, 3, 1, 2, 3],
            "score": [0.6, 0.7, 0.9, 0.5, 0.65, 0.8],
            "model": ["A", "A", "A", "B", "B", "B"],
        }
    )

    fig, ax = pv.scatter(
        data=frame,
        x="feature",
        y="score",
        hue="model",
        fit_line=True,
    )

    assert fig is ax.figure
    assert len(ax.collections) == 2
    assert len(ax.lines) == 2
    assert [collection.get_label() for collection in ax.collections] == ["A", "B"]
    assert ax.get_xlabel() == "feature"
    assert ax.get_ylabel() == "score"
    assert ax.get_legend() is not None
    plt.close(fig)


def test_scatter_rejects_mismatched_size() -> None:
    with pytest.raises(ValueError, match="size"):
        pv.scatter([1, 2, 3], [1, 4, 9], size=[20, 30])


def test_grouped_bar_accepts_matrix_values() -> None:
    values = np.array(
        [
            [0.83, 0.88],
            [0.79, 0.84],
            [0.91, 0.93],
        ]
    )

    fig, ax = pv.grouped_bar(
        values=values,
        categories=["Fold 1", "Fold 2", "Fold 3"],
        groups=["Baseline", "Proposed"],
        ylabel="AUROC",
    )

    assert len(ax.patches) == 6
    assert [tick.get_text() for tick in ax.get_xticklabels()] == [
        "Fold 1",
        "Fold 2",
        "Fold 3",
    ]
    assert ax.get_ylabel() == "AUROC"
    assert ax.get_legend() is not None
    plt.close(fig)


def test_grouped_bar_accepts_dataframe_hue() -> None:
    pd = pytest.importorskip("pandas")
    frame = pd.DataFrame(
        {
            "metric": ["Accuracy", "Accuracy", "F1", "F1"],
            "value": [0.86, 0.89, 0.81, 0.85],
            "model": ["Baseline", "Proposed", "Baseline", "Proposed"],
        }
    )

    fig, ax = pv.bar(data=frame, x="metric", y="value", hue="model")

    assert len(ax.patches) == 4
    assert [tick.get_text() for tick in ax.get_xticklabels()] == ["Accuracy", "F1"]
    assert ax.get_xlabel() == "metric"
    assert ax.get_ylabel() == "value"
    assert ax.get_legend() is not None
    plt.close(fig)


def test_horizontal_bar_supports_groups_errors_and_annotations() -> None:
    values = np.array([[0.2, 0.3], [0.4, 0.35]])

    fig, ax = pv.horizontal_bar(
        values=values,
        categories=["Alpha", "Beta"],
        groups=["A", "B"],
        errors=np.full_like(values, 0.02),
        annotate=True,
        xlabel="Score",
    )

    assert fig is ax.figure
    assert len(ax.patches) == 4
    assert [tick.get_text() for tick in ax.get_yticklabels()] == ["Alpha", "Beta"]
    assert len(ax.texts) == 4
    assert len(ax.collections) >= 2
    assert ax.get_xlabel() == "Score"
    plt.close(fig)


def test_grouped_bar_rejects_unknown_orientation() -> None:
    with pytest.raises(ValueError, match="orientation"):
        pv.grouped_bar(values=[1, 2], orientation="diagonal")


def test_scatter_fit_confidence_interval_and_marker_mapping() -> None:
    pd = pytest.importorskip("pandas")
    frame = pd.DataFrame(
        {
            "x": [0, 1, 2, 3, 0, 1, 2, 3],
            "y": [0.1, 0.9, 2.2, 3.0, 0.4, 1.2, 1.8, 2.7],
            "group": ["A"] * 4 + ["B"] * 4,
        }
    )
    fig, ax = pv.scatter(
        data=frame,
        x="x",
        y="y",
        hue="group",
        fit_line=True,
        fit_ci=0.95,
        markers=["o", "s"],
    )

    assert len(ax.lines) == 2
    assert len(ax.collections) == 4
    assert ax.collections[0].get_paths()[0].vertices.shape != ax.collections[1].get_paths()[0].vertices.shape
    plt.close(fig)


def test_scatter_nan_policy_omits_or_raises() -> None:
    fig, ax = pv.scatter([0, 1, 2], [1, np.nan, 3])
    assert ax.collections[0].get_offsets().shape[0] == 2
    plt.close(fig)

    with pytest.raises(ValueError, match="non-finite"):
        pv.scatter([0, 1], [1, np.nan], nan_policy="raise")


def test_scatter_dataframe_hue_slices_size_and_accepts_style_overrides() -> None:
    pd = pytest.importorskip("pandas")
    frame = pd.DataFrame(
        {"x": [0, 1, 2, 3], "y": [1, 2, 3, 4], "group": ["A", "B", "A", "B"]}
    )

    fig, ax = pv.scatter(
        data=frame,
        x="x",
        y="y",
        hue="group",
        size=[10, 20, 30, 40],
        scatter_kws={"facecolors": "red"},
    )

    assert ax.collections[0].get_sizes().tolist() == [10, 30]
    assert ax.collections[1].get_sizes().tolist() == [20, 40]
    assert np.allclose(ax.collections[0].get_facecolor()[0, :3], [1.0, 0.0, 0.0])
    plt.close(fig)


def test_grouped_bar_allows_color_override_without_keyword_collision() -> None:
    fig, ax = pv.grouped_bar(values=[1, 2], bar_kws={"color": "red"})
    assert np.allclose(ax.patches[0].get_facecolor()[:3], [1.0, 0.0, 0.0])
    plt.close(fig)
