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
def menghasilkan_insight_dari_chart(file_path, kolom_kategori, kolom_1, kolom_2, judul_chart):
    # Baca data dari file CSV
    data = pd.read_csv(file_path)
    
    # Konversi data ke Pandas DataFrame
    df = pd.DataFrame(data)
    
    # Konversi seluruh data ke format JSON
    data_json = df.to_json(orient="records", lines=True)

    # Deskripsi chart dan kode Python untuk membuat chart
    deskripsi_chart = f"""
    Berikut adalah kode Python untuk membuat grafik Double Line Chart dengan dua garis:

    import matplotlib.pyplot as plt

    # Data
    categories = df['{kolom_kategori}']
    sales_1 = df['{kolom_1}']
    sales_2 = df['{kolom_2}']

    # Buat plot
    plt.figure(figsize=(10, 6))

    # Plot garis untuk {kolom_1}
    plt.plot(categories, sales_1, marker='o', linestyle='-', color='b', label='{kolom_1}')

    # Plot garis untuk {kolom_2}
    plt.plot(categories, sales_2, marker='o', linestyle='-', color='orange', label='{kolom_2}')

    # Menambahkan label dan judul
    plt.xlabel('{kolom_kategori}', fontweight='bold')
    plt.ylabel('Sales', fontweight='bold')
    plt.title('{judul_chart}')
    plt.xticks(rotation=45)

    # Menambahkan legenda
    plt.legend()

    # Menambahkan grid
    plt.grid(True)

    # Menambahkan anotasi untuk penjualan tertinggi dan terendah
    max_sales_1 = sales_1.idxmax()
    min_sales_1 = sales_1.idxmin()
    max_sales_2 = sales_2.idxmax()
    min_sales_2 = sales_2.idxmin()

    plt.annotate(f'Highest {kolom_1}: {{sales_1[max_sales_1]}}', xy=(max_sales_1, sales_1[max_sales_1]), xytext=(max_sales_1, sales_1[max_sales_1] + 500),
                 arrowprops=dict(facecolor='blue', shrink=0.05))
    plt.annotate(f'Lowest {kolom_1}: {{sales_1[min_sales_1]}}', xy=(min_sales_1, sales_1[min_sales_1]), xytext=(min_sales_1, sales_1[min_sales_1] + 500),
                 arrowprops=dict(facecolor='blue', shrink=0.05))
    plt.annotate(f'Highest {kolom_2}: {{sales_2[max_sales_2]}}', xy=(max_sales_2, sales_2[max_sales_2]), xytext=(max_sales_2, sales_2[max_sales_2] + 500),
                 arrowprops=dict(facecolor='orange', shrink=0.05))
    plt.annotate(f'Lowest {kolom_2}: {{sales_2[min_sales_2]}}', xy=(min_sales_2, sales_2[min_sales_2]), xytext=(min_sales_2, sales_2[min_sales_2] + 500),
                 arrowprops=dict(facecolor='orange', shrink=0.05))

    # Tampilkan plot
    plt.tight_layout()
    plt.show()
    """

    # Definisikan sistem prompt (termasuk data dan instruksi umum)
    prompt_sistem = f"""
    Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data penjualan yang diberikan dalam bentuk grafik dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.

    Berikut adalah data penjualan yang perlu Anda analisis:
    {data_json}

    Data ini memiliki kolom dan nilai sebagai berikut:
    - {kolom_kategori} yang mewakili kategori produk
    - {kolom_1} yang mewakili nilai total penjualan untuk {kolom_1}
    - {kolom_2} yang mewakili nilai total penjualan untuk {kolom_2}

    Berikut adalah deskripsi chart yang dimaksud dan kode Python untuk membuatnya:
    {deskripsi_chart}

    Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data. Tambahkan elemen storytelling yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas.
    Tambahkan elemen storytelling yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
    """
    
    # Definisikan prompt pengguna (instruksi atau pertanyaan spesifik pengguna)
    prompt_pengguna = f"""
    Buatlah narasi yang menarik yang berisi analisis mendalam mengenai data penjualan berikut:
    - Bandingkan total penjualan antara {kolom_1} dan {kolom_2} per kategori produk. Ceritakan apa yang Anda temukan tentang tren penjualan.
    - Identifikasi kategori produk dengan penjualan tertinggi dan terendah untuk masing-masing kolom. Berikan spekulasi mengapa kategori-kategori tersebut berkinerja seperti itu.
    - Jelaskan bagaimana grafik double line chart menggambarkan pencapaian penjualan. Apakah ada pola musiman atau tren lain yang menonjol?
    - Diskusikan faktor-faktor yang mungkin mempengaruhi pencapaian penjualan per kategori produk. Pertimbangkan faktor-faktor eksternal seperti musim, tren pasar, atau promosi.
    - Berikan rekomendasi strategi yang dapat diterapkan untuk meningkatkan penjualan di kategori dengan penjualan terendah. Usahakan untuk memberikan strategi yang konkret dan berbasis data.
    """

    # Menghasilkan narasi dari AI
    narasi = menghasilkan_narasi(prompt_sistem, prompt_pengguna)

    return narasi

# Bagian ini harus diubah oleh pengguna sesuai dengan dataset mereka
file_data = r"C:\Users\IYOM\myenvir\df_doubleline.csv"  # Ganti dengan path yang benar ke file CSV pengguna

# Kolom yang ada di dataset pengguna
kolom_kategori = "Category"  # Pilih kolom untuk kategori produk
kolom_1 = "Total Sales B2B"  # Pilih kolom untuk nilai total penjualan B2B
kolom_2 = "Total Sales B2C"  # Pilih kolom untuk nilai total penjualan B2C

# Judul grafik
judul_chart = "Annual Product Sales by Category and Business Model"  # Ganti dengan judul yang sesuai

# Hasilkan insight untuk data double line chart
insight_chart = menghasilkan_insight_dari_chart(file_data, kolom_kategori, kolom_1, kolom_2, judul_chart)
print("Insight Double Line Chart:\n", insight_chart)

# Simpan output ke file teks
output_file = os.path.join(os.path.dirname(file_data), "insight_output_line_chart.txt")
with open(output_file, "w") as file:
    file.write("Insight Double Line Chart:\n")
    file.write(insight_chart)
