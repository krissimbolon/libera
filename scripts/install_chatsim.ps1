param(
    [Parameter(Mandatory=$true)][string]$ApkPath,
    [string]$Package = "id.libera.chatsim"
)

$ErrorActionPreference = "Stop"

function Need-Command($name) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
        throw "Command $name tidak ditemukan. Tambahkan Android platform-tools ke PATH."
    }
}

Need-Command adb
if (-not (Test-Path $ApkPath)) { throw "APK tidak ditemukan: $ApkPath" }

Write-Host "=== INSTALL LIBERA CHATSIM ===" -ForegroundColor Cyan
Write-Warning "Target ini DEV-SIM-001 controlled emulator, bukan WhatsApp/DEV-001 fisik."

adb wait-for-device | Out-Null
$devices = adb devices
Write-Host ($devices -join [Environment]::NewLine)

Write-Host "[1/4] Installing debug APK..."
& adb install -r -t $ApkPath
if ($LASTEXITCODE -ne 0) { throw "adb install gagal." }

Write-Host "[2/4] Clearing old app state so frozen seed is imported cleanly..."
& adb shell pm clear $Package | Out-Null
if ($LASTEXITCODE -ne 0) { throw "pm clear gagal." }

Write-Host "[3/4] Launching ChatSim once..."
& adb shell monkey -p $Package -c android.intent.category.LAUNCHER 1 | Out-Null
Start-Sleep -Seconds 5

Write-Host "[4/4] Verifying private SQLite exists through run-as..."
$check = (& adb shell run-as $Package ls -l databases/libera_messages.db 2>&1) -join [Environment]::NewLine
if ($LASTEXITCODE -ne 0 -or $check -notmatch "libera_messages.db") {
    throw "Seed database belum tersedia. Buka ChatSim di emulator dan pastikan layar chat muncul, lalu ulangi verifikasi."
}
Write-Host $check

Write-Host ""
Write-Host "[PASS] ChatSim seeded on DEV-SIM-001." -ForegroundColor Green
Write-Host "Next dry-run acquisition + P5-P10:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\run_libera_demo.ps1 -DryRun"
Write-Host "Next real local Ollama run:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\run_libera_demo.ps1"
