function Get-StateDir([string]$Root) {
  return Join-Path $Root ".tmp-local"
}

function Get-LogDir([string]$Root) {
  return Join-Path (Get-StateDir -Root $Root) "logs"
}

function Get-LaunchersDir([string]$Root) {
  return Join-Path (Get-StateDir -Root $Root) "launchers"
}

function Get-ServiceStatePath([string]$Root) {
  return Join-Path (Get-StateDir -Root $Root) "service-state.json"
}

function Get-LocalWebPortPath([string]$Root) {
  return Join-Path (Get-StateDir -Root $Root) "web-port.txt"
}

function Initialize-LocalState([string]$Root) {
  New-Item -ItemType Directory -Force -Path (Get-StateDir -Root $Root) | Out-Null
  New-Item -ItemType Directory -Force -Path (Get-LogDir -Root $Root) | Out-Null
  New-Item -ItemType Directory -Force -Path (Get-LaunchersDir -Root $Root) | Out-Null
}

function Get-ListeningPid([int]$Port) {
  $lines = cmd /c "netstat -ano | findstr :$Port"
  foreach ($line in $lines) {
    if ($line -match "LISTENING\s+(\d+)$") {
      return [int]$Matches[1]
    }
  }
  return $null
}

function Get-ListeningProcessInfo([int]$Port) {
  $listenerProcessId = Get-ListeningPid -Port $Port
  if (-not $listenerProcessId) {
    return $null
  }

  $process = Get-CimInstance Win32_Process -Filter "ProcessId = $listenerProcessId" -ErrorAction SilentlyContinue
  if (-not $process) {
    return [pscustomobject]@{
      Port = $Port
      Pid = $listenerProcessId
      Name = $null
      CommandLine = $null
    }
  }

  return [pscustomobject]@{
    Port = $Port
    Pid = $listenerProcessId
    Name = $process.Name
    CommandLine = $process.CommandLine
  }
}

function Get-FreeWebPort([int]$PreferredPort) {
  $candidate = $PreferredPort
  while ($candidate -le ($PreferredPort + 20)) {
    if (-not (Get-ListeningPid -Port $candidate)) {
      return $candidate
    }
    $candidate += 1
  }
  throw "Aucun port web libre trouve entre $PreferredPort et $($PreferredPort + 20)."
}

function Save-LocalWebPort([string]$Root, [int]$Port) {
  Initialize-LocalState -Root $Root
  Set-Content -Path (Get-LocalWebPortPath -Root $Root) -Encoding ASCII -Value $Port
}

function Read-LocalWebPort([string]$Root, [int]$DefaultPort = 3001) {
  $path = Get-LocalWebPortPath -Root $Root
  if (Test-Path $path) {
    $raw = Get-Content $path -Raw
    $parsed = 0
    if ([int]::TryParse($raw.Trim(), [ref]$parsed)) {
      return $parsed
    }
  }
  return $DefaultPort
}

function Write-ServiceState([string]$Root, [object]$State) {
  Initialize-LocalState -Root $Root
  $State | ConvertTo-Json -Depth 8 | Set-Content -Path (Get-ServiceStatePath -Root $Root) -Encoding UTF8
}

function Read-ServiceState([string]$Root) {
  $path = Get-ServiceStatePath -Root $Root
  if (-not (Test-Path $path)) {
    return $null
  }

  return Get-Content $path -Raw | ConvertFrom-Json
}

function Remove-LocalStateFiles([string]$Root) {
  $targets = @(
    (Get-ServiceStatePath -Root $Root),
    (Get-LocalWebPortPath -Root $Root)
  )

  foreach ($target in $targets) {
    if (Test-Path $target) {
      Remove-Item $target -Force -ErrorAction SilentlyContinue
    }
  }

  $launchersDir = Get-LaunchersDir -Root $Root
  if (Test-Path $launchersDir) {
    Get-ChildItem $launchersDir -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
  }
}

function Get-ProcessInfo([int]$ProcessId) {
  if (-not $ProcessId) {
    return $null
  }

  return Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId" -ErrorAction SilentlyContinue
}

function Test-IsCadrisProcessRecord([object]$Process, [string]$Root) {
  if (-not $Process) {
    return $false
  }

  $cmd = $Process.CommandLine
  if (-not $cmd) {
    return $false
  }

  $rootPattern = [regex]::Escape($Root)
  return (
    $cmd -match $rootPattern -and
    $cmd -match "next|start-server|uvicorn|npm(\.cmd)? run (dev|start)|@cadris/web|app\.main:app|CONTROL_PLANE_ALLOWED_ORIGINS|CADRIS_RUNTIME_PROVIDER"
  )
}

function Test-IsCadrisPortOwner([object]$PortInfo, [string]$Root) {
  if (-not $PortInfo) {
    return $false
  }

  if ($PortInfo.CommandLine -and (Test-IsCadrisProcessRecord -Process $PortInfo -Root $Root)) {
    return $true
  }

  if ($PortInfo.Port -in @(8000, 8001, 8002)) {
    return (
      ($PortInfo.Name -eq "python.exe" -and $PortInfo.CommandLine -and $PortInfo.CommandLine -match "uvicorn app\.main:app --port 800[012]") -or
      ($PortInfo.Name -eq "cmd.exe" -and $PortInfo.CommandLine -and $PortInfo.CommandLine -match [regex]::Escape($Root))
    )
  }

  return (
    $PortInfo.Name -eq "node.exe" -and
    $PortInfo.CommandLine -and
    $PortInfo.CommandLine -match [regex]::Escape($Root)
  )
}

function Get-CadrisProcessRecords([string]$Root) {
  $rootPattern = [regex]::Escape($Root)
  return Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -and (
      ($_.CommandLine -match $rootPattern -and $_.CommandLine -match "next|start-server|uvicorn|npm(\.cmd)? run (dev|start)|@cadris/web|CONTROL_PLANE_ALLOWED_ORIGINS|CADRIS_RUNTIME_PROVIDER") -or
      ($_.CommandLine -match "uvicorn app\.main:app --port 800[012]")
    )
  } | Select-Object ProcessId, ParentProcessId, Name, CommandLine
}

function Get-ListeningPortRecords([int]$MinPort = 3000, [int]$MaxPort = 3305) {
  $records = @()
  $lines = cmd /c "netstat -ano -p tcp"

  foreach ($line in $lines) {
    if ($line -match "^\s*TCP\s+\S+:(\d+)\s+\S+\s+LISTENING\s+(\d+)$") {
      $port = [int]$Matches[1]
      $processId = [int]$Matches[2]
      if ($port -ge $MinPort -and $port -le $MaxPort) {
        $records += [pscustomobject]@{
          Port = $port
          Pid = $processId
        }
      }
    }
  }

  return $records | Sort-Object Port -Unique
}

function Get-CadrisWebListeners([string]$Root, [int]$MinPort = 3000, [int]$MaxPort = 3305) {
  $listeners = @()
  foreach ($record in Get-ListeningPortRecords -MinPort $MinPort -MaxPort $MaxPort) {
    $process = Get-ProcessInfo -ProcessId $record.Pid
    if (
      $process -and
      $process.Name -eq "node.exe" -and
      $process.CommandLine -and
      $process.CommandLine -match [regex]::Escape($Root) -and
      $process.CommandLine -match "next|start-server|@cadris/web"
    ) {
      $listeners += [pscustomobject]@{
        Port = $record.Port
        Pid = $record.Pid
        Name = $process.Name
        CommandLine = $process.CommandLine
      }
    }
  }

  return $listeners | Sort-Object Port -Unique
}

function Stop-ProcessTree([int]$ProcessId) {
  if (-not $ProcessId) {
    return $false
  }

  $process = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
  if (-not $process) {
    return $false
  }

  cmd /c "taskkill /PID $ProcessId /T /F >NUL 2>NUL" | Out-Null
  Start-Sleep -Milliseconds 200
  return -not (Get-Process -Id $ProcessId -ErrorAction SilentlyContinue)
}

function Stop-CadrisProcesses([string]$Root) {
  Initialize-LocalState -Root $Root

  $stopped = New-Object System.Collections.ArrayList
  $seen = New-Object "System.Collections.Generic.HashSet[int]"
  $state = Read-ServiceState -Root $Root

  function Add-StopCandidate([int]$ProcessId, [string]$Reason) {
    if (-not $ProcessId) {
      return
    }

    if (-not $seen.Add([int]$ProcessId)) {
      return
    }

    $processInfo = Get-ProcessInfo -ProcessId $ProcessId
    $name = if ($processInfo) { $processInfo.Name } else { $null }
    $commandLine = if ($processInfo) { $processInfo.CommandLine } else { $null }

    if (Stop-ProcessTree -ProcessId $ProcessId) {
      [void]$stopped.Add([pscustomobject]@{
        pid = $ProcessId
        name = $name
        reason = $Reason
        commandLine = $commandLine
      })
    }
  }

  if ($state -and $state.services) {
    foreach ($service in $state.services) {
      Add-StopCandidate -ProcessId ([int]$service.rootPid) -Reason "state-root:$($service.name)"
      Add-StopCandidate -ProcessId ([int]$service.listenerPid) -Reason "state-listener:$($service.name)"
    }
  }

  foreach ($port in @(8000, 8001, 8002)) {
    $portInfo = Get-ListeningProcessInfo -Port $port
    if (Test-IsCadrisPortOwner -PortInfo $portInfo -Root $Root) {
      Add-StopCandidate -ProcessId $portInfo.Pid -Reason "reserved-port:$port"
    }
  }

  foreach ($webListener in Get-CadrisWebListeners -Root $Root) {
    Add-StopCandidate -ProcessId $webListener.Pid -Reason "web-listener:$($webListener.Port)"
  }

  foreach ($process in Get-CadrisProcessRecords -Root $Root) {
    Add-StopCandidate -ProcessId ([int]$process.ProcessId) -Reason "process-scan"
  }

  Remove-LocalStateFiles -Root $Root
  return @($stopped)
}

function New-ServiceLogPath([string]$Root, [string]$Name) {
  Initialize-LocalState -Root $Root
  return Join-Path (Get-LogDir -Root $Root) "$Name.log"
}

function Start-BackgroundService(
  [string]$Root,
  [string]$Name,
  [string]$Workdir,
  [hashtable]$Environment,
  [string]$Command
) {
  Initialize-LocalState -Root $Root

  $launcherPath = Join-Path (Get-LaunchersDir -Root $Root) "$Name.cmd"
  $logPath = New-ServiceLogPath -Root $Root -Name $Name

  $lines = @(
    "@echo off",
    "cd /d ""$Workdir"""
  )

  foreach ($entry in $Environment.GetEnumerator()) {
    $lines += "set $($entry.Key)=$($entry.Value)"
  }

  $lines += "$Command 1>> ""$logPath"" 2>>&1"

  Set-Content -Path $launcherPath -Encoding ASCII -Value $lines
  Clear-Content -Path $logPath -ErrorAction SilentlyContinue

  $process = Start-Process -FilePath cmd.exe -ArgumentList "/d", "/c", """$launcherPath""" -WindowStyle Hidden -PassThru
  return [pscustomobject]@{
    Name = $Name
    RootPid = $process.Id
    LauncherPath = $launcherPath
    LogPath = $logPath
  }
}

function Invoke-UrlProbe([string]$Url, [int]$TimeoutSeconds = 5) {
  try {
    $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec $TimeoutSeconds
    return [pscustomobject]@{
      success = $true
      statusCode = [int]$response.StatusCode
      message = "HTTP $([int]$response.StatusCode)"
    }
  } catch {
    $statusCode = $null
    if ($_.Exception.Response -and $_.Exception.Response.StatusCode) {
      $statusCode = [int]$_.Exception.Response.StatusCode.value__
    }

    return [pscustomobject]@{
      success = $false
      statusCode = $statusCode
      message = $_.Exception.Message
    }
  }
}

function Wait-ForServiceReady(
  [string]$Name,
  [string]$Url,
  [int]$TimeoutSeconds = 60,
  [bool]$FailOnServerError = $false
) {
  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)

  while ((Get-Date) -lt $deadline) {
    $probe = Invoke-UrlProbe -Url $Url -TimeoutSeconds 5
    if ($probe.success -and $probe.statusCode -eq 200) {
      return [pscustomobject]@{
        ready = $true
        state = "ok"
        statusCode = 200
        message = "HTTP 200"
      }
    }

    if ($FailOnServerError -and $probe.statusCode -ge 500) {
      return [pscustomobject]@{
        ready = $false
        state = "server-error"
        statusCode = $probe.statusCode
        message = $probe.message
      }
    }

    Start-Sleep -Milliseconds 800
  }

  return [pscustomobject]@{
    ready = $false
    state = "timeout"
    statusCode = $null
    message = "Le service $Name n'a pas repondu en 200 a temps."
  }
}

function Get-LogTail([string]$Path, [int]$LineCount = 30) {
  if (-not (Test-Path $Path)) {
    return "(log introuvable)"
  }

  return (Get-Content -Path $Path -Tail $LineCount -ErrorAction SilentlyContinue) -join [Environment]::NewLine
}
