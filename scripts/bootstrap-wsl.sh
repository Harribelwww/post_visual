#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mamba_root="${MAMBA_ROOT_PREFIX:-${HOME}/micromamba_base}"
micromamba_bin="${MAMBA_EXE:-${mamba_root}/bin/micromamba}"
environment_name="post-visual"

if [[ ! -x "${micromamba_bin}" ]]; then
    echo "micromamba is not executable at ${micromamba_bin}" >&2
    exit 1
fi

export MAMBA_ROOT_PREFIX="${mamba_root}"

if "${micromamba_bin}" env list | awk '{print $1}' | grep -Fxq "${environment_name}"; then
    "${micromamba_bin}" install --yes --name "${environment_name}" --file "${repo_root}/environment.yml"
else
    "${micromamba_bin}" create --yes --file "${repo_root}/environment.yml"
fi

"${micromamba_bin}" run --name "${environment_name}" \
    python -m pip install --editable "${repo_root}" --no-deps

"${micromamba_bin}" run --name "${environment_name}" python --version
"${micromamba_bin}" run --name "${environment_name}" python -c \
    "import matplotlib, numpy, scipy; print(f'matplotlib={matplotlib.__version__} numpy={numpy.__version__} scipy={scipy.__version__}')"
