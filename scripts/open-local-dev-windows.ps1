param(
  [ValidateSet("local", "openai")]
  [string]$Provider = "local",
  [int]$WebPort = 3001
)

$ErrorActionPreference = "Stop"

if ($Provider -eq "openai" -and -not $env:OPENAI_API_KEY) {
  throw "OPENAI_API_KEY est requis pour le mode openai."
}

$root = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "local-dev-helpers.ps1")

$state = Read-ServiceState -Root $root

if ($state) {
  throw "Des processus Cadris sont deja actifs. Arrete d'abord avec .\\scripts\\stop-local.cmd avant d'ouvrir le mode debug."
}

$existingProcesses = Get-CadrisProcessRecords -Root $root
$webListeners = Get-CadrisWebListeners -Root $root

if ($existingProcesses.Count -gt 0 -or $webListeners.Count -gt 0) {
  throw "Des processus Cadris sont deja actifs. Arrete d'abord avec .\\scripts\\stop-local.cmd avant d'ouvrir le mode debug."
}

$resolvedWebPort = Get-FreeWebPort -PreferredPort $WebPort
if ($resolvedWebPort -ne $WebPort) {
  Write-Host "Le port $WebPort est occupe. Utilisation de $resolvedWebPort pour le debug." -ForegroundColor Yellow
}

function Open-ServiceWindow([string]$Title, [string]$Command) {
  Start-Process cmd.exe -ArgumentList "/k", "title $Title && $Command"
}

$runtimeCommand = "cd /d ""$root\apps\runtime"" && set CADRIS_RUNTIME_PROVIDER=$Provider && python -m uvicorn app.main:app --port 8001"
$rendererCommand = "cd /d ""$root\apps\renderer"" && python -m uvicorn app.main:app --port 8002"
$controlCommand = "cd /d ""$root\apps\control-plane"" && set CONTROL_PLANE_ALLOWED_ORIGINS=http://127.0.0.1:$resolvedWebPort,http://localhost:$resolvedWebPort && python -m uvicorn app.main:app --port 8000"
$webCommand = "cd /d ""$root"" && set NEXT_PUBLIC_CADRIS_API_URL=http://127.0.0.1:8000 && set NEXT_PUBLIC_CADRIS_DEV_USER_ID=dev-user && call npm.cmd run dev --workspace @cadris/web -- --port $resolvedWebPort"

Open-ServiceWindow -Title "Cadris Runtime Debug" -Command $runtimeCommand
Start-Sleep -Milliseconds 300
Open-ServiceWindow -Title "Cadris Renderer Debug" -Command $rendererCommand
Start-Sleep -Milliseconds 300
Open-ServiceWindow -Title "Cadris Control Plane Debug" -Command $controlCommand
Start-Sleep -Milliseconds 300
Open-ServiceWindow -Title "Cadris Web Debug" -Command $webCommand

Write-Host "Mode debug ouvert dans 4 fenetres visibles." -ForegroundColor Green
Write-Host "URL debug : http://127.0.0.1:$resolvedWebPort/projects" -ForegroundColor Cyan
Write-Host "Ce mode n'ecrit pas l'etat canonique du mode rapide." -ForegroundColor Yellow
Start-Process "http://127.0.0.1:$resolvedWebPort/projects"
