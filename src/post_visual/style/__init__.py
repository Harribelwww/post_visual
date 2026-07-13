"""Style primitives for the fixed `post_visual` scientific look."""

from .contexts import style_context
from .palettes import available_palettes, get_palette
from .rc import apply_style, scientific_rc

__all__ = [
    "apply_style",
    "available_palettes",
    "get_palette",
    "scientific_rc",
    "style_context",
]

