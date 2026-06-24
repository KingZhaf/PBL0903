# Start APPX frontend in a new PowerShell window
# Usage: .\scripts\run_appx.ps1
$root = Resolve-Path (Join-Path $PSScriptRoot '..')
$python = Join-Path $root ".venv\Scripts\python.exe"
$cmd = "& `"$python`" APPX\appx.py"
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", $cmd
