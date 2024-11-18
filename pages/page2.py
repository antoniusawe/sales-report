import streamlit as st
import pandas as pd
import plotly.express as px
import pages.booking_ryp as booking_ryp
import pages.payable_ryp as payable_ryp

def show(ryp_200hr_data, ryp_300hr_data):
    st.header("RYP Student Database Analysis")

    # Pilihan program
    program_choice = st.radio("Choose Program:", ["200HR", "300HR"], horizontal=True)

    # Memilih data berdasarkan program
    if program_choice == "200HR":
        ryp_data = ryp_200hr_data
    else:
        ryp_data = ryp_300hr_data

    # Validasi kolom data
    required_columns = ['Student still to pay', 'Total Payable (in USD or USD equiv)']
    if not all(col in ryp_data.columns for col in required_columns):
        st.error("Required columns are missing in the data.")
        return

    # Total siswa
    total_students = len(ryp_data)

    payment_data = ryp_data[['Student still to pay', 'Total Payable (in USD or USD equiv)']]
    total_payment_received = payment_data['Total Payable (in USD or USD equiv)'].sum()
    total_pending_payment = payment_data['Student still to pay'].sum()
    outstanding_percentage = (
        (total_pending_payment / total_payment_received * 100) if total_payment_received > 0 else 0
    )

    # Tampilkan total students dengan gaya seperti overview.py
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-around; text-align: center;">
                <div style="margin-right: 20px;">
                    <h2 style="font-size: 24px; color: #333333;">Total Booking</h2>
                    <h1 style="font-size: 50px; color: #333333; margin: 0;">{total_students}</h1>
                    <p style="font-size: 18px; color: #1f77b4;">Number of students</p>
                </div>
                <div style="margin: 0 20px;">
                    <h2 style="font-size: 24px; color: #333333;">Total Payable</h2>
                    <h1 style="font-size: 50px; color: #333333; margin: 0;">${total_payment_received:,.0f}</h1>
                    <p style="font-size: 18px; color: #1f77b4;">in USD or USD equiv</p>
                </div>
                <div style="margin-left: 20px;">
                    <h2 style="font-size: 24px; color: #333333;">Outstanding</h2>
                    <h1 style="font-size: 50px; color: #333333; margin: 0;">${total_pending_payment:,.0f}</h1>
                    <p style="font-size: 18px; color: #1f77b4;">{outstanding_percentage:.2f}% of Total Payable</p>
                </div>
            </div>
        """, 
        unsafe_allow_html=True
    )

    # Tambahkan radio button untuk memilih tampilan
    selected_view = st.radio("View Data", ["Booking", "Payable"], horizontal=True)

    # Tampilkan data berdasarkan pilihan radio button
    if selected_view == "Booking":
        booking_ryp.show_booking(ryp_data, program_choice)
    elif selected_view == "Payable":
        payable_ryp.show_payable(ryp_data, program_choice)
