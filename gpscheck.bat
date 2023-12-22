@echo off & setlocal
set batchPath=%~dp0
PowerShell.exe -ExecutionPolicy Bypass -File "%batchPath%gpscheck.ps1"


