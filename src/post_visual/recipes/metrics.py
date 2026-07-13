"""Metric visualization recipes."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from post_visual.plots.line import line
from post_visual.plots.matrix import heatmap
from post_visual.style.palettes import RGB
from post_visual.style.rc import DEFAULT_FIGSIZE_CM


def confusion_matrix(
    y_true: Any | None = None,
    y_pred: Any | None = None,
    *,
    matrix: Any | None = None,
    labels: Sequence[Any] | None = None,
    display_labels: Sequence[Any] | None = None,
    normalize: str | None = None,
    cmap: str = "Blues",
    annot: bool = True,
    fmt: str | None = None,
    colorbar: bool = True,
    ax: Axes | None = None,
    title: str | None = "Confusion Matrix",
    xlabel: str | None = "Predicted label",
    ylabel: str | None = "True label",
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    heatmap_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Plot a confusion matrix from labels or a precomputed matrix."""

    resolved_labels = labels
    if matrix is None and labels is None and y_true is not None and y_pred is not None:
        resolved_labels = _unique_in_order(np.ravel(np.asarray(y_true)), np.ravel(np.asarray(y_pred)))

    values = _resolve_confusion_values(
        y_true=y_true,
        y_pred=y_pred,
        matrix=matrix,
        labels=resolved_labels,
        normalize=normalize,
    )
    tick_labels = _resolve_display_labels(
        values=values,
        labels=resolved_labels,
        display_labels=display_labels,
    )
    resolved_fmt = fmt or (".0f" if _is_integer_matrix(values) else ".2f")

    kwargs = {
        "annot": annot,
        "fmt": resolved_fmt,
        "cmap": cmap,
        "colorbar": colorbar,
        "xlabels": tick_labels,
        "ylabels": tick_labels,
        "ax": ax,
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel,
        "figsize_cm": figsize_cm,
        "style": style,
        "usetex": usetex,
    }
    if heatmap_kws:
        kwargs.update(heatmap_kws)
    return heatmap(values, **kwargs)


def roc_curve(
    y_true: Any,
    y_score: Any,
    *,
    labels: Sequence[str] | None = None,
    pos_label: Any | None = None,
    baseline: bool = True,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = "ROC Curve",
    xlabel: str = "False Positive Rate",
    ylabel: str = "True Positive Rate",
    legend: bool | None = True,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    line_kws: Mapping[str, Any] | None = None,
    baseline_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Plot one or more binary ROC curves."""

    curves = []
    for label, scores in _iter_score_series(y_score, labels=labels):
        fpr, tpr, _ = _roc_points(y_true=y_true, y_score=scores, pos_label=pos_label)
        score = _auc(fpr, tpr)
        curves.append((fpr, tpr, f"{label} (AUROC={score:.3f})"))

    fig, plot_ax = line(
        series=curves,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        legend=legend,
        figsize_cm=figsize_cm,
        style=style,
        usetex=usetex,
        line_kws=line_kws,
        legend_kws=legend_kws,
    )
    plot_ax.set_xlim(0, 1)
    plot_ax.set_ylim(0, 1)

    if baseline:
        kwargs = {"color": "0.35", "linestyle": "--", "linewidth": 1.0, "label": "Chance"}
        if baseline_kws:
            kwargs.update(baseline_kws)
        plot_ax.plot([0, 1], [0, 1], **kwargs)
        if legend is not False:
            plot_ax.legend(**({"loc": "best", "frameon": True, "fontsize": 13} | dict(legend_kws or {})))
    return fig, plot_ax


def pr_curve(
    y_true: Any,
    y_score: Any,
    *,
    labels: Sequence[str] | None = None,
    pos_label: Any | None = None,
    baseline: bool = True,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = "Precision-Recall Curve",
    xlabel: str = "Recall",
    ylabel: str = "Precision",
    legend: bool | None = True,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    line_kws: Mapping[str, Any] | None = None,
    baseline_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Plot one or more binary precision-recall curves."""

    curves = []
    for label, scores in _iter_score_series(y_score, labels=labels):
        precision, recall, _ = _pr_points(y_true=y_true, y_score=scores, pos_label=pos_label)
        score = _average_precision(precision=precision, recall=recall)
        curves.append((recall, precision, f"{label} (AUPRC={score:.3f})"))

    fig, plot_ax = line(
        series=curves,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        legend=legend,
        figsize_cm=figsize_cm,
        style=style,
        usetex=usetex,
        line_kws=line_kws,
        legend_kws=legend_kws,
    )
    plot_ax.set_xlim(0, 1)
    plot_ax.set_ylim(0, 1)

    if baseline:
        prevalence = _positive_prevalence(y_true=y_true, pos_label=pos_label)
        kwargs = {
            "color": "0.35",
            "linestyle": "--",
            "linewidth": 1.0,
            "label": f"Prevalence={prevalence:.3f}",
        }
        if baseline_kws:
            kwargs.update(baseline_kws)
        plot_ax.axhline(prevalence, **kwargs)
        if legend is not False:
            plot_ax.legend(**({"loc": "best", "frameon": True, "fontsize": 13} | dict(legend_kws or {})))
    return fig, plot_ax


def calibration_curve(
    y_true: Any,
    y_prob: Any,
    *,
    labels: Sequence[str] | None = None,
    pos_label: Any | None = None,
    n_bins: int = 10,
    strategy: str = "uniform",
    show_ece: bool = True,
    palette: str | int | Sequence[RGB] = "furina",
    ax: Axes | None = None,
    title: str | None = "Calibration Curve",
    xlabel: str = "Mean predicted probability",
    ylabel: str = "Observed positive rate",
    legend: bool | None = True,
    figsize_cm: tuple[float, float] = DEFAULT_FIGSIZE_CM,
    style: bool = True,
    usetex: bool = False,
    line_kws: Mapping[str, Any] | None = None,
    baseline_kws: Mapping[str, Any] | None = None,
    legend_kws: Mapping[str, Any] | None = None,
) -> tuple[Figure, Axes]:
    """Plot binary reliability curves and expected calibration error."""

    curves = []
    for label, probabilities in _iter_score_series(y_prob, labels=labels):
        mean_prob, observed, counts = _calibration_points(
            y_true=y_true,
            y_prob=probabilities,
            pos_label=pos_label,
            n_bins=n_bins,
            strategy=strategy,
        )
        ece = float(np.sum(counts * np.abs(observed - mean_prob)) / np.sum(counts))
        display_label = f"{label} (ECE={ece:.3f})" if show_ece else label
        curves.append((mean_prob, observed, display_label))

    fig, plot_ax = line(
        series=curves,
        palette=palette,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        legend=legend,
        figsize_cm=figsize_cm,
        style=style,
        usetex=usetex,
        line_kws=line_kws,
        legend_kws=legend_kws,
    )
    baseline = {"color": "0.3", "linestyle": "--", "linewidth": 1.0, "label": "Perfect calibration"}
    baseline.update(baseline_kws or {})
    plot_ax.plot([0, 1], [0, 1], **baseline)
    plot_ax.set_xlim(0, 1)
    plot_ax.set_ylim(0, 1)
    if legend is not False:
        plot_ax.legend(**({"loc": "best", "frameon": True, "fontsize": 11} | dict(legend_kws or {})))
    return fig, plot_ax


def _resolve_confusion_values(
    *,
    y_true: Any | None,
    y_pred: Any | None,
    matrix: Any | None,
    labels: Sequence[Any] | None,
    normalize: str | None,
) -> np.ndarray:
    if matrix is not None:
        values = np.asarray(matrix, dtype=float if normalize is not None else None)
        if values.ndim != 2 or values.shape[0] != values.shape[1]:
            raise ValueError("`matrix` must be a square two-dimensional array.")
        return _normalize_matrix(values, normalize=normalize)

    if y_true is None or y_pred is None:
        raise ValueError("Provide `y_true` and `y_pred`, or a precomputed `matrix`.")
    values = _confusion_matrix_from_labels(y_true=y_true, y_pred=y_pred, labels=labels)
    return _normalize_matrix(values, normalize=normalize)


def _normalize_matrix(values: np.ndarray, *, normalize: str | None) -> np.ndarray:
    if normalize is None:
        return values
    if normalize == "true":
        denominator = values.sum(axis=1, keepdims=True)
    elif normalize == "pred":
        denominator = values.sum(axis=0, keepdims=True)
    elif normalize == "all":
        denominator = values.sum()
    else:
        raise ValueError("normalize must be one of None, 'true', 'pred', or 'all'.")
    return np.divide(values, denominator, out=np.zeros_like(values, dtype=float), where=denominator != 0)


def _resolve_display_labels(
    *,
    values: np.ndarray,
    labels: Sequence[Any] | None,
    display_labels: Sequence[Any] | None,
) -> list[str]:
    raw_labels = display_labels if display_labels is not None else labels
    if raw_labels is None:
        return [str(index) for index in range(values.shape[0])]
    result = [str(label) for label in raw_labels]
    if len(result) != values.shape[0]:
        raise ValueError(f"display labels must have length {values.shape[0]}.")
    return result


def _is_integer_matrix(values: np.ndarray) -> bool:
    return np.issubdtype(values.dtype, np.integer)


def _iter_score_series(
    y_score: Any,
    *,
    labels: Sequence[str] | None,
) -> list[tuple[str, np.ndarray]]:
    if isinstance(y_score, Mapping):
        return [(str(label), np.ravel(np.asarray(scores))) for label, scores in y_score.items()]

    scores = np.asarray(y_score)
    if scores.ndim == 1:
        label = labels[0] if labels else "Model"
        return [(str(label), scores)]
    if scores.ndim == 2:
        if labels is not None and len(labels) != scores.shape[1]:
            raise ValueError(f"labels must have length {scores.shape[1]}.")
        return [
            (str(labels[index]) if labels is not None else f"Model {index + 1}", scores[:, index])
            for index in range(scores.shape[1])
        ]
    raise ValueError("y_score must be one-dimensional, two-dimensional, or a mapping.")


def _positive_prevalence(*, y_true: Any, pos_label: Any | None) -> float:
    y_array = np.ravel(np.asarray(y_true))
    positive = pos_label if pos_label is not None else 1
    return float(np.mean(y_array == positive))


def _calibration_points(
    *,
    y_true: Any,
    y_prob: Any,
    pos_label: Any | None,
    n_bins: int,
    strategy: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    true_array = np.ravel(np.asarray(y_true))
    prob_array = np.ravel(np.asarray(y_prob, dtype=float))
    if true_array.size != prob_array.size or true_array.size == 0:
        raise ValueError("y_true and y_prob must have the same non-zero length.")
    if not np.all(np.isfinite(prob_array)) or np.any((prob_array < 0) | (prob_array > 1)):
        raise ValueError("y_prob values must be finite probabilities in [0, 1].")
    if n_bins < 2:
        raise ValueError("n_bins must be at least 2.")

    if strategy == "uniform":
        edges = np.linspace(0.0, 1.0, n_bins + 1)
    elif strategy == "quantile":
        edges = np.quantile(prob_array, np.linspace(0.0, 1.0, n_bins + 1))
        edges = np.unique(edges)
        if edges.size < 2:
            raise ValueError("quantile binning requires at least two distinct probabilities.")
        edges[0], edges[-1] = 0.0, 1.0
    else:
        raise ValueError("strategy must be 'uniform' or 'quantile'.")

    bin_ids = np.clip(np.digitize(prob_array, edges[1:-1], right=True), 0, edges.size - 2)
    positive = pos_label if pos_label is not None else 1
    true_binary = true_array == positive
    mean_prob = []
    observed = []
    counts = []
    for bin_index in range(edges.size - 1):
        mask = bin_ids == bin_index
        if not np.any(mask):
            continue
        mean_prob.append(float(np.mean(prob_array[mask])))
        observed.append(float(np.mean(true_binary[mask])))
        counts.append(int(np.sum(mask)))
    return np.asarray(mean_prob), np.asarray(observed), np.asarray(counts)


def _confusion_matrix_from_labels(
    *,
    y_true: Any,
    y_pred: Any,
    labels: Sequence[Any] | None,
) -> np.ndarray:
    true_array = np.ravel(np.asarray(y_true))
    pred_array = np.ravel(np.asarray(y_pred))
    if true_array.size != pred_array.size:
        raise ValueError("y_true and y_pred must have the same length.")
    if true_array.size == 0:
        raise ValueError("y_true and y_pred must contain at least one item.")

    label_values = list(labels) if labels is not None else _unique_in_order(true_array, pred_array)
    label_to_index = {label: index for index, label in enumerate(label_values)}
    values = np.zeros((len(label_values), len(label_values)), dtype=int)
    for true_value, pred_value in zip(true_array, pred_array, strict=True):
        if true_value not in label_to_index or pred_value not in label_to_index:
            continue
        values[label_to_index[true_value], label_to_index[pred_value]] += 1
    return values


def _unique_in_order(*arrays: np.ndarray) -> list[Any]:
    result = []
    seen = set()
    for array in arrays:
        for value in array:
            if value in seen:
                continue
            seen.add(value)
            result.append(value)
    return result


def _roc_points(
    *,
    y_true: Any,
    y_score: Any,
    pos_label: Any | None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    fps, tps, thresholds = _binary_clf_curve(
        y_true=y_true,
        y_score=y_score,
        pos_label=pos_label,
    )
    if fps[-1] <= 0 or tps[-1] <= 0:
        raise ValueError("ROC curve requires at least one positive and one negative sample.")

    fpr = np.r_[0.0, fps / fps[-1]]
    tpr = np.r_[0.0, tps / tps[-1]]
    return fpr, tpr, np.r_[np.inf, thresholds]


def _pr_points(
    *,
    y_true: Any,
    y_score: Any,
    pos_label: Any | None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    fps, tps, thresholds = _binary_clf_curve(
        y_true=y_true,
        y_score=y_score,
        pos_label=pos_label,
    )
    if tps[-1] <= 0:
        raise ValueError("Precision-recall curve requires at least one positive sample.")

    precision = np.divide(tps, tps + fps, out=np.ones_like(tps, dtype=float), where=(tps + fps) != 0)
    recall = tps / tps[-1]
    return np.r_[1.0, precision], np.r_[0.0, recall], thresholds


def _binary_clf_curve(
    *,
    y_true: Any,
    y_score: Any,
    pos_label: Any | None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    true_array = np.ravel(np.asarray(y_true))
    score_array = np.ravel(np.asarray(y_score, dtype=float))
    if true_array.size != score_array.size:
        raise ValueError("y_true and y_score must have the same length.")
    if true_array.size == 0:
        raise ValueError("y_true and y_score must contain at least one item.")

    positive = pos_label if pos_label is not None else 1
    true_binary = true_array == positive
    order = np.argsort(score_array, kind="mergesort")[::-1]
    sorted_scores = score_array[order]
    sorted_true = true_binary[order]

    distinct_indices = np.where(np.diff(sorted_scores))[0]
    threshold_indices = np.r_[distinct_indices, sorted_true.size - 1]
    tps = np.cumsum(sorted_true, dtype=float)[threshold_indices]
    fps = 1 + threshold_indices - tps
    thresholds = sorted_scores[threshold_indices]
    return fps, tps, thresholds


def _auc(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.sum((x[1:] - x[:-1]) * (y[1:] + y[:-1]) / 2))


def _average_precision(*, precision: np.ndarray, recall: np.ndarray) -> float:
    return float(np.sum(np.diff(recall) * precision[1:]))
