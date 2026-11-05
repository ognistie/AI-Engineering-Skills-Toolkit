# Forward arguments unchanged to the portable installer.
$aaesPython = if ($env:AAES_PYTHON) { $env:AAES_PYTHON } else { 'python' }
& $aaesPython (Join-Path $PSScriptRoot 'manage.py') @args
exit $LASTEXITCODE
