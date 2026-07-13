param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $repo

try {
    & $Python -m pip install --upgrade pip
    & $Python -m pip install -e ".[dev]"
    & $Python -c "import post_visual as pv; print('post_visual_ready=true')"
}
finally {
    Pop-Location
}
