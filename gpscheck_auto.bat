@echo off & setlocal
set batchPath=%~dp0
PowerShell.exe -ExecutionPolicy Bypass -File "%batchPath%gpscheck_auto.ps1"


