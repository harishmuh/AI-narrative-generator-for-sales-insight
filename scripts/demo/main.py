# Import necessary libraries
import streamlit as st
import pandas as pd
from utils import load_lottieurl, menghasilkan_insight_dari_chart, menghasilkan_narasi, buat_prompt_sistem
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from bs4 import BeautifulSoup

# URL animasi Lottie
lottie_animation_url = "https://lottie.host/40eb321b-edf1-42f0-b982-a0c33c23b9ec/TbobicdLp3.json"
lottie_animation = load_lottieurl(lottie_animation_url)

# Judul aplikasi
st.markdown('<div class="main-header">Mengubah Insight Dalam Grafik Menjadi Sebuah Narasi</div>', unsafe_allow_html=True)

# Menampilkan animasi Lottie di bawah judul
if lottie_animation:
    st_lottie(lottie_animation, height=150, key="animation")

# Sidebar untuk pengaturan input
st.sidebar.title("Unggah File Anda Disini")
uploaded_file = st.sidebar.file_uploader("Pilih File", type=["csv", "xls", "xlsx", "json"])

# Memproses file yang diunggah
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.markdown('<div class="section-header">Data yang diunggah:</div>', unsafe_allow_html=True)
    st.dataframe(df)

    st.sidebar.title("Pengaturan Grafik")
    jenis_grafik = st.sidebar.selectbox("Pilih jenis grafik", ["Bar Chart", "Pie Chart", "Line Chart", "Double Line Chart", "Scatter Plot", "Histogram", "Funnel Chart", "Gauge / Barometer Chart", "Sankey Diagram", "Stacked Bar Chart", "Waterfall Chart"])
    kolom_x = st.sidebar.selectbox("Pilih kolom untuk sumbu X", df.columns)
    kolom_y_list = []
    kolom_warna_list = None

    if jenis_grafik == "Sankey Diagram":
        kolom_y_list = st.sidebar.multiselect("Pilih kolom untuk sumber, tujuan, dan nilai", df.columns)
    else:
        kolom_y_list = st.sidebar.multiselect("Pilih kolom untuk sumbu Y", df.columns)

    if jenis_grafik == "Stacked Bar Chart":
        kolom_warna_list = st.sidebar.multiselect("Pilih kolom untuk warna", df.columns, default=kolom_y_list)

    judul_chart = st.sidebar.text_input("Masukkan judul grafik")

    # Kotak input untuk pertanyaan pengguna
    st.markdown('<div class="section-header">Buat Grafik dan Insight</div>', unsafe_allow_html=True)
    prompt_pengguna = st.text_area("Masukkan pertanyaan atau instruksi khusus yang ingin Anda tanyakan tentang data ini:", key="user_prompt")

    #  Menambahkan tombol untuk menghasilkan grafik dan insight berdasarkan input pengguna
    if st.button("Hasilkan Grafik dan Insight"):
        # Mengecek apakah tombol "Hasilkan Grafik dan Insight" diklik
        if prompt_pengguna.strip() != "":
            # Mengecek apakah prompt pengguna tidak kosong setelah menghilangkan spasi di awal dan akhir
            with st.spinner('Menghasilkan grafik dan insight...'):
                narasi = menghasilkan_insight_dari_chart(df, jenis_grafik, kolom_x, kolom_y_list, kolom_warna_list, judul_chart)
                 # Memanggil fungsi menghasilkan_insight_dari_chart untuk menghasilkan narasi berdasarkan grafik yang dipilih
                st.markdown(f"<div class='narrative-container'>{narasi}</div>", unsafe_allow_html=True)

# Gaya CSS untuk tampilan profesional dan custom button
st.markdown("""
    <style>
        .main-header {
            font-size: 2.5em;
            font-weight: bold;
            color: #2E86C1;
            text-align: center;
            margin-bottom: 20px;
        }
        .section-header {
            font-size: 1.5em;
            font-weight: bold;
            color: #2E86C1;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .narrative-container {
            font-family: Arial, sans-serif;
            font-size: 16px;
            line-height: 1.5;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 15px;
            margin-top: 10px;
        }
        body[data-theme='dark'] .narrative-container {
            background-color: #333;
            color: #FFF;
        }
        body[data-theme='light'] .narrative-container {
            background-color: #F9F9F9;
            color: #000;
        }
        .stTextInput>div>input {
            color: #FFF;
            background-color: #444;
        }
        .stTextInput>div>textarea {
            color: #FFF;
            background-color: #444;
        }
        body[data-theme='light'] .stTextInput>div>input,
        body[data-theme='light'] .stTextInput>div>textarea {
            color: #000;
            background-color: #FFF;
        }
        .stButton>button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            text-decoration: none;
            color: #2E86C1;
            border: 2px solid #2E86C1;
            border-radius: 5px;
            transition: background-color 0.3s ease, color 0.3s ease;
            background-color: transparent;
        }
        .stButton>button:hover {
            background-color: #2E86C1;
            color: white;
        }
        .stMultiSelect>div>div {
            background-color: #2E86C1;
            color: white;
        }
        .stMultiSelect>div>div:hover {
            background-color: #1F618D;
            color: white;
        }
        .main-footer {
            font-size: 0.9em;
            color: #AAAAAA;
            text-align: center;
            margin-top: 20px;
        }
        .footer-center {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

# Footer aplikasi
st.markdown('<div class="footer-center"><div class="main-footer">Developed by [Group 6 - Tetris] - © 2024</div></div>', unsafe_allow_html=True)
