# Task Capsule: post_visual toolkit

## Goal

Maintain `post_visual` as a Matplotlib-first, primitive-first visualization toolkit with
a completed general core, thin research recipes, and a reproducible native WSL runtime.

## Done When

- Reusable drawing behavior lives in `plots/` or `core/`; recipes remain thin.
- High-level plotting functions accept `ax` and return `(fig, ax)`.
- Native WSL ordinary and external-LaTeX verification pass.
- Durable docs and continuity files are current.

## Relevant Files

- `src/post_visual/`
- `tests/`
- `examples/`
- `environment.yml`
- `conda-lock.yml`
- `scripts/bootstrap-wsl.sh`
- `scripts/test-wsl.sh`
- `scripts/test-latex-wsl.sh`
- `post_visual.toml`
- `docs/setup/wsl-native-runtime.md`
- `.codex/HANDOFF.md`

## Decisions Already Made

- Package name: `post_visual`; recommended alias: `pv`.
- The general plotting core is complete and primitive-first.
- Core dependencies remain lightweight; domain dependencies remain optional.
- PNG and PDF are supported; PGF is excluded.
- MathText is the default; external `usetex` is explicit and strict by default.
- The supported runtime is native WSL with micromamba Python 3.12 and user-owned TeX Live 2026.
- Every repository uses a separate micromamba environment; base stays free of project dependencies.
- Docker is superseded and has no active project entry point.

## Known Dead Ends

- Windows Python/Matplotlib environments are unsupported.
- Mixing Windows executables or caches into WSL verification is unsupported.
- Implicit dependency or TeX package updates are incompatible with the reproducibility policy.

## Phase Plan

1. Done: core style, primitives, recipes, composition helpers, rendering, and export.
2. Done: vector/hybrid PDF and strict external-LaTeX diagnostics/gallery coverage.
3. Done: migrate to native WSL with isolated micromamba and TeX Live prefixes.
4. Deferred until requested: signal traces, spectrograms, attention maps, activations, kernels, swarm collision layout, and broken axes.

## Current Verification Baseline

- Python 3.12.13, Matplotlib 3.11.0, NumPy 2.5.1, SciPy 1.18.0.
- Ruff and compileall pass.
- 80 ordinary tests pass; 2 external-LaTeX tests skip in the ordinary path.
- 2 real external-LaTeX tests pass.
- 32 ordinary artifacts and 13 strict-`usetex` gallery images generate successfully.
- Representative LaTeX figures passed visual inspection.

## Next Step

Publish the complete dirty worktree after reviewing the final diff, then resume feature
work only on explicit request.
