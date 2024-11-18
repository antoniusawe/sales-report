import streamlit as st
import pandas as pd
from pages.occupancy_rate import show_occupancy_rate
from pages.occupancy_zscore import show_occupancy_zscore  # Import fungsi Z-Score

def show_location(filtered_occupancy_data, filtered_sales_data, program_choice, selected_year, selected_month):
    st.header("Total Available Rooms per Site")

    # Menghitung total 'Available' berdasarkan 'Site' dan 'Batch start date' sesuai data yang sudah difilter
    available_data_by_site = filtered_occupancy_data.groupby(['Site', 'Batch start date'])['Available'].sum().reset_index()

    # Menghitung total available rooms per Site
    total_available_per_site = available_data_by_site.groupby('Site')['Available'].sum().reset_index()

    # Menambahkan kolom 'Batch Details' dengan informasi batch start date dan jumlah available untuk setiap site
    total_available_per_site['Batch Details'] = total_available_per_site['Site'].apply(
        lambda site: ", ".join([f"{date} ({available})" for date, available in zip(
            available_data_by_site[available_data_by_site['Site'] == site]['Batch start date'],
            available_data_by_site[available_data_by_site['Site'] == site]['Available']
        )])
    )

    # Menampilkan data dalam format grid
    num_columns = 2
    rows = [st.columns(num_columns) for _ in range((len(total_available_per_site) + num_columns - 1) // num_columns)]

    for index, row in enumerate(total_available_per_site.iterrows()):
        site_name = row[1]['Site']
        total_available = row[1]['Available']
        batch_details = row[1]['Batch Details']

        row_index = index // num_columns
        col_index = index % num_columns

        with rows[row_index][col_index]:
            st.markdown(f"""
                <div style='
                    text-align: center; 
                    width: 200px; 
                    padding: 20px; 
                    margin: 10px; 
                    border-radius: 15px; 
                    background: linear-gradient(145deg, #e6e6e6, #ffffff);
                    box-shadow:  5px 5px 15px #aaaaaa, 
                                 -5px -5px 15px #ffffff;
                '>
                    <div style='font-size: 16px; color: #333333;'>{site_name}</div>
                    <br>
                    <div style='font-size: 48px; color: #202fb2;'>{total_available}</div>
                    <div style='color: #202fb2; font-size: 18px;'>Total Available Rooms</div>
                    <br>
                    <div style='font-size: 16px; color: #333333;'>Batch:</div>
                    <div style='font-size: 14px; color: #666666;'>{batch_details}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tombol untuk Generate Occupancy Rate
    if st.button("Generate Occupancy Rate"):
        show_occupancy_rate(filtered_occupancy_data, program_choice, selected_year, selected_month)

    # Tombol untuk Generate Z-Score
    if st.button("Generate Z-Score"):
        show_occupancy_zscore(filtered_occupancy_data, program_choice, selected_year, selected_month)
