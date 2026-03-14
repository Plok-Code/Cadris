@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0open-local-dev-windows.ps1" %*
