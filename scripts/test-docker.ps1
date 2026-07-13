param(
    [string]$PythonImage = "python:3.12-slim"
)

$ErrorActionPreference = "Stop"

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$testCommand = "python -m pip install --upgrade pip && python -m pip install -e '.[dev]' && python -m pytest -p no:cacheprovider && python examples/line_mvp.py && python examples/primitives_mvp.py && python examples/second_batch_mvp.py && python examples/recipes_mvp.py && python examples/comparison_recipes.py && python examples/interpretation_recipes.py && python examples/signal_recipes.py && python examples/annotation_mvp.py && python examples/layout_image_mvp.py && python examples/annotation_point_mvp.py && python examples/distribution_enhancements.py && python examples/line_scatter_enhancements.py && python examples/axes_helpers_mvp.py"

docker pull $PythonImage
if ($LASTEXITCODE -ne 0) {
    throw "docker pull failed with exit code $LASTEXITCODE. Is Docker Desktop running?"
}

docker run --rm `
    -v "${repo}:/workspace" `
    -w /workspace `
    -e MPLBACKEND=Agg `
    -e PIP_ROOT_USER_ACTION=ignore `
    $PythonImage `
    sh -lc $testCommand

if ($LASTEXITCODE -ne 0) {
    throw "docker verification failed with exit code $LASTEXITCODE."
}
