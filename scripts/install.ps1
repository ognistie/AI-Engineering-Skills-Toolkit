[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateSet('codex', 'claude')]
    [string]$Target,
    [string]$Skill = 'all',
    [string]$InstallPath
)

$ErrorActionPreference = 'Stop'
$installArgs = @('install', '--target', $Target)
if ($Skill -ne 'all') { $installArgs += @('--skill', $Skill) }
if ($InstallPath) { $installArgs += @('--destination', $InstallPath) }
& (Join-Path $PSScriptRoot 'manage.ps1') @installArgs
exit $LASTEXITCODE
