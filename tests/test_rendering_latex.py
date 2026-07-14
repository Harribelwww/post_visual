from __future__ import annotations

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import pytest

import post_visual as pv


pytestmark = pytest.mark.skipif(
    os.environ.get("POST_VISUAL_LATEX_INTEGRATION") != "1",
    reason="requires the native external-LaTeX integration environment",
)


def test_real_latex_diagnostics_render_png_and_pdf(tmp_path: Path) -> None:
    result = pv.latex_diagnostics(
        pv.LatexConfig(engine="usetex", strict=True),
        output_dir=tmp_path,
        smoke=True,
    )
    assert result.available, result.actionable_message()
    assert result.png_path is not None and result.png_path.stat().st_size > 0
    assert result.pdf_path is not None and result.pdf_path.stat().st_size > 0
    assert result.latex.version
    assert result.dvipng.version


def test_real_latex_context_and_bad_preamble(tmp_path: Path) -> None:
    with pv.latex_context("usetex", strict=True) as config:
        assert config.engine == "usetex"

    with pytest.raises(pv.LatexUnavailableError, match="smoke render failed"):
        with pv.latex_context(
            "usetex",
            preamble=r"\usepackage{post_visual_missing_package}",
            strict=True,
        ):
            pass
