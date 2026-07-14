# Working Context

Last updated: 2026-07-15
Status: standby

## Current Goal

No migration or publication task is active. Maintain `post_visual` from the synchronized
native WSL `main` branch and activate new context only for explicitly requested work.

## Scope

- Primary workspace: `/home/harribelwww/workspace/post_visual`
- micromamba root: `/home/harribelwww/micromamba_base`
- project environment: `/home/harribelwww/micromamba_base/envs/post-visual`
- TeX root: `/home/harribelwww/tex_env`

## Current State

- The plotting core, thin recipes, rendering diagnostics, and PNG/vector/hybrid PDF
  export implementation are complete.
- Native WSL2 on Ubuntu 26.04 is the only supported runtime.
- micromamba manages the isolated Python 3.12 environment; TeX Live 2026 remains in the
  independent user-owned `~/tex_env` prefix.
- `environment.yml` records direct dependencies and `conda-lock.yml` locks linux-64.
- Active bootstrap and verification entry points are Bash scripts with executable Git
  modes.
- The migration-era Windows repository copy and active Docker/PowerShell assets were
  removed. Historical decision and handoff text remains provenance only.
- The completed migration and implementation are on `main`, which tracks
  `origin/main` through SSH key authentication.
- The worktree was clean and local/remote divergence was `0 / 0` at formal closure.

## Required Reading

- `AGENTS.md`
- `.codex/WORKSPACE.md`
- `docs/INDEX.md`
- `docs/setup/wsl-native-runtime.md`
- `docs/setup/wsl-migration.md`
- `docs/decisions/0005-native-wsl-micromamba-texlive.md`

## Verification State

- Passed: Ruff, compileall, 80 ordinary tests, and 2 expected external-LaTeX skips.
- Passed: all ordinary examples and 32 generated artifacts.
- Passed: real LaTeX doctor PNG/PDF, 2 integration tests, and 13 strict-`usetex`
  gallery images.
- Passed: representative visual inspection.
- Passed: documentation paths, 67 local links, continuity audit, route-sync audit,
  workspace-doc audit, and standard-doc audit.
- Passed: repository and migration garbage cleanup; generated verification artifacts
  were removed before publication.

## Risks / Maintenance Rules

- Dependency and TeX updates must be explicit and followed by full verification.
- Keep project dependencies out of the micromamba base prefix.
- Keep generated figures, caches, and editable-install metadata out of Git.
- Do not restore Windows, Docker, or PowerShell runtime entry points.

## Next Entry Point

1. Run `git status --short --branch` and confirm the current branch before editing.
2. Use `docs/INDEX.md` to load only task-relevant durable documentation.
3. Set this handoff to `active` only when work becomes incomplete or cross-session.
4. Create or reactivate a task capsule only for genuinely multi-session work.
