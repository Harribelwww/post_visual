from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

import post_visual as pv


def test_text_and_arrow_annotations_reuse_axes() -> None:
    fig, ax = plt.subplots()
    pv.annotate_text("Region", (0.1, 0.9), coordinates="axes", ax=ax, text_kws={"bbox": {"facecolor": "white"}})
    returned_fig, returned_ax = pv.annotate_arrow("Peak", (0.5, 0.8), (0.7, 0.5), ax=ax)

    assert returned_fig is fig
    assert returned_ax is ax
    assert [text.get_text() for text in ax.texts] == ["Region", "Peak"]
    assert ax.texts[1].arrow_patch is not None
    plt.close(fig)


def test_significance_bracket_supports_both_orientations() -> None:
    fig, ax = plt.subplots()
    pv.significance_bracket(0, 1, 1.2, label="p < .01", ax=ax)
    pv.significance_bracket(0, 1, 1.4, orientation="horizontal", ax=ax)

    assert len(ax.lines) == 2
    assert [text.get_text() for text in ax.texts] == ["p < .01", "*"]
    plt.close(fig)


def test_point_range_draws_forest_style_intervals() -> None:
    fig, ax = pv.forest_plot(
        [0.8, 1.1, 1.4],
        [0.6, 0.9, 1.1],
        [1.0, 1.3, 1.8],
        categories=["A", "B", "C"],
        reference=1.0,
        annotate=True,
    )

    assert [tick.get_text() for tick in ax.get_yticklabels()] == ["A", "B", "C"]
    assert len(ax.lines) >= 2
    assert len(ax.texts) == 3
    plt.close(fig)


def test_annotations_and_point_range_validate_inputs() -> None:
    with pytest.raises(ValueError, match="coordinates"):
        pv.annotate_text("bad", (0, 0), coordinates="figure")
    with pytest.raises(ValueError, match="start"):
        pv.significance_bracket(1, 0, 2)
    with pytest.raises(ValueError, match="between"):
        pv.point_range([2], [0], [1])
