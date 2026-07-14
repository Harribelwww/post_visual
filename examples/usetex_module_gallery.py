"""Generate one real-LaTeX example for every public plotting/recipe module."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import post_visual as pv


FigureFactory = Callable[[], tuple[object, object]]

MODULE_EXAMPLES: tuple[tuple[str, FigureFactory], ...]


def _plots_annotations():
    x = np.linspace(0.0, 1.0, 40)
    y = np.exp(-3.0 * (x - 0.55) ** 2)
    fig, ax = pv.line(
        x=x,
        y=y,
        title=r"Annotations: $f(x)=\exp[-3(x-0.55)^2]$",
        xlabel=r"Normalized time $t/T$",
        ylabel=r"Response $f(x)$",
        usetex=True,
    )
    peak = int(np.argmax(y))
    pv.annotate_arrow(
        r"Maximum $f(x_\ast)$",
        (x[peak], y[peak]),
        (0.72, 0.78),
        ax=ax,
        usetex=True,
    )
    return fig, ax


def _plots_bars():
    return pv.grouped_bar(
        np.array([[0.78, 0.84], [0.81, 0.88], [0.83, 0.91]]),
        categories=[r"Fold $1$", r"Fold $2$", r"Fold $3$"],
        groups=[r"Baseline $M_0$", r"Proposed $M_1$"],
        title=r"Grouped estimates $\hat{\mu}\pm\sigma$",
        ylabel=r"Score $s$",
        usetex=True,
    )


def _plots_distributions():
    rng = np.random.default_rng(17)
    values = np.column_stack(
        [rng.normal(0.0, 0.8, 80), rng.normal(0.7, 0.55, 80)]
    )
    return pv.violin(
        values,
        labels=[r"Control $p_0(x)$", r"Treatment $p_1(x)$"],
        title=r"Estimated densities $p_k(x)$",
        ylabel=r"Observation $x$",
        usetex=True,
    )


def _plots_image():
    grid = np.linspace(-1.0, 1.0, 96)
    xx, yy = np.meshgrid(grid, grid)
    image = np.exp(-4.0 * (xx**2 + yy**2)) * np.cos(5.0 * xx)
    return pv.image(
        image,
        title=r"Image field $I(x,y)=e^{-4r^2}\cos(5x)$",
        colorbar=True,
        colorbar_label=r"Intensity $I$",
        usetex=True,
    )


def _plots_intervals():
    estimates = np.array([0.88, 1.03, 1.21, 1.38])
    return pv.point_range(
        estimates,
        estimates - np.array([0.12, 0.10, 0.13, 0.15]),
        estimates + np.array([0.14, 0.12, 0.16, 0.17]),
        categories=[r"$M_0$", r"$M_1$", r"$M_2$", r"$M_3$"],
        reference=1.0,
        title=r"Interval estimates $\hat{\theta}_k$",
        xlabel=r"Effect $\theta$ with $95\%$ interval",
        usetex=True,
    )


def _plots_line():
    x = np.linspace(0.0, 2.0 * np.pi, 80)
    y = np.sin(x)
    return pv.line(
        x=x,
        y=y,
        lower=y - 0.15,
        upper=y + 0.15,
        title=r"Line primitive: $y=\sin(x)$",
        xlabel=r"Phase $x$ (rad)",
        ylabel=r"Amplitude $y$",
        usetex=True,
    )


def _plots_matrix():
    matrix = np.array([[1.0, 0.42, -0.18], [0.42, 1.0, 0.31], [-0.18, 0.31, 1.0]])
    return pv.heatmap(
        matrix,
        xlabels=[r"$x_1$", r"$x_2$", r"$x_3$"],
        ylabels=[r"$x_1$", r"$x_2$", r"$x_3$"],
        annot=True,
        cmap="coolwarm",
        title=r"Correlation matrix $R_{ij}$",
        colorbar_kws={"label": r"Correlation $\rho$"},
        usetex=True,
    )


def _plots_scatter():
    rng = np.random.default_rng(23)
    x = np.linspace(-1.0, 1.0, 60)
    y = 0.4 + 0.75 * x + rng.normal(0.0, 0.12, x.size)
    return pv.scatter(
        x=x,
        y=y,
        fit_line=True,
        fit_ci=0.95,
        title=r"Regression $y=\beta_0+\beta_1x+\epsilon$",
        xlabel=r"Predictor $x$",
        ylabel=r"Outcome $y$",
        usetex=True,
    )


def _recipes_comparison():
    return pv.model_comparison(
        np.array([[0.78, 0.83], [0.84, 0.88], [0.87, 0.92]]),
        models=[r"$M_0$", r"$M_1$", r"$M_2$"],
        metrics=[r"Dataset $\mathcal{D}_1$", r"Dataset $\mathcal{D}_2$"],
        title=r"Model comparison $\hat{s}_{mk}$",
        ylabel=r"Mean score $\bar{s}$",
        usetex=True,
    )


def _recipes_interpretation():
    return pv.feature_importance(
        np.array([0.21, -0.16, 0.12, 0.07]),
        names=[r"$x_1$", r"$x_2$", r"$x_3$", r"$x_4$"],
        title=r"Feature contributions $\phi_j$",
        xlabel=r"Signed importance $\phi_j$",
        usetex=True,
    )


def _recipes_metrics():
    return pv.confusion_matrix(
        matrix=np.array([[34, 4, 2], [3, 31, 6], [1, 5, 36]]),
        display_labels=[r"Class $A$", r"Class $B$", r"Class $C$"],
        title=r"Confusion counts $C_{ij}$",
        xlabel=r"Predicted class $\hat{y}$",
        ylabel=r"Reference class $y$",
        usetex=True,
    )


def _recipes_signal():
    matrix = np.array(
        [
            [1.0, 0.62, 0.33, 0.21],
            [0.62, 1.0, 0.48, 0.36],
            [0.33, 0.48, 1.0, 0.71],
            [0.21, 0.36, 0.71, 1.0],
        ]
    )
    return pv.connectivity_matrix(
        matrix,
        labels=[r"$F_3$", r"$F_4$", r"$P_3$", r"$P_4$"],
        triangle="upper",
        annot=True,
        title=r"Connectivity $W_{ij}$",
        colorbar_label=r"Coherence $\gamma_{ij}$",
        usetex=True,
    )


def _recipes_training():
    epochs = np.arange(1, 9)
    history = {
        "epoch": epochs,
        r"Training $\mathcal{L}$": np.exp(-0.42 * epochs) + 0.18,
        r"Validation $\mathcal{L}$": np.exp(-0.34 * epochs) + 0.24,
    }
    return pv.training_curves(
        history,
        x="epoch",
        title=r"Optimization of $\mathcal{L}(\theta)$",
        xlabel=r"Epoch $e$",
        ylabel=r"Loss $\mathcal{L}$",
        usetex=True,
    )


MODULE_EXAMPLES = (
    ("plots_annotations", _plots_annotations),
    ("plots_bars", _plots_bars),
    ("plots_distributions", _plots_distributions),
    ("plots_image", _plots_image),
    ("plots_intervals", _plots_intervals),
    ("plots_line", _plots_line),
    ("plots_matrix", _plots_matrix),
    ("plots_scatter", _plots_scatter),
    ("recipes_comparison", _recipes_comparison),
    ("recipes_interpretation", _recipes_interpretation),
    ("recipes_metrics", _recipes_metrics),
    ("recipes_signal", _recipes_signal),
    ("recipes_training", _recipes_training),
)


def main(output_dir: str | Path | None = None) -> list[Path]:
    """Render and verify the 13-module real-LaTeX gallery."""

    destination = (
        Path(output_dir)
        if output_dir is not None
        else Path(__file__).parent / "out" / "usetex"
    )
    destination.mkdir(parents=True, exist_ok=True)

    outputs: list[Path] = []
    with pv.latex_context("usetex", strict=True, allow_fallback=False):
        if not mpl.rcParams["text.usetex"]:
            raise RuntimeError("real-LaTeX gallery requires text.usetex=True")
        for module_name, factory in MODULE_EXAMPLES:
            fig, _ = factory()
            path = pv.save_figure(fig, destination / f"{module_name}.png")
            plt.close(fig)
            if not path.is_file() or path.stat().st_size == 0:
                raise RuntimeError(f"failed to generate {path}")
            outputs.append(path)

    if len(outputs) != len(MODULE_EXAMPLES):
        raise RuntimeError("real-LaTeX gallery did not cover every module")
    return outputs


if __name__ == "__main__":
    for output in main():
        print(output)
