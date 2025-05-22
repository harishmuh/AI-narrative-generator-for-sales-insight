import pandas as pd
import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import matplotlib.pyplot as plt

# Fungsi untuk menghasilkan narasi dari AI
def menghasilkan_narasi(prompt_sistem, prompt_pengguna):
    pesan = [
        {"role": "system", "content": prompt_sistem},
        {"role": "user", "content": prompt_pengguna}
    ]
    respons = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=pesan,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return respons.choices[0].message.content

# Memuat variabel lingkungan
load_dotenv()

# Konfigurasi untuk Azure OpenAI API dari file .env
azure_endpoint = os.getenv('AZURE_ENDPOINT')
api_key = os.getenv('API_KEY')
api_version = os.getenv('API_VERSION')

# Menginisialisasi klien Azure OpenAI
client = AzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=api_key,
    api_version=api_version
)

# Fungsi untuk menghasilkan insight dari data chart
def menghasilkan_insight_dari_chart(file_path, kolom_kategori, kolom_nilai, judul_chart):
    # Baca data dari file CSV
    data = pd.read_csv(file_path)
    
    # Konversi data ke Pandas DataFrame
    df = pd.DataFrame(data)
    
    # Konversi data ke format JSON
    data_json = df[[kolom_kategori, kolom_nilai]].to_json(orient="records", lines=True)

    # Deskripsi chart dan kode Python untuk membuat chart
    deskripsi_chart = f"""
Berikut adalah kode Python untuk membuat grafik Bar Chart:

import matplotlib.pyplot as plt

# Data
categories = df['{kolom_kategori}']
values = df['{kolom_nilai}']

# Membuat grafik Bar Chart
plt.figure(figsize=(16, 12))
plt.barh(categories, values)  # Menggunakan barh untuk horizontal bar chart
plt.title('{judul_chart}', fontsize=16)
plt.xlabel('{kolom_nilai}', fontsize=14)
plt.ylabel('{kolom_kategori}', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout(pad=5.0)
plt.grid(True)
plt.show()
"""

    # Definisikan sistem prompt (termasuk data dan instruksi umum)
    prompt_sistem = f"""
Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data yang diberikan dalam bentuk grafik dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.

Berikut adalah data yang perlu Anda analisis:
{data_json}

Data ini memiliki kolom dan value sebagai berikut:
- {kolom_kategori} yang mewakili kategori produk
- {kolom_nilai} yang mewakili jumlah penjualan

Berikut adalah deskripsi chart yang dimaksud dan kode Python untuk membuatnya:
{deskripsi_chart}

Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data.
Tambahkan elemen storytelling yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
"""
    
    # Definisikan prompt pengguna (instruksi atau pertanyaan spesifik pengguna)
    prompt_pengguna = f"""
Buatlah narasi yang berisi analisis yang harus mencakup:
- Kategori produk dengan penjualan tertinggi dan terendah
- Perbandingan antar kategori produk
- Faktor-faktor yang mungkin menyebabkan variasi dalam penjualan
- Rekomendasi berdasarkan temuan
"""

    # Menghasilkan narasi dari AI
    narasi = menghasilkan_narasi(prompt_sistem, prompt_pengguna)

    return narasi

# Bagian ini harus diubah oleh pengguna sesuai dengan dataset mereka
file_data = r"C:\Users\IYOM\myenvir\df_barchart.csv"  # Ganti dengan path yang benar ke file CSV pengguna

# Kolom yang ada di dataset pengguna
kolom_kategori = "product_category"  # Pilih kolom untuk kategori
kolom_nilai = "quantity_sold"  # Pilih kolom untuk nilai

# Judul grafik
judul_chart = "Penjualan Berdasarkan Kategori Produk 2022"  # Ganti dengan judul yang sesuai

# Hasilkan insight untuk data bar chart
insight_chart = menghasilkan_insight_dari_chart(file_data, kolom_kategori, kolom_nilai, judul_chart)
print("Insight Bar Chart:\n", insight_chart)

# Simpan output ke file teks
output_file = os.path.join(os.path.dirname(file_data), "insight_output_barchart.txt")
with open(output_file, "w") as file:
    file.write("Insight Bar Chart:\n")
    file.write(insight_chart)
