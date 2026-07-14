# Fixed LaTeX Test Environment

`post_visual` uses a native user-owned TeX Live 2026 tree for external-LaTeX diagnostics,
tests, and examples. Docker is not part of this environment.

## Validated Snapshot

| Component | Fixed or observed value |
| --- | --- |
| TeX Live tree | `/home/harribelwww/tex_env/texlive/2026` |
| Stable entry point | `/home/harribelwww/tex_env/current` |
| Installer profile | `/home/harribelwww/tex_env/profiles/texlive-2026.profile` |
| Package list | `/home/harribelwww/tex_env/package-lists/texlive-2026-packages.txt` |
| Python environment | `/home/harribelwww/micromamba_base/envs/post-visual` |
| Python | 3.12.13 |
| TeX engine | pdfTeX 1.40.29, TeX Live 2026 |
| `dvipng` | 1.18 |
| Matplotlib | 3.11.0 |
| NumPy / SciPy / pandas | 2.5.1 / 1.18.0 / 3.0.3 |
| pytest / Ruff | 9.1.1 / 0.15.21 |

Snapshot SHA256 values recorded after setup:

```text
383230f26ccdf856c63e0ce42688b8c90f6410fbdf0f3d8695e96c4292a7fee1  texlive-2026.profile
00938c2aaa0a05a82526dd194f29ae1c2c763e0b5682b78fb40304dc0114abf6  texlive-2026-packages.txt
```

The initial user-level installation omits TeX documentation and source files. Matplotlib
support was completed with `dvipng`, `cm-super`, and `type1cm`; `underscore` was already
present. Ghostscript 10.07.1 comes from the `post-visual` micromamba environment.

## Routine Verification

Run from the workspace root:

```bash
scripts/test-latex-wsl.sh
```

The script:

1. Prepends `$HOME/tex_env/current/bin/x86_64-linux` for the command.
2. Reports Python, LaTeX, and `dvipng` versions.
3. Runs `post-visual doctor --latex` and real PNG/PDF smoke renders.
4. Runs the two external-LaTeX integration tests.
5. Generates 13 non-empty strict-`usetex` module PNGs.

## Verified Coverage

| Layer | Modules | Output directory |
| --- | --- | --- |
| `plots/` | `annotations`, `bars`, `distributions`, `image`, `intervals`, `line`, `matrix`, `scatter` | `examples/out/usetex/plots_*.png` |
| `recipes/` | `comparison`, `interpretation`, `metrics`, `signal`, `training` | `examples/out/usetex/recipes_*.png` |

Infrastructure modules under `style/`, `core/`, and `rendering/` are exercised through
all 13 figures. Every gallery figure enters strict `usetex` mode with fallback disabled.

## Maintenance

Do not update TeX packages during routine verification. Before an intentional update,
run `tlmgr update --list`, review the change set, update explicitly, regenerate the
package list, and rerun the complete ordinary and LaTeX verification paths.
