# Workspace Overview

## Purpose

This workspace develops `post_visual`, a Matplotlib-first visualization toolkit for
data-science research results with a consistent scientific style.

## Current State

- The general scientific plotting core, composition helpers, and thin research recipes are complete.
- The repository lives at `/home/harribelwww/workspace/post_visual` in the WSL Linux filesystem.
- The supported runtime is native WSL2 on Ubuntu 26.04; Docker is not used.
- micromamba 2.8.1 is installed under `/home/harribelwww/micromamba_base`.
- The isolated `post-visual` environment uses Python 3.12.13 and is locked by `conda-lock.yml`.
- TeX Live 2026 lives under `/home/harribelwww/tex_env/texlive/2026` and is reached through `/home/harribelwww/tex_env/current`.
- Ordinary native verification passes with 80 tests and 2 expected external-LaTeX skips.
- Real external-LaTeX verification passes with 2 tests, doctor PNG/PDF renders, and 13 gallery PNGs.
- The worktree remains intentionally dirty with the completed plotting, rendering, and runtime migration changes.

## Design Direction

Primitive-first is the governing architecture. Reusable behavior belongs in `plots/` or
`core/`; recipes normalize inputs, attach recurring semantics, and delegate rendering.
Every high-level single-axes function accepts `ax` and returns `(fig, ax)`.

MathText is the default formula engine. Optional `usetex` uses the native versioned TeX
Live tree. Supported outputs are PNG and PDF, including vector and per-artist hybrid PDF;
PGF remains excluded.

## Important Docs

- `README.md`: human landing page.
- `docs/INDEX.md`: canonical documentation index.
- `docs/architecture/toolkit-architecture.md`: implemented package architecture.
- `docs/architecture/plot-catalog.md`: supported plot types and priorities.
- `docs/setup/wsl-native-runtime.md`: environment bootstrap, locking, TeX, and verification.
- `docs/setup/wsl-migration.md`: completed migration record.
- `docs/decisions/0005-native-wsl-micromamba-texlive.md`: current runtime decision.
- `.codex/HANDOFF.md`: active working context.

## Environment Notes

- Git repository: `git@github.com:Harribelwww/post_visual.git` (`main`, SSH key authentication).
- micromamba root: `/home/harribelwww/micromamba_base`.
- project environment: `/home/harribelwww/micromamba_base/envs/post-visual`.
- interactive shell convention: `ma <environment>` activates any environment, `ma` lists
  environments, and `moff` deactivates; no project environment auto-activates.
- TeX root: `/home/harribelwww/tex_env`.
- Windows Python, Conda, Matplotlib, LaTeX, and Docker are outside the supported workflow.

## Next Implementation Direction

1. Commit or otherwise publish the complete dirty worktree now that WSL verification is restored.
2. Add domain recipes or visual-regression baselines only when requested.
3. Treat dependency and TeX updates as explicit maintenance with full re-verification.
