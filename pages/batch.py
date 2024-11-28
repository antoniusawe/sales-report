import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def show_batch(filtered_df_sales):
    st.header("Overview by Batch")
    st.caption("This overview uses the **SCHEDULE DATE** as the primary reference for the analysis.")

    # Validasi kolom yang diperlukan
    required_columns = ['corrected_schedule_month', 'NAME', 'LOCATION', 'define_accommodation', 'DATE OF PAYMENT']
    missing_columns = [col for col in required_columns if col not in filtered_df_sales.columns]
    if missing_columns:
        st.error(f"Kolom berikut tidak ada dalam dataset: {', '.join(missing_columns)}")
        return

    # Konversi `corrected_schedule_month` ke format datetime
    filtered_df_sales['corrected_schedule_month'] = pd.to_datetime(
        filtered_df_sales['corrected_schedule_month'], errors='coerce'
    )

    # Ambil bulan dan tahun sebagai Batch Identifier
    filtered_df_sales['BATCH'] = filtered_df_sales['corrected_schedule_month'].dt.strftime('%b-%Y')

    # Mengurutkan data berdasarkan urutan kalender pada `BATCH`
    filtered_df_sales['BATCH_SORT'] = pd.to_datetime(filtered_df_sales['BATCH'], format='%b-%Y', errors='coerce')

    # Urutkan berdasarkan BATCH_SORT dan `DATE OF PAYMENT`
    filtered_df_sales['DATE OF PAYMENT'] = pd.to_datetime(filtered_df_sales['DATE OF PAYMENT'], errors='coerce')
    filtered_df_sales = filtered_df_sales.sort_values(by=['BATCH_SORT', 'DATE OF PAYMENT'])

    # **Agregasi Data Berdasarkan BATCH**
    # Hitung jumlah nama unik yang dijual untuk setiap batch dan lokasi
    batch_summary = (
        filtered_df_sales.groupby(['BATCH', 'LOCATION'])
        .agg(unique_names=('NAME', 'nunique'))
        .reset_index()
    )

    # Urutkan kembali berdasarkan urutan kalender
    batch_summary['BATCH_SORT'] = pd.to_datetime(batch_summary['BATCH'], format='%b-%Y', errors='coerce')
    batch_summary = batch_summary.sort_values(by=['BATCH_SORT', 'LOCATION'])

    # Jika data batch kosong, tampilkan peringatan
    if batch_summary.empty:
        st.warning("No data available for the selected criteria.")
        return

    # **Visualisasi: Stacked Bar Chart**
    fig_stacked = px.bar(
        batch_summary,
        x='unique_names',  # Jumlah nama unik di X-axis
        y='BATCH',  # Batch di Y-axis
        color='LOCATION',
        title="Total Sales by Batch (Schedule Month)",
        labels={'unique_names': 'Number of Unique Names', 'BATCH': 'Batch', 'LOCATION': 'Location'},
        text='unique_names',
        orientation='h',  # Bar chart horizontal
        barmode='stack'  # Mode stack untuk lokasi
    )
    fig_stacked.update_layout(
        xaxis_title="Number of Sales",
        yaxis_title="Batch",
        legend_title="Location",
        height=700  # Tinggi grafik untuk menampung semua Batch
    )
    st.plotly_chart(fig_stacked, use_container_width=True)

    # **Breakdown per Accommodation**

    # Konversi 'DATE OF PAYMENT' menjadi datetime
    filtered_df_sales['DATE OF PAYMENT'] = pd.to_datetime(filtered_df_sales['DATE OF PAYMENT'], errors='coerce')
    filtered_df_sales = filtered_df_sales.sort_values(by=['NAME', 'DATE OF PAYMENT'])

    # Hapus duplikat berdasarkan 'NAME', hanya ambil yang paling awal
    unique_bookings = filtered_df_sales.drop_duplicates(subset='NAME', keep='first')

    # Konversi 'corrected_schedule_month' menjadi datetime
    unique_bookings['corrected_schedule_month'] = pd.to_datetime(unique_bookings['corrected_schedule_month'], errors='coerce')

    # Hapus baris dengan nilai kosong pada 'corrected_schedule_month'
    unique_bookings = unique_bookings.dropna(subset=['corrected_schedule_month'])

    # Tambahkan kolom bulan dan tahun untuk agregasi
    unique_bookings['Month_Name'] = unique_bookings['corrected_schedule_month'].dt.strftime('%B')  # Nama bulan
    unique_bookings['Year'] = unique_bookings['corrected_schedule_month'].dt.year.astype(int)  # Tahun sebagai integer
    unique_bookings['Month_Num'] = unique_bookings['corrected_schedule_month'].dt.month  # Nomor bulan

    # Agregasi data berdasarkan lokasi, define_accommodation, bulan, dan tahun
    aggregated_data = (
        unique_bookings.groupby(['LOCATION', 'define_accommodation', 'Year', 'Month_Num', 'Month_Name'])
        .size()
        .reset_index(name='count')
    )

    # Buat kolom untuk visualisasi yang menggabungkan bulan dan tahun
    aggregated_data['Month_Year'] = aggregated_data['Month_Name'] + " " + aggregated_data['Year'].astype(str)

    # Urutkan data berdasarkan Year, Month_Num, dan lokasi
    aggregated_data = aggregated_data.sort_values(by=['Year', 'Month_Num', 'LOCATION'])

    # Buang kolom sementara jika tidak diperlukan
    aggregated_data = aggregated_data.drop(columns=['Month_Num'])

    # Jika data agregasi kosong, tampilkan peringatan
    if aggregated_data.empty:
        st.warning("No data available for the selected criteria.")
    else:
        # Definisikan warna tetap untuk setiap 'define_accommodation'
        accommodation_colors = {
            "DORM": "#89CFF0",        # Baby Blue
            "PRIVATE": "#0000FF",     # Blue
            "TWIN": "#7393B3",        # Blue Gray
            "TWIN DELUXE": "#6495ED", # Cornflower Blue
            "DELUXE": "#6082B6",      # Glaucous
            "GRAND DELUXE": "#1F51FF",# Neon Blue
            "PRIVATE DELUXE": "#96DED1", # Robin Egg Blue
            "TRIPLE": "#9FE2BF",      # Seafoam Green
            "NO ACCOMMODATION": "#0818A8", # Zaffre
            "3DAYS SHT": "#008080"    # Teal
        }

        # Tampilkan visualisasi per LOCATION
        locations = aggregated_data['LOCATION'].unique()
        for location in locations:
            # Filter data untuk lokasi ini
            location_data = aggregated_data[aggregated_data['LOCATION'] == location]

            # Buat bar chart horizontal untuk lokasi ini
            fig = px.bar(
                location_data,
                x='count',                         # Jumlah booking
                y='Month_Year',                    # Gabungan bulan dan tahun di Y-axis
                color='define_accommodation',      # Stack berdasarkan akomodasi
                color_discrete_map=accommodation_colors,  # Gunakan color mapping
                orientation='h',                   # Horizontal bar chart
                title=f"Accommodation Sales in {location}",
                labels={
                    'count': 'Number of Sales',
                    'Month_Year': 'Month',
                    'define_accommodation': 'Accommodation'
                },
                text='count',
                barmode='stack'
            )
            fig.update_layout(
                xaxis_title="Number of Sales",
                yaxis_title="Month",
                legend_title="Accommodation",
                height=500  # Tinggi grafik agar rapi
            )

            # Tampilkan grafik di Streamlit
            st.plotly_chart(fig, use_container_width=True)
