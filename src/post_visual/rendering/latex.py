"""Scoped MathText and external LaTeX rendering contexts."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import matplotlib as mpl

from .config import LatexConfig, LatexEngine, _ACTIVE_LATEX_CONFIG, resolve_latex_config
from .diagnostics import LatexUnavailableError, latex_diagnostics


@contextmanager
def latex_context(
    engine: LatexEngine | None = None,
    *,
    preamble: tuple[str, ...] | list[str] | str | None = None,
    strict: bool | None = None,
    allow_fallback: bool | None = None,
    mathtext_fontset: str | None = None,
    config_path: str | Path | None = None,
) -> Iterator[LatexConfig]:
    """Apply resolved rendering settings and restore all active state on exit."""

    resolved = resolve_latex_config(
        engine=engine,
        preamble=preamble,
        strict=strict,
        allow_fallback=allow_fallback,
        mathtext_fontset=mathtext_fontset,
        config_path=config_path,
    )
    effective = resolved
    if resolved.engine == "usetex":
        diagnostics = latex_diagnostics(resolved, smoke=resolved.strict)
        if not diagnostics.available:
            if not resolved.allow_fallback:
                raise LatexUnavailableError(diagnostics.actionable_message())
            effective = LatexConfig(
                engine="mathtext",
                preamble=resolved.preamble,
                strict=resolved.strict,
                allow_fallback=True,
                mathtext_fontset=resolved.mathtext_fontset,
            )

    token = _ACTIVE_LATEX_CONFIG.set(effective)
    try:
        with mpl.rc_context(rc=effective.rc_params()):
            yield effective
    finally:
        _ACTIVE_LATEX_CONFIG.reset(token)
