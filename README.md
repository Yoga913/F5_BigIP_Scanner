# Pemindai Kerentanan F5 BIG-IP Berbasis Shodan

Ini adalah alat berbasis Python yang digunakan untuk memindai perangkat **F5 BIG-IP** yang rentan menggunakan **Shodan** dan **aiohttp** untuk permintaan asinkron. Alat ini dirancang untuk membantu profesional keamanan mengidentifikasi kerentanan di perangkat mereka dan memastikan keamanan perangkat F5. 
**Gunakan alat ini secara bertanggung jawab dan hanya pada sistem yang Anda miliki izin untuk diuji.**

## Fitur
- **Integrasi Shodan API**: Secara otomatis mendapatkan perangkat F5 BIG-IP melalui pencarian di Shodan.
- **Pemindaian Asinkron**: Memanfaatkan `aiohttp` untuk melakukan banyak pemindaian kerentanan secara paralel.
- **Rotasi User-Agent**: Menghindari deteksi sederhana dengan merotasi daftar user-agent.
- **Output CSV**: Menyimpan hasil pemindaian dalam file CSV untuk analisis lebih lanjut.
- **Logging**: Menyimpan log pemindaian, termasuk kesalahan dan perangkat yang rentan, ke dalam file log.

## Instalasi
### Persyaratan
Pastikan Anda telah menginstal dependensi berikut:
- Python 3.7+
- `shodan`
- `aiohttp`
- `requests`
- `csv`
- `colorama`
- `logging`
- `asyncio`

Anda bisa menginstal dependensi ini menggunakan `pip`:

```bash
pip install shodan aiohttp requests colorama
```

### Clone Repositori
Untuk memulai, clone repositori ini:

```bash
git clone https://github.com/Yoga913/f5-bigip-scanner.git
cd f5-bigip-scanner
```

## Penggunaan
### 1. Mengatur API Key Shodan
Sebelum menjalankan alat ini, Anda perlu mengatur kunci API Shodan. Dapatkan kunci API dari akun Shodan Anda dan masukkan ke dalam skrip:
```python
SHODAN_API_KEY = "YOUR_SHODAN_API_KEY"
```

### 2. Menjalankan Pemindai
Setelah kunci API diatur, Anda dapat menjalankan pemindai untuk mencari perangkat F5 BIG-IP yang rentan:
```bash
python f5_bigip_scanner.py
```

Skrip ini akan:
1. Mencari perangkat F5 BIG-IP melalui Shodan.
2. Berusaha mengeksploitasi perangkat dengan mengirimkan perintah dan memeriksa kerentanan.
3. Mencatat hasil ke dalam file `scanner.log`.
4. Menyimpan perangkat yang rentan dan tidak rentan dalam file `f5bigip_results.csv`.

### 3. Output CSV
Skrip ini menghasilkan file CSV (`f5bigip_results.csv`) yang berisi hasil pemindaian kerentanan, termasuk:
- **Alamat IP** dari perangkat yang dipindai.
- **Status** perangkat (VULNERABLE atau NOT VULNERABLE).

### 4. Log
Semua aktivitas pemindaian dicatat dalam file `scanner.log`. Ini mencakup deteksi kerentanan yang berhasil dan kesalahan apa pun yang terjadi selama pemindaian.

## Contoh Penggunaan
```bash
python f5_bigip_scanner.py
```

### Output:
```text
VULNERABLE: https://x.x.x.x/mgmt/tm/util/bash
NOT VULNERABLE: https://y.y.y.y/mgmt/tm/util/bash
```

## Peringatan
**Alat ini hanya untuk tujuan edukasi.** Pengujian atau pemindaian sistem tanpa izin adalah ilegal. Gunakan alat ini hanya pada jaringan dan perangkat yang Anda miliki izin eksplisit untuk diuji. Penulis tidak bertanggung jawab atas penyalahgunaan alat ini.

## Kontribusi
Kontribusi sangat diterima! Jika Anda menemukan bug atau ingin menambahkan fitur baru, jangan ragu untuk membuka pull request atau membuat issue.

## Lisensi
Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file [LICENSE](LICENSE) untuk informasi lebih lanjut.
