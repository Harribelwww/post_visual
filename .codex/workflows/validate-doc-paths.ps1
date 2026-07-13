$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$repo = Split-Path -Parent $root
Set-Location $repo

$paths = @(
  "AGENTS.md",
  "README.md",
  "docs/INDEX.md",
  "docs/architecture/README.md",
  "docs/architecture/toolkit-architecture.md",
  "docs/architecture/plot-catalog.md",
  "docs/setup/README.md",
  "docs/decisions/README.md",
  "docs/decisions/0001-initial-toolkit-scope.md",
  ".codex/WORKSPACE.md",
  ".codex/HANDOFF.md",
  ".codex/manifest.yaml",
  ".codex/ROUTING.md",
  ".codex/handoffs/README.md",
  ".codex/tasks/README.md",
  ".codex/workflows/continuity-maintenance.md",
  ".codex/workflows/docs-hygiene.md",
  ".codex/workflows/session-closure.md",
  ".codex/workflows/route-sync.md",
  ".codex/workflows/validate-doc-paths.ps1",
  "sci_plot.m"
)

$missing = @()
foreach ($path in $paths) {
  if (-not (Test-Path -LiteralPath $path)) {
    $missing += $path
  }
}

if ($missing.Count -gt 0) {
  Write-Error ("Missing documentation paths:`n" + ($missing -join "`n"))
}

Write-Output "documentation_paths_ok=true"
