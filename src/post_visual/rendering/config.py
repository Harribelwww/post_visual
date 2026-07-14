"""Project-scoped rendering configuration."""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Literal

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised on Python 3.10
    import tomli as tomllib


LatexEngine = Literal["mathtext", "usetex"]
_ACTIVE_LATEX_CONFIG: ContextVar[LatexConfig | None] = ContextVar(
    "post_visual_latex_config",
    default=None,
)


@dataclass(frozen=True, slots=True)
class LatexConfig:
    """Configuration for MathText or external LaTeX rendering."""

    engine: LatexEngine = "mathtext"
    preamble: tuple[str, ...] = ()
    strict: bool = True
    allow_fallback: bool = False
    mathtext_fontset: str = "stix"

    def __post_init__(self) -> None:
        if self.engine not in {"mathtext", "usetex"}:
            raise ValueError("latex engine must be 'mathtext' or 'usetex'")
        if not self.mathtext_fontset:
            raise ValueError("mathtext_fontset must not be empty")
        object.__setattr__(self, "preamble", tuple(str(item) for item in self.preamble))

    def rc_params(self) -> dict[str, Any]:
        """Return the Matplotlib rcParams represented by this configuration."""

        rc: dict[str, Any] = {
            "mathtext.fontset": self.mathtext_fontset,
            "text.usetex": self.engine == "usetex",
        }
        if self.preamble:
            rc["text.latex.preamble"] = "\n".join(self.preamble)
        return rc


def find_project_config(start: str | Path | None = None) -> Path | None:
    """Find the nearest ``post_visual.toml`` from *start* upwards."""

    current = Path.cwd() if start is None else Path(start)
    current = current.resolve()
    if current.is_file():
        current = current.parent
    for directory in (current, *current.parents):
        candidate = directory / "post_visual.toml"
        if candidate.is_file():
            return candidate
    return None


def load_project_config(path: str | Path | None = None) -> LatexConfig:
    """Load ``[latex]`` settings from a project configuration file."""

    config_path = Path(path).resolve() if path is not None else find_project_config()
    if config_path is None:
        return LatexConfig()
    if not config_path.is_file():
        raise FileNotFoundError(f"post_visual configuration not found: {config_path}")

    with config_path.open("rb") as stream:
        document = tomllib.load(stream)
    raw = document.get("latex", {})
    if not isinstance(raw, dict):
        raise ValueError("[latex] must be a TOML table")
    allowed = {"engine", "preamble", "strict", "allow_fallback", "mathtext_fontset"}
    unknown = sorted(set(raw) - allowed)
    if unknown:
        raise ValueError(f"unknown [latex] setting(s): {', '.join(unknown)}")

    preamble = raw.get("preamble", ())
    if isinstance(preamble, str):
        preamble = (preamble,)
    if not isinstance(preamble, (list, tuple)) or not all(
        isinstance(item, str) for item in preamble
    ):
        raise ValueError("latex.preamble must be a string or an array of strings")

    return LatexConfig(
        engine=raw.get("engine", "mathtext"),
        preamble=tuple(preamble),
        strict=raw.get("strict", True),
        allow_fallback=raw.get("allow_fallback", False),
        mathtext_fontset=raw.get("mathtext_fontset", "stix"),
    )


def resolve_latex_config(
    *,
    engine: LatexEngine | None = None,
    preamble: tuple[str, ...] | list[str] | str | None = None,
    strict: bool | None = None,
    allow_fallback: bool | None = None,
    mathtext_fontset: str | None = None,
    config_path: str | Path | None = None,
) -> LatexConfig:
    """Resolve explicit, active-context, project, and default configuration."""

    active = _ACTIVE_LATEX_CONFIG.get()
    base = active if active is not None else load_project_config(config_path)
    if isinstance(preamble, str):
        preamble = (preamble,)
    updates = {
        "engine": engine,
        "preamble": tuple(preamble) if preamble is not None else None,
        "strict": strict,
        "allow_fallback": allow_fallback,
        "mathtext_fontset": mathtext_fontset,
    }
    return replace(base, **{key: value for key, value in updates.items() if value is not None})


def write_project_config(config: LatexConfig, path: str | Path = "post_visual.toml") -> Path:
    """Write a deterministic project-level TOML configuration."""

    import json

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    preamble = ", ".join(json.dumps(item) for item in config.preamble)
    content = (
        "[latex]\n"
        f"engine = {json.dumps(config.engine)}\n"
        f"preamble = [{preamble}]\n"
        f"strict = {str(config.strict).lower()}\n"
        f"allow_fallback = {str(config.allow_fallback).lower()}\n"
        f"mathtext_fontset = {json.dumps(config.mathtext_fontset)}\n"
    )
    output.write_text(content, encoding="utf-8")
    return output
