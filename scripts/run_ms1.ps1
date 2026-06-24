# Start MS1 in a new PowerShell window
# Usage: double-click or run from PowerShell: .\scripts\run_ms1.ps1
$root = Resolve-Path (Join-Path $PSScriptRoot '..')
$python = Join-Path $root ".venv\Scripts\python.exe"
$cmd = "& `"$python`" SiteA\MS1\ms1.py runserver 0.0.0.0:5051"
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", $cmd
