# Start MS2 in a new PowerShell window
# Usage: double-click or run from PowerShell: .\scripts\run_ms2.ps1
$root = Resolve-Path (Join-Path $PSScriptRoot '..')
$python = Join-Path $root ".venv\Scripts\python.exe"
$cmd = "& `"$python`" SiteA\MS2\ms2.py runserver 0.0.0.0:5052"
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", $cmd
