#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mamba_root="${MAMBA_ROOT_PREFIX:-${HOME}/micromamba_base}"
micromamba_bin="${MAMBA_EXE:-${mamba_root}/bin/micromamba}"
environment_name="post-visual"
texlive_root="${POST_VISUAL_TEXLIVE_ROOT:-${HOME}/tex_env/current}"
texlive_bin="${texlive_root}/bin/x86_64-linux"

if [[ ! -x "${texlive_bin}/latex" ]]; then
    echo "TeX Live latex is not executable at ${texlive_bin}/latex" >&2
    exit 1
fi

export MAMBA_ROOT_PREFIX="${mamba_root}"
export PATH="${texlive_bin}:${PATH}"
export MPLBACKEND=Agg

run() {
    "${micromamba_bin}" run --name "${environment_name}" "$@"
}

cd "${repo_root}"
run python --version
latex --version | sed -n '1,2p'
dvipng --version | sed -n '1,2p'
run post-visual doctor --latex --output-dir artifacts/latex-doctor
POST_VISUAL_LATEX_INTEGRATION=1 run \
    python -m pytest -p no:cacheprovider tests/test_rendering_latex.py
run python examples/usetex_module_gallery.py
