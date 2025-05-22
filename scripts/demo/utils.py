import os
import requests
from dotenv import load_dotenv
from openai import AzureOpenAI
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
import plotly.express as px
import plotly.graph_objects as go
import re
import html


load_dotenv()

azure_endpoint = os.getenv('AZURE_ENDPOINT')
api_key = os.getenv('API_KEY')
api_version = os.getenv('API_VERSION')

client = AzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=api_key,
    api_version=api_version
)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

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

def buat_prompt_sistem(data, jenis_grafik, kolom_x=None, kolom_y_list=None, kolom_warna_list=None):
    data_json = data.to_json(orient="records", lines=True)
    kolom_y_list_str = ', '.join(kolom_y_list) if kolom_y_list else ''
    kolom_warna_list_str = ', '.join(kolom_warna_list) if kolom_warna_list else ''

    if jenis_grafik == "Stacked Bar Chart":
        prompt = f"""
        Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data yang diberikan dalam bentuk grafik batang bertumpuk / stacked bar chart dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.
        Stacked barchart digunakan untuk membandingkan total nilai antar kategori utama, serta melihat kontribusi setiap subkategori dalam total tersebut.
        Berikut adalah data yang perlu Anda analisis:
        {data_json}

        Data ini untuk stacked bar chart yang memiliki variabel sebagai berikut:
        - {kolom_x} yang mewakili kolom dengan nilai kategori yang dapat dibagi ke dalam subkategori atau grup
        - {kolom_y_list_str} yang mewakili nilai untuk masing-masing kategori. Setiap kategori memiliki nilai kuantitatif untuk setiap subkategori yang akan ditampilkan dalam batang bertumpuk

        Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data.
        
        Berikut adalah poin-poin utama yang perlu Anda sampaikan dalam insight:
        1. Poin pertama insight...
        2. Poin kedua insight...
        3. Poin ketiga insight...

        Tambahkan elemen storytelling dalam narasi infografis yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
        """
    elif jenis_grafik == "Bar Chart":
        prompt = f"""
        Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data yang diberikan dalam bentuk grafik batang dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.

        Berikut adalah data yang perlu Anda analisis:
        {data_json}

        Data ini untuk bar chart yang memiliki kolom dan value sebagai berikut:
        - {kolom_x} yang mewakili kolom dengan nilai kategori
        - {kolom_y_list_str} yang mewakili nilai untuk masing-masing kategori

        Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data.
        
        Berikut adalah poin-poin utama yang perlu Anda sampaikan dalam insight:
        1. Poin pertama insight...
        2. Poin kedua insight...
        3. Poin ketiga insight...

        Tambahkan elemen storytelling dalam narasi infografis yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
        """
    elif jenis_grafik == "Line Chart":
        prompt = f"""
        Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data yang diberikan dalam bentuk line chart dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.
        Tambahkan elemen storytelling dalam narasi infografis yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
        Berikut adalah poin-poin utama yang perlu Anda sampaikan dalam insight:
        1. Poin pertama insight...
        2. Poin kedua insight...
        3. Poin ketiga insight...
        Berikut adalah data yang perlu Anda analisis:
        {data.to_json(orient="records", lines=True)}

        Data ini untuk line chart yang memiliki kolom dan nilai sebagai berikut:
        - {kolom_x} yang mewakili kolom dengan nilai kategori
        - {kolom_y_list} yang mewakili nilai untuk masing-masing kategori
        Untuk menghitung nilai tertinggi dan terendah pada sumbu {kolom_y_list} serta memberikan anotasi pada grafik, lakukan langkah-langkah berikut:
        1. Hitung nilai maksimum dan minimum untuk setiap kolom {kolom_y_list} menggunakan metode `max()` dan `min()`.
        2. Dapatkan indeks dari nilai maksimum dan minimum menggunakan metode `idxmax()` dan `idxmin()`.
        """
    elif jenis_grafik == "Double Line Chart":
        prompt = f"""
        Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data yang diberikan dalam bentuk grafik garis ganda dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.

        Berikut adalah data yang perlu Anda analisis:
        {data_json}

        Data ini untuk double line chart yang memiliki kolom dan value sebagai berikut:
        - {kolom_x} yang mewakili kolom dengan nilai kategori
        - {kolom_y_list_str} yang mewakili nilai untuk masing-masing kategori
        - Kolom Warna: {kolom_warna_list_str}
        Untuk menghitung nilai tertinggi dan terendah pada sumbu {kolom_y_list} serta memberikan anotasi pada grafik, lakukan langkah-langkah berikut:
        1. Hitung nilai maksimum dan minimum untuk setiap kolom {kolom_y_list} menggunakan metode `max()` dan `min()`.
        2. Dapatkan indeks dari nilai maksimum dan minimum menggunakan metode `idxmax()` dan `idxmin()`.
        Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data.
        
        Berikut adalah poin-poin utama yang perlu Anda sampaikan dalam insight:
        1. Poin pertama insight...
        2. Poin kedua insight...
        3. Poin ketiga insight...

        Tambahkan elemen storytelling dalam narasi infografis yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
        """
    elif jenis_grafik == "Scatter Plot":
        prompt = f"""
        Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data yang diberikan dalam bentuk grafik sebar dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.

        Berikut adalah data yang perlu Anda analisis:
        {data_json}

        Data ini untuk scatter plot yang dapat mengidentifikasi Pola dan Tren serta Hubungan antara Variabel,  sebagai berikut:
        - {kolom_x} yang mewakili kolom dengan nilai kuantitatif
        - {kolom_y_list_str} yang mewakili nilai kuantitatif
        - {kolom_warna_list_str} yang mewakili kolom untuk warna (opsional)

        Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data.
        
        Berikut adalah poin-poin utama yang perlu Anda sampaikan dalam insight:
        1. Poin pertama insight...
        2. Poin kedua insight...
        3. Poin ketiga insight...

        Tambahkan elemen storytelling dalam narasi infografis yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
        """
    elif jenis_grafik == "Histogram":
        prompt = f"""
        Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data yang diberikan dalam bentuk histogram dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.

        Berikut adalah data yang perlu Anda analisis:
        {data_json}

        Data ini untuk histogram yang memiliki variabel sebagai berikut:
        - {kolom_x} yang mewakili kolom dengan nilai kuantitatif

        Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data.
        
        Berikut adalah poin-poin utama yang perlu Anda sampaikan dalam insight:
        1. Poin pertama insight...
        2. Poin kedua insight...
        3. Poin ketiga insight...

        Tambahkan elemen storytelling dalam narasi infografis yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
        """
    elif jenis_grafik == "Pie Chart":
        prompt = f"""
        Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data yang diberikan dalam bentuk grafik pai dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.

        Berikut adalah data yang perlu Anda analisis:
        {data_json}

        Data ini untuk pie chart yang memiliki kolom dan value sebagai berikut:
        - {kolom_x} yang mewakili kolom dengan nilai kategori
        - {kolom_y_list[0]} yang mewakili nilai untuk masing-masing kategori

         Untuk menghitung persentase setiap kategori dalam sebuah pie chart, langkah-langkahnya adalah sebagai berikut:

        1. Hitung Total Nilai:
        Jumlahkan semua nilai dalam {kolom_y_list_str} untuk mendapatkan total keseluruhan.
        
        2. Hitung Persentase Setiap Kategori:
        Untuk setiap kategori, bagi nilai kategori tersebut yaitu pada {kolom_x} dengan total keseluruhan, kemudian kalikan dengan 100 untuk mendapatkan persentase.

        Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data.
        
        Berikut adalah poin-poin utama yang perlu Anda sampaikan dalam insight:
        1. Poin pertama insight...
        2. Poin kedua insight...
        3. Poin ketiga insight...

        Tambahkan elemen storytelling dalam narasi infografis yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
        """
    elif jenis_grafik == "Funnel Chart":
        prompt = f"""
        Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data yang diberikan dalam bentuk grafik corong dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.

        Berikut adalah data yang perlu Anda analisis:
        {data_json}

        Data ini untuk funnel chart yang memiliki kolom dan value sebagai berikut:
        - {kolom_x} yang mewakili kolom dengan nilai kategori yang berisi tahapan berurutan yang menunjukkan proses atau aliran. 
        - {kolom_y_list_str} yang mewakili nilai untuk masing-masing tahapan atau proses.

        Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data.
        
        Berikut adalah poin-poin utama yang perlu Anda sampaikan dalam insight:
        1. Poin pertama insight...
        2. Poin kedua insight...
        3. Poin ketiga insight...

        Tambahkan elemen storytelling dalam narasi infografis yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
        """
    elif jenis_grafik == "Gauge / Barometer Chart":
        prompt = f"""
        Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data yang diberikan dalam bentuk grafik pengukur dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.

        Berikut adalah data yang perlu Anda analisis:
        {data_json}

        Data ini untuk gauge chart yang memiliki kolom dan value sebagai berikut:
        - {kolom_x} yang mewakili kolom dengan nilai kategori
        - {kolom_y_list_str} yang mewakili nilai untuk masing-masing kategori

        Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data.
        
        Berikut adalah poin-poin utama yang perlu Anda sampaikan dalam insight:
        1. Poin pertama insight...
        2. Poin kedua insight...
        3. Poin ketiga insight...

        Tambahkan elemen storytelling dalam narasi infografis yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
        """
    elif jenis_grafik == "Sankey Diagram":
        prompt = f"""
        Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data yang diberikan dalam bentuk diagram sankey dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.

        Berikut adalah data yang perlu Anda analisis:
        {data_json}

        Data ini untuk sankey diagram yang memiliki kolom dan value sebagai berikut:
        - Node (Simpul): {kolom_x} yang mewakili kolom dengan nilai kategori
        - Source (Sumber): {kolom_y_list[0]} yang mewakili sumber aliran
        - Target (Tujuan): {kolom_y_list[1]} yang mewakili tujuan aliran
        - Value (Nilai): {kolom_y_list[2]} yang mewakili besarnya aliran

        Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data.
        
        Berikut adalah poin-poin utama yang perlu Anda sampaikan dalam insight:
        1. Poin pertama insight...
        2. Poin kedua insight...
        3. Poin ketiga insight...

        Tambahkan elemen storytelling dalam narasi infografis yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
        """
    elif jenis_grafik == "Waterfall Chart":
        prompt = f"""
        Anda adalah seorang analis data AI. Tugas Anda adalah menganalisis data yang diberikan dalam bentuk grafik waterfall dan menghasilkan insight dalam bentuk narasi storytelling yang cocok untuk sebuah infografis.

        Berikut adalah data yang perlu Anda analisis:
        {data_json}

        Data ini untuk waterfall chart yang memiliki kolom dan value sebagai berikut:
        - {kolom_x} yang mewakili kolom dengan nilai kategori atau label yang menggambarkan langkah atau komponen spesifik dari total perubahan.
        - {kolom_y_list_str} yang mewakili nilai kuantitatif untuk masing-masing kategori yang berurutan, di mana setiap nilai menunjukkan perubahan (positif atau negatif) dari nilai sebelumnya.

        Pastikan analisis Anda didasarkan pada perhitungan matematis yang akurat untuk memastikan tidak ada kesalahan atau kekeliruan dalam interpretasi data.
        
        Berikut adalah poin-poin utama yang perlu Anda sampaikan dalam insight:
        1. Poin pertama insight...
        2. Poin kedua insight...
        3. Poin ketiga insight...

        Tambahkan elemen storytelling dalam narasi infografis yang membuat analisis ini lebih menarik dan mudah dipahami oleh audiens yang lebih luas yang tidak memiliki latar belakang teknis.
        """
    else:
        raise ValueError("Jenis grafik tidak didukung")
    
    return prompt

# Fungsi untuk membuat prompt sistem untuk setiap jenis grafik
def menghasilkan_insight_dari_chart(data, jenis_grafik, kolom_x, kolom_y_list=None, kolom_warna_list=None, judul_chart=None):
    prompt_sistem = buat_prompt_sistem(data, jenis_grafik, kolom_x, kolom_y_list, kolom_warna_list)
    prompt_pengguna = st.session_state.user_prompt if "user_prompt" in st.session_state else ""
    narasi = menghasilkan_narasi(prompt_sistem, prompt_pengguna)
    
    if jenis_grafik == "Bar Chart":
        fig, ax = plt.subplots(figsize=(10, 6))
        data.plot(kind='bar', x=kolom_x, y=kolom_y_list, ax=ax)
        ax.set_title(judul_chart if judul_chart else jenis_grafik)
        st.pyplot(fig)
    elif jenis_grafik == "Double Line Chart":
        fig, ax = plt.subplots(figsize=(10, 6))
        for y in kolom_y_list:
            ax.plot(data[kolom_x], data[y], marker='o', label=y)
            max_value = data[y].max()
            min_value = data[y].min()
            max_index = data[y].idxmax()
            min_index = data[y].idxmin()
            ax.annotate(f'Highest {y}: {max_value}', xy=(max_index, max_value), xytext=(max_index, max_value + 500),
                        arrowprops=dict(facecolor='black', shrink=0.05))
            ax.annotate(f'Lowest {y}: {min_value}', xy=(min_index, min_value), xytext=(min_index, min_value - 500),
                        arrowprops=dict(facecolor='black', shrink=0.05))
        ax.set_title(judul_chart if judul_chart else jenis_grafik)
        ax.set_xlabel(kolom_x)
        ax.set_ylabel('Sales')
        ax.legend()
        st.pyplot(fig)
    elif jenis_grafik == "Line Chart":
        fig, ax = plt.subplots(figsize=(10, 6))
        insight_points = []  # Inisialisasi insight_points
        for y in kolom_y_list:
            ax.plot(data[kolom_x], data[y], marker='o', label=y)
            max_value = data[y].max()
            min_value = data[y].min()
            max_index = data[y].idxmax()
            min_index = data[y].idxmin()
            ax.annotate(f'Highest {y}: {max_value}', xy=(max_index, max_value), xytext=(max_index, max_value + 500),
                        arrowprops=dict(facecolor='black', shrink=0.05))
            ax.annotate(f'Lowest {y}: {min_value}', xy=(min_index, min_value), xytext=(min_index, min_value - 500),
                        arrowprops=dict(facecolor='black', shrink=0.05))
            insight_points.append(f'- Nilai tertinggi untuk {y} terjadi pada {data[kolom_x][max_index]} dengan nilai {max_value}.')
            insight_points.append(f'- Nilai terendah untuk {y} terjadi pada {data[kolom_x][min_index]} dengan nilai {min_value}.')
        ax.set_title(judul_chart if judul_chart else jenis_grafik)
        ax.set_xlabel(kolom_x)
        ax.set_ylabel('Value')
        ax.legend()
        st.pyplot(fig)
        
    elif jenis_grafik == "Scatter Plot":
        fig, ax = plt.subplots(figsize=(10, 6))
        for y in kolom_y_list:
            data.plot(kind='scatter', x=kolom_x, y=y, ax=ax)
        ax.set_title(judul_chart if judul_chart else jenis_grafik)
        st.pyplot(fig)
    elif jenis_grafik == "Histogram":
        fig, ax = plt.subplots(figsize=(10, 6))
        try:
            if kolom_y_list:
                data[kolom_y_list].plot(kind='hist', ax=ax)
            else:
                data[kolom_x].plot(kind='hist', ax=ax)
            ax.set_title(judul_chart if judul_chart else jenis_grafik)
            st.pyplot(fig)
        except TypeError as e:
            st.error("Data untuk histogram harus berupa data numerik.")
    elif jenis_grafik == "Pie Chart":
        # Calculate percentage contribution
        total = data[kolom_y_list[0]].sum()
        data['percent'] = (data[kolom_y_list[0]] / total) * 100
        data_json = data.to_json(orient="records", lines=True)

        fig = go.Figure(data=[go.Pie(
            labels = data[kolom_x],  
            values = data[kolom_y_list[0]],  
            textinfo = "label+percent",
            insidetextorientation = "radial"
        )])
        fig.update_layout(title=judul_chart if judul_chart else 'Pie Chart')
        st.plotly_chart(fig, use_container_width=True)
    elif jenis_grafik == "Stacked Bar Chart":
        fig, ax = plt.subplots(figsize=(10, 6))
        # Membatasi jumlah subkategori menjadi maksimal 5
        kolom_y_list = kolom_y_list[:5]
        
        # Menentukan posisi batang
        ind = range(len(data[kolom_x]))

        # Membuat stacked barchart
        bar_plots = []
        bottom = None
        for i, kolom in enumerate(kolom_y_list):
            if bottom is None:
                bar_plots.append(ax.bar(ind, data[kolom], label=kolom))
                bottom = data[kolom]
            else:
                bar_plots.append(ax.bar(ind, data[kolom], bottom=bottom, label=kolom))
                bottom += data[kolom]
        
        # Menambahkan label, judul, dan legenda
        ax.set_xlabel(kolom_x, fontweight='bold')
        ax.set_ylabel('Value', fontweight='bold')
        ax.set_title(judul_chart if judul_chart else 'Stacked Barchart')
        ax.set_xticks(ind)
        ax.set_xticklabels(data[kolom_x])
        ax.legend(title='Subcategory')

        # Menampilkan stacked barchart
        st.pyplot(fig)
    elif jenis_grafik == "Funnel Chart":
        fig = go.Figure(go.Funnel(
            y = data[kolom_x],
            x = data[kolom_y_list[0]]
        ))
        fig.update_layout(title=judul_chart if judul_chart else 'Funnel Chart')
        st.plotly_chart(fig, use_container_width=True)
    elif jenis_grafik == "Funnel Chart":
        fig = go.Figure(go.Funnel(
            y = data[kolom_x],
            x = data[kolom_y_list[0]]
        ))
        fig.update_layout(title=judul_chart if judul_chart else 'Funnel Chart')
        st.plotly_chart(fig, use_container_width=True)
    elif jenis_grafik == "Gauge / Barometer Chart":
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = data[kolom_y_list[0]].iloc[0],
            delta = {'reference': data[kolom_x][0]},
            title = {'text': judul_chart if judul_chart else 'Gauge Chart'},
            gauge = {
                'axis': {'range': [0, data[kolom_x][0] * 1.2]},
                'steps': [
                    {'range': [0, data[kolom_x][0] * 0.5], 'color': "lightgray"},
                    {'range': [data[kolom_x][0] * 0.5, data[kolom_x][0]], 'color': "gray"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': data[kolom_x][0]}
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
    elif jenis_grafik == "Sankey Diagram":
        if kolom_y_list and len(kolom_y_list) >= 3:
            all_nodes = list(pd.concat([data[kolom_y_list[0]], data[kolom_y_list[1]]]).unique())
            node_indices = {node: idx for idx, node in enumerate(all_nodes)}
            source_indices = data[kolom_y_list[0]].map(node_indices).tolist()
            target_indices = data[kolom_y_list[1]].map(node_indices).tolist()
            values = data[kolom_y_list[2]].tolist()

            fig = go.Figure(go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=all_nodes
                ),
                link=dict(
                    source=source_indices,
                    target=target_indices,
                    value=values
                )
            ))
            fig.update_layout(title=judul_chart if judul_chart else 'Sankey Diagram')
            st.plotly_chart(fig, use_container_width=True)
    elif jenis_grafik == "Waterfall Chart":
        if kolom_y_list and len(kolom_y_list) >= 1:
            data['delta'] = data[kolom_y_list[0]].diff().fillna(data[kolom_y_list[0]])

            sumbu_x = list(data[kolom_x])
            sumbu_y = list(data['delta'])

            measure_changes = ['relative'] * len(data)
            measure_changes[-1] = 'total'
            sumbu_x.append('Total')
            sumbu_y.append(data[kolom_y_list[0]].sum())

            label_waterfall = [f'{str(i)}' if i > 0 else str(i) for i in sumbu_y]

            layout_waterfall = go.Layout(
                title=judul_chart if judul_chart else 'Waterfall Chart',
                yaxis={'title': 'Amount'},
                xaxis={'title': kolom_x}
            )

            waterfall_plot = go.Waterfall(
                x=sumbu_x,
                y=sumbu_y,
                measure=measure_changes,
                text=label_waterfall,
                textposition='outside'
            )

            fig = go.Figure(data=[waterfall_plot], layout=layout_waterfall)

            st.plotly_chart(fig)
    
    return narasi
