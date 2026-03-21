param(
  [ValidateSet("local", "openai")]
  [string]$Provider = "local",
  [int]$WebPort = 3001,
  [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "local-dev-helpers.ps1")

if ($Provider -eq "openai" -and -not $env:OPENAI_API_KEY) {
  throw "OPENAI_API_KEY est requis pour le mode openai."
}

function Show-CleanupSummary([object[]]$StoppedProcesses) {
  if (-not $StoppedProcesses -or $StoppedProcesses.Count -eq 0) {
    return
  }

  Write-Host "Nettoyage agressif termine : $($StoppedProcesses.Count) processus Cadris arretes." -ForegroundColor Yellow
}

function Build-WebApp() {
  Write-Host "Build web en cours..." -ForegroundColor Cyan
  cmd.exe /d /c "cd /d ""$root"" && npm.cmd run build:web"
  if ($LASTEXITCODE -ne 0) {
    throw "Le build web a echoue."
  }
}

function Assert-ServiceReady(
  [string]$Name,
  [string]$Url,
  [string]$LogPath,
  [bool]$FailOnServerError = $false
) {
  $result = Wait-ForServiceReady -Name $Name -Url $Url -TimeoutSeconds 90 -FailOnServerError:$FailOnServerError
  if ($result.ready) {
    Write-Host "${Name}: pret ($Url)" -ForegroundColor Green
    return
  }

  Write-Host ""
  Write-Host "Echec de demarrage pour $Name." -ForegroundColor Red
  Write-Host "URL testee : $Url" -ForegroundColor DarkGray
  Write-Host "Raison : $($result.message)" -ForegroundColor DarkGray
  Write-Host "Log : $LogPath" -ForegroundColor Yellow
  Write-Host "Dernieres lignes :" -ForegroundColor Yellow
  Write-Host (Get-LogTail -Path $LogPath -LineCount 40)
  throw "Le service $Name n'a pas demarre correctement."
}

Initialize-LocalState -Root $root
$stoppedProcesses = Stop-CadrisProcesses -Root $root
Show-CleanupSummary -StoppedProcesses $stoppedProcesses

$resolvedWebPort = Get-FreeWebPort -PreferredPort $WebPort
Save-LocalWebPort -Root $root -Port $resolvedWebPort

if ($resolvedWebPort -ne $WebPort) {
  Write-Host "Le port $WebPort est occupe. Utilisation de $resolvedWebPort pour le web." -ForegroundColor Yellow
}

Build-WebApp

$runtimeUrl = "http://127.0.0.1:8001/health"
$rendererUrl = "http://127.0.0.1:8002/health"
$controlUrl = "http://127.0.0.1:8000/health"
$webUrl = "http://127.0.0.1:$resolvedWebPort/projects"

try {
  $runtimeService = Start-BackgroundService -Root $root -Name "runtime" -Workdir (Join-Path $root "apps\runtime") -Environment @{
    CADRIS_RUNTIME_PROVIDER = $Provider
  } -Command "python -m uvicorn cadris_runtime.main:app --port 8001"

  $rendererService = Start-BackgroundService -Root $root -Name "renderer" -Workdir (Join-Path $root "apps\renderer") -Environment @{} -Command "python -m uvicorn app.main:app --port 8002"

  $controlService = Start-BackgroundService -Root $root -Name "control-plane" -Workdir (Join-Path $root "apps\control-plane") -Environment @{
    CONTROL_PLANE_ALLOWED_ORIGINS = "http://127.0.0.1:$resolvedWebPort,http://localhost:$resolvedWebPort"
  } -Command "python -m uvicorn cadris_cp.main:app --port 8000"

  $webService = Start-BackgroundService -Root $root -Name "web" -Workdir $root -Environment @{
    NEXT_PUBLIC_CADRIS_API_URL = "http://127.0.0.1:8000"
    NEXT_PUBLIC_CADRIS_DEV_USER_ID = "dev-user"
  } -Command "call npm.cmd run start --workspace @cadris/web -- --port $resolvedWebPort"

  Assert-ServiceReady -Name "runtime" -Url $runtimeUrl -LogPath $runtimeService.LogPath
  Assert-ServiceReady -Name "renderer" -Url $rendererUrl -LogPath $rendererService.LogPath
  Assert-ServiceReady -Name "control-plane" -Url $controlUrl -LogPath $controlService.LogPath
  Assert-ServiceReady -Name "web" -Url $webUrl -LogPath $webService.LogPath -FailOnServerError:$true

  $state = [ordered]@{
    mode = "fast"
    provider = $Provider
    startedAt = (Get-Date).ToString("o")
    webPort = $resolvedWebPort
    webUrl = $webUrl
    services = @(
      [ordered]@{
        name = "runtime"
        rootPid = $runtimeService.RootPid
        listenerPid = (Get-ListeningPid -Port 8001)
        port = 8001
        url = $runtimeUrl
        logPath = $runtimeService.LogPath
      },
      [ordered]@{
        name = "renderer"
        rootPid = $rendererService.RootPid
        listenerPid = (Get-ListeningPid -Port 8002)
        port = 8002
        url = $rendererUrl
        logPath = $rendererService.LogPath
      },
      [ordered]@{
        name = "control-plane"
        rootPid = $controlService.RootPid
        listenerPid = (Get-ListeningPid -Port 8000)
        port = 8000
        url = $controlUrl
        logPath = $controlService.LogPath
      },
      [ordered]@{
        name = "web"
        rootPid = $webService.RootPid
        listenerPid = (Get-ListeningPid -Port $resolvedWebPort)
        port = $resolvedWebPort
        url = $webUrl
        logPath = $webService.LogPath
      }
    )
  }

  Write-ServiceState -Root $root -State $state

  Write-Host ""
  Write-Host "Cadris est pret." -ForegroundColor Green
  Write-Host "URL : $webUrl" -ForegroundColor Cyan
  Write-Host "Check : .\\scripts\\check-local.cmd" -ForegroundColor Cyan
  Write-Host "Arret : .\\scripts\\stop-local.cmd" -ForegroundColor Cyan
  Write-Host ""

  if (-not $NoBrowser) {
    Start-Process $webUrl
  }
} catch {
  Write-Host ""
  Write-Host "Demarrage annule. Nettoyage en cours..." -ForegroundColor Yellow
  Stop-CadrisProcesses -Root $root | Out-Null
  throw
}
