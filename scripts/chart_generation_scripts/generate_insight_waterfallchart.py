import pandas as pd
import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import plotly.graph_objects as go

# Fungsi untuk menghasilkan narasi dari AI
def generate_narrative(system_prompt, user_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    response = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return response.choices[0].message.content

# Load environment variables
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

def buat_insight_dari_grafik(file_path, sumbu_x, nilai, judul):
    # Baca data dari file CSV
    data = pd.read_csv(file_path)
    
    # Konversi data ke Pandas DataFrame
    df = pd.DataFrame(data)
    
    # Konversi data ke format JSON
    data_json = df.to_json(orient="records", lines=True)

    # Deskripsi chart dan kode Python untuk membuat chart
    chart_description = f"""
    Berikut adalah kode Python untuk membuat grafik Waterfall Chart:

    import plotly.graph_objects as go

    sumbu_x = {df[sumbu_x].tolist()}
    sumbu_y = {df[nilai].tolist()}
    
    measure_changes = ['relative'] * len(sumbu_y) + ['total']
    sumbu_x.append('Total')
    sumbu_y.append(sum(sumbu_y))
    
    fig = go.Figure(go.Waterfall(
        name="20", orientation="v",
        measure=measure_changes,
        x=sumbu_x,
        textposition="outside",
        text=sumbu_y,
        y=sumbu_y,
        connector={{"line": {{"color": "rgb(63, 63, 63)"}}}}
    ))

    fig.update_layout(
        title="{judul}",
        showlegend=True
    )

    fig.show()
    """

    # Definisikan sistem prompt (termasuk data dan instruksi umum)
    sistem_prompt = f"""
Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data penjualan yang diberikan dalam bentuk grafik dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.

Berikut adalah data penjualan yang perlu Anda analisis:
{data_json}

Data ini memiliki kolom dan value sebagai berikut:
- {sumbu_x} pada sumbu X
- {nilai} pada sumbu Y

Berikut adalah deskripsi chart yang dimaksud dan kode Python untuk membuatnya:
{chart_description}

Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data. Berikan narasi yang mudah dipahami dan menarik agar dapat dengan mudah dipahami oleh orang yang tidak memiliki latar belakang teknis.
Tambahkan elemen storytelling yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
"""
    
    # Definisikan prompt pengguna (instruksi atau pertanyaan spesifik pengguna)
    prompt_pengguna = f"""
Berikan narasi analisis harus mencakup:
- Identifikasi bulan dengan penjualan tertinggi dan terendah.
- Bandingkan jumlah penjualan antara bulan.
- Identifikasi faktor-faktor yang mungkin menyebabkan variasi dalam distribusi.
- Berikan rekomendasi berdasarkan temuan.
"""

    # Menghasilkan narasi dari AI
    narasi = generate_narrative(sistem_prompt, prompt_pengguna)

    return narasi

# File CSV yang diunggah oleh pengguna
data_file = r"C:\Users\IYOM\myenvir\data_waterfall.csv"

# Kolom yang ada di dataset pengguna
sumbu_x = "Month"  # Ganti dengan nama kolom yang sesuai di dataset Anda
nilai = "sales_amount"  # Ganti dengan nama kolom yang sesuai di dataset Anda

# Judul grafik
judul_grafik = "Distribusi Penjualan Berdasarkan Bulan" # Ganti dengan judul yang sesuai

# Hasilkan insight untuk data penjualan
insight_waterfall = buat_insight_dari_grafik(data_file, sumbu_x, nilai, judul_grafik)
print("Insight Grafik Waterfall:\n", insight_waterfall)

# Simpan output ke file teks
output_file = os.path.join(os.path.dirname(data_file), "insight_output_waterfall.txt")
with open(output_file, "w") as file:
    file.write("Insight Grafik Waterfall:\n")
    file.write(insight_waterfall)