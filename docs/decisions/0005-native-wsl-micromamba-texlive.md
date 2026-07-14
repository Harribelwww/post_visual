# Decision 0005: Native WSL With micromamba And TeX Live

Date: 2026-07-14

Status: accepted; supersedes Decision 0004.

## Decision

`post_visual` uses a native WSL2 runtime. micromamba manages a dedicated Python 3.12
environment named `post-visual` under `/home/harribelwww/micromamba_base`. A user-owned
TeX Live 2026 installation under `/home/harribelwww/tex_env` provides optional external
LaTeX rendering. Docker is not part of development, verification, or figure generation.

The micromamba base prefix remains free of project dependencies so it can manage isolated
environments for other repositories. `environment.yml` expresses direct dependencies and
`conda-lock.yml` records the exact linux-64 resolution. Scientific dependencies come from
conda-forge with strict channel priority; the repository is installed editable after the
environment is created.

TeX Live remains outside the micromamba prefix. Versioned TeX trees are reached through
`/home/harribelwww/tex_env/current`, and package/profile snapshots are recorded under
`/home/harribelwww/tex_env/profiles` and `package-lists`.

## Rationale

- WSL is now the permanent Linux development environment.
- Native environments improve interactive development and editor integration.
- micromamba provides repository-level isolation without a populated base environment.
- A versioned user-owned TeX Live tree avoids system-wide TeX installation and supports
  explicit package management through `tlmgr`.
- Separating Python and TeX ownership keeps their update cycles clear while verification
  scripts assemble the required `PATH` deterministically.

## Verification Contract

| Path | Required coverage |
| --- | --- |
| `scripts/test-wsl.sh` | Ruff, compileall, ordinary pytest suite, MathText, PNG, vector/hybrid PDF, and all ordinary examples |
| `scripts/test-latex-wsl.sh` | `latex`/`dvipng` discovery, real PNG/PDF doctor renders, 2 integration tests, and 13 strict-`usetex` module figures |

## Consequences

- `/usr/bin/python3`, Windows Python, Windows Conda, and Windows LaTeX are unsupported.
- Every repository receives its own micromamba environment.
- Routine tests do not update conda or TeX packages implicitly.
- Dependency or TeX updates require lock/package-list refresh and full verification.
- Decision 0004 and its historical digests remain as provenance only.
