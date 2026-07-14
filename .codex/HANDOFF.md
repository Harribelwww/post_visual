# Working Context

Last updated: 2026-07-15
Status: active

## Current Goal

Publish the complete native WSL runtime and visualization-toolkit worktree to GitHub over
the configured SSH remote.

## Scope

- Primary workspace: `/home/harribelwww/workspace/post_visual`
- micromamba prefix: `/home/harribelwww/micromamba_base`
- TeX prefix: `/home/harribelwww/tex_env`
- External user configuration touched: `/home/harribelwww/.bashrc`
- Editable area: current workspace, the two user-owned runtime prefixes, and the user shell
  configuration when explicitly requested

## Current State

- The plotting, recipe, rendering, and export implementation is complete.
- The repository now uses native WSL2 on Ubuntu 26.04; Docker has no active role.
- micromamba 2.8.1 manages the isolated `post-visual` Python 3.12 environment.
- `environment.yml` records direct dependencies and `conda-lock.yml` locks linux-64 packages.
- TeX Live 2026 is installed at `~/tex_env/texlive/2026`; `~/tex_env/current` is the stable entry point.
- TeX installer profile and package list are saved under `~/tex_env/profiles` and `~/tex_env/package-lists`.
- Decision 0005 supersedes the historical Docker-only Decision 0004.
- Former container and Windows orchestration assets were removed from active project paths.
- Active setup and validation workflows are Bash-only.
- `~/.bashrc` initializes the fixed micromamba root and exposes only generic `ma`/`moff`
  helpers; `ma post-visual` activates this environment without repository-specific
  auto-activation or a dedicated environment-name command.
- The final cleanup removed the legacy platform-specific development script, generated caches,
  generated figures, installer downloads/extraction trees, temporary migration archives,
  and micromamba tarball/index caches.
- The migration-era Windows project copy under
  `C:\Users\HARRIBELWWW\Desktop\tmp\post_visual` was checksum-compared against the WSL
  workspace, confirmed to contain no unique newer code, and has now been completely deleted
  from Windows.
- Git `origin` is `git@github.com:Harribelwww/post_visual.git`; local `main` tracks
  `origin/main`, and fetch plus push dry-run succeed through the SSH key.
- The worktree remains intentionally dirty with pre-existing completed implementation plus this runtime migration.

## Required Reading

- `AGENTS.md`
- `.codex/WORKSPACE.md`
- `docs/INDEX.md`
- `.codex/tasks/post-visual-toolkit.md`
- `docs/setup/wsl-native-runtime.md`
- `docs/decisions/0005-native-wsl-micromamba-texlive.md`

## Runtime Files Added Or Changed

- `environment.yml`: readable micromamba dependency policy.
- `conda-lock.yml`: exact linux-64 dependency lock.
- `scripts/bootstrap-wsl.sh`: create/update the isolated environment and editable install.
- `scripts/test-wsl.sh`: Ruff, compileall, ordinary tests, and examples.
- `scripts/test-latex-wsl.sh`: native TeX doctor, tests, and gallery.
- `tests/test_rendering_latex.py`: runtime-neutral external-LaTeX skip reason.
- `docs/setup/wsl-native-runtime.md`: canonical native environment guide.
- `docs/setup/wsl-migration.md`: completed migration acceptance record.
- `docs/setup/latex-test-environment.md`: native TeX snapshot.
- `docs/decisions/0005-native-wsl-micromamba-texlive.md`: accepted runtime decision.
- `README.md`, `docs/INDEX.md`, setup/architecture/decision indexes: native WSL routes.
- `.codex/WORKSPACE.md`, `.codex/tasks/post-visual-toolkit.md`, `.codex/manifest.yaml`, `.codex/ROUTING.md`: synchronized continuation facts.
- `.codex/workflows/validate-doc-paths.sh`: native documentation-path validation.

## Removed Legacy Runtime Assets

Legacy orchestration scripts, container build/test assets, the temporary container
guide, and the former documentation-path workflow were removed. Decision 0004
remains for historical provenance and is not an active route.

## Commands Run

- Pre-migration worktree snapshot: created, verified, and removed after the native migration was accepted.
- micromamba 2.8.1 installed and configured for conda-forge with strict priority.
- `scripts/bootstrap-wsl.sh`: created Python 3.12.13 environment and editable install.
- conda-lock with explicit micromamba solver: generated `conda-lock.yml`.
- Native TeX Live 2026 installer: installed user-owned tree under `~/tex_env`.
- `tlmgr install dvipng cm-super type1cm`: completed.
- `scripts/test-wsl.sh`: passed.
- `scripts/test-latex-wsl.sh`: passed.
- Representative annotations, matrix, model-comparison, and doctor PNGs visually inspected: passed.
- `micromamba clean --all --yes`: removed downloadable package archives and index caches.
- Post-cleanup smoke check: Python imports, pdfTeX, and `dvipng` remain available.
- Doc Maintainer continuity and workspace-doc audits: no missing roles, stale manifest paths,
  route drift, or broken local links.
- `~/.bashrc`: added generic `ma`/`moff` helpers, removed the temporary `post-visual`
  dedicated helper, and passed Bash syntax plus activation checks.
- Windows migration-copy audit: confirmed no WSL-missing code, removed the old repository
  copy and legacy runtime assets, and later confirmed the Windows path no longer exists.
- GitHub SSH audit: `git ls-remote` and `git push --dry-run origin main` succeeded; no HTTPS
  or GitHub CLI authentication is required for the selected publish path.
- 2026-07-15 pre-publish verification: `scripts/test-wsl.sh` and
  `scripts/test-latex-wsl.sh` both passed again; 45 example/gallery images and 2 doctor
  artifacts were counted and then removed with all generated caches before staging.

## Environment Snapshot

The durable TeX snapshot is:

```text
383230f26ccdf856c63e0ce42688b8c90f6410fbdf0f3d8695e96c4292a7fee1  texlive-2026.profile
00938c2aaa0a05a82526dd194f29ae1c2c763e0b5682b78fb40304dc0114abf6  texlive-2026-packages.txt
```

## Verification State

- Passed: Ruff and compileall.
- Passed: 80 ordinary tests; 2 expected external-LaTeX skips.
- Passed: all ordinary examples and 32 generated artifacts.
- Passed: real LaTeX doctor PNG/PDF.
- Passed: 2 external-LaTeX integration tests.
- Passed: all 13 strict-`usetex` gallery images.
- Passed: representative visual inspection.
- Passed: documentation path check, 67 local-link checks, continuity audit, route-sync audit, workspace-doc audit, and standard-doc audit.
- Passed: `sci_plot.m` was confirmed to differ only by CRLF, then normalized to LF without changing MATLAB code.
- Passed: migration download archives, extraction trees, and generated repository
  caches/artifacts were removed; micromamba download/index caches were cleaned and its
  extracted shared package store remains managed runtime state.
- Passed: no active platform-specific orchestration file or path, editable-install
  metadata, Python bytecode cache, pytest cache, or Ruff cache remains.
- Passed: `~/.bashrc` syntax; `ma post-visual` activated the expected environment.

## Risks / Open Questions

- The complete implementation and migration are still uncommitted.
- TeX and conda updates must remain explicit; routine tests must not update either environment.
- Generated test/example artifacts are intentionally ignored and removed after verification.
- micromamba's extracted shared package store remains because it backs the installed
  environment and future environment reuse; it is managed state, not installation trash.

## Next Steps

1. Commit and push the complete worktree on `agent/wsl-native-migration` through SSH.
2. Review and merge the published branch into `main` when ready.
3. Resume feature work only after the migration changes are safely integrated.
