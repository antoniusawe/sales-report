import streamlit as st
import pandas as pd
import plotly.express as px

def show_occupancy_rate(filtered_occupancy_data, program_choice, selected_year, selected_month):
    st.header(f"Occupancy Rate Analysis for {program_choice}")

    # Tampilkan informasi tahun dan bulan yang dipilih
    if selected_year != "All":
        st.subheader(f"Year: {selected_year}")
    if selected_month != "All":
        st.subheader(f"Month: {selected_month}")

    # Pastikan kolom 'Fill' dan 'Capacity' ada di data untuk menghitung occupancy rate
    if 'Fill' in filtered_occupancy_data.columns and 'Capacity' in filtered_occupancy_data.columns:
        
        # Hitung occupancy rate dalam persentase
        filtered_occupancy_data['Occupancy Rate (%)'] = (filtered_occupancy_data['Fill'] / filtered_occupancy_data['Capacity']) * 100
        filtered_occupancy_data['Occupancy Rate (%)'] = filtered_occupancy_data['Occupancy Rate (%)'].round(2)  # Membulatkan ke dua desimal

        # Mengelompokkan data berdasarkan 'Site' dan menghitung rata-rata occupancy rate
        occupancy_rate_by_site = filtered_occupancy_data.groupby('Site').agg(
            Capacity=('Capacity', 'sum'),
            Fill=('Fill', 'sum'),
            Occupancy_Rate=('Occupancy Rate (%)', 'mean')
        ).reset_index()

        # Tampilkan data Occupancy Rate per Site dalam tabel
        st.subheader("Average Occupancy Rate per Site")
        st.dataframe(occupancy_rate_by_site.rename(columns={
            'Capacity': 'Total Capacity',
            'Fill': 'Total Fill',
            'Occupancy_Rate': 'Average Occupancy Rate (%)'
        }))

        # Buat grafik Occupancy Rate per Site menggunakan Plotly
        fig = px.bar(
            occupancy_rate_by_site,
            x="Site",
            y="Occupancy_Rate",
            title="Average Occupancy Rate by Site",
            labels={"Occupancy_Rate": "Occupancy Rate (%)", "Site": "Site"},
            color="Occupancy_Rate",
        )
        fig.update_layout(xaxis_tickangle=-45)  # Memutar label X untuk keterbacaan
        st.plotly_chart(fig, use_container_width=True)

        # Analisis per Bulan (jika ada kolom 'Month')
        if 'Month' in filtered_occupancy_data.columns:
            # Konversi 'Month' ke datetime untuk diurutkan, lalu kembalikan ke nama bulan
            filtered_occupancy_data['Month_dt'] = pd.to_datetime(filtered_occupancy_data['Month'], format='%B')
            occupancy_rate_by_month = filtered_occupancy_data.groupby('Month_dt').agg(
                Capacity=('Capacity', 'sum'),
                Fill=('Fill', 'sum'),
                Occupancy_Rate=('Occupancy Rate (%)', 'mean')
            ).reset_index()
            occupancy_rate_by_month = occupancy_rate_by_month.sort_values(by='Month_dt')  # Urutkan berdasarkan datetime

            # Ubah 'Month_dt' kembali menjadi nama bulan
            occupancy_rate_by_month['Month'] = occupancy_rate_by_month['Month_dt'].dt.strftime('%B')
            occupancy_rate_by_month = occupancy_rate_by_month.drop(columns=['Month_dt'])  # Hapus kolom datetime

            # Tampilkan data Occupancy Rate per Month dalam tabel
            st.subheader("Average Occupancy Rate per Month")
            st.dataframe(occupancy_rate_by_month.rename(columns={
                'Capacity': 'Total Capacity',
                'Fill': 'Total Fill',
                'Occupancy_Rate': 'Average Occupancy Rate (%)'
            }))

            # Grafik Occupancy Rate per Month
            fig_month = px.line(
                occupancy_rate_by_month,
                x="Month",
                y="Occupancy_Rate",
                title="Average Occupancy Rate by Month",
                labels={"Occupancy_Rate": "Occupancy Rate (%)", "Month": "Month"},
                markers=True,
            )
            fig_month.update_layout(xaxis_tickangle=-45)  # Memutar label X untuk keterbacaan
            st.plotly_chart(fig_month, use_container_width=True)

    else:
        st.error("Data tidak memiliki kolom 'Fill' dan 'Capacity' yang diperlukan untuk menghitung occupancy rate.")
