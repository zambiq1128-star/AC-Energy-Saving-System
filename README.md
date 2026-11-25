# Automatic AC Energy Saving System (Multi Ruangan)

Program projek II Kelompok 7 WI1102. Ini lanjutan dari program projek I, jadi rumus
simulasinya masih sama. Yang baru:

- Bisa banyak ruangan sekaligus. Ruangannya bisa ditambah, dilihat, diubah, dan dihapus.
- Suhu luar per jam diambil dari internet lewat Open-Meteo (gratis, tanpa API key).
- Biaya dihitung per ruangan, lalu dijumlah. Ada juga info ruangan paling boros dan
  perbandingan kalau semua ruangan pakai mode Nyaman atau Hemat.
- Kodenya dipecah jadi fungsi-fungsi di beberapa file.

## Cara menjalankan

1. Extract zip-nya. Semua file `.py` harus ada di folder yang sama.
2. Install library `requests` (cukup sekali):
   ```
   pip install -r requirements.txt
   ```
3. Jalankan:
   ```
   python main.py
   ```

Kalau gak ada internet atau `requests` belum ter-install, program tetap bisa dipakai.
Nanti ada pilihan pakai data contoh atau isi 4 suhu rata-rata sendiri (cara projek I).

## Isi tiap file

| File | Isinya | Fungsi |
|---|---|---|
| `main.py` | Alur program dan menu utama | `main`, `siapkan_cuaca`, `menu_simulasi`, `menu_ringkasan`, `menu_pengaturan` |
| `masukan.py` | Cek semua input pengguna | `adalah_angka`, `input_angka`, `input_pilihan`, `input_ya_tidak`, `input_teks`, `tunggu_enter`, `tunggu_lanjut` |
| `cuaca.py` | Suhu luar 24 jam | `cari_kota`, `ambil_suhu_hari_ini`, `suhu_default`, `interpolasi_suhu` |
| `perhitungan.py` | Rumus simulasi dari projek I | `data_ac`, `hitung_k`, `hitung_panas_bangunan`, `atur_mode`, `hitung_daya_ac`, `hitung_kwh`, `tentukan_status`, `simulasi_ruangan`, `statistik_suhu`, `simulasi_semua`, `indeks_paling_boros` |
| `ruangan.py` | Kelola list ruangan | `nama_sudah_dipakai`, `isi_data_ruangan`, `isi_dan_cek`, `tambah_ruangan`, `pilih_ruangan`, `lihat_ruangan`, `ubah_ruangan`, `hapus_ruangan`, `contoh_ruangan` |
| `tampilan.py` | Semua yang muncul di layar | `bersihkan_layar`, `ketik_pelan`, `loading`, `garis`, `judul`, `layar_baru`, `rupiah`, `rupiah_kolom`, `bar`, `cetak_menu`, `cetak_grafik_suhu_luar`, `cetak_daftar_ruangan`, `cetak_data_satu_ruangan`, `cetak_tabel_simulasi`, `cetak_ringkasan`, `cetak_perbandingan` |

## Menu

1. Tambah ruangan
2. Lihat daftar ruangan
3. Ubah data ruangan (tekan Enter kalau nilainya gak mau diubah)
4. Hapus ruangan
5. Simulasi 24 jam, bisa satu ruangan atau semua (ketik 0)
6. Ringkasan biaya dan perbandingan Nyaman vs Hemat
7. Grafik suhu luar per jam
8. Pengaturan: lokasi, tarif listrik, jam mulai
0. Keluar

## Catatan

- Biaya sebulan dihitung dari biaya sehari dikali 30, sama kayak projek I.
- Kalau bar `█░` kelihatan aneh di terminal, ganti `BLOK_ISI` dan `BLOK_KOSONG` di
  `tampilan.py` jadi `"#"` dan `"."`.
- Layar dibersihkan tiap pindah menu. Kalau dijalankan dari IDE yang terminalnya gak
  bisa dibersihkan (misalnya IDLE), program tetap jalan, cuma layarnya gak bersih.
