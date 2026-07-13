from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

import post_visual as pv


def test_line_accepts_xy_arrays_and_scale_alias() -> None:
    x = np.array([1, 10, 100])
    y = np.array([2, 3, 5])

    fig, ax = pv.line(x, y, plot_type="sx", label="demo")

    assert fig is ax.figure
    assert ax.get_xscale() == "log"
    assert ax.get_yscale() == "linear"
    assert len(ax.lines) == 1
    assert ax.lines[0].get_markerfacecolor() == "white"
    assert ax.get_legend() is not None
    plt.close(fig)


def test_line_accepts_matrix_and_series_labels() -> None:
    x = np.array([1, 2, 3])
    first = np.column_stack([x, x**2])
    second = x**3

    fig, ax = pv.line(
        series=[
            (first, "squared"),
            (x, second, "cubed"),
        ]
    )

    assert len(ax.lines) == 2
    assert [line.get_label() for line in ax.lines] == ["squared", "cubed"]
    assert ax.get_legend() is not None
    plt.close(fig)


def test_line_accepts_dataframe_hue() -> None:
    pd = pytest.importorskip("pandas")
    frame = pd.DataFrame(
        {
            "epoch": [1, 2, 3, 1, 2, 3],
            "loss": [0.9, 0.6, 0.4, 1.0, 0.7, 0.5],
            "model": ["A", "A", "A", "B", "B", "B"],
        }
    )

    fig, ax = pv.line(data=frame, x="epoch", y="loss", hue="model")

    assert len(ax.lines) == 2
    assert [line.get_label() for line in ax.lines] == ["A", "B"]
    assert ax.get_xlabel() == "epoch"
    assert ax.get_ylabel() == "loss"
    plt.close(fig)


def test_log_scale_rejects_non_positive_values() -> None:
    with pytest.raises(ValueError, match="positive"):
        pv.line([0, 1, 2], [1, 2, 3], plot_type="sx")


def test_line_draws_direct_confidence_band() -> None:
    x = np.linspace(0, 1, 8)
    y = x**2
    fig, ax = pv.line(x, y, lower=y - 0.1, upper=y + 0.1)

    assert len(ax.lines) == 1
    assert len(ax.collections) == 1
    plt.close(fig)


def test_line_nan_policy_supports_gaps_omit_and_raise() -> None:
    fig, ax = pv.line([0, 1, 2], [1, np.nan, 3], nan_policy="gap")
    assert np.isnan(ax.lines[0].get_ydata()[1])
    plt.close(fig)

    fig, ax = pv.line([0, 1, 2], [1, np.nan, 3], nan_policy="omit")
    assert len(ax.lines[0].get_ydata()) == 2
    plt.close(fig)

    with pytest.raises(ValueError, match="non-finite"):
        pv.line([0, 1], [1, np.nan], nan_policy="raise")
