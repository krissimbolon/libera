# Peta Lokalisasi Kasus Galloway ke Skenario Indonesia

Dokumen ini menetapkan transformasi P2. Semua identitas pada dataset adaptasi bersifat fiktif dan tidak merujuk pada orang nyata.

## Prinsip
- struktur relasi dan pola peristiwa mengikuti kasus Galloway;
- nama, lokasi, nomor telepon, hotel, alamat, dan platform dilokalisasi/fiktifkan;
- tidak menambahkan tindak pidana utama baru di luar desain sumber;
- pesan yang benar-benar berasal dari line Exhibit 1A tetap memiliki `source_original_line`;
- pesan tambahan diberi provenance `SYNTHETIC_BRIDGE`, `SYNTHETIC_CONTEXT`, atau `SYNTHETIC_DISTRACTOR`;
- konten eksplisit yang tidak diperlukan untuk tujuan forensik disanitasi, terutama untuk aktor di bawah umur.

## Latar geografis
- Negara: Indonesia
- Wilayah utama: Bandung Raya, Jawa Barat
- Alamat spesifik, nama hotel, dan tempat usaha: fiktif
- Lokasi yang dipakai hanya cukup rinci untuk timeline/forensic reasoning; tidak menggunakan alamat pribadi nyata.

## Transformasi aktor
| Aktor sumber | Aktor adaptasi | Peran |
|---|---|---|
| Cornelius “Chip” Galloway | Raka Pradana | pengendali/koordinator utama |
| Danielle Galloway | Dini Pradana | koordinator/logistik |
| Marcus Taylor | Reza Mahendra | transportasi/koordinasi |
| Matthew Woods “Staxx” | Bagas “Bags” Wicaksono | enforcer/anggota kelompok |
| K.T. | Kirana | korban dewasa |
| T.S. | Tania | korban dewasa |
| M.V. | Maya | korban dewasa |
| Juvenile J | Jihan | korban di bawah umur; konten seksual eksplisit tidak dibuat |
| Juvenile M | Mila | korban di bawah umur; konten seksual eksplisit tidak dibuat |
| Renee | Rena | korban/aktor tambahan |
| Renee 2 | Nara | korban/aktor tambahan |
| Chocolate | Caca | aktor tambahan |
| unknown john/buyer | Kontak Tidak Dikenal ### | calon pelanggan fiktif |

## Transformasi objek/lokasi
| Unsur sumber | Adaptasi Indonesia |
|---|---|
| Albuquerque, New Mexico | Bandung Raya, Jawa Barat |
| Howard Johnson Inn | Hotel Puspa (fiktif) |
| Motel 6 / lokasi hotel lain | Penginapan Meranti (fiktif) |
| Third Street residence | rumah kontrakan fiktif di Bandung |
| Backpage.com | Forum Iklan X (fiktif) |
| Booking.com record | catatan platform pemesanan hotel |
| nomor telepon AS | nomor uji/fiktif Indonesia |
| USD | rupiah |

## Batas transformasi
Lokalisasi tidak boleh:
- mengaitkan kasus dengan hotel/usaha/orang nyata di Indonesia;
- membuat alamat operasional nyata;
- memperkenalkan korban atau tindak pidana utama baru sebagai fakta;
- mengubah struktur event utama hanya untuk mencapai 10.000 baris.

Pesan tambahan untuk mencapai 10.000 berfungsi sebagai konteks, bridge, atau distractor dalam semesta kasus yang sama.
