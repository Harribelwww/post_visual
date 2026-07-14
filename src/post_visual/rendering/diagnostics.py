"""External LaTeX discovery and smoke-render diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
from typing import Any

import matplotlib.pyplot as plt

from .config import LatexConfig


@dataclass(frozen=True, slots=True)
class ExecutableStatus:
    """Discovery result for one required external executable."""

    name: str
    path: str | None
    version: str | None
    error: str | None = None

    @property
    def available(self) -> bool:
        return self.path is not None and self.error is None


@dataclass(frozen=True, slots=True)
class LatexDiagnostics:
    """Structured result returned by :func:`latex_diagnostics`."""

    latex: ExecutableStatus
    dvipng: ExecutableStatus
    smoke_requested: bool
    png_ok: bool | None
    pdf_ok: bool | None
    png_path: Path | None
    pdf_path: Path | None
    errors: tuple[str, ...] = ()

    @property
    def available(self) -> bool:
        executables_ok = self.latex.available and self.dvipng.available
        smoke_ok = not self.smoke_requested or (self.png_ok is True and self.pdf_ok is True)
        return executables_ok and smoke_ok and not self.errors

    def actionable_message(self) -> str:
        if self.available:
            return "external LaTeX is available"
        details = list(self.errors)
        for status in (self.latex, self.dvipng):
            if status.path is None:
                details.append(f"{status.name} was not found on PATH")
            elif status.error:
                details.append(f"{status.name}: {status.error}")
        suffix = "; ".join(dict.fromkeys(details)) or "unknown LaTeX failure"
        return (
            f"external LaTeX is unavailable: {suffix}. "
            "Run `post-visual doctor --latex` inside the TeX Live Docker container."
        )

    def to_dict(self) -> dict[str, Any]:
        def executable(status: ExecutableStatus) -> dict[str, Any]:
            return {
                "name": status.name,
                "path": status.path,
                "version": status.version,
                "error": status.error,
                "available": status.available,
            }

        return {
            "available": self.available,
            "message": self.actionable_message(),
            "latex": executable(self.latex),
            "dvipng": executable(self.dvipng),
            "smoke_requested": self.smoke_requested,
            "png_ok": self.png_ok,
            "pdf_ok": self.pdf_ok,
            "png_path": str(self.png_path) if self.png_path else None,
            "pdf_path": str(self.pdf_path) if self.pdf_path else None,
            "errors": list(self.errors),
        }


class LatexUnavailableError(RuntimeError):
    """Raised when explicitly requested external LaTeX cannot be used."""


def _executable_status(name: str) -> ExecutableStatus:
    path = shutil.which(name)
    if path is None:
        return ExecutableStatus(name=name, path=None, version=None)
    try:
        result = subprocess.run(
            [path, "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        version = (result.stdout or result.stderr).splitlines()[0].strip()
        return ExecutableStatus(name=name, path=path, version=version)
    except (OSError, subprocess.SubprocessError) as exc:
        return ExecutableStatus(name=name, path=path, version=None, error=str(exc))


def _smoke_render(config: LatexConfig, output_dir: Path) -> tuple[bool, bool, tuple[str, ...]]:
    errors: list[str] = []
    outcomes: dict[str, bool] = {}
    for suffix in ("png", "pdf"):
        fig = None
        try:
            with plt.rc_context(rc=config.rc_params()):
                fig, ax = plt.subplots(figsize=(2.4, 1.6))
                ax.plot([0, 1], [0, 1], label=r"$y = x^2$")
                ax.set_xlabel(r"$\alpha + \beta$")
                ax.legend()
                fig.savefig(output_dir / f"latex-smoke.{suffix}", dpi=120)
            outcomes[suffix] = True
        except Exception as exc:  # Matplotlib wraps TeX failures in backend-specific errors.
            outcomes[suffix] = False
            errors.append(f"{suffix} smoke render failed: {exc}")
        finally:
            if fig is not None:
                plt.close(fig)
    return outcomes["png"], outcomes["pdf"], tuple(errors)


def latex_diagnostics(
    config: LatexConfig | None = None,
    *,
    output_dir: str | Path | None = None,
    smoke: bool = True,
) -> LatexDiagnostics:
    """Discover LaTeX tools and optionally perform real PNG/PDF smoke renders."""

    active_config = config or LatexConfig(engine="usetex")
    if active_config.engine != "usetex":
        active_config = LatexConfig(
            engine="usetex",
            preamble=active_config.preamble,
            strict=active_config.strict,
            allow_fallback=active_config.allow_fallback,
            mathtext_fontset=active_config.mathtext_fontset,
        )
    latex = _executable_status("latex")
    dvipng = _executable_status("dvipng")
    can_smoke = smoke and latex.available and dvipng.available

    if output_dir is None:
        with TemporaryDirectory(prefix="post-visual-latex-") as temporary:
            directory = Path(temporary)
            png_ok, pdf_ok, errors = (
                _smoke_render(active_config, directory) if can_smoke else (None, None, ())
            )
            return LatexDiagnostics(
                latex=latex,
                dvipng=dvipng,
                smoke_requested=smoke,
                png_ok=png_ok,
                pdf_ok=pdf_ok,
                png_path=None,
                pdf_path=None,
                errors=errors,
            )

    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    png_ok, pdf_ok, errors = (
        _smoke_render(active_config, directory) if can_smoke else (None, None, ())
    )
    return LatexDiagnostics(
        latex=latex,
        dvipng=dvipng,
        smoke_requested=smoke,
        png_ok=png_ok,
        pdf_ok=pdf_ok,
        png_path=directory / "latex-smoke.png" if png_ok else None,
        pdf_path=directory / "latex-smoke.pdf" if pdf_ok else None,
        errors=errors,
    )
