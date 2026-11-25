# Modul cuaca: ambil suhu luar per jam (24 angka) dari Open-Meteo
# Open-Meteo gratis dan gak perlu API key (https://open-meteo.com)
# Kalau gagal, ada cadangan: data default atau interpolasi dari projek I

# requests perlu di-install dulu: pip install requests
# kalau belum ada, program tetap jalan, cuma gak bisa ambil data online
try:
    import requests
except ImportError:
    requests = None

URL_CARI_KOTA = "https://geocoding-api.open-meteo.com/v1/search"
URL_PRAKIRAAN = "https://api.open-meteo.com/v1/forecast"


def cari_kota(nama_kota):
    # nama kota jadi [nama lengkap, lintang, bujur], atau None kalau gagal
    if requests is None:
        return None

    parameter = {"name": nama_kota, "count": 1, "language": "id", "format": "json"}
    try:
        respon = requests.get(URL_CARI_KOTA, params=parameter, timeout=8)
        data = respon.json()
    except Exception:
        return None  # internet mati atau server gak jawab

    if "results" not in data or len(data["results"]) == 0:
        return None  # kotanya gak ketemu

    kota = data["results"][0]
    nama_lengkap = kota["name"]
    if "admin1" in kota:
        nama_lengkap = nama_lengkap + ", " + kota["admin1"]  # tambah nama provinsi
    return [nama_lengkap, kota["latitude"], kota["longitude"]]


def ambil_suhu_hari_ini(lintang, bujur):
    # prakiraan suhu jam 00.00 sampai 23.00 hari ini, atau None kalau gagal
    if requests is None:
        return None

    parameter = {
        "latitude": lintang,
        "longitude": bujur,
        "hourly": "temperature_2m",  # suhu udara 2 meter di atas tanah
        "timezone": "auto",          # jam ikut zona waktu kotanya
        "forecast_days": 1,
    }
    try:
        respon = requests.get(URL_PRAKIRAAN, params=parameter, timeout=8)
        data = respon.json()
        daftar_suhu = data["hourly"]["temperature_2m"]
    except Exception:
        return None

    if len(daftar_suhu) < 24:
        return None

    suhu_luar = []
    for jam in range(24):
        suhu_luar.append(round(daftar_suhu[jam], 1))
    return suhu_luar


def suhu_default():
    # cadangan: contoh suhu per jam waktu cerah di Bandung
    return [20.1, 19.8, 19.5, 19.3, 19.1, 19.0, 19.4, 20.6, 22.3, 24.0, 25.6, 26.8,
            27.6, 28.0, 28.1, 27.7, 26.8, 25.5, 24.1, 23.0, 22.2, 21.5, 21.0, 20.5]


def interpolasi_suhu(pagi, siang, sore, malam):
    # cara projek I: 4 suhu rata-rata disambung garis lurus jadi 24 suhu per jam
    # titiknya ada di jam 8, 13, 16, dan 23
    titik_jam = [8, 13, 16, 23]
    titik_suhu = [pagi, siang, sore, malam]
    suhu_luar = []
    for jam in range(24):
        jam_x = jam
        if jam_x < 8:
            jam_x += 24
        nilai = titik_suhu[0]
        for j in range(4):
            b = (j + 1) % 4
            jam_a = titik_jam[j]
            jam_b = titik_jam[b]
            if b == 0:
                jam_b += 24
            if jam_x >= jam_a and jam_x < jam_b:
                fraksi = (jam_x - jam_a) / (jam_b - jam_a)
                nilai = titik_suhu[j] + fraksi * (titik_suhu[b] - titik_suhu[j])
        suhu_luar.append(round(nilai, 1))
    return suhu_luar
