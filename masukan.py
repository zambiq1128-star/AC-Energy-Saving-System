# Modul masukan: semua input dari pengguna dicek di sini
# Kalau ada "default", tekan Enter aja buat pakai nilai itu


def adalah_angka(teks):
    # boleh desimal, pakai titik atau koma
    teks = teks.replace(",", ".")
    return teks.replace(".", "", 1).isdigit()


def input_angka(pesan, minimum, maksimum, bulat=False, default=None):
    if default is not None:
        pesan = pesan + " [Enter = " + str(default) + "]"
    pesan = pesan + ": "

    # ulangi terus sampai angkanya benar
    while True:
        teks = input(pesan).strip()

        if teks == "" and default is not None:
            return default

        if bulat:
            valid = teks.isdigit()
        else:
            valid = adalah_angka(teks)

        if valid:
            angka = float(teks.replace(",", "."))
            if angka >= minimum and angka <= maksimum:
                if bulat:
                    return int(angka)
                return angka

        if bulat:
            print("   Isinya harus angka bulat " + str(minimum) + " sampai " + str(maksimum) + ". Coba lagi.")
        else:
            print("   Isinya harus angka " + str(minimum) + " sampai " + str(maksimum) + ". Coba lagi.")


def input_pilihan(pesan, daftar_pilihan, default=None):
    # jawabannya harus salah satu isi list, misalnya ["1", "2", "3"]
    if default is not None:
        pesan = pesan + " [Enter = " + str(default) + "]"
    pesan = pesan + ": "

    while True:
        teks = input(pesan).strip()
        if teks == "" and default is not None:
            return default
        if teks in daftar_pilihan:
            return teks
        print("   Pilihannya cuma " + ", ".join(daftar_pilihan) + ". Coba lagi.")


def input_ya_tidak(pesan, default=None):
    # hasilnya True kalau y, False kalau n
    if default is None:
        pesan = pesan + " (y/n): "
    elif default:
        pesan = pesan + " (y/n) [Enter = y]: "
    else:
        pesan = pesan + " (y/n) [Enter = n]: "

    while True:
        teks = input(pesan).strip().lower()
        if teks == "" and default is not None:
            return default
        if teks == "y":
            return True
        if teks == "n":
            return False
        print("   Jawab y atau n aja.")


def input_teks(pesan, panjang_maks=15, default=None):
    # teks gak boleh kosong dan gak boleh kepanjangan (biar tabel tetap rapi)
    if default is not None:
        pesan = pesan + " [Enter = " + default + "]"
    pesan = pesan + ": "

    while True:
        teks = input(pesan).strip()
        if teks == "" and default is not None:
            return default
        if teks == "":
            print("   Belum diisi. Coba lagi.")
        elif len(teks) > panjang_maks:
            print("   Kepanjangan, maksimal " + str(panjang_maks) + " huruf.")
        else:
            return teks


def tunggu_enter():
    input("\n Tekan Enter untuk kembali ke menu...")


def tunggu_lanjut():
    input("\n Tekan Enter untuk lanjut...")
