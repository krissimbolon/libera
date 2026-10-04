param(
    [string]$ArtifactsPath = "",
    [string]$P5LockManifestPath = "runtime\working\P5\p5_lock_manifest.json"
)

$ErrorActionPreference = "Continue"

function Show-Status {
    param([string]$Label, [bool]$Ok, [string]$Detail = "")
    $state = if ($Ok) { "OK" } else { "MISSING/NOT VERIFIED" }
    $suffix = if ($Detail) { " - $Detail" } else { "" }
    Write-Host ("[{0}] {1}{2}" -f $state, $Label, $suffix)
}

Write-Host "=== LIBERA PRESENTATION PROGRESS CHECK ===" -ForegroundColor Cyan
Write-Host "Read-only checker: this script does not modify evidence or runtime outputs."
Write-Host ""

# Git
$head = (& git rev-parse HEAD 2>$null)
$originMain = (& git rev-parse origin/main 2>$null)
$branch = (& git branch --show-current 2>$null)
Show-Status "Git branch main" ($branch -eq "main") "branch=$branch"
Show-Status "Local HEAD matches origin/main" ($head -and $originMain -and ($head -eq $originMain)) "HEAD=$head origin/main=$originMain"

# Find latest actual ChatSim acquisition if caller did not provide artifacts path.
$latestAcq = Get-ChildItem ".\demo_evidence" -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -like "ACQ-SIM-001_*" } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $ArtifactsPath -and $latestAcq) {
    $ArtifactsPath = Join-Path $latestAcq.FullName "artifacts\artifacts.csv"
}

Write-Host ""
Write-Host "--- P3 / P4 ---" -ForegroundColor Yellow
Show-Status "Actual ACQ-SIM folder" ([bool]$latestAcq) $(if ($latestAcq) { $latestAcq.FullName } else { "" })
if ($latestAcq) {
    Show-Status "acquisition_manifest.json" (Test-Path (Join-Path $latestAcq.FullName "acquisition_manifest.json"))
    Show-Status "sha256_manifest.csv" (Test-Path (Join-Path $latestAcq.FullName "sha256_manifest.csv"))
    Show-Status "artifact_manifest.json" (Test-Path (Join-Path $latestAcq.FullName "artifacts\artifact_manifest.json"))
}
Show-Status "P4 artifacts.csv" ($ArtifactsPath -and (Test-Path $ArtifactsPath)) $ArtifactsPath

if ($ArtifactsPath -and (Test-Path $ArtifactsPath)) {
    try {
        $hash = (Get-FileHash $ArtifactsPath -Algorithm SHA256).Hash
        $rowCount = (Import-Csv $ArtifactsPath | Measure-Object).Count
        Write-Host "      P4 SHA256=$hash"
        Write-Host "      P4 rows=$rowCount"
    } catch {
        Write-Host "      Could not summarize P4: $($_.Exception.Message)"
    }
}

Write-Host ""
Write-Host "--- P5 ---" -ForegroundColor Yellow
$p5Files = @(
    "timeline.csv",
    "entities.csv",
    "relationships.csv",
    "baseline_findings.json",
    "baseline_manifest.json",
    "p5_examiner_packet.csv",
    "p5_examiner_packet_manifest.json",
    "p5_lock_manifest.json"
)
foreach ($f in $p5Files) {
    Show-Status "P5 $f" (Test-Path (Join-Path "runtime\working\P5" $f))
}
if (Test-Path $P5LockManifestPath) {
    & py -3 -m src.baseline.p5_lock --verify --manifest $P5LockManifestPath
    Show-Status "P5 cryptographic lock verify" ($LASTEXITCODE -eq 0)
}

Write-Host ""
Write-Host "--- LOCAL AI ENVIRONMENT ---" -ForegroundColor Yellow
$ollamaCmd = Get-Command ollama -ErrorAction SilentlyContinue
Show-Status "Ollama command" ([bool]$ollamaCmd)
if ($ollamaCmd) {
    $models = (& ollama list 2>$null | Out-String)
    Show-Status "bge-m3 model" ($models -match "bge-m3")
    Show-Status "qwen2.5:1.5b model" ($models -match "qwen2\.5:1\.5b")
}

Write-Host ""
Write-Host "--- P6 / P7 / P8 ---" -ForegroundColor Yellow
Show-Status "P6 chunks.jsonl" (Test-Path "runtime\working\P6\chunks.jsonl")
Show-Status "P6 index.json" (Test-Path "runtime\working\P6\index.json")
Show-Status "P8 experiment_output.json" (Test-Path "runtime\working\P8\experiment_output.json")
Show-Status "P8 run_log.jsonl" (Test-Path "runtime\working\P8\run_log.jsonl")
Show-Status "P8 p8_lock_manifest.json" (Test-Path "runtime\working\P8\p8_lock_manifest.json")

Write-Host ""
Write-Host "--- P9 / P10 ---" -ForegroundColor Yellow
Show-Status "P9 evaluation.json" (Test-Path "runtime\working\P9\evaluation.json")
Show-Status "P10 run_report.md" (Test-Path "runtime\working\P10\run_report.md")

Write-Host ""
Write-Host "--- PRESENTATION EVIDENCE ---" -ForegroundColor Yellow
$shots = @(
    "01_chatsim.png",
    "02_acquisition.png",
    "03_sha256.png",
    "04_p4_artifacts.png",
    "05_p5_examiner.png",
    "06_p5_lock.png",
    "07_p6_retrieval.png",
    "08_p8_abc.png",
    "09_p8_lock.png",
    "10_p10_report.png"
)
$shotCount = 0
foreach ($s in $shots) {
    if (Test-Path (Join-Path "presentation_evidence" $s)) { $shotCount++ }
}
Write-Host "Screenshots present: $shotCount/10"

Write-Host ""
Write-Host "=== END PROGRESS CHECK ===" -ForegroundColor Cyan
Write-Host "If something says MISSING/NOT VERIFIED, report that exact line instead of guessing."
