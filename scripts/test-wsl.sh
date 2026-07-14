#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mamba_root="${MAMBA_ROOT_PREFIX:-${HOME}/micromamba_base}"
micromamba_bin="${MAMBA_EXE:-${mamba_root}/bin/micromamba}"
environment_name="post-visual"

export MAMBA_ROOT_PREFIX="${mamba_root}"
export MPLBACKEND=Agg

run() {
    "${micromamba_bin}" run --name "${environment_name}" "$@"
}

cd "${repo_root}"
run python -m ruff check src tests examples
run python -m compileall -q src tests examples
run python -m pytest -p no:cacheprovider

examples=(
    line_mvp.py
    primitives_mvp.py
    second_batch_mvp.py
    recipes_mvp.py
    comparison_recipes.py
    interpretation_recipes.py
    signal_recipes.py
    annotation_mvp.py
    layout_image_mvp.py
    annotation_point_mvp.py
    distribution_enhancements.py
    line_scatter_enhancements.py
    axes_helpers_mvp.py
    rendering_smoke.py
)

for example in "${examples[@]}"; do
    run python "examples/${example}"
done
