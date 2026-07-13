"""Scientific plotting helpers for data-science research results."""

from .core.export import save_figure
from .core.axes import format_axis, inset_axes, secondary_axis, shared_legend
from .core.layout import label_panels, panel_grid
from .plots.annotations import annotate_arrow, annotate_text, event_lines, event_spans, significance_bracket
from .plots.bars import bar, grouped_bar, horizontal_bar
from .plots.distributions import box, ecdf, hist, kde, strip, violin
from .plots.intervals import errorbar, forest_plot, interval_band, point_range
from .plots.image import image, image_grid
from .plots.line import line, plot_line
from .plots.matrix import grid_color, heatmap
from .plots.scatter import scatter
from .recipes import (
    ablation,
    calibration_curve,
    confusion_matrix,
    connectivity_matrix,
    embedding,
    feature_importance,
    model_comparison,
    pr_curve,
    roc_curve,
    training_curves,
)
from .style import (
    apply_style,
    available_palettes,
    get_palette,
    scientific_rc,
    style_context,
)

__all__ = [
    "apply_style",
    "annotate_arrow",
    "annotate_text",
    "ablation",
    "available_palettes",
    "bar",
    "box",
    "calibration_curve",
    "confusion_matrix",
    "connectivity_matrix",
    "embedding",
    "ecdf",
    "errorbar",
    "event_lines",
    "event_spans",
    "feature_importance",
    "forest_plot",
    "format_axis",
    "get_palette",
    "grid_color",
    "grouped_bar",
    "horizontal_bar",
    "heatmap",
    "hist",
    "image",
    "image_grid",
    "interval_band",
    "inset_axes",
    "kde",
    "line",
    "label_panels",
    "model_comparison",
    "plot_line",
    "panel_grid",
    "pr_curve",
    "point_range",
    "roc_curve",
    "save_figure",
    "scatter",
    "secondary_axis",
    "scientific_rc",
    "shared_legend",
    "significance_bracket",
    "style_context",
    "strip",
    "training_curves",
    "violin",
]
