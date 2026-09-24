param(
    [switch]$InstallOllama
)

$ErrorActionPreference = "Stop"
Write-Host "=== LIBERA LOCAL PREFLIGHT ==="

function Fail($msg) { Write-Error $msg; exit 1 }

# Repository / frozen corpus
if (-not (Test-Path "data\adaptasi_indonesia\corpus_whatsapp_10000.csv")) {
    Fail "Run this script from the repository root on branch p3-p10-final-integration."
}
$expected = "A014A02EBAD298A33267DA8631F3A2D1906A537AE558C1849622904C225467E6"
$actual = (Get-FileHash "data\adaptasi_indonesia\corpus_whatsapp_10000.csv" -Algorithm SHA256).Hash.ToUpper()
if ($actual -ne $expected) { Fail "Frozen P2 hash mismatch. Expected $expected, got $actual" }
Write-Host "[PASS] Frozen P2 hash matches."

# Python
$py = Get-Command py -ErrorAction SilentlyContinue
if (-not $py) { Fail "Python launcher (py) not found. Install Python 3.10+ and retry." }
$pyVersion = & py -3 --version
Write-Host "[PASS] $pyVersion"

# Free disk
$root = (Get-Location).Path
$driveName = ([System.IO.Path]::GetPathRoot($root)).TrimEnd("\").TrimEnd(":")
$drive = Get-PSDrive -Name $driveName
$freeGB = [math]::Round($drive.Free / 1GB, 1)
Write-Host "[INFO] Free disk on $($drive.Name): $freeGB GB"
if ($freeGB -lt 12) {
    Write-Warning "Less than 12 GB free. Model pulls + runtime/acquisition copies may fail. Free more space first."
}

# Ollama
$ollama = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollama -and $InstallOllama) {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) { Fail "winget not found; install Ollama manually from the official installer." }
    Write-Host "[SETUP] Installing Ollama using winget..."
    & winget install --id Ollama.Ollama -e --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { Fail "Ollama installation failed." }
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    $ollama = Get-Command ollama -ErrorAction SilentlyContinue
}
if (-not $ollama) {
    Write-Warning "Ollama not found. Dry-run works now; install Ollama before the real P6-P8 local run."
} else {
    Write-Host "[PASS] Ollama executable: $($ollama.Source)"
    try {
        $version = & ollama --version
        Write-Host "[PASS] $version"
    } catch {
        Write-Warning "Ollama executable exists but version check failed."
    }
}

Write-Host ""
Write-Host "Next commands:"
Write-Host "  1) py -3 -m pytest tests/test_p6_p7_pipeline.py tests/test_post_p2_pipeline.py -v"
Write-Host "  2) powershell -ExecutionPolicy Bypass -File scripts\run_libera_local.ps1 -DryRun"
Write-Host "  3) powershell -ExecutionPolicy Bypass -File scripts\run_libera_local.ps1"
Write-Host ""
Write-Host "For the final P9 blind evaluation, add -GroundTruthPath only AFTER P8 output is locked."
