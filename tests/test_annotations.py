from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

import post_visual as pv


def test_event_lines_add_vertical_lines_labels_and_legend() -> None:
    fig, ax = plt.subplots()

    returned_fig, returned_ax = pv.event_lines(
        [2.0, 4.0], labels=["Warmup", "Decay"], legend=True, ax=ax
    )

    assert returned_fig is fig
    assert returned_ax is ax
    assert len(ax.lines) == 2
    assert [text.get_text() for text in ax.texts] == ["Warmup", "Decay"]
    assert ax.get_legend() is not None
    plt.close(fig)


def test_event_lines_support_horizontal_threshold() -> None:
    fig, ax = pv.event_lines([0.8], labels=["Target"], orientation="horizontal")

    assert len(ax.lines) == 1
    assert ax.texts[0].get_text() == "Target"
    plt.close(fig)


def test_event_spans_add_vertical_and_horizontal_intervals() -> None:
    fig, ax = plt.subplots()
    pv.event_spans([(1.0, 2.0)], labels=["Stimulus"], ax=ax)
    pv.event_spans([(0.2, 0.4)], orientation="horizontal", annotate=False, ax=ax)

    assert len(ax.patches) == 2
    assert [text.get_text() for text in ax.texts] == ["Stimulus"]
    plt.close(fig)


def test_event_annotations_validate_lengths_bounds_and_orientation() -> None:
    with pytest.raises(ValueError, match="labels"):
        pv.event_lines([1, 2], labels=["Only one"])
    with pytest.raises(ValueError, match="start"):
        pv.event_spans([(2, 1)])
    with pytest.raises(ValueError, match="orientation"):
        pv.event_lines([1], orientation="diagonal")
