from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

import post_visual as pv


def test_embedding_accepts_precomputed_coordinates_and_labels() -> None:
    coords = np.array([[-1.0, 0.0], [-0.8, 0.2], [0.9, -0.1], [1.1, 0.1]])

    fig, ax = pv.embedding(coords, labels=["Control", "Control", "Case", "Case"])

    assert fig is ax.figure
    assert len(ax.collections) == 2
    assert [text.get_text() for text in ax.get_legend().get_texts()] == ["Control", "Case"]
    assert ax.get_xlabel() == "Dimension 1"
    assert ax.get_ylabel() == "Dimension 2"
    plt.close(fig)


def test_embedding_pca_adds_centers_ellipses_and_variance_labels() -> None:
    rng = np.random.default_rng(4)
    data = np.vstack([rng.normal(-1, 0.2, (8, 4)), rng.normal(1, 0.2, (8, 4))])
    labels = np.array(["A"] * 8 + ["B"] * 8)

    fig, ax = pv.embedding(
        data,
        labels=labels,
        method="pca",
        centers=True,
        confidence_ellipse=True,
    )

    assert len(ax.collections) == 4
    assert len(ax.patches) == 2
    assert ax.get_xlabel().startswith("PC1 (")
    assert ax.get_ylabel().startswith("PC2 (")
    plt.close(fig)


def test_feature_importance_sorts_top_k_and_colors_signs() -> None:
    values = np.array([0.04, -0.21, 0.13, -0.08])

    fig, ax = pv.feature_importance(
        values,
        names=["Age", "Alpha", "Beta", "Theta"],
        top_k=3,
    )

    assert len(ax.patches) == 3
    assert [tick.get_text() for tick in ax.get_yticklabels()] == ["Theta", "Beta", "Alpha"]
    widths = [patch.get_width() for patch in ax.patches]
    assert np.allclose(widths, [-0.08, 0.13, -0.21])
    assert len(ax.texts) == 3
    plt.close(fig)


def test_feature_importance_accepts_grouped_values_and_errors() -> None:
    values = np.array([[0.10, 0.12], [0.18, 0.15], [0.08, 0.11]])

    fig, ax = pv.feature_importance(
        values,
        names=["F1", "F2", "F3"],
        groups=["Model A", "Model B"],
        errors=np.full_like(values, 0.01),
        top_k=None,
        annotate=False,
    )

    assert len(ax.patches) == 6
    assert ax.get_legend() is not None
    assert len(ax.collections) >= 2
    plt.close(fig)


def test_embedding_rejects_unknown_method() -> None:
    with pytest.raises(ValueError, match="method"):
        pv.embedding([[0, 1], [1, 0]], method="umap")
