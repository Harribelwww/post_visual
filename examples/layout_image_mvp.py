"""Generate multi-panel and image-grid examples."""

from __future__ import annotations

from pathlib import Path

import numpy as np

import post_visual as pv


def main() -> list[Path]:
    output_dir = Path(__file__).parent / "out"
    x = np.linspace(0, 2 * np.pi, 80)
    fig, axes = pv.panel_grid(
        1,
        3,
        n_panels=3,
        labels=True,
        suptitle="Multi-panel Layout MVP",
        panel_size_cm=(5.5, 5.0),
    )
    pv.line(x, np.sin(x), ax=axes[0, 0], title="Signal A", xlabel="Time", ylabel="Value")
    pv.scatter(x[::4], np.cos(x[::4]), ax=axes[0, 1], title="Signal B", xlabel="Time")
    pv.interval_band(
        x,
        np.sin(x) - 0.15,
        np.sin(x) + 0.15,
        center=np.sin(x),
        ax=axes[0, 2],
        title="Signal C",
        xlabel="Time",
    )
    layout_path = pv.save_figure(fig, output_dir / "panel_grid_mvp.png")

    coordinates = np.linspace(-1, 1, 64)
    xx, yy = np.meshgrid(coordinates, coordinates)
    images = [
        np.exp(-((xx - shift) ** 2 + (yy + shift) ** 2) / 0.18)
        for shift in (-0.35, 0.0, 0.35)
    ]
    fig, axes = pv.image_grid(
        images,
        titles=["Condition A", "Condition B", "Condition C"],
        ncols=3,
        colorbar="shared",
        colorbar_label="Normalized intensity",
        cmap="magma",
    )
    image_path = pv.save_figure(fig, output_dir / "image_grid_mvp.png")
    return [layout_path, image_path]


if __name__ == "__main__":
    for path in main():
        print(path)
