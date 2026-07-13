"""Generate an MVP line-plot example."""

from __future__ import annotations

from pathlib import Path

import numpy as np

import post_visual as pv


def main() -> Path:
    x = np.geomspace(1, 100, 32)
    baseline = np.log1p(x)
    proposed = 1.18 * np.log1p(x) - 0.15

    fig, ax = pv.line(
        series=[
            (x, baseline, "Baseline"),
            (x, proposed, "Proposed"),
        ],
        plot_type="sx",
        title=r"Line Plot MVP",
        xlabel=r"Sample count $n$",
        ylabel=r"Score",
        palette="furina",
    )

    output_path = Path(__file__).parent / "out" / "line_mvp.png"
    pv.save_figure(fig, output_path)
    return output_path


if __name__ == "__main__":
    print(main())

