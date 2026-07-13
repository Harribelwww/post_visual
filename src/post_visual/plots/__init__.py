"""Plot primitives."""

from .annotations import annotate_arrow, annotate_text, event_lines, event_spans, significance_bracket
from .bars import bar, grouped_bar, horizontal_bar
from .distributions import box, ecdf, hist, kde, strip, violin
from .intervals import errorbar, forest_plot, interval_band, point_range
from .image import image, image_grid
from .line import line, plot_line
from .matrix import grid_color, heatmap
from .scatter import scatter

__all__ = [
    "bar",
    "annotate_arrow",
    "annotate_text",
    "box",
    "ecdf",
    "grouped_bar",
    "grid_color",
    "horizontal_bar",
    "errorbar",
    "event_lines",
    "event_spans",
    "forest_plot",
    "heatmap",
    "hist",
    "image",
    "image_grid",
    "interval_band",
    "kde",
    "line",
    "plot_line",
    "point_range",
    "scatter",
    "significance_bracket",
    "strip",
    "violin",
]
