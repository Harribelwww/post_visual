from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

import post_visual as pv


def test_connectivity_matrix_masks_redundant_triangle() -> None:
    matrix = np.array([[1.0, 0.7, 0.2], [0.7, 1.0, 0.5], [0.2, 0.5, 1.0]])

    fig, ax = pv.connectivity_matrix(
        matrix,
        labels=["F3", "F4", "C3"],
        triangle="upper",
        annot=True,
        symmetric=True,
    )

    plotted = np.asarray(ax.images[0].get_array())
    assert np.all(np.isnan(plotted[np.tril_indices(3, k=-1)]))
    assert len(ax.texts) == 6
    assert [tick.get_text() for tick in ax.get_xticklabels()] == ["F3", "F4", "C3"]
    plt.close(fig)


def test_connectivity_difference_uses_symmetric_zero_centered_limits() -> None:
    matrix = np.array([[0.0, -0.3], [0.2, 0.0]])

    fig, ax = pv.connectivity_matrix(matrix, center=0.0, colorbar=False)

    image = ax.images[0]
    assert image.get_clim() == (-0.3, 0.3)
    assert image.get_cmap().name == "RdBu_r"
    plt.close(fig)


def test_connectivity_matrix_rejects_asymmetric_input_when_requested() -> None:
    with pytest.raises(ValueError, match="symmetric"):
        pv.connectivity_matrix([[1.0, 0.4], [0.2, 1.0]], symmetric=True)


def test_connectivity_matrix_rejects_non_square_input() -> None:
    with pytest.raises(ValueError, match="square"):
        pv.connectivity_matrix([[1.0, 0.2, 0.3], [0.2, 1.0, 0.4]])
