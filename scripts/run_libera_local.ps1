param(
    [switch]$DryRun,
    [switch]$UseLockedP5,
    [string]$P5LockManifestPath = "runtime/working/P5/p5_lock_manifest.json",
    [string]$AcquisitionPath = "",
    [string]$AcquisitionSha256 = "",
    [string]$ArtifactsPath = "",
    [string]$GroundTruthPath = ""
)
$ErrorActionPreference = "Stop"
$UsedDryAcquisition = $false

# Fail before any stage can overwrite evidence or an already locked experiment.
if ($GroundTruthPath) {
    throw "GroundTruthPath is forbidden in this pipeline (including DryRun). Use scripts/run_p9_final.ps1 on existing locked outputs."
}
if (Test-Path "runtime/working/P8/p8_lock_manifest.json") {
    throw "Final P8 lock exists: pipeline rerun refused before any outputs are overwritten. Use scripts/run_p9_final.ps1 for evaluation."
}
if ($AcquisitionPath -and (-not $AcquisitionSha256 -or $AcquisitionSha256 -notmatch '^[0-9a-fA-F]{64}$')) {
    throw "AcquisitionPath requires AcquisitionSha256 from a trusted separate custody record."
}
if ($AcquisitionPath -and $ArtifactsPath) {
    throw "Supply AcquisitionPath or ArtifactsPath, not both."
}
if ($ArtifactsPath) {
    Write-Warning "Supplied ArtifactsPath bypasses acquisition verification. Its source provenance and integrity must be independently verified by the operator."
}

function Run-Python {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$PyArgs)
    & py -3 @PyArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed: py -3 $($PyArgs -join ' ')"
    }
}

Write-Host "=== LIBERA P3-P10 LOCAL RUN ==="
Write-Host "Frozen P2 is read-only and SHA-256 pinned."

if (-not $ArtifactsPath) {
    if ($AcquisitionPath) {
        Write-Host "[P4] Extracting supplied acquisition working copy..."
        Run-Python -m src.forensics.extract_artifacts --input $AcquisitionPath --expected-sha256 $AcquisitionSha256
    } else {
        Write-Host "[P3] No real acquisition supplied: building CONTROLLED DRY-RUN ACQ-DRY-001."
        Write-Warning "This is NOT physical-device acquisition and must not be presented as ACQ-001."
        $UsedDryAcquisition = $true
        Run-Python -m src.forensics.acquisition_simulator
        New-Item -ItemType Directory -Force -Path "runtime\working" | Out-Null
        Copy-Item "runtime\private\ACQ-DRY-001\acquisition_manifest.json" "runtime\working\current_acquisition_manifest.json" -Force
        $freshAcquisition = Get-Content "runtime/private/ACQ-DRY-001/acquisition_manifest.json" -Raw | ConvertFrom-Json
        if (-not $freshAcquisition.acquisition_sha256) { throw "Fresh P3 acquisition record has no SHA-256." }
        Run-Python -m src.forensics.extract_artifacts --expected-sha256 $freshAcquisition.acquisition_sha256
    }
    $ArtifactsPath = "runtime/working/P4/artifacts.csv"
}

if ($UseLockedP5) {
    Write-Host "[P5] Verifying previously reviewed/locked traditional baseline..."
    Run-Python -m src.baseline.p5_lock --verify --manifest $P5LockManifestPath
} else {
    Write-Host "[P5] Running deterministic traditional baseline..."
    Run-Python -m src.baseline.traditional_baseline --artifacts $ArtifactsPath
}
Write-Host "[P6] Building evidence-aware chunks..."
Run-Python -m src.ai_rag.chunker --input $ArtifactsPath --output runtime/working/P6/chunks.jsonl --min-size 30 --max-size 60 --time-window-minutes 120
Run-Python -m src.ai_rag.leakage_check --input runtime/working/P6/chunks.jsonl

if ($DryRun) {
    Write-Host "[P6-P8] CI-style dry-run: hashing embeddings + no model call."
    Run-Python -m src.ai_rag.retriever build --chunks runtime/working/P6/chunks.jsonl --namespace case_evidence --index runtime/working/P6/index.json --embedding-method hashing
    Run-Python -m src.ai_rag.run_experiment --dry-run --index runtime/working/P6/index.json --questions configs/investigation_tasks.json --output runtime/working/P8/experiment_output.json
} else {
    if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
        throw "Ollama is not installed or not in PATH. Install/start Ollama, then rerun; or use -DryRun."
    }
    Write-Host "[P6] Ensuring locked local models are available..."
    & ollama pull bge-m3
    if ($LASTEXITCODE -ne 0) { throw "ollama pull bge-m3 failed" }
    & ollama pull qwen2.5:1.5b
    if ($LASTEXITCODE -ne 0) { throw "ollama pull qwen2.5:1.5b failed" }

    Write-Host "[P6] Building BGE-M3 local index..."
    Run-Python -m src.ai_rag.retriever build --chunks runtime/working/P6/chunks.jsonl --namespace case_evidence --index runtime/working/P6/index.json --embedding-method ollama --embedding-model bge-m3

    Write-Host "[P7-P8] Running locked A/B/C local experiment..."
    Run-Python -m src.ai_rag.run_experiment --index runtime/working/P6/index.json --questions configs/investigation_tasks.json --output runtime/working/P8/experiment_output.json --model qwen2.5:1.5b --prompt-version v2-forensic-grounded --temperature 0.1 --seed 42 --num-ctx 8192 --top-k 8
}

if ($DryRun) {
    Write-Warning "DryRun uses stub responses: no final P8 lock is created and GT access remains closed."
} else {
    Write-Host "[P8] Locking real experiment outputs before separate ground-truth evaluation..."
    Run-Python tools/lock_p8_outputs.py --artifacts $ArtifactsPath --baseline runtime/working/P5/baseline_findings.json --experiment runtime/working/P8/experiment_output.json --run-log runtime/working/P8/run_log.jsonl --output runtime/working/P8/p8_lock_manifest.json
}

Write-Host "[P9] Running no-ground-truth integrity precheck only..."
Run-Python -m src.evaluation.evaluate_experiment --artifacts $ArtifactsPath --experiment runtime/working/P8/experiment_output.json --baseline runtime/working/P5/baseline_findings.json

Write-Host "[P10] Building runtime report..."
Run-Python -m src.report.build_report

Write-Host ""
Write-Host "=== COMPLETE ==="
Write-Host "P10 report: runtime/working/P10/run_report.md"
Write-Host "P8 output: runtime/working/P8/experiment_output.json"
Write-Host "P9 metrics: runtime/working/P9/evaluation.json"
if ($UsedDryAcquisition) {
    Write-Warning "P3 used ACQ-DRY-001 software dry-run. Do not present it as an Android/WhatsApp acquisition."
}
