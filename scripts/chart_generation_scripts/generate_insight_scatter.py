import pandas as pd
import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import matplotlib.pyplot as plt

# Fungsi untuk menghasilkan narasi dari AI
def generate_narrative(prompt_sistem, prompt_pengguna):
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
def generate_insight_from_chart(file_path, kolom_x, kolom_y, judul_chart):
    # Baca data dari file CSV
    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        return f"Error membaca file CSV: {e}"
    
    # Periksa apakah kolom yang dibutuhkan ada di DataFrame
    if kolom_x not in data.columns or kolom_y not in data.columns:
        return f"Kolom {kolom_x} atau {kolom_y} tidak ditemukan di file CSV."
    
    # Konversi data ke format JSON
    data_json = data.to_json(orient="records", lines=True)

    # Deskripsi chart dan kode Python untuk membuat chart
    deskripsi_chart = f"""
Berikut adalah kode Python untuk membuat grafik Scatter Plot:

import matplotlib.pyplot as plt

# Data
x = df['{kolom_x}']
y = df['{kolom_y}']

# Membuat grafik Scatter Plot
plt.figure(figsize=(10, 6))
plt.scatter(x, y)
plt.title('{judul_chart}')
plt.xlabel('{kolom_x}')
plt.ylabel('{kolom_y}')
plt.grid(True)
plt.show()
"""

    # Definisikan sistem prompt (termasuk data dan instruksi umum)
    prompt_sistem = f"""
Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data penjualan yang diberikan dalam bentuk grafik dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.

Berikut adalah data yang perlu Anda analisis:
{data_json}

Data ini memiliki kolom dan value sebagai berikut:
- {kolom_x} yang mewakili sumbu x
- {kolom_y} yang mewakili sumbu y

Berikut adalah deskripsi chart yang dimaksud dan kode Python untuk membuatnya:
{deskripsi_chart}

Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data. Tambahkan elemen storytelling yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
"""
    
    # Definisikan prompt pengguna (instruksi atau pertanyaan spesifik pengguna)
    prompt_pengguna = f"""
Buatlah narasi yang berisi analisis yang harus mencakup:
- Korelasi antara kedua variabel {kolom_x} dan {kolom_y}
- Pola atau tren yang terlihat dalam data
- Poin-poin outlier yang signifikan
- Rekomendasi berdasarkan temuan
"""

    # Menghasilkan narasi dari AI
    narasi = generate_narrative(prompt_sistem, prompt_pengguna)

    return narasi

# Bagian ini harus diubah oleh pengguna sesuai dengan dataset mereka
file_data = r"C:\Users\IYOM\myenvir\df_scatter.csv"  # Ganti dengan path yang benar ke file CSV pengguna

# Kolom yang ada di dataset pengguna
kolom_x = "Sales"  # Pilih kolom untuk sumbu x
kolom_y = "Profit"  # Pilih kolom untuk sumbu y

# Judul grafik
judul_chart = "Hubungan Sales dengan Profit"  # Ganti dengan judul yang sesuai

# Hasilkan insight untuk scatter plot
insight_chart = generate_insight_from_chart(file_data, kolom_x, kolom_y, judul_chart)
print("Insight Scatter Plot:\n", insight_chart)
