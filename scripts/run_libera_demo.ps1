param(
    [string]$OutputRoot = ".\demo_evidence",
    [switch]$DryRun,
    [switch]$LaunchWorkbench,
    [string]$GroundTruthPath = ""
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

Write-Host ""
Write-Host "Continuing P5-P10 from acquired ChatSim ART evidence..." -ForegroundColor Green
$runnerArgs = @("-ExecutionPolicy","Bypass","-File","scripts/run_libera_local.ps1","-ArtifactsPath",$artifactCsv)
if ($DryRun) { $runnerArgs += "-DryRun" }
if ($GroundTruthPath) { $runnerArgs += @("-GroundTruthPath",$GroundTruthPath) }
& powershell @runnerArgs
if ($LASTEXITCODE -ne 0) { throw "P5-P10 pipeline failed." }

if ($LaunchWorkbench) {
    $env:LIBERA_ARTIFACT_DIR = $artifactDir
    if (-not (Get-Command streamlit -ErrorAction SilentlyContinue)) {
        Write-Warning "Streamlit not found; run: py -3 -m pip install -r requirements-demo.txt"
    } else {
        Write-Host "Launching LIBERA Forensic Workbench..." -ForegroundColor Green
        & streamlit run workbench/libera_workbench.py
    }
}

Write-Host ""
Write-Host "ChatSim evidence root: $($latest.FullName)"
Write-Host "Normalized ART evidence: $artifactCsv"
Write-Host "Remember: DEV-SIM-001 / ACQ-SIM-001 is a controlled simulation track."
