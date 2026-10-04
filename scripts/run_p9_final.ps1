param(
    [Parameter(Mandatory=$true)][string]$GroundTruthPath,
    [string]$ArtifactsPath = "",
    [string]$LockManifest = "runtime\working\P8\p8_lock_manifest.json",
    [string]$OutputDirectory = "",
    [string]$AcquisitionManifestPath = "",
    [string]$ArtifactManifestPath = "",
    # refuse (default, fail-closed): stop before private GT when any citation is invalid.
    # quarantine: documented policy p9-strict-citation-quarantine-v1 used for the 2026-09-25 v6 run.
    [ValidateSet("refuse","quarantine")][string]$CitationPolicy = "refuse"
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

Write-Host "=== Libera LOCKED-OUTPUT P9 EVALUATION ===" -ForegroundColor Cyan
Write-Host "This script does NOT rerun P6/P7/P8."
Write-Host "It evaluates the already-locked experiment output only."

$ExperimentPath = $lock.files.p8_experiment_output.path
$BaselinePath = $lock.files.p5_baseline.path
$ConfigPath = $lock.files.p6_p7_config.path
if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path (Split-Path $LockManifest -Parent) "P9_final"
}
$EvaluationPath = Join-Path $OutputDirectory "evaluation.json"
$ReportPath = Join-Path $OutputDirectory "run_report.md"
if ((Test-Path $EvaluationPath) -or (Test-Path $ReportPath)) {
    throw "Final evaluation/report already exists. Choose a new OutputDirectory to preserve the audit trail."
}

Write-Host "[1/4] Verifying every P8 locked file BEFORE opening ground truth..."
Run-Python -m src.evaluation.evaluate_experiment `
    --verify-lock-only --artifacts $ArtifactsPath --experiment $ExperimentPath `
    --baseline $BaselinePath --lock-manifest $LockManifest
if ($CitationPolicy -eq "refuse") {
    # Public lock + evidence-integrity verification must finish before any private GT contents are read.
    Run-Python tools/verify_p8_lock.py --lock-manifest $LockManifest --artifacts $ArtifactsPath
}

Write-Host "[2/4] Validating/locking private ground truth..."
$gtLock = $GroundTruthPath + ".lock.json"
Run-Python tools/lock_private_ground_truth.py $GroundTruthPath --output $gtLock

Write-Host "[3/4] Evaluating (citation policy: $CitationPolicy)..."
Run-Python -m src.evaluation.evaluate_experiment `
    --artifacts $ArtifactsPath `
    --experiment $ExperimentPath `
    --baseline $BaselinePath `
    --ground-truth $GroundTruthPath `
    --ground-truth-lock $gtLock `
    --outputs-locked `
    --lock-manifest $LockManifest `
    --citation-policy $CitationPolicy `
    --output $EvaluationPath

if (-not $ArtifactManifestPath) {
    $ArtifactManifestPath = Join-Path (Split-Path $ArtifactsPath -Parent) "artifact_manifest.json"
}
if (-not $AcquisitionManifestPath) {
    $AcquisitionManifestPath = Join-Path (Split-Path (Split-Path $ArtifactsPath -Parent) -Parent) "acquisition_manifest.json"
}
Write-Host "[4/4] Building P10 for the selected locked run..."
Run-Python -m src.report.build_report --evaluation $EvaluationPath `
    --p8-lock $LockManifest --config $ConfigPath --experiment $ExperimentPath --output $ReportPath `
    --artifact-manifest $ArtifactManifestPath --acquisition-manifest $AcquisitionManifestPath

Write-Host ""
$evaluation = Get-Content $EvaluationPath -Raw | ConvertFrom-Json
Write-Host "[P9] $($evaluation.status)"
if ($evaluation.ground_truth_evaluation.independent_ground_truth -eq $false) {
    Write-Warning "Reconstructed provenance proxy only; this is NOT original blind key-evidence ground truth."
}
if ($evaluation.precheck_status -ne "P9_PRECHECK_PASS") {
    Write-Warning "Citation/integrity findings remain in the report; completion does not mean model accuracy passed."
}
Write-Host "P9: $EvaluationPath"
Write-Host "P10: $ReportPath"
Write-Host "GT lock: $gtLock"
