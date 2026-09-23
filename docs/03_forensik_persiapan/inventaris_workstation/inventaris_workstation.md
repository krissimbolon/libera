# Inventaris Workstation Forensik

## Sistem Operasi

Hasil command:

`Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber, OsArchitecture`

- WindowsProductName: **Windows 10 Home Single Language**
- WindowsVersion: **2009**
- OsBuildNumber: **26200**
- OsArchitecture: **64-bit**

Catatan:
- Nilai di atas dicatat persis dari output PowerShell untuk reproducibility.
- Tidak dilakukan normalisasi atau koreksi nama produk OS pada tahap inventaris ini.

## Runtime / tooling

- ADB: sudah didokumentasikan pada `../tooling/README.md`.
- Python command `python --version`: **TIDAK TERSEDIA**
- Output Windows: `Python was not found; run without arguments to install from the Microsoft Store...`
- Python launcher `py --version`: **TIDAK TERSEDIA** (`CommandNotFoundException`).
- Python launcher `py --version`: **Python 3.14.7** setelah pemasangan Python Install Manager.
- Kesimpulan: **Python runtime tersedia dan dapat dipanggil melalui launcher `py`**.
- Hashing tool: **BELUM DIKUNCI**.
- Acquisition tool: **BELUM DIKUNCI**.
- Extraction tool: **BELUM DIKUNCI**.
