"""Named color palettes derived from the MATLAB style baseline."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeAlias

RGB: TypeAlias = tuple[float, float, float]


PALETTES: dict[str, tuple[RGB, ...]] = {
    "furina": (
        (20 / 255, 21 / 255, 33 / 255),
        (45 / 255, 60 / 255, 129 / 255),
        (147 / 255, 117 / 255, 98 / 255),
        (78 / 255, 164 / 255, 239 / 255),
        (218 / 255, 226 / 255, 237 / 255),
    ),
    "nilou": (
        (20 / 255, 54 / 255, 95 / 255),
        (214 / 255, 79 / 255, 56 / 255),
        (118 / 255, 162 / 255, 185 / 255),
        (191 / 255, 217 / 255, 229 / 255),
    ),
}

_PALETTE_ALIASES = {
    "1": "furina",
    "2": "nilou",
}


def available_palettes() -> tuple[str, ...]:
    """Return the stable named palettes available in the core package."""

    return tuple(PALETTES)


def get_palette(name: str | int = "furina", n: int | None = None) -> list[RGB]:
    """Return a named palette, cycling colors when `n` exceeds its length.

    Parameters
    ----------
    name:
        Palette name. Integer aliases mirror the original MATLAB script:
        `1` means Furina and `2` means Nilou.
    n:
        Optional number of colors. When omitted, the base palette is returned.
    """

    palette_name = _normalize_palette_name(name)
    base = list(PALETTES[palette_name])

    if n is None:
        return base
    if n < 0:
        raise ValueError("n must be non-negative.")
    if not base:
        return []
    return [base[i % len(base)] for i in range(n)]


def resolve_colors(
    palette: str | int | Sequence[RGB] = "furina",
    n: int | None = None,
) -> list[RGB] | Sequence[RGB]:
    """Resolve a named palette or cycle a custom color sequence."""

    if isinstance(palette, str | int):
        return get_palette(palette, n=n)

    colors = list(palette)
    if n is None:
        return colors
    if n < 0:
        raise ValueError("n must be non-negative.")
    if not colors:
        raise ValueError("Custom palette must contain at least one color.")
    return [colors[i % len(colors)] for i in range(n)]


def _normalize_palette_name(name: str | int) -> str:
    key = str(name).strip().lower()
    key = _PALETTE_ALIASES.get(key, key)
    if key not in PALETTES:
        available = ", ".join(available_palettes())
        raise ValueError(f"Unknown palette {name!r}. Available palettes: {available}.")
    return key

