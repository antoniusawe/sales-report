import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def show_occupancy(filtered_df_occupancy, program_choice, selected_year, selected_month, selected_week):
    st.header(f"Occupancy Rate Analysis for {program_choice}")

    # Tampilkan informasi filter
    if selected_year != "All":
        st.subheader(f"Year: {selected_year}")
    if selected_month != "All":
        st.subheader(f"Month: {selected_month}")
    if selected_week != "All":
        st.subheader(f"Week: {selected_week}")

    # Validasi apakah data occupancy tersedia
    if filtered_df_occupancy.empty:
        st.warning("Filtered occupancy data is empty. Please check your filters.")
        return

    # Pastikan kolom penting tersedia
    required_columns = ['SITE', 'ROOM', 'FILL', 'CAPACITY', 'MONTH', 'YEAR', 'WEEK']
    missing_columns = [col for col in required_columns if col not in filtered_df_occupancy.columns]
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return

    # Filter berdasarkan Year
    if selected_year != "All":
        filtered_df_occupancy = filtered_df_occupancy[filtered_df_occupancy['YEAR'] == int(selected_year)]

    # Filter berdasarkan Month
    if selected_month != "All":
        filtered_df_occupancy = filtered_df_occupancy[filtered_df_occupancy['MONTH'] == selected_month]

    # Filter berdasarkan Week
    if selected_week != "All":
        filtered_df_occupancy = filtered_df_occupancy[filtered_df_occupancy['WEEK'] == selected_week]

    # Breakdown data per Site, Room, dan Month
    occupancy_rate_by_site_room = (
        filtered_df_occupancy.groupby(['SITE', 'ROOM', 'MONTH'])
        .agg(
            Total_Capacity=('CAPACITY', 'sum'),
            Total_Fill=('FILL', 'sum')
        )
        .reset_index()
    )

    # Hitung ulang Occupancy Rate berdasarkan Total Fill dan Total Capacity
    occupancy_rate_by_site_room['Occupancy Rate (%)'] = (
        (occupancy_rate_by_site_room['Total_Fill'] / occupancy_rate_by_site_room['Total_Capacity']) * 100
    ).round(2)

    # Sort Bulan agar sesuai dengan urutan kalender
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    occupancy_rate_by_site_room['MONTH'] = pd.Categorical(
        occupancy_rate_by_site_room['MONTH'], categories=month_order, ordered=True
    )
    occupancy_rate_by_site_room = occupancy_rate_by_site_room.sort_values(by=['SITE', 'MONTH', 'ROOM'])

    # Tampilkan tabel breakdown Occupancy Rate per Site
    st.subheader("Occupancy Rate Breakdown by Site")
    sites = occupancy_rate_by_site_room['SITE'].unique()
    for site in sites:
        site_data = occupancy_rate_by_site_room[occupancy_rate_by_site_room['SITE'] == site]
        st.subheader(site)

        # Pindahkan MONTH ke paling kiri dan hapus kolom SITE
        site_data = site_data[['MONTH', 'ROOM', 'Total_Capacity', 'Total_Fill', 'Occupancy Rate (%)']]

        # Tampilkan tabel per site
        st.dataframe(site_data.rename(columns={
            'ROOM': 'Room',
            'MONTH': 'Month',
            'Total_Capacity': 'Total Capacity',
            'Total_Fill': 'Total Fill',
            'Occupancy Rate (%)': 'Occupancy Rate (%)'
        }))

        # **Buat Horizontal Bar Chart dengan Occupancy Rate**
        fig = px.bar(
            site_data,
            x='Occupancy Rate (%)',
            y='MONTH',  # Harus konsisten dengan nama kolom
            color='ROOM',
            orientation='h',
            title=f"Occupancy Rate in {site} (in %)",
            labels={'Occupancy Rate (%)': 'Occupancy Rate (%)', 'MONTH': 'Month', 'ROOM': 'Room'},
            text='Occupancy Rate (%)',
            color_discrete_sequence=px.colors.qualitative.Set2  # Pilihan warna
        )
        fig.update_layout(
            xaxis_title="Occupancy Rate (%)",
            yaxis_title="Month",
            legend_title="Room",
            height=500  # Sesuaikan tinggi chart
        )

        # Tampilkan grafik di Streamlit
        st.plotly_chart(fig, use_container_width=True)
