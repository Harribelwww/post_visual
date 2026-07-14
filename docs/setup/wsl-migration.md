# WSL Migration Record

Status: completed on 2026-07-14; verified, published, and formally closed on 2026-07-15.

`post_visual` now lives at `/home/harribelwww/workspace/post_visual` in the WSL Linux
filesystem. The supported runtime is native WSL: micromamba manages the project Python
environment and a user-level TeX Live 2026 tree provides external LaTeX. Docker is no
longer part of the project workflow.

## Final Topology

- WSL2 distribution: Ubuntu 26.04
- repository: `/home/harribelwww/workspace/post_visual`
- micromamba root: `/home/harribelwww/micromamba_base`
- environment: `/home/harribelwww/micromamba_base/envs/post-visual`
- TeX Live: `/home/harribelwww/tex_env/texlive/2026`
- stable TeX path: `/home/harribelwww/tex_env/current`

See the [native WSL runtime guide](wsl-native-runtime.md) for operational commands.

## Acceptance Result

- The complete dirty worktree was preserved before environment changes.
- Git remains on `main` tracking `origin/main`.
- Repository files use the Linux filesystem and LF line endings except the existing
  MATLAB baseline working-tree conversion.
- Python 3.12.13 and the scientific stack are isolated in `post-visual`.
- TeX Live is isolated under `~/tex_env` and is not installed system-wide.
- Ruff, compileall, 80 ordinary tests, and all ordinary examples passed.
- Two real external-LaTeX tests and all 13 gallery images passed.
- Real PNG and PDF doctor renders succeeded.
- Representative LaTeX outputs passed visual inspection.
- The migration-era Windows repository copy was checksum-compared, confirmed to contain
  no newer unique code, and deleted from Windows.
- Legacy Docker and PowerShell runtime assets were removed from active repository paths;
  retained references are historical documentation only.
- The native Bash entry points are committed with executable permissions.
- The complete migration was committed, fast-forwarded into `main`, and pushed to
  `origin/main` using SSH key authentication without force-pushing.
- The local `main` worktree was clean and synchronized with `origin/main` at formal
  closure.

Decision 0005 supersedes the former Docker-only runtime decision. Historical Docker
digests and results remain in Decision 0004 for traceability, but no active setup path
depends on Docker or Windows Python.
