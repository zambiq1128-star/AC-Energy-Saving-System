# Modul perhitungan: rumus simulasi dari projek I, dipecah jadi fungsi kecil
# Modul ini gak minta input dan gak nge-print, cuma ngitung lalu return hasil

# data AC per ukuran PK (urutan index-nya sama)
# watt = listrik yang dipakai saat AC kerja penuh
# kapasitas = berapa derajat C per jam yang bisa diturunkan AC saat kerja penuh
DAFTAR_PK = ["0.5", "1", "1.5", "2"]
DAFTAR_WATT = [400, 800, 1200, 1700]
DAFTAR_KAPASITAS = [3.0, 5.0, 7.0, 9.0]

DAFTAR_MODE = ["Nyaman", "Hemat", "Custom"]


def data_ac(pk):
    # cari watt dan kapasitas sesuai PK
    for i in range(len(DAFTAR_PK)):
        if DAFTAR_PK[i] == pk:
            return DAFTAR_WATT[i], DAFTAR_KAPASITAS[i]
    return DAFTAR_WATT[1], DAFTAR_KAPASITAS[1]  # jaga-jaga, anggap 1 PK


def hitung_k(matahari, sirkulasi):
    # k = seberapa cepat panas dari luar masuk
    k = 0.15
    if matahari:
        k = k + 0.1
    if sirkulasi:
        k = k + 0.1
    return k


def hitung_panas_bangunan(matahari):
    # panas yang tersimpan di tembok, atap, dan elektronik
    panas_bangunan = 3.0
    if matahari:
        panas_bangunan += 2.0
    return panas_bangunan


def atur_mode(nama_mode, ruangan, kapasitas):
    # tiap mode punya target suhu dan batas daya sendiri
    if nama_mode == "Nyaman":
        target = 24.0
        batas_daya = kapasitas  # boleh kerja 100%
    elif nama_mode == "Hemat":
        target = 26.0
        batas_daya = 0.6 * kapasitas  # maksimal 60%
    else:
        target = ruangan["target_custom"]
        batas_daya = (ruangan["persen_custom"] / 100) * kapasitas
    return target, batas_daya


def hitung_daya_ac(suhu, target, prediksi_naik, batas_daya):
    # kebutuhan = koreksi ke target (x0.8) + perkiraan suhu naik jam ini
    kebutuhan = 0.8 * (suhu - target) + prediksi_naik

    if kebutuhan <= 0:
        return 0  # sudah dingin brr
    elif kebutuhan > batas_daya:
        return batas_daya  # mentok di batas
    else:
        return kebutuhan  # AC menyesuaikan


def hitung_kwh(daya_ac, kapasitas, watt):
    # listrik yang dipakai AC selama satu jam
    persen_kerja = daya_ac / kapasitas
    if daya_ac > 0 and persen_kerja < 0.3:
        persen_listrik = 0.3  # kalau nyala, minimal 30%
    else:
        persen_listrik = persen_kerja
    return watt * persen_listrik / 1000


def tentukan_status(daya_ac, batas_daya):
    if daya_ac == 0:
        return "MATI"
    elif daya_ac == batas_daya:
        return "MAKS"
    else:
        return "ADAPTIF"


def simulasi_ruangan(ruangan, nama_mode, suhu_luar, jam_mulai, tarif):
    # simulasi 24 jam buat satu ruangan dengan satu mode
    watt, kapasitas = data_ac(ruangan["pk"])
    k = hitung_k(ruangan["matahari"], ruangan["sirkulasi"])
    panas_bangunan = hitung_panas_bangunan(ruangan["matahari"])
    target, batas_daya = atur_mode(nama_mode, ruangan, kapasitas)

    suhu = ruangan["suhu_awal"]
    total_kwh = 0
    riwayat_suhu = []
    tabel_jam = []  # tiap baris: [jam, suhu luar, suhu ruang, persen kerja, status, biaya]

    for i in range(24):
        jam = (jam_mulai + i) % 24  # habis jam 23 balik ke 0

        # panas dari luar (hukum Newton) + panas dari orang
        panas_masuk = k * (suhu_luar[jam] + panas_bangunan - suhu)
        panas_orang = 0.1 * ruangan["orang"]
        prediksi_naik = panas_masuk + panas_orang

        # AC menyesuaikan, lalu suhu ruangan berubah
        daya_ac = hitung_daya_ac(suhu, target, prediksi_naik, batas_daya)
        suhu = suhu + prediksi_naik - daya_ac
        riwayat_suhu.append(suhu)

        # listrik dan biaya jam ini
        kwh = hitung_kwh(daya_ac, kapasitas, watt)
        total_kwh += kwh
        biaya = kwh * tarif

        status = tentukan_status(daya_ac, batas_daya)
        tabel_jam.append([jam, suhu_luar[jam], suhu, daya_ac / kapasitas * 100, status, biaya])

    rata_rata, terendah, tertinggi = statistik_suhu(riwayat_suhu)

    return {
        "nama": ruangan["nama"],
        "mode": nama_mode,
        "target": target,
        "k": k,
        "orang": ruangan["orang"],
        "tabel_jam": tabel_jam,
        "rata_rata": rata_rata,
        "terendah": terendah,
        "tertinggi": tertinggi,
        "kwh_hari": total_kwh,
        "biaya_hari": total_kwh * tarif,
        "biaya_bulan": total_kwh * tarif * 30,
    }


def statistik_suhu(riwayat_suhu):
    # rata-rata, terendah, dan tertinggi
    jumlah = 0
    terendah = riwayat_suhu[0]
    tertinggi = riwayat_suhu[0]
    for s in riwayat_suhu:
        jumlah += s
        if s > tertinggi:
            tertinggi = s
        if s < terendah:
            terendah = s
    return jumlah / len(riwayat_suhu), terendah, tertinggi


def simulasi_semua(daftar_ruangan, suhu_luar, jam_mulai, tarif, mode_paksa=None):
    # simulasi tiap ruangan di list
    # mode_paksa diisi kalau semua ruangan mau dipaksa pakai mode yang sama
    daftar_hasil = []
    for ruangan in daftar_ruangan:
        if mode_paksa is None:
            nama_mode = ruangan["mode"]
        else:
            nama_mode = mode_paksa
        hasil = simulasi_ruangan(ruangan, nama_mode, suhu_luar, jam_mulai, tarif)
        daftar_hasil.append(hasil)
    return daftar_hasil


def indeks_paling_boros(daftar_hasil):
    # ruangan dengan biaya harian paling besar
    indeks = 0
    for i in range(1, len(daftar_hasil)):
        if daftar_hasil[i]["biaya_hari"] > daftar_hasil[indeks]["biaya_hari"]:
            indeks = i
    return indeks
