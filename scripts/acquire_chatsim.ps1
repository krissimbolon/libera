param(
    [string]$OutputRoot = ".\\demo_evidence",
    [string]$Package = "id.libera.chatsim",
    [string]$AcquisitionId = "ACQ-001"
)

$ErrorActionPreference = "Stop"

function Need-Command($name) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
        throw "Command '$name' tidak ditemukan. Pastikan Android platform-tools/ADB ada di PATH."
    }
}

Need-Command adb

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$acqDir = Join-Path $OutputRoot ($AcquisitionId + "_" + $timestamp)
$masterDir = Join-Path $acqDir "master"
$workingDir = Join-Path $acqDir "working"
New-Item -ItemType Directory -Force -Path $masterDir, $workingDir | Out-Null

Write-Host "=== LIBERA DEV-001 Logical Acquisition ===" -ForegroundColor Cyan
adb wait-for-device | Out-Null

$serial = (adb get-serialno).Trim()
$model = (adb shell getprop ro.product.model).Trim()
$manufacturer = (adb shell getprop ro.product.manufacturer).Trim()
$androidVersion = (adb shell getprop ro.build.version.release).Trim()
$sdk = (adb shell getprop ro.build.version.sdk).Trim()
$adbVersion = ((adb version) -join " ").Trim()

Write-Host "Device: $manufacturer $model / Android $androidVersion (SDK $sdk)"
Write-Host "Serial: $serial"

adb shell am force-stop $Package | Out-Null

$dbCheck = (adb shell run-as $Package ls databases/libera_messages.db 2>&1) -join [Environment]::NewLine
if ($LASTEXITCODE -ne 0 -or $dbCheck -notmatch "libera_messages.db") {
    throw "Database tidak dapat diakses via run-as. Pastikan debug APK terpasang dan ChatSim sudah dibuka minimal sekali."
}

$masterDb = Join-Path $masterDir "libera_messages.db"
$cmd = 'adb exec-out run-as ' + $Package + ' cat databases/libera_messages.db > "' + $masterDb + '"'
cmd.exe /d /s /c $cmd
if ($LASTEXITCODE -ne 0) {
    throw "ADB acquisition gagal."
}

if (-not (Test-Path $masterDb) -or (Get-Item $masterDb).Length -eq 0) {
    throw "Acquired database kosong."
}

$masterHash = (Get-FileHash -Algorithm SHA256 $masterDb).Hash.ToLower()
$workingDb = Join-Path $workingDir "libera_messages.db"
Copy-Item $masterDb $workingDb
$workingHash = (Get-FileHash -Algorithm SHA256 $workingDb).Hash.ToLower()

if ($masterHash -ne $workingHash) {
    throw "Hash master dan working copy tidak cocok."
}

$packageDump = (adb shell dumpsys package $Package 2>&1) -join [Environment]::NewLine
$versionName = ""
if ($packageDump -match "versionName=([^\\s]+)") {
    $versionName = $Matches[1]
}

$manifest = [ordered]@{
    acquisition_id = $AcquisitionId
    device_id = "DEV-001"
    acquisition_type = "LOGICAL_APP_PRIVATE_FILE_COPY"
    research_simulation = $true
    package = $Package
    app_version = $versionName
    completed_at = (Get-Date).ToString("o")
    adb_serial = $serial
    manufacturer = $manufacturer
    model = $model
    android_version = $androidVersion
    android_sdk = $sdk
    adb_version = $adbVersion
    master_relative_path = "master/libera_messages.db"
    master_size_bytes = (Get-Item $masterDb).Length
    master_sha256 = $masterHash
    working_relative_path = "working/libera_messages.db"
    working_sha256 = $workingHash
    working_matches_master = ($masterHash -eq $workingHash)
    method_note = "Debug/research logical acquisition using adb exec-out + run-as against researcher-controlled LIBERA ChatSim. This is not physical or full-filesystem acquisition."
}

$manifestPath = Join-Path $acqDir "acquisition_manifest.json"
$manifest | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $manifestPath

$hashCsv = Join-Path $acqDir "sha256_manifest.csv"
"evidence_id,relative_path,size_bytes,sha256,copy_role,verified_against" | Set-Content -Encoding UTF8 $hashCsv
"$AcquisitionId,master/libera_messages.db,$((Get-Item $masterDb).Length),$masterHash,MASTER," | Add-Content -Encoding UTF8 $hashCsv
"$AcquisitionId,working/libera_messages.db,$((Get-Item $workingDb).Length),$workingHash,WORKING,master/libera_messages.db" | Add-Content -Encoding UTF8 $hashCsv

Write-Host ""
Write-Host "ACQUISITION COMPLETE" -ForegroundColor Green
Write-Host "Path    : $acqDir"
Write-Host "SHA-256 : $masterHash"
Write-Host "Master = Working: $($masterHash -eq $workingHash)"
Write-Host ""
Write-Host "Next:"
Write-Host ('python tools/extract_acquired_chatsim.py "' + $workingDb + '" --out "' + (Join-Path $acqDir "artifacts") + '"')
