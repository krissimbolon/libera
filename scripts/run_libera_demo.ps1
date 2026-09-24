param(
    [string]$OutputRoot = ".\demo_evidence"
)

$ErrorActionPreference = "Stop"

Write-Host "=== LIBERA DEMO PIPELINE ===" -ForegroundColor Cyan

& powershell -ExecutionPolicy Bypass -File scripts/acquire_chatsim.ps1 -OutputRoot $OutputRoot
if ($LASTEXITCODE -ne 0) {
    throw "Acquisition step failed."
}

$latest = Get-ChildItem $OutputRoot -Directory |
    Where-Object { $_.Name -like "ACQ-001_*" } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $latest) {
    throw "Tidak menemukan acquisition folder."
}

$workingDb = Join-Path $latest.FullName "working\libera_messages.db"
$artifactDir = Join-Path $latest.FullName "artifacts"

python tools/extract_acquired_chatsim.py $workingDb --out $artifactDir
if ($LASTEXITCODE -ne 0) {
    throw "Extraction step failed."
}

$env:LIBERA_ARTIFACT_DIR = $artifactDir

Write-Host ""
Write-Host "Launching LIBERA Forensic Workbench..." -ForegroundColor Green
Write-Host "Artifacts: $artifactDir"

streamlit run workbench/libera_workbench.py
