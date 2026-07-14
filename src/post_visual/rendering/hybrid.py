"""Per-artist rasterization for hybrid PDF export."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any

from matplotlib.artist import Artist
from matplotlib.collections import PathCollection, QuadMesh
from matplotlib.contour import ContourSet
from matplotlib.figure import Figure


@dataclass(frozen=True, slots=True)
class HybridConfig:
    """Density thresholds used to select rasterized artists."""

    scatter_threshold: int = 5_000
    mesh_threshold: int = 10_000
    contour_threshold: int = 10_000

    def __post_init__(self) -> None:
        for name in ("scatter_threshold", "mesh_threshold", "contour_threshold"):
            if getattr(self, name) < 1:
                raise ValueError(f"{name} must be at least 1")


def coerce_hybrid_config(value: HybridConfig | Mapping[str, Any] | None) -> HybridConfig:
    if value is None:
        return HybridConfig()
    if isinstance(value, HybridConfig):
        return value
    return HybridConfig(**dict(value))


def _path_vertices(artist: PathCollection) -> int:
    return sum(len(path.vertices) for path in artist.get_paths())


def should_rasterize(artist: Artist, config: HybridConfig) -> bool:
    """Return whether a supported high-density artist should be rasterized."""

    if isinstance(artist, ContourSet):
        if not artist.filled:
            return False
        if hasattr(artist, "get_paths"):
            vertices = sum(len(path.vertices) for path in artist.get_paths())
        else:  # Matplotlib 3.7 stores one PathCollection per contour level.
            vertices = sum(
                len(path.vertices)
                for collection in artist.collections
                for path in collection.get_paths()
            )
        return vertices >= config.contour_threshold
    if isinstance(artist, QuadMesh):
        array = artist.get_array()
        return array is not None and array.size >= config.mesh_threshold
    if isinstance(artist, PathCollection):
        offsets = artist.get_offsets()
        offset_count = len(offsets) if offsets is not None else 0
        if offset_count > 1:
            return offset_count >= config.scatter_threshold
        return _path_vertices(artist) >= config.contour_threshold
    return False


def select_hybrid_artists(fig: Figure, config: HybridConfig) -> tuple[Artist, ...]:
    """Select supported dense artists without mutating the figure."""

    selected: list[Artist] = []
    seen: set[int] = set()
    for artist in fig.findobj():
        if id(artist) not in seen and should_rasterize(artist, config):
            selected.append(artist)
            seen.add(id(artist))
    return tuple(selected)


@contextmanager
def hybrid_rasterization(
    fig: Figure,
    config: HybridConfig | Mapping[str, Any] | None = None,
) -> Iterator[tuple[Artist, ...]]:
    """Temporarily rasterize selected artists and always restore their state."""

    resolved = coerce_hybrid_config(config)
    selected = select_hybrid_artists(fig, resolved)
    original = tuple((artist, artist.get_rasterized()) for artist in selected)
    try:
        for artist, _ in original:
            artist.set_rasterized(True)
        yield selected
    finally:
        for artist, rasterized in original:
            artist.set_rasterized(rasterized)
