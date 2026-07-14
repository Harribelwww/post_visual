"""Command-line entry points for project rendering configuration and diagnostics."""

from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path
from typing import Sequence

from .rendering import (
    LatexConfig,
    latex_diagnostics,
    load_project_config,
    write_project_config,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="post-visual")
    subparsers = parser.add_subparsers(dest="command", required=True)

    configure = subparsers.add_parser("configure", help="write project post_visual.toml")
    configure.add_argument("--path", type=Path, default=Path("post_visual.toml"))
    configure.add_argument("--engine", choices=("mathtext", "usetex"))
    configure.add_argument("--preamble", action="append")
    configure.add_argument("--strict", action=argparse.BooleanOptionalAction, default=None)
    configure.add_argument(
        "--allow-fallback",
        action=argparse.BooleanOptionalAction,
        default=None,
    )
    configure.add_argument("--mathtext-fontset")

    doctor = subparsers.add_parser("doctor", help="diagnose rendering dependencies")
    doctor.add_argument("--latex", action="store_true", required=True)
    doctor.add_argument("--config", type=Path)
    doctor.add_argument("--output-dir", type=Path, default=Path("artifacts/latex-doctor"))
    return parser


def _configure(args: argparse.Namespace) -> int:
    base = load_project_config(args.path) if args.path.is_file() else LatexConfig()
    updates = {
        "engine": args.engine,
        "preamble": tuple(args.preamble) if args.preamble is not None else None,
        "strict": args.strict,
        "allow_fallback": args.allow_fallback,
        "mathtext_fontset": args.mathtext_fontset,
    }
    config = replace(base, **{key: value for key, value in updates.items() if value is not None})
    output = write_project_config(config, args.path)
    print(f"configuration_written={output.resolve()}")
    return 0


def _doctor(args: argparse.Namespace) -> int:
    config = load_project_config(args.config)
    config = replace(config, engine="usetex", strict=True, allow_fallback=False)
    result = latex_diagnostics(config, output_dir=args.output_dir, smoke=True)
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    return 0 if result.available else 1


def main(argv: Sequence[str] | None = None) -> int:
    """Run the ``post-visual`` command-line interface."""

    args = _parser().parse_args(argv)
    if args.command == "configure":
        return _configure(args)
    if args.command == "doctor":
        return _doctor(args)
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
