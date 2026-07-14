# Setup Notes

`post_visual` uses a native WSL runtime. Docker is not part of the supported workflow.

## Canonical Environment

- Workspace: `/home/harribelwww/workspace/post_visual`
- micromamba root: `/home/harribelwww/micromamba_base`
- project environment: `post-visual`
- TeX Live root: `/home/harribelwww/tex_env/texlive/2026`
- stable TeX Live entry point: `/home/harribelwww/tex_env/current`
- Python: 3.12
- package channel: conda-forge with strict channel priority

Read the [native WSL runtime guide](wsl-native-runtime.md) for bootstrap, verification,
environment locking, TeX Live maintenance, and optional extras. The
[WSL migration record](wsl-migration.md) describes the completed transition.

For interactive work, the user-level micromamba shell hook is initialized by `~/.bashrc`:

```bash
ma post-visual  # activate this repository's environment
ma              # list available environments
moff            # deactivate the current environment
```

The helpers are generic, so new repository environments do not require additional shell
functions.

## Routine Verification

From the workspace root:

```bash
scripts/bootstrap-wsl.sh
scripts/test-wsl.sh
scripts/test-latex-wsl.sh
```

The ordinary script runs Ruff, compileall, 80 ordinary tests with 2 expected
external-LaTeX skips, and all ordinary examples. The LaTeX script runs diagnostics,
real PNG/PDF smoke renders, 2 integration tests, and the 13-module strict-`usetex`
gallery.

Project defaults live in `post_visual.toml`:

```text
post-visual configure --engine mathtext
post-visual configure --engine usetex --preamble '\usepackage{amsmath}'
post-visual doctor --latex --output-dir artifacts/latex-doctor
```

Configuration precedence is function arguments, active `latex_context`, the nearest
project `post_visual.toml`, then package defaults. Requested `usetex` never silently
falls back unless fallback is explicitly enabled.

## Optional Extras

Install optional domain packages only when needed and keep them out of the core
environment declaration:

```bash
micromamba run -n post-visual python -m pip install -e ".[signal]"
micromamba run -n post-visual python -m pip install -e ".[image]"
micromamba run -n post-visual python -m pip install -e ".[explain]"
micromamba run -n post-visual python -m pip install -e ".[embedding]"
```

After an intentional dependency change, update `environment.yml`, regenerate
`conda-lock.yml`, and rerun both verification scripts.
