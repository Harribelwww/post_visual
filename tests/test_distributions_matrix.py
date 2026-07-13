from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

import post_visual as pv


def test_hist_accepts_dataframe_hue() -> None:
    pd = pytest.importorskip("pandas")
    frame = pd.DataFrame(
        {
            "score": [0.62, 0.71, 0.76, 0.81, 0.58, 0.64, 0.68, 0.73],
            "model": ["A", "A", "A", "A", "B", "B", "B", "B"],
        }
    )

    fig, ax = pv.hist(data=frame, x="score", hue="model", bins=4)

    assert fig is ax.figure
    assert len(ax.patches) == 8
    assert ax.get_xlabel() == "score"
    assert ax.get_ylabel() == "Count"
    assert ax.get_legend() is not None
    plt.close(fig)


def test_box_and_violin_accept_matrix_values() -> None:
    values = np.array(
        [
            [0.82, 0.87],
            [0.79, 0.84],
            [0.85, 0.91],
            [0.81, 0.89],
        ]
    )

    fig, ax = pv.box(values, labels=["Baseline", "Proposed"], ylabel="AUROC")
    assert len(ax.patches) == 2
    assert [tick.get_text() for tick in ax.get_xticklabels()] == ["Baseline", "Proposed"]
    assert ax.get_ylabel() == "AUROC"
    plt.close(fig)

    fig, ax = pv.violin(values, labels=["Baseline", "Proposed"])
    assert len(ax.collections) >= 2
    assert [tick.get_text() for tick in ax.get_xticklabels()] == ["Baseline", "Proposed"]
    plt.close(fig)


def test_box_accepts_dataframe_groups() -> None:
    pd = pytest.importorskip("pandas")
    frame = pd.DataFrame(
        {
            "metric": ["Accuracy", "Accuracy", "F1", "F1"],
            "value": [0.86, 0.89, 0.81, 0.85],
        }
    )

    fig, ax = pv.box(data=frame, x="metric", y="value")

    assert len(ax.patches) == 2
    assert [tick.get_text() for tick in ax.get_xticklabels()] == ["Accuracy", "F1"]
    assert ax.get_xlabel() == "metric"
    assert ax.get_ylabel() == "value"
    plt.close(fig)


def test_heatmap_accepts_dataframe_and_annotations() -> None:
    pd = pytest.importorskip("pandas")
    frame = pd.DataFrame(
        [[8, 1], [2, 7]],
        index=["True A", "True B"],
        columns=["Pred A", "Pred B"],
    )

    fig, ax = pv.heatmap(frame, annot=True, title="Confusion")

    assert fig is ax.figure
    assert len(ax.images) == 1
    assert len(fig.axes) == 2
    assert len(ax.texts) == 4
    assert [tick.get_text() for tick in ax.get_xticklabels()] == ["Pred A", "Pred B"]
    assert [tick.get_text() for tick in ax.get_yticklabels()] == ["True A", "True B"]
    assert ax.get_title() == "Confusion"
    plt.close(fig)


def test_heatmap_rejects_label_length_mismatch() -> None:
    with pytest.raises(ValueError, match="xlabels"):
        pv.heatmap(np.ones((2, 2)), xlabels=["only one"])


def test_grid_color_accepts_center_coordinates_and_colorbar_label() -> None:
    values = np.arange(12, dtype=float).reshape(3, 4)

    fig, ax = pv.grid_color(
        values,
        x=[0.0, 0.5, 1.0, 1.5],
        y=[2.0, 4.0, 6.0],
        colorbar_label="Power (dB)",
    )

    assert fig is ax.figure
    assert len(ax.collections) == 1
    assert len(fig.axes) == 2
    assert fig.axes[1].get_ylabel() == "Power (dB)"
    plt.close(fig)


def test_grid_color_center_uses_symmetric_limits_and_existing_axes() -> None:
    fig, ax = plt.subplots()

    returned_fig, returned_ax = pv.grid_color(
        [[-2.0, 1.0], [0.5, 3.0]], center=0.0, cmap="RdBu_r", ax=ax
    )

    assert returned_fig is fig
    assert returned_ax is ax
    assert ax.collections[0].norm.vmin == -3.0
    assert ax.collections[0].norm.vmax == 3.0
    plt.close(fig)


def test_grid_color_rejects_invalid_coordinates() -> None:
    with pytest.raises(ValueError, match="x"):
        pv.grid_color(np.ones((2, 3)), x=[0, 2])
    with pytest.raises(ValueError, match="strictly increasing"):
        pv.grid_color(np.ones((2, 2)), y=[0, 0])


def test_kde_and_ecdf_accept_dataframe_hue() -> None:
    pd = pytest.importorskip("pandas")
    frame = pd.DataFrame({"score": [0.5, 0.6, 0.7, 0.8, 0.55, 0.65, 0.75, 0.9], "model": ["A"] * 4 + ["B"] * 4})

    fig, ax = pv.kde(data=frame, x="score", hue="model", fill=True)
    assert len(ax.lines) == 2
    assert len(ax.collections) == 2
    assert ax.get_legend() is not None
    plt.close(fig)

    fig, ax = pv.ecdf(data=frame, x="score", hue="model")
    assert len(ax.lines) == 2
    assert ax.get_ylim()[1] >= 1.0
    plt.close(fig)


def test_strip_can_overlay_box_and_is_seeded() -> None:
    values = np.array([[0.6, 0.8], [0.7, 0.9], [0.65, 0.85]])
    fig, ax = pv.box(values, labels=["A", "B"])
    pv.strip(values, labels=["A", "B"], ax=ax, seed=3)

    assert len(ax.collections) == 2
    assert [tick.get_text() for tick in ax.get_xticklabels()] == ["A", "B"]
    plt.close(fig)


def test_kde_and_strip_validate_degenerate_inputs() -> None:
    with pytest.raises(ValueError, match="distinct"):
        pv.kde([1, 1, 1])
    with pytest.raises(ValueError, match="jitter"):
        pv.strip([1, 2], jitter=-0.1)
