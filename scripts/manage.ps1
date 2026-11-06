# Forward arguments unchanged to the portable installer.
$manager = Join-Path $PSScriptRoot 'manage.py'
if ($env:AAES_PYTHON) {
    & $env:AAES_PYTHON $manager @args
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $manager @args
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python $manager @args
} else {
    Write-Error 'Install Python 3.12+ or set AAES_PYTHON to its executable.'
    exit 2
}
exit $LASTEXITCODE
