# Stop APPX and microservice Python processes started from this workspace's venv
# Usage: .\scripts\stop_all.ps1
$root = Resolve-Path (Join-Path $PSScriptRoot '..')
$venvPython = Join-Path $root ".venv\Scripts\python.exe"

# Find processes where CommandLine contains the workspace venv python and one of the script names
Get-CimInstance Win32_Process |
    Where-Object { $_.CommandLine -and $_.CommandLine -like "*$venvPython*" -and ($_.CommandLine -match 'ms1.py|ms2.py|ms3.py|appx.py') } |
    ForEach-Object {
        Write-Output "Stopping PID $($_.ProcessId): $($_.CommandLine)"
        try { Stop-Process -Id $_.ProcessId -Force -ErrorAction Stop } catch { Write-Warning "Failed to stop PID $($_.ProcessId): $($_.Exception.Message)" }
    }

# Also attempt to stop any python processes that look like they run site scripts (fallback)
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -and $_.Path -like "*$($env:USERPROFILE)*" } | ForEach-Object {
    Write-Output "Stopping python PID $($_.Id) (fallback)"
    try { Stop-Process -Id $_.Id -Force -ErrorAction Stop } catch { }
}

Write-Output "Stop sequence complete."
