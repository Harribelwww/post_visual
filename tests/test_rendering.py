from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pytest

import post_visual as pv
from post_visual.cli import main
from post_visual.rendering.diagnostics import ExecutableStatus


def _diagnostics(*, available: bool) -> pv.LatexDiagnostics:
    path = "/usr/bin/tool" if available else None
    status_latex = ExecutableStatus("latex", path, "latex 1" if path else None)
    status_dvipng = ExecutableStatus("dvipng", path, "dvipng 1" if path else None)
    return pv.LatexDiagnostics(
        latex=status_latex,
        dvipng=status_dvipng,
        smoke_requested=True,
        png_ok=True if available else None,
        pdf_ok=True if available else None,
        png_path=None,
        pdf_path=None,
    )


def test_project_configuration_and_resolution_precedence(tmp_path: Path, monkeypatch) -> None:
    config_path = tmp_path / "post_visual.toml"
    pv.write_project_config(
        pv.LatexConfig(engine="usetex", preamble=(r"\usepackage{amsmath}",)),
        config_path,
    )
    loaded = pv.load_project_config(config_path)
    assert loaded.engine == "usetex"
    assert loaded.preamble == (r"\usepackage{amsmath}",)

    explicit = pv.resolve_latex_config(engine="mathtext", config_path=config_path)
    assert explicit.engine == "mathtext"
    assert explicit.preamble == loaded.preamble

    monkeypatch.setattr(
        "post_visual.rendering.latex.latex_diagnostics",
        lambda *args, **kwargs: _diagnostics(available=True),
    )
    with pv.latex_context("usetex", preamble=("outer",), strict=True):
        nested = pv.resolve_latex_config(engine="mathtext", config_path=config_path)
        assert nested.engine == "mathtext"
        assert nested.preamble == ("outer",)


def test_latex_context_restores_rcparams_and_active_context(monkeypatch) -> None:
    before_usetex = mpl.rcParams["text.usetex"]
    before_fontset = mpl.rcParams["mathtext.fontset"]
    monkeypatch.setattr(
        "post_visual.rendering.latex.latex_diagnostics",
        lambda *args, **kwargs: _diagnostics(available=True),
    )

    with pv.latex_context("usetex", preamble="test", strict=True) as active:
        assert active.engine == "usetex"
        assert mpl.rcParams["text.usetex"] is True
        assert pv.resolve_latex_config().preamble == ("test",)

    assert mpl.rcParams["text.usetex"] == before_usetex
    assert mpl.rcParams["mathtext.fontset"] == before_fontset
    assert pv.resolve_latex_config().engine == "mathtext"

    with pytest.raises(RuntimeError, match="inside context"):
        with pv.latex_context("mathtext"):
            raise RuntimeError("inside context")
    assert mpl.rcParams["text.usetex"] == before_usetex


def test_unavailable_usetex_requires_explicit_fallback(monkeypatch) -> None:
    monkeypatch.setattr(
        "post_visual.rendering.latex.latex_diagnostics",
        lambda *args, **kwargs: _diagnostics(available=False),
    )
    with pytest.raises(pv.LatexUnavailableError, match="doctor --latex"):
        with pv.latex_context("usetex"):
            pass

    with pv.latex_context("usetex", allow_fallback=True) as effective:
        assert effective.engine == "mathtext"
        assert mpl.rcParams["text.usetex"] is False

    report = _diagnostics(available=False).to_dict()
    assert report["available"] is False
    assert "doctor --latex" in report["message"]


def test_bad_preamble_is_reported_in_strict_mode(monkeypatch) -> None:
    failed = replace(_diagnostics(available=True), png_ok=False, errors=("bad preamble",))
    monkeypatch.setattr(
        "post_visual.rendering.latex.latex_diagnostics",
        lambda *args, **kwargs: failed,
    )
    with pytest.raises(pv.LatexUnavailableError, match="bad preamble"):
        with pv.latex_context("usetex", preamble=r"\usepackage{missing}", strict=True):
            pass


def test_save_figure_rejects_unsupported_formats(tmp_path: Path) -> None:
    fig, _ = plt.subplots()
    with pytest.raises(ValueError, match="unsupported export format"):
        pv.save_figure(fig, tmp_path / "figure.svg")
    with pytest.raises(ValueError, match="only valid for PDF"):
        pv.save_figure(fig, tmp_path / "figure.png", pdf_mode="hybrid")
    plt.close(fig)


def test_vector_and_hybrid_pdf_structure_and_state_restoration(tmp_path: Path) -> None:
    rng = np.random.default_rng(10)
    fig, ax = plt.subplots()
    collection = ax.scatter(rng.normal(size=12_000), rng.normal(size=12_000), s=4)
    line = ax.plot([0, 1], [0, 1])[0]
    vector = pv.save_figure(fig, tmp_path / "vector.pdf", pdf_mode="vector")
    hybrid = pv.save_figure(
        fig,
        tmp_path / "hybrid.pdf",
        pdf_mode="hybrid",
        hybrid_kws={"scatter_threshold": 1_000},
    )

    assert collection.get_rasterized() is False
    assert line.get_rasterized() is False
    assert b"/Subtype /Image" not in vector.read_bytes()
    assert b"/Subtype /Image" in hybrid.read_bytes()
    assert hybrid.stat().st_size < vector.stat().st_size
    plt.close(fig)


def test_hybrid_selects_dense_scatter_and_mesh_but_not_lines() -> None:
    fig, ax = plt.subplots()
    dense = ax.scatter(np.arange(20), np.arange(20))
    sparse = ax.scatter([0, 1], [1, 0])
    mesh = ax.pcolormesh(np.arange(5).reshape(1, 5))
    line = ax.plot([0, 1], [0, 1])[0]
    selected = pv.select_hybrid_artists(
        fig,
        pv.HybridConfig(scatter_threshold=10, mesh_threshold=5),
    )
    assert dense in selected
    assert mesh in selected
    assert sparse not in selected
    assert line not in selected
    plt.close(fig)


def test_hybrid_selects_filled_contours_but_not_line_contours() -> None:
    grid = np.linspace(-2, 2, 80)
    x, y = np.meshgrid(grid, grid)
    z = np.sin(x**2 + y**2)
    fig, ax = plt.subplots()
    filled = ax.contourf(x, y, z, levels=20)
    lines = ax.contour(x, y, z, levels=10)

    selected = pv.select_hybrid_artists(
        fig,
        pv.HybridConfig(contour_threshold=10),
    )
    assert filled in selected or any(
        collection in selected for collection in getattr(filled, "collections", ())
    )
    assert lines not in selected
    assert not any(collection in selected for collection in getattr(lines, "collections", ()))
    plt.close(fig)


def test_hybrid_restores_state_when_save_fails(tmp_path: Path, monkeypatch) -> None:
    fig, ax = plt.subplots()
    collection = ax.scatter(np.arange(20), np.arange(20))

    def fail(*args, **kwargs):
        assert collection.get_rasterized() is True
        raise RuntimeError("save failed")

    monkeypatch.setattr(fig, "savefig", fail)
    with pytest.raises(RuntimeError, match="save failed"):
        pv.save_figure(
            fig,
            tmp_path / "failed.pdf",
            pdf_mode="hybrid",
            hybrid_kws={"scatter_threshold": 10},
        )
    assert collection.get_rasterized() is False
    plt.close(fig)


def test_cli_configure_writes_project_file(tmp_path: Path, capsys) -> None:
    path = tmp_path / "post_visual.toml"
    result = main(
        [
            "configure",
            "--path",
            str(path),
            "--engine",
            "usetex",
            "--preamble",
            r"\usepackage{amsmath}",
            "--allow-fallback",
        ]
    )
    assert result == 0
    assert pv.load_project_config(path).engine == "usetex"
    assert "configuration_written=" in capsys.readouterr().out
