$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
. (Join-Path $PSScriptRoot "local-dev-helpers.ps1")

$state = Read-ServiceState -Root $root
$webListeners = Get-CadrisWebListeners -Root $root
$allProcesses = Get-CadrisProcessRecords -Root $root
$issuesFound = $false

if (-not $state) {
  Write-Host "Aucun etat canonique detecte." -ForegroundColor Yellow
  if ($allProcesses.Count -gt 0 -or $webListeners.Count -gt 0) {
    Write-Host "stale process detected: des processus Cadris tournent sans etat officiel." -ForegroundColor Red
    Write-Host "Arret conseille : .\\scripts\\stop-local.cmd" -ForegroundColor Yellow
    $issuesFound = $true
  } else {
    Write-Host "Demarrage conseille : .\\scripts\\start-local.cmd" -ForegroundColor Cyan
  }

  if ($issuesFound) {
    exit 1
  }

  exit 0
}

$expectedPidSet = New-Object "System.Collections.Generic.HashSet[int]"
foreach ($service in $state.services) {
  if ($service.rootPid) {
    $null = $expectedPidSet.Add([int]$service.rootPid)
  }
  if ($service.listenerPid) {
    $null = $expectedPidSet.Add([int]$service.listenerPid)
  }
}

$staleProcesses = @($allProcesses | Where-Object {
  -not $expectedPidSet.Contains([int]$_.ProcessId)
})

$workingAlternateWebListeners = @()
foreach ($listener in $webListeners) {
  if ($listener.Port -eq [int]$state.webPort) {
    continue
  }

  $probe = Invoke-UrlProbe -Url "http://127.0.0.1:$($listener.Port)/projects" -TimeoutSeconds 5
  if ($probe.success -and $probe.statusCode -eq 200) {
    $workingAlternateWebListeners += $listener
  }
}

Write-Host "Mode : $($state.mode)" -ForegroundColor Cyan
Write-Host "Provider : $($state.provider)" -ForegroundColor Cyan
Write-Host "URL : $($state.webUrl)" -ForegroundColor Cyan
Write-Host ""

if ($workingAlternateWebListeners.Count -gt 0) {
  $ports = ($workingAlternateWebListeners | ForEach-Object { $_.Port }) -join ", "
  Write-Host "wrong port: le web repond sur $ports alors que l'etat canonique attend $($state.webPort)." -ForegroundColor Red
  $issuesFound = $true
}

if ($staleProcesses.Count -gt 0) {
  Write-Host "stale process detected: $($staleProcesses.Count) processus Cadris parasites encore presents." -ForegroundColor Red
  $issuesFound = $true
}

foreach ($service in $state.services) {
  $probe = Invoke-UrlProbe -Url $service.url -TimeoutSeconds 10
  $listener = Get-ListeningProcessInfo -Port ([int]$service.port)

  if ($probe.success -and $probe.statusCode -eq 200) {
    Write-Host "$($service.name): OK (200)" -ForegroundColor Green
    continue
  }

  if ($service.name -eq "web" -and $workingAlternateWebListeners.Count -gt 0) {
    Write-Host "$($service.name): wrong port (attendu $($service.port), autre port actif detecte)" -ForegroundColor Red
    $issuesFound = $true
    continue
  }

  if ($listener) {
    if ($probe.statusCode -ge 500) {
      Write-Host "$($service.name): KO (HTTP $($probe.statusCode))" -ForegroundColor Red
    } else {
      Write-Host "$($service.name): warming up" -ForegroundColor Yellow
    }
  } else {
    Write-Host "$($service.name): KO (aucun listener sur le port $($service.port))" -ForegroundColor Red
  }

  Write-Host "  log: $($service.logPath)" -ForegroundColor DarkGray
  $issuesFound = $true
}

if ($issuesFound) {
  Write-Host ""
  Write-Host "Diagnostic : .\\scripts\\stop-local.cmd puis .\\scripts\\start-local.cmd" -ForegroundColor Yellow
  exit 1
}

exit 0
