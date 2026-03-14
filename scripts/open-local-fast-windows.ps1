param(
  [ValidateSet("local", "openai")]
  [string]$Provider = "local",
  [int]$WebPort = 3001
)

$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "start-local.ps1") -Provider $Provider -WebPort $WebPort
