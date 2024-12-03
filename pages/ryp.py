import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

import pages.booking_ryp as booking_ryp
import pages.payable_ryp as payable_ryp

def calculate_payment_metrics(data):
    """Menghitung metrik pembayaran dari dataset."""
    total_students = len(data)
    total_payment_received = data['TOTAL PAYABLE (IN USD OR USD EQUIV)'].sum()
    total_pending_payment = data['STUDENT STILL TO PAY'].sum()
    outstanding_percentage = (
        (total_pending_payment / total_payment_received * 100) if total_payment_received > 0 else 0
    )
    return total_students, total_payment_received, total_pending_payment, outstanding_percentage

def validate_columns(data, required_columns):
    """Validasi apakah kolom yang dibutuhkan ada di dataset."""
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        st.error(f"Required columns are missing: {', '.join(missing_columns)}")
        return False
    return True

def show_ryp(df_ryp_200hr, df_ryp_300hr):
    # Header utama untuk halaman
    st.header("RYP Student Database")
    st.caption("Overview of student data for 200HR and 300HR programs.")

    # Radio button untuk memilih program
    program_choice = st.radio(
        "Choose Program:",
        ["All", "200HR", "300HR"],
        horizontal=True,
        key="program_choice_radio"  # Key unik
    )

    # Filter data berdasarkan pilihan program
    if program_choice == "All":
        df_ryp_200hr['PROGRAM'] = '200HR'
        df_ryp_300hr['PROGRAM'] = '300HR'
        ryp_data = pd.concat([df_ryp_200hr, df_ryp_300hr], ignore_index=True)
    elif program_choice == "200HR":
        ryp_data = df_ryp_200hr.copy()
    else:
        ryp_data = df_ryp_300hr.copy()

    # Validasi kolom data
    required_columns = ['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT', 'STUDENT STILL TO PAY', 'TOTAL PAYABLE (IN USD OR USD EQUIV)']
    if not validate_columns(ryp_data, required_columns):
        return

    # Proses kolom tanggal booking
    ryp_data['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT'] = pd.to_datetime(
        ryp_data['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT'], errors='coerce'
    )

    # Tambahkan dropdown pilihan Year
    year_options = ["All"] + sorted(ryp_data['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT'].dropna().dt.year.unique().tolist())
    selected_year = st.selectbox("Select Year", year_options, key="year_dropdown")

    # Filter data berdasarkan Year
    if selected_year != "All":
        ryp_data = ryp_data[ryp_data['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT'].dt.year == int(selected_year)]

    # Menentukan apakah Month dropdown harus dinonaktifkan
    month_disabled = selected_year == "All"

    # Tambahkan dropdown pilihan Month hanya jika Year bukan "All"
    if not month_disabled:
        # Menampilkan opsi bulan
        month_options = ["All"] + sorted(ryp_data['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT'].dropna().dt.strftime('%B').unique().tolist())
        selected_month = st.selectbox("Select Month", month_options, key="month_dropdown")

        # Filter data berdasarkan Month
        if selected_month != "All":
            ryp_data = ryp_data[ryp_data['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT'].dt.strftime('%B') == selected_month]
    else:
        # Jika Year adalah "All", tampilkan Select Month yang tidak tersedia
        selected_month = st.selectbox("Select Month", ["All"], disabled=True)

    # Perhitungan metrik pembayaran
    total_students, total_payment_received, total_pending_payment, outstanding_percentage = calculate_payment_metrics(ryp_data)

    # Tampilkan metrik dengan gaya HTML
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div style="margin-right: 20px;">
                <h2 style="font-size: 20px; color: #333333;">Total Booking</h2>
                <h1 style="font-size: 46px; color: #333333; margin: 0;">{total_students}</h1>
                <p style="font-size: 18px; color: #1f77b4;">Number of students</p>
            </div>
            <div style="margin: 0 20px;">
                <h2 style="font-size: 20px; color: #333333;">Total Payable</h2>
                <h1 style="font-size: 46px; color: #333333; margin: 0;">${total_payment_received:,.0f}</h1>
                <p style="font-size: 18px; color: #1f77b4;">in USD or USD equiv</p>
            </div>
            <div style="margin-left: 20px;">
                <h2 style="font-size: 20px; color: #333333;">Outstanding</h2>
                <h1 style="font-size: 46px; color: #333333; margin: 0;">${total_pending_payment:,.0f}</h1>
                <p style="font-size: 18px; color: #1f77b4;">{outstanding_percentage:.2f}% of Total Payable</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Tambahkan radio button untuk memilih tampilan
    selected_view = st.radio(
        "View Data",
        ["Booking", "Payable"],
        horizontal=True,
        key="view_data_radio"  # Key unik
    )

    # Tampilkan data berdasarkan pilihan radio button
    if selected_view == "Booking":
        booking_ryp.show_booking(ryp_data, program_choice)
    elif selected_view == "Payable":
        payable_ryp.show_payable(ryp_data, program_choice)
