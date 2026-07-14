# Decision 0004: Docker-Only Runtime And TeX Live Integration

Date: 2026-07-13

Status: superseded by Decision 0005 on 2026-07-14.

## Transition Note

On 2026-07-14, the project completed its migration to a native WSL runtime using
micromamba and a user-owned TeX Live installation. Decision 0005 supersedes this
decision. The Docker contract below is retained only as historical provenance; no
active setup or verification path uses it. See the
[native WSL decision](0005-native-wsl-micromamba-texlive.md).

## Decision

`post_visual` development checks, tests, diagnostics, and figure generation run in
Docker. The Windows host is only responsible for Docker orchestration, source/data
mounts, and receiving generated artifacts. A host Python, Matplotlib, Conda, or LaTeX
installation is not required and is not part of the supported verification path.

The ordinary verification container remains based on `python:3.12-slim` and stays
TeX-free. External LaTeX integration uses
`texlive/texlive:latest@sha256:d39efa547acfa518072600315280f92357ca8e0b9e295e09b6ccd5f5d82a1373`.
A multi-stage build copies TeX Live 2026 into `python:3.12-slim`, so Python, Matplotlib,
the package, and TeX executables run inside the same container. The integration script
prints the requested reference and resolved repository digest before verification.

The resulting `post-visual-latex:texlive-2026` image is the canonical routine test
environment. The integration script reuses it by default and rebuilds only when the
image is missing or `-Rebuild` is passed. The Python base is also digest-pinned. The
upstream TeX Live image is therefore a rebuild input, not a runtime prerequisite.

## Rationale

- The previous Windows Matplotlib environments were unreliable and could fail through
  interpreter, DLL, native-library, or path mismatches.
- Linux containers cannot reliably execute or reuse Windows Python or TeX binaries.
- Matplotlib `usetex` requires its TeX executables and Python process to share the same
  container filesystem and environment.
- Keeping TeX Live out of the ordinary test image preserves a fast default verification
  loop while retaining a reproducible external-LaTeX integration path.

## Verification Matrix

| Path | Container contents | Required coverage |
| --- | --- | --- |
| `scripts/test-docker.ps1` | Python 3.12, Matplotlib, project dev dependencies; no TeX Live | Ruff/tests/examples, MathText, PNG, vector PDF, hybrid PDF |
| `scripts/test-latex-docker.ps1` | Canonical `post-visual-latex:texlive-2026` image built from pinned TeX Live 2026 and Python bases | `latex`/`dvipng` discovery, `usetex`, real PNG/PDF smoke renders, actionable failure diagnostics, and 13 module-level example PNGs |

## Consequences

- Documentation and automation must not instruct users to create or activate a local
  Python environment for project verification.
- Host Python, Conda, Matplotlib, TeX executables, fonts, caches, and installation
  directories must not be mounted into verification containers.
- Generated figures and reports are written into mounted workspace output directories.
- `post-visual configure` and `post-visual doctor --latex` are invoked inside the TeX Live
  container for supported integration verification.
- Project configuration should live in the mounted workspace. Host user-level Python or
  Matplotlib configuration is not part of the reproducible configuration chain.
- Environment snapshot versions and the current validated local image ID are maintained
  in `docs/setup/latex-test-environment.md`; an intentional rebuild requires reviewing
  and refreshing that snapshot.
