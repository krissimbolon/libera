param(
    [string]$Root = "D:\\KSI\\Libera Private Evidence"
)

$folders = @(
    "07_P3_forensik",
    "07_P3_forensik\\01_master_evidence",
    "07_P3_forensik\\02_working_copy",
    "07_P3_forensik\\03_acquisition_logs",
    "07_P3_forensik\\04_hash_manifest",
    "07_P3_forensik\\05_photos_device",
    "07_P3_forensik\\06_chain_of_custody",
    "07_P3_forensik\\07_dry_run",
    "07_P3_forensik\\08_tool_versions",
    "07_P3_forensik\\09_simulasi_whatsapp"
)

foreach ($folder in $folders) {
    $path = Join-Path $Root $folder
    New-Item -ItemType Directory -Force -Path $path | Out-Null
}

Write-Host "Struktur P3 siap di: $Root\\07_P3_forensik"
