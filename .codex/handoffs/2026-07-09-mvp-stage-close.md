# Handoff: MVP stage close

Date: 2026-07-09
Source session: Codex desktop

## Goal

Close the first implementation stage for `post_visual` and leave a clean resume point.

## Done

- Created the Python package MVP under `src/post_visual/`.
- Implemented style primitives, rcParams, scoped style contexts, axes/figure helpers, and export helper.
- Implemented `pv.line`, `pv.scatter`, `pv.grouped_bar`, and `pv.bar`.
- Added tests for style, line, scatter, and grouped-bar behavior.
- Added MVP examples: `examples/line_mvp.py` and `examples/primitives_mvp.py`.
- Established Docker-first build-stage verification through `scripts/test-docker.ps1`.
- Updated README, setup docs, documentation index, architecture docs, plot catalog, workspace overview, and active handoff.

## In Progress

- No code implementation is currently in progress.
- Next planned implementation area is distributions and heatmaps.

## Git State

- `git status --short --branch` fails because the workspace is not recognized as a valid git repository.
- There is an empty or incomplete `.git` directory; do not rely on Git state until it is repaired or initialized.

## Changed Files

- `pyproject.toml`
- `.gitignore`
- `.dockerignore`
- `src/post_visual/**`
- `tests/**`
- `examples/line_mvp.py`
- `examples/primitives_mvp.py`
- `scripts/setup-dev.ps1`
- `scripts/test-docker.ps1`
- `README.md`
- `docs/INDEX.md`
- `docs/architecture/toolkit-architecture.md`
- `docs/architecture/plot-catalog.md`
- `docs/setup/README.md`
- `.codex/WORKSPACE.md`
- `.codex/HANDOFF.md`
- `.codex/tasks/post-visual-toolkit.md`

## Decisions

- Build-stage validation uses Docker by default.
- Standard local Python setup is retained for interactive use through `scripts/setup-dev.ps1`, but it is not the default verification path.
- High-level plotting functions continue to accept `ax` and return `(fig, ax)`.
- Domain-specific dependencies remain optional.

## Blockers

- None for the next implementation stage.
- Git metadata is invalid, so repository status cannot be used until fixed.

## Verification

- Docker verification passed with `python:3.12-slim`: `10 passed`.
- MVP examples generated: `line_mvp.png`, `scatter_mvp.png`, and `grouped_bar_mvp.png`.
- Documentation path validation passed with `documentation_paths_ok=true`.
- PowerShell script parsing passed for setup and Docker test scripts.

## Next Entry Point

1. Read `.codex/WORKSPACE.md`, `.codex/HANDOFF.md`, and `docs/INDEX.md`.
2. Review `docs/architecture/toolkit-architecture.md` and `docs/architecture/plot-catalog.md`.
3. Implement distributions and heatmaps.
4. Verify with `powershell -ExecutionPolicy Bypass -File scripts/test-docker.ps1`.

