"""Generate a compositional event-annotation example."""

from __future__ import annotations

from pathlib import Path

import numpy as np

import post_visual as pv


def main() -> list[Path]:
    output_dir = Path(__file__).parent / "out"
    epochs = np.arange(1, 31)
    score = 0.52 + 0.34 * (1 - np.exp(-epochs / 10))

    fig, ax = pv.line(
        epochs,
        score,
        label="Validation score",
        title="Training Events MVP",
        xlabel="Epoch",
        ylabel="Score",
    )
    pv.event_spans(
        [(1, 5)],
        labels=["Warmup"],
        colors="#4C78A8",
        ax=ax,
    )
    pv.event_lines(
        [16, 24],
        labels=["LR decay", "Early stop check"],
        colors=["#E64B35", "#59A14F"],
        ax=ax,
    )
    path = pv.save_figure(fig, output_dir / "event_annotations_mvp.png")
    return [path]


if __name__ == "__main__":
    for path in main():
        print(path)
