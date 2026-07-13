from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

import post_visual as pv


def test_format_axis_applies_percent_and_scientific_formatters() -> None:
    fig, ax = plt.subplots()
    returned_fig, returned_ax = pv.format_axis(ax, style="percent", scale=1.0)
    assert returned_fig is fig
    assert returned_ax is ax
    assert "PercentFormatter" in type(ax.yaxis.get_major_formatter()).__name__
    pv.format_axis(ax, axis="x", style="scientific")
    assert "ScalarFormatter" in type(ax.xaxis.get_major_formatter()).__name__
    plt.close(fig)


def test_shared_legend_deduplicates_labels() -> None:
    fig, axes = plt.subplots(1, 2)
    for ax in axes:
        ax.plot([0, 1], [0, 1], label="Shared")
    returned_fig, legend = pv.shared_legend(axes, legend_kws={"loc": "upper center"})
    assert returned_fig is fig
    assert [text.get_text() for text in legend.get_texts()] == ["Shared"]
    plt.close(fig)


def test_secondary_axis_and_inset_axes_reuse_parent_figure() -> None:
    fig, ax = plt.subplots()
    returned_fig, secondary = pv.secondary_axis(
        ax,
        functions=(lambda value: value * 1000, lambda value: value / 1000),
        label="Milliseconds",
    )
    assert returned_fig is fig
    assert secondary.get_xlabel() == "Milliseconds"

    returned_fig, inset = pv.inset_axes(ax, [0.55, 0.55, 0.35, 0.35])
    assert returned_fig is fig
    assert inset in ax.child_axes
    plt.close(fig)


def test_axes_helpers_validate_inputs() -> None:
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="axis"):
        pv.format_axis(ax, axis="z")
    with pytest.raises(ValueError, match="width"):
        pv.inset_axes(ax, [0, 0, 0, 1])
    plt.close(fig)
