# Automatic AC Energy Saving System - Multi Ruangan (Projek II)
# Kelompok 7 WI1102, lanjutan program projek I
# coded by cluny(!?)
#
# File ini cuma ngatur alur menu. Sisanya ada di modul lain:
#   masukan.py     cek input
#   cuaca.py       suhu luar per jam (Open-Meteo + cadangan)
#   perhitungan.py simulasi AC, listrik, biaya
#   ruangan.py     tambah / ubah / hapus ruangan
#   tampilan.py    layar, tabel, bar, rupiah

import time

import cuaca
import masukan
import perhitungan
import ruangan
import tampilan


def siapkan_cuaca(pengaturan):
    # coba ambil dari internet dulu, kalau gagal pakai cadangan
    tampilan.layar_baru("Data cuaca")
    kota = masukan.input_teks(" Kota tempat ruangan berada", 40, "Bandung")
    tampilan.loading("Mengambil prakiraan suhu " + kota)

    hasil_kota = cuaca.cari_kota(kota)
    if hasil_kota is not None:
        nama_lengkap, lintang, bujur = hasil_kota
        suhu_luar = cuaca.ambil_suhu_hari_ini(lintang, bujur)
        if suhu_luar is not None:
            pengaturan["kota"] = nama_lengkap
            pengaturan["suhu_luar"] = suhu_luar
            pengaturan["sumber"] = "Open-Meteo, hari ini"
            print(" Dapat. Suhu di " + nama_lengkap + " hari ini " + str(min(suhu_luar)) + " sampai " + str(max(suhu_luar)) + " C.")
            masukan.tunggu_lanjut()
            return

    # sampai sini berarti gagal
    print(" Data cuaca online gagal diambil.")
    if cuaca.requests is None:
        print(" Library requests belum ter-install (pip install requests).")
    else:
        print(" Coba cek internet atau ejaan nama kotanya.")
    print("\n Pakai data cadangan aja:")
    print("   1 = Data contoh (hari cerah di Bandung)")
    print("   2 = Isi 4 suhu rata-rata sendiri (cara projek I)")
    print("   3 = Coba lagi atau ganti kota")
    pilihan = masukan.input_pilihan(" Pilih (1/2/3)", ["1", "2", "3"])

    if pilihan == "1":
        pengaturan["kota"] = "Bandung"
        pengaturan["suhu_luar"] = cuaca.suhu_default()
        pengaturan["sumber"] = "data contoh"
        print("\n Oke, pakai data contoh Bandung.")
        masukan.tunggu_lanjut()
    elif pilihan == "2":
        pagi = masukan.input_angka(" Rata-rata suhu pagi (05.00-10.59)", 10, 45)
        siang = masukan.input_angka(" Rata-rata suhu siang (11.00-14.59)", 10, 45)
        sore = masukan.input_angka(" Rata-rata suhu sore (15.00-17.59)", 10, 45)
        malam = masukan.input_angka(" Rata-rata suhu malam (18.00-04.59)", 10, 45)
        pengaturan["kota"] = kota
        pengaturan["suhu_luar"] = cuaca.interpolasi_suhu(pagi, siang, sore, malam)
        pengaturan["sumber"] = "isi sendiri"
        print("\n Oke, suhu per jam sudah dihitung dari 4 suhu tadi.")
        masukan.tunggu_lanjut()
    else:
        siapkan_cuaca(pengaturan)  # ulang dari awal


def menu_simulasi(daftar_ruangan, pengaturan):
    indeks = ruangan.pilih_ruangan(daftar_ruangan, "Simulasi 24 jam", " Nomor ruangan yang mau disimulasikan", True)
    if indeks is None:
        return

    if indeks == -1:
        dipilih = daftar_ruangan  # semua ruangan
    else:
        dipilih = [daftar_ruangan[indeks]]  # satu ruangan, tapi tetap dalam list

    tampilan.loading("Menghitung simulasi")
    daftar_hasil = perhitungan.simulasi_semua(dipilih, pengaturan["suhu_luar"],
                                              pengaturan["jam_mulai"], pengaturan["tarif"])

    # satu layar per ruangan
    for i in range(len(daftar_hasil)):
        tampilan.cetak_tabel_simulasi(daftar_hasil[i])
        if i < len(daftar_hasil) - 1:
            masukan.tunggu_lanjut()

    # kalau lebih dari satu ruangan, tutup dengan ringkasan
    if len(daftar_hasil) > 1:
        masukan.tunggu_lanjut()
        tampilan.cetak_ringkasan(daftar_hasil, perhitungan.indeks_paling_boros(daftar_hasil))


def menu_ringkasan(daftar_ruangan, pengaturan):
    if len(daftar_ruangan) == 0:
        tampilan.layar_baru("Ringkasan biaya")
        print(" Belum ada ruangan. Tambahkan dulu lewat menu 1.")
        return

    suhu_luar = pengaturan["suhu_luar"]
    jam_mulai = pengaturan["jam_mulai"]
    tarif = pengaturan["tarif"]

    tampilan.loading("Menghitung biaya semua ruangan")

    # biaya pakai mode pilihan tiap ruangan
    hasil_pilihan = perhitungan.simulasi_semua(daftar_ruangan, suhu_luar, jam_mulai, tarif)
    tampilan.cetak_ringkasan(hasil_pilihan, perhitungan.indeks_paling_boros(hasil_pilihan))
    masukan.tunggu_lanjut()

    # bandingkan kalau semua Nyaman vs semua Hemat
    hasil_nyaman = perhitungan.simulasi_semua(daftar_ruangan, suhu_luar, jam_mulai, tarif, "Nyaman")
    hasil_hemat = perhitungan.simulasi_semua(daftar_ruangan, suhu_luar, jam_mulai, tarif, "Hemat")
    tampilan.cetak_perbandingan(hasil_nyaman, hasil_hemat)


def menu_pengaturan(pengaturan):
    tampilan.layar_baru("Pengaturan")
    print("  1 = Ganti lokasi / ambil ulang data cuaca")
    print("  2 = Ganti tarif listrik (sekarang Rp " + str(pengaturan["tarif"]) + " per kWh)")
    print("  3 = Ganti jam mulai simulasi (sekarang jam " + str(pengaturan["jam_mulai"]).zfill(2) + ".00)")
    print("  0 = Kembali")
    pilihan = masukan.input_pilihan(" Pilih", ["1", "2", "3", "0"])

    if pilihan == "1":
        siapkan_cuaca(pengaturan)
    elif pilihan == "2":
        pengaturan["tarif"] = masukan.input_angka(" Tarif listrik per kWh (Rp)", 1, 10000, False, pengaturan["tarif"])
        tampilan.loading("Menyimpan")
        print(" Tarif sekarang Rp " + str(pengaturan["tarif"]) + " per kWh.")
        masukan.tunggu_enter()
    elif pilihan == "3":
        pengaturan["jam_mulai"] = masukan.input_angka(" Simulasi mulai jam (0-23)", 0, 23, True, pengaturan["jam_mulai"])
        tampilan.loading("Menyimpan")
        print(" Simulasi sekarang mulai jam " + str(pengaturan["jam_mulai"]).zfill(2) + ".00.")
        masukan.tunggu_enter()


def main():
    tampilan.bersihkan_layar()
    tampilan.ketik_pelan("Beep..\nBeep..\n\nAutomatic AC Energy Saving System (Multi Ruangan) successfully loaded")
    masukan.tunggu_lanjut()

    # pengaturan yang sama untuk semua ruangan
    pengaturan = {"kota": "", "suhu_luar": [], "sumber": "", "tarif": 0, "jam_mulai": 0}
    daftar_ruangan = []

    siapkan_cuaca(pengaturan)

    tampilan.layar_baru("Tarif listrik dan jam mulai")
    pengaturan["tarif"] = masukan.input_angka(" Tarif listrik per kWh (Rp)", 1, 10000, False, 1444.70)
    jam_sekarang = time.localtime().tm_hour
    pengaturan["jam_mulai"] = masukan.input_angka(" Simulasi mulai jam (0-23)", 0, 23, True, jam_sekarang)

    if masukan.input_ya_tidak("\n Mau langsung pakai 3 ruangan contoh?", True):
        daftar_ruangan = ruangan.contoh_ruangan()
        tampilan.loading("Memuat ruangan contoh")
        print(" Kamar Tidur, Ruang Tamu, dan Ruang Kerja sudah siap.")
    else:
        print("\n Oke, mulai dari daftar ruangan kosong.")
    masukan.tunggu_lanjut()

    # loop menu utama
    pilihan = ""
    while pilihan != "0":
        tampilan.cetak_menu(pengaturan, len(daftar_ruangan))
        pilihan = masukan.input_pilihan(" Pilih menu", ["1", "2", "3", "4", "5", "6", "7", "8", "0"])

        if pilihan == "1":
            ruangan.tambah_ruangan(daftar_ruangan)
        elif pilihan == "2":
            ruangan.lihat_ruangan(daftar_ruangan)
        elif pilihan == "3":
            ruangan.ubah_ruangan(daftar_ruangan)
        elif pilihan == "4":
            ruangan.hapus_ruangan(daftar_ruangan)
        elif pilihan == "5":
            menu_simulasi(daftar_ruangan, pengaturan)
        elif pilihan == "6":
            menu_ringkasan(daftar_ruangan, pengaturan)
        elif pilihan == "7":
            tampilan.cetak_grafik_suhu_luar(pengaturan)
        elif pilihan == "8":
            menu_pengaturan(pengaturan)

        # menu 8 balik sendiri, sisanya tunggu Enter dulu
        if pilihan != "0" and pilihan != "8":
            masukan.tunggu_enter()

    tampilan.bersihkan_layar()
    tampilan.ketik_pelan("~~~ Terima kasih sudah pakai Automatic AC Energy Saving System :)")


# program mulai dari sini
main()
