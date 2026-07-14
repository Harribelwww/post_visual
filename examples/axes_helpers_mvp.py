"""Generate axes-helper composition example."""

from __future__ import annotations

from pathlib import Path

import numpy as np

import post_visual as pv


def main() -> list[Path]:
    output_dir = Path(__file__).parent / "out"
    fig, axes = pv.panel_grid(1, 2, labels=True, suptitle="Axes Helpers MVP")
    x = np.linspace(0, 1, 40)
    pv.line(x, 0.55 + 0.35 * x, label="Proposed", ax=axes[0, 0], title="Percent format", xlabel="Progress", ylabel="Accuracy")
    pv.format_axis(axes[0, 0], style="percent", scale=1.0, decimals=0)
    pv.secondary_axis(
        axes[0, 0],
        functions=(lambda value: value * 100, lambda value: value / 100),
        label="Progress (%)",
    )

    pv.line(x, np.exp(5 * x), label="Growth", ax=axes[0, 1], title="Inset detail", xlabel="Time", ylabel="Response")
    _, inset = pv.inset_axes(axes[0, 1], [0.12, 0.36, 0.4, 0.32])
    pv.line(x[:12], np.exp(5 * x[:12]), ax=inset, style=False, marker=None, line_kws={"linewidth": 1.0})
    inset.set_title("Early", fontsize=7, pad=2)
    inset.tick_params(labelsize=6)
    inset.tick_params(labelsize=6)
    inset.tick_params(labelsize=6)
    pv.shared_legend(axes, legend_kws={"loc": "outside lower center", "ncol": 2})
    path = pv.save_figure(fig, output_dir / "axes_helpers_mvp.png")
    return [path]


if __name__ == "__main__":
    for path in main():
        print(path)
