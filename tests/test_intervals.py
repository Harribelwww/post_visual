from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

import post_visual as pv


def test_errorbar_accepts_symmetric_and_asymmetric_errors() -> None:
    fig, ax = pv.errorbar(
        [1, 2, 3],
        [0.5, 0.7, 0.8],
        xerr=[0.1, 0.1, 0.2],
        yerr=[[0.05, 0.06, 0.04], [0.08, 0.07, 0.05]],
        label="Estimate",
    )

    assert fig is ax.figure
    assert len(ax.lines) >= 1
    assert len(ax.collections) >= 2
    assert ax.get_legend() is not None
    plt.close(fig)


def test_errorbar_reuses_existing_axes() -> None:
    fig, ax = plt.subplots()

    returned_fig, returned_ax = pv.errorbar([0, 1], [1, 2], yerr=[0.1, 0.2], ax=ax)

    assert returned_fig is fig
    assert returned_ax is ax
    plt.close(fig)


def test_interval_band_draws_center_and_horizontal_band() -> None:
    fig, ax = pv.interval_band(
        [0, 1, 2],
        [0.2, 0.3, 0.4],
        [0.6, 0.7, 0.8],
        center=[0.4, 0.5, 0.6],
        orientation="horizontal",
        label="95% CI",
    )

    assert len(ax.collections) == 1
    assert len(ax.lines) == 1
    assert ax.get_legend() is not None
    plt.close(fig)


def test_interval_band_rejects_invalid_bounds_and_center() -> None:
    with pytest.raises(ValueError, match="lower"):
        pv.interval_band([0, 1], [0.5, 0.7], [0.4, 0.8])
    with pytest.raises(ValueError, match="center"):
        pv.interval_band([0, 1], [0.2, 0.3], [0.5, 0.6], center=[0.4, 0.8])
