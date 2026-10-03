param(
    [Parameter(Mandatory=$true)][string]$GroundTruthPath,
    [string]$ArtifactsPath = "",
    [string]$LockManifest = "runtime\working\P8\p8_lock_manifest.json"
)

$ErrorActionPreference = "Stop"

function Run-Python {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$PyArgs)
    & py -3 @PyArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed: py -3 $($PyArgs -join ' ')"
    }
}

if (-not (Test-Path $GroundTruthPath)) { throw "Private ground truth not found: $GroundTruthPath" }
if (-not (Test-Path $LockManifest)) { throw "P8 lock manifest not found: $LockManifest" }

$lock = Get-Content $LockManifest -Raw | ConvertFrom-Json
if ($lock.status -ne "P8_OUTPUTS_LOCKED_BEFORE_GROUND_TRUTH") {
    throw "Invalid P8 lock manifest status: $($lock.status)"
}

if (-not $ArtifactsPath) {
    $ArtifactsPath = $lock.files.p4_artifacts.path
}
if (-not (Test-Path $ArtifactsPath)) {
    throw "Locked P4 artifacts not found at: $ArtifactsPath"
}

Write-Host "=== LIBERA FINAL BLIND P9 ===" -ForegroundColor Cyan
Write-Host "This script does NOT rerun P6/P7/P8."
Write-Host "It evaluates the already-locked experiment output only."

# Public lock verification must finish before any private GT contents are read.
Write-Host "[1/4] Verifying all locked P8 inputs before private GT access..."
Run-Python tools/verify_p8_lock.py --lock-manifest $LockManifest --artifacts $ArtifactsPath
$ExperimentPath = $lock.files.p8_experiment_output.path
$BaselinePath = $lock.files.p5_baseline.path

Write-Host "[2/4] Locking private ground truth..."
$gtLock = $GroundTruthPath + ".lock.json"
Run-Python tools/lock_private_ground_truth.py $GroundTruthPath --output $gtLock

Write-Host "[3/4] Rechecking P8 cryptographic lock and evaluating..."
Run-Python -m src.evaluation.evaluate_experiment `
    --artifacts $ArtifactsPath `
    --experiment $ExperimentPath `
    --baseline $BaselinePath `
    --ground-truth $GroundTruthPath `
    --outputs-locked `
    --lock-manifest $LockManifest `
    --output runtime/working/P9/evaluation.json

Write-Host "[4/4] Rebuilding P10 report with final P9 metrics..."
Run-Python -m src.report.build_report

Write-Host ""
Write-Host "[PASS] Final blind evaluation complete." -ForegroundColor Green
Write-Host "P9: runtime\working\P9\evaluation.json"
Write-Host "P10: runtime\working\P10\run_report.md"
Write-Host "GT lock: $gtLock"
