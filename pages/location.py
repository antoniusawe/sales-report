import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def show_location(filtered_df_sales):
    st.header("Accommodation Sales by Location and Month")
    st.caption("This overview uses the **DATE OF PAYMENT** as the primary reference for the analysis.")

    # Mengurutkan data berdasarkan NAME dan DATE OF PAYMENT (oldest first)
    filtered_df_sales['DATE OF PAYMENT'] = pd.to_datetime(filtered_df_sales['DATE OF PAYMENT'], errors='coerce')
    filtered_df_sales = filtered_df_sales.sort_values(by=['NAME', 'DATE OF PAYMENT'])

    # Hapus duplikat berdasarkan 'NAME', hanya ambil yang paling awal
    unique_bookings = filtered_df_sales.drop_duplicates(subset='NAME', keep='first')

    # Tambahkan kolom nomor bulan untuk pengurutan
    unique_bookings['MONTH_NUM'] = pd.to_datetime(unique_bookings['MONTH'], format='%B', errors='coerce').dt.month

    # Urutkan data berdasarkan LOCATION dan MONTH_NUM
    unique_bookings = unique_bookings.sort_values(by=['LOCATION', 'MONTH_NUM'])

    # Agregasi data berdasarkan LOCATION, MONTH, dan define_accommodation
    aggregated_data = unique_bookings.groupby(['LOCATION', 'MONTH', 'define_accommodation']).size().reset_index(name='count')

    # Konversi urutan bulan menjadi nama bulan
    aggregated_data['MONTH'] = pd.to_datetime(aggregated_data['MONTH'], format='%B', errors='coerce')
    aggregated_data = aggregated_data.sort_values(by=['LOCATION', 'MONTH'])
    aggregated_data['MONTH'] = aggregated_data['MONTH'].dt.strftime('%B')

    # Jika data agregasi kosong, tampilkan peringatan
    if aggregated_data.empty:
        st.warning("No data available for the selected criteria.")
        return

    # Tampilkan visualisasi per LOCATION
    locations = aggregated_data['LOCATION'].unique()
    for location in locations:
        # st.subheader(f"Sales for {location}")

        # Filter data untuk lokasi ini
        location_data = aggregated_data[aggregated_data['LOCATION'] == location]

        # **Definisikan Warna Tetap untuk Setiap Accommodation**
    accommodation_colors = {
        "DORM": "#89CFF0",  # Baby Blue
        "PRIVATE": "#0000FF",  # Blue
        "TWIN": "#7393B3",  # Blue Gray
        "TWIN DELUXE": "#6495ED",  # Cornflower Blue
        "DELUXE": "#6082B6",  # Glaucous
        "GRAND DELUXE": "#1F51FF",  # Neon Blue
        "PRIVATE DELUXE": "#96DED1",  # Robin Egg Blue
        "TRIPLE": "#9FE2BF",  # Seafoam Green
        "NO ACCOMMODATION": "#0818A8",  # Zaffre
        "3DAYS SHT": "#008080"  # Tßeal
    }

    # Tampilkan visualisasi per LOCATION
    locations = aggregated_data['LOCATION'].unique()
    for location in locations:
        # Filter data untuk lokasi ini
        location_data = aggregated_data[aggregated_data['LOCATION'] == location]

        # Buat bar chart horizontal untuk lokasi ini
        fig = px.bar(
            location_data,
            x='count',  # Jumlah booking
            y='MONTH',  # Bulan di Y-axis
            color='define_accommodation',  # Stack berdasarkan akomodasi
            color_discrete_map=accommodation_colors,  # Gunakan color mapping
            orientation='h',  # Horizontal bar chart
            title=f"Accommodation Sales in {location}",
            labels={'count': 'Number of Sales', 'MONTH': 'Month', 'define_accommodation': 'Accommodation'},
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
