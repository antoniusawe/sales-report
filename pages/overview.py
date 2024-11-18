import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

def show_overview(filtered_occupancy_data, filtered_sales_data):
    st.header("Overview of Bali Program Data")

    # Total Booking: Hitung jumlah nilai yang ada di kolom 'NAME' dari 'filtered_sales_data'
    total_booking = filtered_sales_data['NAME'].count()  # Hitung jumlah booking

    # Amount: Hitung jumlah dari kolom 'TOTAL AMOUNT' di 'filtered_sales_data'
    total_amount = filtered_sales_data['TOTAL AMOUNT'].sum()  # Menghitung total amount

    # Occupancy: Menghitung rata-rata occupancy setelah konversi ke format numerik
    filtered_occupancy_data['Occupancy'] = filtered_occupancy_data['Occupancy'].str.replace('%', '').astype(float)
    average_occupancy = filtered_occupancy_data['Occupancy'].mean()  # Rata-rata occupancy dalam bentuk numerik

    # Tampilkan Total Booking, Total Amount, dan Occupancy berdampingan
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div style="margin-right: 20px;">
                <h2 style="font-size: 24px; color: #333333;">Total Booking</h2>
                <h1 style="font-size: 50px; color: #333333; margin: 0;">{total_booking}</h1>
                <p style="font-size: 18px; color: #1f77b4;">Number of students</p>
            </div>
            <div style="margin: 0 20px;">
                <h2 style="font-size: 24px; color: #333333;">Amount</h2>
                <h1 style="font-size: 50px; color: #333333; margin: 0;">${total_amount:,.0f}</h1>
                <p style="font-size: 18px; color: #1f77b4;">in USD or USD equiv</p>
            </div>
            <div style="margin-left: 20px;">
                <h2 style="font-size: 24px; color: #333333;">Occupancy</h2>
                <h1 style="font-size: 50px; color: #333333; margin: 0;">{average_occupancy:.2f}%</h1>
                <p style="font-size: 18px; color: #1f77b4;">Average occupancy</p>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Chart: Group by 'Site' dan sum 'Fill', lalu urutkan dari terbesar ke terkecil
    # st.subheader("Occupancy by Site")
    site_fill_data = filtered_occupancy_data.groupby('Site')['Fill'].sum().sort_values(ascending=False).reset_index()

    # Membuat chart interaktif menggunakan Plotly
    fig = px.bar(
        site_fill_data,
        x="Site",
        y="Fill",
        title="Total Fill by Site",
        labels={"Fill": "Total Fill", "Site": "Site"},
        color="Fill",
    )
    fig.update_layout(xaxis_tickangle=-90)  # Memutar label X 90 derajat untuk keterbacaan

    # Menampilkan chart interaktif di Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Chart kedua: Group by 'Room' dan sum 'Fill', lalu urutkan dari terbesar ke terkecil
    # st.subheader("Occupancy by Room Type")
    room_fill_data = filtered_occupancy_data.groupby('Room')['Fill'].sum().sort_values(ascending=False).reset_index()
    fig_room = px.bar(
        room_fill_data,
        x="Room",
        y="Fill",
        title="Total Fill by Room Type",
        labels={"Fill": "Total Fill", "Room": "Room Type"},
        color="Fill",
    )
    fig_room.update_layout(xaxis_tickangle=-90)  # Memutar label X 90 derajat untuk keterbacaan
    st.plotly_chart(fig_room, use_container_width=True)

    # Chart ketiga: Group by 'Month' dan sum 'Fill', lalu urutkan berdasarkan urutan bulan
    # st.subheader("Occupancy by Month")
    # Konversi 'Month' ke datetime agar bisa diurutkan dengan benar
    filtered_occupancy_data['Month'] = pd.to_datetime(filtered_occupancy_data['Month'], format='%B')
    month_fill_data = filtered_occupancy_data.groupby('Month')['Fill'].sum().sort_values(ascending=False).reset_index()
    month_fill_data['Month'] = month_fill_data['Month'].dt.strftime('%B')  # Ubah kembali ke nama bulan

    fig_month = px.bar(
        month_fill_data,
        x="Month",
        y="Fill",
        title="Total Fill by Month",
        labels={"Fill": "Total Fill", "Month": "Month"},
        color="Fill",
    )
    fig_month.update_layout(xaxis_tickangle=-90)  # Memutar label X 90 derajat untuk keterbacaan
    st.plotly_chart(fig_month, use_container_width=True)
