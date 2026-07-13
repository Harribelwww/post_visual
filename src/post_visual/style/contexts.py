"""Scoped style helpers."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import Any

import matplotlib as mpl

from .rc import scientific_rc


@contextmanager
def style_context(
    palette: str | int = "furina",
    *,
    usetex: bool = False,
    extra: Mapping[str, Any] | None = None,
) -> Iterator[None]:
    """Temporarily apply the `post_visual` scientific matplotlib style."""

    rc = scientific_rc(palette=palette, usetex=usetex)
    if extra:
        rc.update(extra)
    with mpl.rc_context(rc=rc):
        yield

