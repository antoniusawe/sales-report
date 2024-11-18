import streamlit as st
import pandas as pd
import pages.overview as overview  # Import file overview
import pages.location as location  # Import file location
import pages.batch as batch  # Import file location

def show(occupancy_data, sales_data):
    # Radio button untuk memilih program
    program_choice = st.radio("Choose program:", ["200HR", "300HR"], horizontal=True, key="program_choice")

    # Filter data berdasarkan pilihan program
    filtered_occupancy_data = occupancy_data[occupancy_data['Category'] == program_choice]
    filtered_sales_data = sales_data[sales_data['Category'] == program_choice]

    # Dropdown untuk memilih Year, sesuai dengan data hasil filter Program
    years = ["All"] + sorted(filtered_occupancy_data['Year'].unique().tolist())
    selected_year = st.selectbox("Select Year", years, key="year_select")

    # Filter data berdasarkan Year (kecuali jika "All" dipilih)
    if selected_year != "All":
        filtered_occupancy_data = filtered_occupancy_data[filtered_occupancy_data['Year'] == selected_year]
        filtered_sales_data = filtered_sales_data[filtered_sales_data['Year'] == selected_year]

        # Konversi kolom Month menjadi datetime dan mengurutkannya
        filtered_occupancy_data['Month'] = pd.to_datetime(filtered_occupancy_data['Month'], format='%B')

        # Membuat list bulan yang diurutkan dalam format string untuk dropdown
        months = ["All"] + filtered_occupancy_data['Month'].dt.month_name().unique().tolist()
        selected_month = st.selectbox("Select Month", months, key="month_select")

        # Filter data berdasarkan Month yang dipilih
        if selected_month != "All":
            filtered_occupancy_data = filtered_occupancy_data[filtered_occupancy_data['Month'].dt.month_name() == selected_month]
            filtered_sales_data = filtered_sales_data[filtered_sales_data['Month'] == selected_month]
    else:
        selected_month = "All"  # Jika "All" dipilih di Year, otomatis bulan menjadi "All" juga

    # Menampilkan pilihan halaman (Overview, Location, Batch)
    view_choice = st.radio("Select Analysis:", ["Overview", "Location", "Batch"], horizontal=True, key="view_choice")

    # Menampilkan konten berdasarkan pilihan tampilan
    if view_choice == "Overview":
        overview.show_overview(filtered_occupancy_data, filtered_sales_data)
    elif view_choice == "Location":
        # Pastikan bahwa program_choice, selected_year, dan selected_month diteruskan ke show_location
        location.show_location(filtered_occupancy_data, filtered_sales_data, program_choice, selected_year, selected_month)
    elif view_choice == "Batch":
        batch.show_batch(filtered_sales_data, program_choice, selected_year, selected_month)
