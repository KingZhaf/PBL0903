# Start all microservices in separate PowerShell windows
# Usage: .\scripts\start_all.ps1
$root = Resolve-Path (Join-Path $PSScriptRoot '..')
$python = Join-Path $root ".venv\Scripts\python.exe"
$cmd1 = "& `"$python`" SiteA\MS1\ms1.py runserver 0.0.0.0:5051"
$cmd2 = "& `"$python`" SiteA\MS2\ms2.py runserver 0.0.0.0:5052"
$cmd3 = "& `"$python`" SiteB\MS3\ms3.py runserver 0.0.0.0:5053"
$cmd4 = "& `"$python`" APPX\appx.py"
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", $cmd1
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", $cmd2
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", $cmd3
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", $cmd4
