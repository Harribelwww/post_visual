# Native WSL Runtime

## Supported Topology

`post_visual` runs natively in WSL2 on Ubuntu 26.04. Docker, Windows Python, Windows
Conda, and Windows LaTeX are not supported runtime paths.

The environment is split into two independent user-owned prefixes:

```text
/home/harribelwww/micromamba_base
  bin/micromamba
  envs/post-visual
  pkgs

/home/harribelwww/tex_env
  texlive/2026
  current -> texlive/2026
  profiles/texlive-2026.profile
  package-lists/texlive-2026-packages.txt
  user/2026
```

micromamba manages Python and compiled scientific dependencies. TeX Live is an external
rendering toolchain shared at the user level but reached through the stable `current`
path. Each future repository must use its own micromamba environment.

## micromamba

The micromamba shell hook sets:

```bash
export MAMBA_EXE="$HOME/micromamba_base/bin/micromamba"
export MAMBA_ROOT_PREFIX="$HOME/micromamba_base"
```

The root configuration uses only conda-forge with strict channel priority. Do not install
project dependencies into the base prefix and do not auto-activate `post-visual` from
shell startup files.

The user shell initializes the micromamba hook from `~/.bashrc` and provides generic
environment helpers instead of repository-specific auto-activation:

```bash
ma                 # list environments
ma post-visual     # activate this repository's environment
moff               # deactivate the current environment
```

`ma <environment>` works for future repository environments without adding another
shortcut. After changing the shell configuration, load it into the current terminal with
`source ~/.bashrc`; new Bash terminals load it automatically. Do not add functions named
after individual environments unless there is a specific long-term need.

Create or synchronize the repository environment with:

```bash
scripts/bootstrap-wsl.sh
```

The script consumes `environment.yml`, creates or updates the named `post-visual`
environment, and installs this repository in editable mode without asking pip to replace
the conda-managed scientific stack.

`environment.yml` is the readable dependency policy. `conda-lock.yml` fixes the resolved
linux-64 packages, builds, URLs, and checksums. Regenerate the lock only after an
intentional environment change:

```bash
micromamba run -n post-visual conda-lock lock \
  --file environment.yml \
  --platform linux-64 \
  --lockfile conda-lock.yml \
  --micromamba \
  --conda "$HOME/micromamba_base/bin/micromamba" \
  --without-cuda
```

## TeX Live

The native TeX Live 2026 installation lives at `$HOME/tex_env/texlive/2026`. The stable
`$HOME/tex_env/current` symlink lets scripts remain unchanged when a future yearly tree
is installed. TeX Live is not installed into the micromamba environment.

The initial installation omits documentation and source trees. Matplotlib's external
LaTeX path additionally requires `dvipng`, `cm-super`, `type1cm`, and `underscore`;
Ghostscript is supplied by the `post-visual` micromamba environment.

The recorded environment surfaces are:

```text
$HOME/tex_env/profiles/texlive-2026.profile
$HOME/tex_env/package-lists/texlive-2026-packages.txt
```

Do not run an unreviewed `tlmgr update --all` as part of routine tests. Inspect updates,
apply them intentionally, refresh the package list, and rerun the full LaTeX verification.

## Verification

Ordinary verification:

```bash
scripts/test-wsl.sh
```

External-LaTeX verification:

```bash
scripts/test-latex-wsl.sh
```

The LaTeX script prepends `$HOME/tex_env/current/bin/x86_64-linux` only for that command,
sets the headless Agg backend, runs `post-visual doctor --latex`, executes the dedicated
integration tests, and generates all 13 module-gallery PNGs.

The migration baseline verified on 2026-07-14 is:

- Python 3.12.13
- Matplotlib 3.11.0
- NumPy 2.5.1
- SciPy 1.18.0
- pandas 3.0.3
- pdfTeX 1.40.29 from TeX Live 2026
- dvipng 1.18
- 80 ordinary tests passed and 2 external-LaTeX tests skipped
- 2 external-LaTeX integration tests passed
- 32 ordinary artifacts and 13 strict-`usetex` gallery PNGs generated

## Troubleshooting

- If micromamba cannot write its process lock, run commands in the normal WSL user
  session and confirm that `$HOME/.cache/mamba` is user-writable.
- If `latex` or `dvipng` is missing, confirm that
  `$HOME/tex_env/current/bin/x86_64-linux` exists and points to the current TeX tree.
- If LaTeX formats or fonts change, clear Matplotlib's TeX cache and rerun
  `post-visual doctor --latex` before changing package code.
- Do not use `/usr/bin/python3` for project verification.
