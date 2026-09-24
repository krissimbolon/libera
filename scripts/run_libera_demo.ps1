param(
    [string]$OutputRoot = ".\demo_evidence",
    [switch]$DryRun,
    [switch]$StopAfterP4,
    [switch]$UseLockedP5,
    [switch]$LaunchWorkbench
)

$ErrorActionPreference = "Stop"

Write-Host "=== LIBERA CHATSIM FORENSIC DEMO ===" -ForegroundColor Cyan
Write-Warning "ChatSim is a researcher-controlled Android messaging simulator, NOT WhatsApp."

& powershell -ExecutionPolicy Bypass -File scripts/acquire_chatsim.ps1 -OutputRoot $OutputRoot -AcquisitionId "ACQ-SIM-001"
if ($LASTEXITCODE -ne 0) { throw "ChatSim acquisition failed." }

$latest = Get-ChildItem $OutputRoot -Directory |
    Where-Object { $_.Name -like "ACQ-SIM-001_*" } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
if (-not $latest) { throw "No ACQ-SIM-001 folder found." }

$workingDb = Join-Path $latest.FullName "working\libera_messages.db"
$artifactDir = Join-Path $latest.FullName "artifacts"
& py -3 tools/extract_acquired_chatsim.py $workingDb --out $artifactDir
if ($LASTEXITCODE -ne 0) { throw "ChatSim P4 extraction failed." }

$artifactCsv = Join-Path $artifactDir "artifacts.csv"
if (-not (Test-Path $artifactCsv)) { throw "Normalized artifacts.csv not found." }

# Copy safe manifests into runtime so P10 reports the actual acquisition mode.
$runtimeP3 = "runtime\private\ACQ-SIM-001"
$runtimeP4 = "runtime\working\P4"
New-Item -ItemType Directory -Force -Path $runtimeP3, $runtimeP4 | Out-Null
Copy-Item (Join-Path $latest.FullName "acquisition_manifest.json") (Join-Path $runtimeP3 "acquisition_manifest.json") -Force
Copy-Item (Join-Path $latest.FullName "acquisition_manifest.json") "runtime\working\current_acquisition_manifest.json" -Force
Copy-Item (Join-Path $artifactDir "artifact_manifest.json") (Join-Path $runtimeP4 "artifact_manifest.json") -Force

if ($StopAfterP4) {
    Write-Host ""
    Write-Host "P4 COMPLETE — STOPPING BEFORE P5 HUMAN QC" -ForegroundColor Yellow
    Write-Host "ChatSim evidence root: $($latest.FullName)"
    Write-Host "Normalized ART evidence: $artifactCsv"
    Write-Host ("Next: powershell -ExecutionPolicy Bypass -File scripts\\run_p5_examiner_review.ps1 -ArtifactsPath `"{0}`"" -f $artifactCsv)
    return
}

Write-Host ""
Write-Host "Continuing P5-P10 from acquired ChatSim ART evidence..." -ForegroundColor Green
$runnerArgs = @("-ExecutionPolicy","Bypass","-File","scripts/run_libera_local.ps1","-ArtifactsPath",$artifactCsv)
if ($DryRun) { $runnerArgs += "-DryRun" }
if ($UseLockedP5) { $runnerArgs += "-UseLockedP5" }
& powershell @runnerArgs
if ($LASTEXITCODE -ne 0) { throw "P5-P10 pipeline failed." }

if ($LaunchWorkbench) {
    Write-Host "Launching SQLite ChatSim Workbench..." -ForegroundColor Green
    & powershell -ExecutionPolicy Bypass -File scripts/run_workbench.ps1
}

Write-Host ""
Write-Host "ChatSim evidence root: $($latest.FullName)"
Write-Host "Normalized ART evidence: $artifactCsv"
Write-Host "P8 is now hash-locked. Do NOT rerun P8 after opening evaluator ground truth."
Write-Host "For final P9, use scripts\run_p9_final.ps1 on the existing locked outputs."
Write-Host "Remember: DEV-SIM-001 / ACQ-SIM-001 is a controlled simulation track."
