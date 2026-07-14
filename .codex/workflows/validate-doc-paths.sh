#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${repo_root}"

paths=(
    AGENTS.md
    README.md
    environment.yml
    conda-lock.yml
    docs/INDEX.md
    docs/architecture/README.md
    docs/architecture/toolkit-architecture.md
    docs/architecture/plot-catalog.md
    docs/setup/README.md
    docs/setup/wsl-native-runtime.md
    docs/setup/wsl-migration.md
    docs/setup/latex-test-environment.md
    docs/decisions/README.md
    docs/decisions/0001-initial-toolkit-scope.md
    docs/decisions/0002-primitives-before-recipes.md
    docs/decisions/0003-general-core-closure.md
    docs/decisions/0004-docker-only-runtime-and-texlive.md
    docs/decisions/0005-native-wsl-micromamba-texlive.md
    .codex/WORKSPACE.md
    .codex/HANDOFF.md
    .codex/manifest.yaml
    .codex/ROUTING.md
    .codex/handoffs/README.md
    .codex/tasks/README.md
    .codex/workflows/continuity-maintenance.md
    .codex/workflows/docs-hygiene.md
    .codex/workflows/session-closure.md
    .codex/workflows/route-sync.md
    .codex/workflows/validate-doc-paths.sh
    scripts/bootstrap-wsl.sh
    scripts/test-wsl.sh
    scripts/test-latex-wsl.sh
    sci_plot.m
)

missing=()
for path in "${paths[@]}"; do
    [[ -e "${path}" ]] || missing+=("${path}")
done

if (( ${#missing[@]} )); then
    printf 'Missing documentation paths:\n' >&2
    printf '%s\n' "${missing[@]}" >&2
    exit 1
fi

echo "documentation_paths_ok=true"
