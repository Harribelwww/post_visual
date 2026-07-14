from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

import post_visual as pv


def test_panel_grid_hides_extra_axes_and_adds_labels() -> None:
    fig, axes = pv.panel_grid(2, 2, n_panels=3, labels=True, suptitle="Overview")

    assert axes.shape == (2, 2)
    assert axes.ravel()[3].get_visible() is False
    assert [ax.texts[0].get_text() for ax in axes.ravel()[:3]] == ["(a)", "(b)", "(c)"]
    assert fig._suptitle.get_text() == "Overview"
    plt.close(fig)


def test_label_panels_accepts_custom_labels() -> None:
    fig, axes = plt.subplots(1, 2, squeeze=False)

    returned = pv.label_panels(axes, labels=["Left", "Right"])

    assert returned.shape == (1, 2)
    assert [ax.texts[0].get_text() for ax in axes.ravel()] == ["Left", "Right"]
    plt.close(fig)


def test_image_supports_grayscale_and_existing_axes() -> None:
    fig, ax = plt.subplots()

    returned_fig, returned_ax = pv.image(
        np.arange(16).reshape(4, 4), ax=ax, colorbar=True, colorbar_label="Intensity"
    )

    assert returned_fig is fig
    assert returned_ax is ax
    assert len(ax.images) == 1
    assert len(fig.axes) == 2
    assert ax.axison is False
    plt.close(fig)


def test_image_grid_shares_limits_and_hides_extra_axes() -> None:
    images = [np.full((3, 3), value, dtype=float) for value in (0, 2, 5)]

    fig, axes = pv.image_grid(images, titles=["A", "B", "C"], ncols=2, colorbar="shared")

    assert axes.shape == (2, 2)
    assert axes.ravel()[3].get_visible() is False
    assert [ax.images[0].norm.vmin for ax in axes.ravel()[:3]] == [0.0, 0.0, 0.0]
    assert [ax.images[0].norm.vmax for ax in axes.ravel()[:3]] == [5.0, 5.0, 5.0]
    assert len(fig.axes) == 5
    plt.close(fig)


def test_image_grid_accepts_rgb_and_validates_titles() -> None:
    rgb = np.zeros((4, 4, 3), dtype=float)
    fig, axes = pv.image_grid([rgb, rgb + 0.5], ncols=2)
    assert all(len(ax.images) == 1 for ax in axes.ravel())
    plt.close(fig)

    with pytest.raises(ValueError, match="titles"):
        pv.image_grid([rgb, rgb], titles=["one"])


def test_image_grid_rejects_shared_colorbar_without_shared_limits() -> None:
    images = [np.arange(4).reshape(2, 2), np.arange(100, 104).reshape(2, 2)]
    with pytest.raises(ValueError, match="shared colorbar"):
        pv.image_grid(images, shared_limits=False, colorbar="shared")
