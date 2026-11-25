# Modul tampilan: semua urusan cetak ke layar ada di sini
# (bersihin layar, judul, tabel, bar, format rupiah)

import os
import time

LEBAR = 78
BLOK_ISI = "█"      # kalau di terminal muncul aneh, ganti jadi "#"
BLOK_KOSONG = "░"   # ... dan yang ini jadi "."


# ---------- alat bantu tampilan ----------

def bersihkan_layar():
    # Windows pakai "cls", Mac/Linux pakai "clear"
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def ketik_pelan(teks, jeda=0.03):
    # efek teks berjalan dari projek I
    for huruf in teks:
        print(huruf, end="", flush=True)
        time.sleep(jeda)
    print()


def loading(pesan):
    # pesan singkat + titik-titik, biar ada jeda sebelum hasil muncul
    print("\n " + pesan, end="", flush=True)
    for i in range(3):
        time.sleep(0.4)
        print(".", end="", flush=True)
    print()
    time.sleep(0.4)


def garis(simbol="-"):
    print(simbol * LEBAR)


def judul(teks):
    garis("=")
    print(teks.upper().center(LEBAR))
    garis("=")


def layar_baru(teks_judul):
    # setiap pindah layar: bersihin dulu, baru tulis judul
    bersihkan_layar()
    judul(teks_judul)


def rupiah(angka):
    # 1234567.8 jadi "Rp 1.234.568"
    teks = format(round(angka), ",").replace(",", ".")
    return "Rp " + teks


def rupiah_kolom(angka, lebar):
    # sama kayak rupiah(), tapi rata kanan buat tabel
    teks = format(round(angka), ",").replace(",", ".")
    return "Rp " + teks.rjust(lebar - 3)


def bar(nilai, maksimum, panjang=10):
    # contoh: bar(3, 10) jadi "███░░░░░░░"
    if maksimum <= 0:
        isi = 0
    else:
        isi = round(nilai / maksimum * panjang)
    if isi > panjang:
        isi = panjang
    if isi < 0:
        isi = 0
    return BLOK_ISI * isi + BLOK_KOSONG * (panjang - isi)


def ya_tidak(nilai):
    if nilai:
        return "Ya"
    return "Tidak"


def teks_mode(ruangan):
    # mode Custom ikut ditulis target dan batas dayanya
    if ruangan["mode"] == "Custom":
        return "Custom " + str(ruangan["target_custom"]) + "C/" + str(round(ruangan["persen_custom"])) + "%"
    return ruangan["mode"]


# ---------- menu dan data ----------

def cetak_menu(pengaturan, jumlah_ruangan):
    layar_baru("Automatic AC Energy Saving System")
    suhu = pengaturan["suhu_luar"]
    print(" Lokasi      :", pengaturan["kota"], "(" + pengaturan["sumber"] + ")")
    print(" Suhu luar   :", min(suhu), "sampai", max(suhu), "C")
    print(" Tarif       : Rp", pengaturan["tarif"], "per kWh")
    print(" Mulai jam   :", str(pengaturan["jam_mulai"]).zfill(2) + ".00")
    print(" Ruangan     :", jumlah_ruangan)
    garis()
    print("  1. Tambah ruangan")
    print("  2. Lihat daftar ruangan")
    print("  3. Ubah data ruangan")
    print("  4. Hapus ruangan")
    print("  5. Simulasi 24 jam")
    print("  6. Ringkasan biaya dan perbandingan Nyaman vs Hemat")
    print("  7. Grafik suhu luar per jam")
    print("  8. Pengaturan (lokasi, tarif, jam mulai)")
    print("  0. Keluar")
    garis()


def cetak_grafik_suhu_luar(pengaturan):
    suhu_luar = pengaturan["suhu_luar"]
    layar_baru("Suhu luar per jam")
    print(" " + pengaturan["kota"], "(" + pengaturan["sumber"] + ")")
    garis()
    terendah = min(suhu_luar)
    tertinggi = max(suhu_luar)
    for jam in range(24):
        # bar dihitung mulai dari (terendah - 1) biar bedanya kelihatan
        panjang_bar = bar(suhu_luar[jam] - (terendah - 1), tertinggi - (terendah - 1), 40)
        keterangan = ""
        if suhu_luar[jam] == tertinggi:
            keterangan = "  paling panas"
        elif suhu_luar[jam] == terendah:
            keterangan = "  paling dingin"
        print(" " + str(jam).zfill(2) + ".00 |", str(suhu_luar[jam]).rjust(4), "C |", panjang_bar + keterangan)
        time.sleep(0.03)
    garis()


def cetak_daftar_ruangan(daftar_ruangan):
    if len(daftar_ruangan) == 0:
        print(" Belum ada ruangan. Tambahkan dulu lewat menu 1.")
        return
    print(" No | Nama ruangan    | Suhu awal | Orang | Matahari | Jendela | AC     | Mode")
    garis()
    for i in range(len(daftar_ruangan)):
        r = daftar_ruangan[i]
        print(" " + str(i + 1).rjust(2), "|", r["nama"].ljust(15), "|",
              (str(r["suhu_awal"]) + " C").rjust(9), "|", str(r["orang"]).rjust(5), "|",
              ya_tidak(r["matahari"]).ljust(8), "|", ya_tidak(r["sirkulasi"]).ljust(7), "|",
              (r["pk"] + " PK").ljust(6), "|", teks_mode(r))
    garis()


def cetak_data_satu_ruangan(r):
    # dipakai buat cek ulang sebelum data disimpan
    garis()
    print(" Nama ruangan   :", r["nama"])
    print(" Suhu sekarang  :", r["suhu_awal"], "C")
    print(" Jumlah orang   :", r["orang"])
    print(" Kena matahari  :", ya_tidak(r["matahari"]))
    print(" Jendela dibuka :", ya_tidak(r["sirkulasi"]))
    print(" Ukuran AC      :", r["pk"], "PK")
    print(" Mode           :", teks_mode(r))
    garis()


# ---------- hasil simulasi ----------

def cetak_tabel_simulasi(hasil):
    layar_baru("Simulasi " + hasil["nama"] + " (mode " + hasil["mode"] + ")")
    print(" Target", hasil["target"], "C | k =", round(hasil["k"], 2), "| Orang:", hasil["orang"])
    garis()
    print(" Jam   | Luar | Ruang | Daya AC         | Status  |    Biaya")
    garis()
    for baris in hasil["tabel_jam"]:
        jam, luar, ruang, persen, status, biaya = baris
        teks_jam = str(jam).zfill(2) + ".00"
        teks_daya = bar(persen, 100) + " " + (str(round(persen)) + "%").rjust(4)
        print(" " + teks_jam, "|", str(luar).rjust(4), "|", str(round(ruang, 1)).rjust(5), "|",
              teks_daya, "|", status.ljust(7), "|", rupiah_kolom(biaya, 8))
        time.sleep(0.04)  # baris muncul satu per satu, kayak jam yang jalan
    garis()
    print(" Rata-rata suhu ruangan :", round(hasil["rata_rata"], 1), "C",
          "(terendah", str(round(hasil["terendah"], 1)) + ", tertinggi", str(round(hasil["tertinggi"], 1)) + ")")
    print(" Energi sehari          :", round(hasil["kwh_hari"], 2), "kWh")
    print(" Biaya sehari           :", rupiah(hasil["biaya_hari"]))
    print(" Kira-kira sebulan      :", rupiah(hasil["biaya_bulan"]))
    if hasil["tertinggi"] > hasil["target"] + 1:
        print(" Catatan: AC kurang kuat di jam terpanas, suhu sempat di atas target.")


def cetak_ringkasan(daftar_hasil, indeks_boros):
    layar_baru("Ringkasan biaya per ruangan")
    total_kwh = 0
    total_hari = 0
    total_bulan = 0
    for hasil in daftar_hasil:
        total_kwh += hasil["kwh_hari"]
        total_hari += hasil["biaya_hari"]
        total_bulan += hasil["biaya_bulan"]

    print(" Ruangan         | Mode    | kWh/hari |  Biaya/hari  |  Biaya/bulan  | Porsi")
    garis()
    for i in range(len(daftar_hasil)):
        hasil = daftar_hasil[i]
        if total_hari > 0:
            porsi = hasil["biaya_hari"] / total_hari * 100
        else:
            porsi = 0
        tanda = ""
        if i == indeks_boros:
            tanda = " *"
        print(" " + hasil["nama"].ljust(15), "|", hasil["mode"].ljust(7), "|",
              str(round(hasil["kwh_hari"], 2)).rjust(8), "|", rupiah_kolom(hasil["biaya_hari"], 12), "|",
              rupiah_kolom(hasil["biaya_bulan"], 13), "|", bar(porsi, 100, 8), (str(round(porsi)) + "%").rjust(4) + tanda)
        time.sleep(0.1)
    garis()
    print(" " + "TOTAL".ljust(15), "|", "".ljust(7), "|", str(round(total_kwh, 2)).rjust(8), "|",
          rupiah_kolom(total_hari, 12), "|", rupiah_kolom(total_bulan, 13), "|")
    garis("=")
    boros = daftar_hasil[indeks_boros]
    print(" * Paling boros:", boros["nama"] + ",", rupiah(boros["biaya_bulan"]), "per bulan.")


def cetak_perbandingan(hasil_nyaman, hasil_hemat):
    layar_baru("Kalau semua Nyaman vs semua Hemat")
    print(" Ruangan         | Suhu N/H    | Nyaman/bulan | Hemat/bulan  | Lebih hemat")
    garis()
    total_nyaman = 0
    total_hemat = 0
    for i in range(len(hasil_nyaman)):
        n = hasil_nyaman[i]
        h = hasil_hemat[i]
        selisih = n["biaya_bulan"] - h["biaya_bulan"]
        if n["biaya_bulan"] > 0:
            persen = selisih / n["biaya_bulan"] * 100
        else:
            persen = 0
        teks_suhu = str(round(n["rata_rata"], 1)) + "/" + str(round(h["rata_rata"], 1)) + "C"
        print(" " + n["nama"].ljust(15), "|", teks_suhu.ljust(11), "|", rupiah_kolom(n["biaya_bulan"], 12), "|",
              rupiah_kolom(h["biaya_bulan"], 12), "|", bar(persen, 100, 10), (str(round(persen)) + "%").rjust(4))
        total_nyaman += n["biaya_bulan"]
        total_hemat += h["biaya_bulan"]
        time.sleep(0.1)
    garis()
    total_selisih = total_nyaman - total_hemat
    if total_nyaman > 0:
        total_persen = total_selisih / total_nyaman * 100
    else:
        total_persen = 0
    print(" " + "TOTAL".ljust(15), "|", "".ljust(11), "|", rupiah_kolom(total_nyaman, 12), "|",
          rupiah_kolom(total_hemat, 12), "|", bar(total_persen, 100, 10), (str(round(total_persen)) + "%").rjust(4))
    garis("=")

    # kalimat kesimpulan
    print(" Kalau semua ruangan pakai mode Hemat, tagihan AC turun " + rupiah(total_selisih))
    print(" per bulan (" + str(round(total_persen)) + "%), atau sekitar " + rupiah(total_selisih * 12) + " setahun.")
    print(" Ruangannya memang jadi sedikit lebih hangat, sekitar 26 C, bukan 24 C.")
