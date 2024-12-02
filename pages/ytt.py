import streamlit as st
import pandas as pd

import pages.booking as booking
import pages.location as location
import pages.batch as batch
import pages.occupancy as occupancy

def show(df_sales, df_occupancy, df_leads):
    # Tambahkan opsi "All" untuk produk
    product_options = ["All", "200HR", "300HR"]  # Tambahkan opsi secara manual
    product_choice = st.radio("Choose product:", product_options, horizontal=True, key="product_choice")

    with st.spinner('Processing...'):
        # Filter data berdasarkan pilihan produk, kecuali jika "All" dipilih
        if product_choice != "All":
            filtered_df_sales = df_sales[df_sales['define_product'].str.strip() == product_choice]
            filtered_df_occupancy = df_occupancy[df_occupancy['CATEGORY'].str.strip() == product_choice]
        else:
            filtered_df_sales = df_sales.copy()
            filtered_df_occupancy = df_occupancy.copy()

        # Menambahkan kolom WEEK ke df_occupancy jika belum ada
        if 'WEEK' not in filtered_df_occupancy.columns:
            if 'BATCH START DATE' in filtered_df_occupancy.columns:
                filtered_df_occupancy['BATCH START DATE'] = pd.to_datetime(
                    filtered_df_occupancy['BATCH START DATE'], errors='coerce'
                )
                filtered_df_occupancy['WEEK'] = filtered_df_occupancy['BATCH START DATE'].apply(
                    lambda x: f"WEEK {((x.day - 1) // 7) + 1}" if pd.notnull(x) else None
                )
            else:
                st.error("Kolom 'BATCH START DATE' tidak ditemukan dalam occupancy data.")
                return

        # Menambahkan kolom WEEK ke df_leads berdasarkan 'created_at'
        if 'CREATED_AT' in df_leads.columns:
            df_leads['CREATED_AT'] = pd.to_datetime(df_leads['CREATED_AT'], errors='coerce')
            df_leads['WEEK'] = df_leads['CREATED_AT'].apply(lambda x: f"WEEK {((x.day - 1) // 7) + 1}" if pd.notnull(x) else None)
            df_leads['YEAR'] = df_leads['CREATED_AT'].dt.year.astype(int)
            df_leads['MONTH'] = df_leads['CREATED_AT'].dt.month_name().str.upper()

        # Dropdown untuk memilih Year, hilangkan .0
        years = ["All"] + sorted(filtered_df_sales['YEAR'].dropna().astype(int).unique().tolist())
        selected_year = st.selectbox("Select Year", years, key="year_select")

        # Filter data berdasarkan Year (kecuali jika "All" dipilih)
        if selected_year != "All":
            filtered_df_sales = filtered_df_sales[filtered_df_sales['YEAR'] == selected_year]
            filtered_df_leads = df_leads[df_leads['YEAR'] == int(selected_year)]
        else:
            filtered_df_leads = df_leads.copy()

            # Konversi kolom Month menjadi string nama bulan (jika berubah menjadi datetime)
            filtered_df_sales['MONTH'] = pd.to_datetime(filtered_df_sales['MONTH'], format='%B', errors='coerce').dt.strftime('%B')

        # Membuat dropdown untuk memilih bulan
        months = ["All"] + filtered_df_sales['MONTH'].dropna().unique().tolist()
        selected_month = st.selectbox("Select Month", months, key="month_select")

        # Filter data berdasarkan Month yang dipilih
        if selected_month != "All":
            filtered_df_sales = filtered_df_sales[filtered_df_sales['MONTH'] == selected_month]
            filtered_df_leads = filtered_df_leads[filtered_df_leads['MONTH'] == selected_month]

        # Membuat dropdown untuk memilih WEEK
        weeks = ["All"] + filtered_df_sales['WEEK'].dropna().unique().tolist()
        selected_week = st.selectbox("Select Week", weeks, key="week_select")

        # Filter data berdasarkan WEEK yang dipilih
        if selected_week != "All":
            filtered_df_sales = filtered_df_sales[filtered_df_sales['WEEK'] == selected_week]
            filtered_df_leads = filtered_df_leads[filtered_df_leads['WEEK'] == selected_week]
        else:
            selected_month = "All"  # Jika "All" dipilih di Year, otomatis bulan menjadi "All"
            selected_week = "All"  # Jika "All" dipilih di Year, otomatis minggu menjadi "All"

    # Pastikan format kolom YEAR tetap string angka tanpa pemisah ribuan
    if not filtered_df_sales['YEAR'].isnull().all():
        filtered_df_sales['YEAR'] = filtered_df_sales['YEAR'].fillna(0).astype(int).astype(str)
    else:
        st.warning("Kolom YEAR hanya mengandung NaN atau kosong.")

    filtered_df_sales['MONTH'] = filtered_df_sales['MONTH'].astype(str)

    # Menampilkan pilihan halaman (Overview, Location, Batch)
    view_choice = st.radio("Select View:", ["Booking", "Location", "Batch", "Occupancy Rate", "Leads"], horizontal=True, key="view_choice")

    # Menampilkan konten berdasarkan pilihan tampilan
    if view_choice == "Booking":
        booking.show_booking(filtered_df_sales, filtered_df_leads)
    elif view_choice == "Location":
        location.show_location(filtered_df_sales)
    elif view_choice == "Batch":
        batch.show_batch(filtered_df_sales)
    elif view_choice == "Occupancy Rate":
        occupancy.show_occupancy(
            filtered_df_occupancy=filtered_df_occupancy,
            program_choice=product_choice,
            selected_year=selected_year,
            selected_month=selected_month,
            selected_week=selected_week
        )
