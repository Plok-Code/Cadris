$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "local-dev-helpers.ps1")

$stoppedProcesses = Stop-CadrisProcesses -Root $root

if (-not $stoppedProcesses -or $stoppedProcesses.Count -eq 0) {
  Write-Host "Aucun processus Cadris local a arreter." -ForegroundColor Yellow
  exit 0
}

Write-Host "Arret termine : $($stoppedProcesses.Count) processus Cadris fermes." -ForegroundColor Green
