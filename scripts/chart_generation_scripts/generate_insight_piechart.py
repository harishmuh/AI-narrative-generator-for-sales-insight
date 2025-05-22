import pandas as pd
import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

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
def menghasilkan_insight_dari_chart(file_path, kolom_1, kolom_2, judul_chart):
    # Baca data dari file CSV
    data = pd.read_csv(file_path)
    
    # Konversi data ke Pandas DataFrame
    df = pd.DataFrame(data)
    
    # Konversi data ke format JSON
    data_json = df.to_json(orient="records", lines=True)

    # Deskripsi chart dan kode Python untuk membuat chart
    deskripsi_chart = f"""
Berikut adalah kode Python untuk membuat grafik Pie Chart:

import matplotlib.pyplot as plt

# Data
labels = df['{kolom_1}']
sizes = df['{kolom_2}']

# Membuat grafik Pie Chart
plt.figure(figsize=(10, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('{judul_chart}')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
"""

    # Definisikan sistem prompt (termasuk data dan instruksi umum)
    prompt_sistem = f"""
Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data penjualan yang diberikan dalam bentuk grafik dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.

Berikut adalah data penjualan yang perlu Anda analisis:
{data_json}

Grafik ini adalah pie chart {deskripsi_chart} yang menunjukkan distribusi "{kolom_2}" berdasarkan "{kolom_1}" dengan judul "{judul_chart}". 
Instruksi untuk menghitung persentase:
1. Hitung total penjualan.
2. Bagi setiap nilai penjualan dengan total penjualan dan kalikan dengan 100 untuk mendapatkan persentase.

Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data.
Tambahkan elemen storytelling yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
"""

    # Definisikan prompt pengguna (instruksi atau pertanyaan spesifik pengguna)
    prompt_pengguna = f"""
Buatlah narasi yang berisi analisis yang harus mencakup:
- Sebutkan jumlah dan persentase kategori dengan proporsi terbesar dan terkecil
- Bandingkan perbedaan atau selisih jumlah dan persentase antar kategori
- Identifikasi faktor-faktor yang mungkin menyebabkan variasi dalam distribusi
- Berikan rekomendasi berdasarkan temuan
"""

    # Menghasilkan narasi dari AI
    narasi = menghasilkan_narasi(prompt_sistem, prompt_pengguna)

    return narasi

# Bagian ini harus diubah oleh pengguna sesuai dengan dataset mereka
file_data = r"C:\Users\IYOM\myenvir\df_piechart.csv"  # Ganti dengan path yang benar ke file CSV pengguna

# Kolom yang ada di dataset pengguna
kolom_1 = "city"  # Pilih kolom untuk label
kolom_2 = "sales_amount"  # Pilih kolom untuk nilai

# Judul grafik
judul_chart = "Distribusi Penjualan Berdasarkan Kota"  # Ganti dengan judul yang sesuai

# Hasilkan insight untuk data pie chart
insight_chart = menghasilkan_insight_dari_chart(file_data, kolom_1, kolom_2, judul_chart)
print("Insight Pie Chart:\n", insight_chart)

# Simpan output ke file teks
output_file = os.path.join(os.path.dirname(file_data), "insight_output_piechart.txt")
with open(output_file, "w") as file:
    file.write("Insight Pie Chart:\n")
    file.write(insight_chart)
