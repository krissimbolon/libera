param([int]$Port = 8501)
$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $RepoRoot
$WorkbenchPython = Join-Path $RepoRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $WorkbenchPython)) {
    throw 'Buat .venv lalu install requirements-demo.txt terlebih dahulu. Lihat docs/06_report/STREAMLIT_CHATSIM.md.'
}
& $WorkbenchPython -m streamlit run workbench/libera_workbench.py --server.address 127.0.0.1 --server.port $Port --server.headless true --browser.gatherUsageStats false
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
