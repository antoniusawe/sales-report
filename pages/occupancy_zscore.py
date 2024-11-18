import streamlit as st
import pandas as pd
import plotly.express as px

def show_occupancy_zscore(filtered_occupancy_data, program_choice, selected_year, selected_month):
    # Penjelasan Z-Score
    st.markdown("""
        ### Apa Itu Z-Score?
        Z-score adalah cara untuk mengukur seberapa jauh suatu nilai dari rata-rata dalam satuan deviasi standar. 
        Z-score dihitung dengan rumus:
        
        \[
        Z\text{-Score} = \frac{(\text{Occupancy Rate} - \text{Mean Occupancy Rate})}{\text{Standard Deviation of Occupancy Rate}}
        \]
        
        Dengan kata lain, z-score menunjukkan seberapa "menonjol" atau "rendah" occupancy rate dari suatu site dibandingkan dengan site lainnya dalam data Anda.
        
        ### Interpretasi Hasil
        - **Z-Score Positif**: Jika suatu site memiliki z-score positif (misalnya Melati dengan nilai z-score 0.1359), 
          itu berarti occupancy rate site ini **di atas rata-rata** dibandingkan site lain dalam dataset Anda. 
          Semakin tinggi nilai z-score positif, semakin besar occupancy rate dibandingkan rata-rata.
        - **Z-Score Negatif**: Jika suatu site memiliki z-score negatif (misalnya Pelaga dengan nilai z-score -0.4928), 
          itu berarti occupancy rate site ini **di bawah rata-rata**. 
          Semakin rendah nilai z-score negatif, semakin jauh occupancy rate dari rata-rata occupancy rate dalam dataset.
        - **Nilai Z-Score Dekat Nol**: Jika suatu site memiliki z-score mendekati nol (misalnya The Mansion dengan 0.0604), 
          occupancy rate site tersebut mendekati rata-rata occupancy rate dari semua site.

        ### Mengapa Z-Score Berguna?
        Z-score membuat perbandingan antar-site menjadi lebih adil, karena sekarang occupancy rate diukur berdasarkan seberapa jauh dari rata-rata 
        (mengabaikan perbedaan kapasitas). Dengan z-score, kita dapat melihat site mana yang performanya lebih tinggi atau lebih rendah dalam konteks 
        keseluruhan, tanpa dipengaruhi oleh kapasitas masing-masing site.
    """)
    st.header(f"Normalized Occupancy Rate Analysis (Z-Score) for {program_choice}")

    # Tampilkan informasi tahun dan bulan yang dipilih dalam format teks sederhana
    if selected_year != "All" or selected_month != "All":
        year_month_info = f"Year: {selected_year}" if selected_year != "All" else ""
        month_info = f"Month: {selected_month}" if selected_month != "All" else ""
        st.markdown(f"**{year_month_info} {month_info}**")

    # Pastikan kolom 'Fill' dan 'Capacity' ada di data untuk menghitung occupancy rate
    if 'Fill' in filtered_occupancy_data.columns and 'Capacity' in filtered_occupancy_data.columns:
        
        # Hitung occupancy rate dalam persentase
        filtered_occupancy_data['Occupancy Rate (%)'] = (filtered_occupancy_data['Fill'] / filtered_occupancy_data['Capacity']) * 100
        filtered_occupancy_data['Occupancy Rate (%)'] = filtered_occupancy_data['Occupancy Rate (%)'].round(2)  # Membulatkan ke dua desimal

        # Menghitung rata-rata dan standar deviasi occupancy rate untuk normalisasi
        mean_occupancy_rate = filtered_occupancy_data['Occupancy Rate (%)'].mean()
        std_occupancy_rate = filtered_occupancy_data['Occupancy Rate (%)'].std()

        # Menghitung z-score untuk occupancy rate normalisasi
        filtered_occupancy_data['Occupancy Z-Score'] = ((filtered_occupancy_data['Occupancy Rate (%)'] - mean_occupancy_rate) / std_occupancy_rate).round(2)

        # Mengelompokkan data berdasarkan 'Site' dan menghitung rata-rata occupancy rate dan z-score
        occupancy_normalized_by_site = filtered_occupancy_data.groupby('Site').agg(
            Capacity=('Capacity', 'sum'),
            Fill=('Fill', 'sum'),
            Average_Occupancy_Rate=('Occupancy Rate (%)', 'mean'),
            Normalized_Occupancy_ZScore=('Occupancy Z-Score', 'mean')
        ).reset_index()

        # Tampilkan data Occupancy Rate per Site dalam tabel dengan z-score
        # st.subheader("Normalized Occupancy Rate per Site (Z-Score)")
        st.dataframe(occupancy_normalized_by_site.rename(columns={
            'Capacity': 'Total Capacity',
            'Fill': 'Total Fill',
            'Average_Occupancy_Rate': 'Average Occupancy Rate (%)',
            'Normalized_Occupancy_ZScore': 'Normalized Occupancy Z-Score'
        }))

        # Buat grafik Occupancy Z-Score per Site menggunakan Plotly
        fig = px.bar(
            occupancy_normalized_by_site,
            x="Site",
            y="Normalized_Occupancy_ZScore",
            title="Normalized Occupancy Rate by Site (Z-Score)",
            labels={"Normalized_Occupancy_ZScore": "Occupancy Z-Score", "Site": "Site"},
            color="Normalized_Occupancy_ZScore",
            color_continuous_scale="Viridis"
        )
        fig.update_layout(xaxis_tickangle=-45)  # Memutar label X untuk keterbacaan
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Data tidak memiliki kolom 'Fill' dan 'Capacity' yang diperlukan untuk menghitung occupancy rate.")
