# Modul ruangan: tambah, pilih, ubah, dan hapus ruangan
# Semua ruangan disimpan di satu list, tiap ruangan berupa dictionary, contoh:
# {"nama": "Kamar", "suhu_awal": 30.0, "orang": 2, "matahari": True,
#  "sirkulasi": False, "pk": "1", "mode": "Hemat",
#  "target_custom": None, "persen_custom": None}

import masukan
import tampilan
from perhitungan import DAFTAR_PK, DAFTAR_MODE


def nama_sudah_dipakai(daftar_ruangan, nama, kecuali=-1):
    # cek nama kembar, huruf besar/kecil dianggap sama
    # "kecuali" = ruangan yang lagi diubah, biar gak dianggap kembar sama dirinya sendiri
    for i in range(len(daftar_ruangan)):
        if i != kecuali and daftar_ruangan[i]["nama"].lower() == nama.lower():
            return True
    return False


def isi_data_ruangan(daftar_ruangan, lama=None, indeks_lama=-1):
    # minta data satu ruangan; kalau "lama" diisi, Enter = nilai lama dipakai
    if lama is None:
        lama = {"nama": None, "suhu_awal": None, "orang": None, "matahari": None,
                "sirkulasi": None, "pk": None, "mode": None,
                "target_custom": None, "persen_custom": None}

    nama = masukan.input_teks(" Nama ruangan", 15, lama["nama"])
    while nama_sudah_dipakai(daftar_ruangan, nama, indeks_lama):
        print("   Nama " + nama + " sudah ada. Pakai nama lain.")
        nama = masukan.input_teks(" Nama ruangan", 15, lama["nama"])

    suhu_awal = masukan.input_angka(" Suhu ruangan sekarang (C)", 10, 45, False, lama["suhu_awal"])
    orang = masukan.input_angka(" Jumlah orang di ruangan", 0, 20, True, lama["orang"])
    matahari = masukan.input_ya_tidak(" Kena sinar matahari langsung?", lama["matahari"])
    sirkulasi = masukan.input_ya_tidak(" Jendela/pintu sering dibuka?", lama["sirkulasi"])
    pk = masukan.input_pilihan(" Ukuran AC (0.5 / 1 / 1.5 / 2 PK)", DAFTAR_PK, lama["pk"])

    print("\n Mode AC:")
    print("   1 = Nyaman (target 24 C, AC boleh kerja penuh)")
    print("   2 = Hemat  (target 26 C, daya AC maksimal 60%)")
    print("   3 = Custom (target dan batas daya diatur sendiri)")
    nomor_lama = None
    if lama["mode"] is not None:
        nomor_lama = str(DAFTAR_MODE.index(lama["mode"]) + 1)
    nomor_mode = masukan.input_pilihan(" Pilih mode (1/2/3)", ["1", "2", "3"], nomor_lama)
    mode = DAFTAR_MODE[int(nomor_mode) - 1]

    target_custom = lama["target_custom"]
    persen_custom = lama["persen_custom"]
    if mode == "Custom":
        target_custom = masukan.input_angka(" Suhu target (18-30 C)", 18, 30, False, target_custom)
        persen_custom = masukan.input_angka(" Batas daya AC (30-100 %)", 30, 100, False, persen_custom)

    return {"nama": nama, "suhu_awal": suhu_awal, "orang": orang, "matahari": matahari,
            "sirkulasi": sirkulasi, "pk": pk, "mode": mode,
            "target_custom": target_custom, "persen_custom": persen_custom}


def isi_dan_cek(daftar_ruangan, judul, lama=None, indeks_lama=-1):
    # isi data, tampilkan lagi, lalu tanya mau disimpan atau nggak
    # hasilnya dictionary ruangan, atau None kalau batal
    while True:
        tampilan.layar_baru(judul)
        if lama is not None:
            print(" Tekan Enter kalau nilainya gak mau diubah.\n")
        baru = isi_data_ruangan(daftar_ruangan, lama, indeks_lama)

        print("\n Cek lagi datanya:")
        tampilan.cetak_data_satu_ruangan(baru)
        if masukan.input_ya_tidak(" Simpan data ini?", True):
            return baru
        if not masukan.input_ya_tidak(" Mau isi ulang?", True):
            return None


def tambah_ruangan(daftar_ruangan):
    baru = isi_dan_cek(daftar_ruangan, "Tambah ruangan ke-" + str(len(daftar_ruangan) + 1))
    if baru is None:
        print("\n Oke, ruangan gak jadi ditambah.")
        return
    tampilan.loading("Menyimpan")
    daftar_ruangan.append(baru)
    print(" " + baru["nama"], "sudah ditambahkan.")


def pilih_ruangan(daftar_ruangan, judul, pesan, boleh_semua=False):
    # hasilnya index ruangan, -1 kalau pilih semua, atau None kalau list masih kosong
    tampilan.layar_baru(judul)
    if len(daftar_ruangan) == 0:
        print(" Belum ada ruangan. Tambahkan dulu lewat menu 1.")
        return None

    tampilan.cetak_daftar_ruangan(daftar_ruangan)
    if boleh_semua:
        nomor = masukan.input_angka(pesan + " (0 = semua)", 0, len(daftar_ruangan), True)
    else:
        nomor = masukan.input_angka(pesan, 1, len(daftar_ruangan), True)
    return nomor - 1


def lihat_ruangan(daftar_ruangan):
    tampilan.layar_baru("Daftar ruangan")
    tampilan.cetak_daftar_ruangan(daftar_ruangan)


def ubah_ruangan(daftar_ruangan):
    indeks = pilih_ruangan(daftar_ruangan, "Ubah data ruangan", " Nomor ruangan yang mau diubah")
    if indeks is None:
        return
    lama = daftar_ruangan[indeks]
    baru = isi_dan_cek(daftar_ruangan, "Ubah " + lama["nama"], lama, indeks)
    if baru is None:
        print("\n Oke, data " + lama["nama"] + " gak diubah.")
        return
    tampilan.loading("Menyimpan perubahan")
    daftar_ruangan[indeks] = baru
    print(" Data " + baru["nama"] + " sudah diperbarui.")


def hapus_ruangan(daftar_ruangan):
    indeks = pilih_ruangan(daftar_ruangan, "Hapus ruangan", " Nomor ruangan yang mau dihapus")
    if indeks is None:
        return
    nama = daftar_ruangan[indeks]["nama"]
    if masukan.input_ya_tidak(" Yakin mau hapus " + nama + "?"):
        tampilan.loading("Menghapus")
        daftar_ruangan.pop(indeks)
        print(" " + nama + " sudah dihapus.")
    else:
        print(" Oke, gak jadi dihapus.")


def contoh_ruangan():
    # 3 ruangan contoh biar bisa langsung dicoba
    return [
        {"nama": "Kamar Tidur", "suhu_awal": 29.0, "orang": 2, "matahari": False,
         "sirkulasi": False, "pk": "1", "mode": "Hemat",
         "target_custom": None, "persen_custom": None},
        {"nama": "Ruang Tamu", "suhu_awal": 31.0, "orang": 4, "matahari": True,
         "sirkulasi": True, "pk": "1.5", "mode": "Nyaman",
         "target_custom": None, "persen_custom": None},
        {"nama": "Ruang Kerja", "suhu_awal": 30.0, "orang": 1, "matahari": True,
         "sirkulasi": False, "pk": "1", "mode": "Custom",
         "target_custom": 25.0, "persen_custom": 80.0},
    ]
