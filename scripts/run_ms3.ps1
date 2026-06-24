# Start MS3 in a new PowerShell window
# Usage: double-click or run from PowerShell: .\scripts\run_ms3.ps1
$root = Resolve-Path (Join-Path $PSScriptRoot '..')
$python = Join-Path $root ".venv\Scripts\python.exe"
$cmd = "& `"$python`" SiteB\MS3\ms3.py runserver 0.0.0.0:5053"
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", $cmd
