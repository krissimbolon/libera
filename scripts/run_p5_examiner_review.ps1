param(
    [string]$ArtifactsPath = "runtime\working\P4\artifacts.csv",
    [int]$TopN = 20,
    [int]$MaxReviewItems = 12
)

$ErrorActionPreference = "Stop"

function Run-Python {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$PyArgs)
    & py -3 @PyArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed: py -3 $($PyArgs -join ' ')"
    }
}

if (-not (Test-Path $ArtifactsPath)) {
    throw "P4 artifacts not found: $ArtifactsPath"
}

Write-Host "=== LIBERA P5 TRADITIONAL BASELINE + <=5 MIN EXAMINER QC ===" -ForegroundColor Cyan
Write-Host "[P5] Running deterministic baseline..."
Run-Python -m src.baseline.traditional_baseline --artifacts $ArtifactsPath --tasks configs/investigation_tasks.json --output-dir runtime/working/P5 --top-n $TopN

Write-Host "[P5-QC] Building deterministic examiner packet..."
Run-Python -m src.baseline.examiner_packet --baseline runtime/working/P5/baseline_findings.json --output runtime/working/P5/p5_examiner_packet.csv --manifest runtime/working/P5/p5_examiner_packet_manifest.json --max-items $MaxReviewItems

$packetPath = "runtime\working\P5\p5_examiner_packet.csv"
$rows = @(Import-Csv $packetPath)
if ($rows.Count -eq 0) {
    throw "Examiner packet is empty."
}

Write-Host ""
Write-Host "HUMAN QC START" -ForegroundColor Yellow
Write-Host "Goal: verify candidate relevance/traceability only; this is NOT ground truth."
Write-Host "Decision: S=SUPPORTED, N=NOT_SUPPORTED, U=UNCERTAIN."
Write-Host "For N/U, enter a short reason. Target: <=300 seconds total."
Write-Host ""

$timer = [System.Diagnostics.Stopwatch]::StartNew()
for ($i = 0; $i -lt $rows.Count; $i++) {
    $r = $rows[$i]
    Write-Host ("-" * 88)
    Write-Host ("[{0}/{1}] {2} | task(s) {3} | rank {4} | score {5}" -f ($i + 1), $rows.Count, $r.evidence_id, $r.linked_task_ids, $r.best_rank, $r.automated_score) -ForegroundColor Cyan
    Write-Host ("{0} | {1} -> {2}" -f $r.timestamp, $r.sender, $r.receiver)
    Write-Host ("keywords: {0}" -f $r.matched_keywords)

    $text = [string]$r.text
    if ($text.Length -gt 500) { $text = $text.Substring(0, 500) + "..." }
    Write-Host ("text: {0}" -f $text)

    do {
        $answer = (Read-Host "Decision [S/N/U]").Trim().ToUpperInvariant()
    } while ($answer -notin @("S", "N", "U"))

    switch ($answer) {
        "S" { $r.examiner_decision = "SUPPORTED" }
        "N" { $r.examiner_decision = "NOT_SUPPORTED" }
        "U" { $r.examiner_decision = "UNCERTAIN" }
    }

    if ($answer -in @("N", "U")) {
        do {
            $note = (Read-Host "Short reason").Trim()
        } while (-not $note)
        $r.examiner_note = $note
    } else {
        $r.examiner_note = ""
    }
}

$timer.Stop()
$rows | Export-Csv $packetPath -NoTypeInformation -Encoding UTF8

Write-Host ""
Write-Host ("Human QC elapsed: {0:N1} seconds" -f $timer.Elapsed.TotalSeconds)
if ($timer.Elapsed.TotalSeconds -gt 300) {
    Write-Warning "QC exceeded the 5-minute presentation timebox. Keep the result, but report actual elapsed time."
} else {
    Write-Host "[PASS] Human QC completed inside the 5-minute timebox." -ForegroundColor Green
}

Write-Host "[P5-LOCK] Locking P4 input + P5 baseline + completed examiner review..."
Run-Python -m src.baseline.p5_lock --artifacts $ArtifactsPath --tasks configs/investigation_tasks.json --p5-dir runtime/working/P5 --packet $packetPath --output runtime/working/P5/p5_lock_manifest.json

Write-Host ""
Write-Host "P5 READY FOR AI" -ForegroundColor Green
Write-Host "  baseline : runtime\working\P5\baseline_findings.json"
Write-Host "  QC packet: runtime\working\P5\p5_examiner_packet.csv"
Write-Host "  P5 lock  : runtime\working\P5\p5_lock_manifest.json"
Write-Host "Do not edit P5 outputs after this point. Continue P6-P8 only after verifying this lock."
