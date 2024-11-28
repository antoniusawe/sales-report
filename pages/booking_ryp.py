import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def show_booking(data, program_choice):
    """
    Menampilkan data booking berdasarkan pilihan program dengan distribusi bulanan.
    :param data: DataFrame yang telah difilter untuk Booking.
    :param program_choice: Pilihan program dari pengguna (All, 200HR, 300HR).
    """

    # Header untuk bagian Booking
    st.subheader(f"Booking Details ({program_choice})")
    st.caption("Details about student bookings and related information.")

    # Validasi data kosong
    if data.empty:
        st.warning("No booking data available for the selected program.")
        return

    # Proses kolom tanggal booking menjadi bulan
    if 'DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT' in data.columns:
        data['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT'] = pd.to_datetime(
            data['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT'], errors='coerce'
        )
        
        # Filter data dengan tanggal booking valid
        valid_data = data[data['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT'].notnull()]
        
        # Ekstrak bulan dari tanggal booking
        valid_data['BOOKING MONTH'] = valid_data['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT'].dt.to_period('M').astype(str)
        
        # Hitung jumlah booking per bulan
        booking_distribution = valid_data.groupby('BOOKING MONTH')['NAME OF STUDENT'].count().reset_index()
        booking_distribution.rename(columns={'NAME OF STUDENT': 'COUNT'}, inplace=True)
        
        # Sorting bulan agar terurut
        booking_distribution['BOOKING MONTH'] = pd.to_datetime(booking_distribution['BOOKING MONTH'], format='%Y-%m')
        booking_distribution.sort_values(by='BOOKING MONTH', inplace=True)
        booking_distribution['BOOKING MONTH'] = booking_distribution['BOOKING MONTH'].dt.strftime('%b %Y')

        # Visualisasi distribusi booking per bulan
        # st.markdown("### Booking Distribution by Month")
        fig_monthly = px.bar(
            booking_distribution,
            x='BOOKING MONTH',
            y='COUNT',
            title='Booking Distribution per Month',
            labels={'BOOKING MONTH': 'Month', 'COUNT': 'Number of Bookings'},
        )
        st.plotly_chart(fig_monthly)

        # Visualisasi distribusi Booking Source (Doughnut Chart)
        if 'BOOKING SOURCE' in valid_data.columns:
            booking_source_counts = valid_data['BOOKING SOURCE'].value_counts().reset_index()
            booking_source_counts.columns = ['BOOKING SOURCE', 'COUNT']

            # st.markdown("### Booking Distribution by Source")
            fig_source = px.pie(
                booking_source_counts,
                names='BOOKING SOURCE',
                values='COUNT',
                title='Booking Source Distribution',
                hole=0.4  # Membuat bentuk doughnut
            )
            st.plotly_chart(fig_source)
        else:
            st.warning("Booking source information is not available.")
    else:
        st.warning("Booking deposit date information is not available.")

    # # Tambahkan tabel data booking untuk ditampilkan
    # st.markdown("### Booking Data Table")
    # st.dataframe(data)

    # Visualisasi distribusi booking per hari
    daily_booking = valid_data.groupby('DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT')['NAME OF STUDENT'].count().reset_index()
    daily_booking.rename(columns={'NAME OF STUDENT': 'BOOKING COUNT', 'DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT': 'DATE'}, inplace=True)

    # Hitung rata-rata booking per hari
    average_booking = daily_booking['BOOKING COUNT'].mean()

    # Chart booking per hari dengan garis rata-rata
    st.markdown("### Daily Booking Trends with Average Line")
    fig_daily = go.Figure()

    # Tambahkan garis jumlah booking harian
    fig_daily.add_trace(go.Scatter(
        x=daily_booking['DATE'],
        y=daily_booking['BOOKING COUNT'],
        mode='lines+markers',
        name='Daily Bookings',
        line=dict(color='blue', width=2),
    ))

    # Tambahkan garis rata-rata booking
    fig_daily.add_trace(go.Scatter(
        x=daily_booking['DATE'],
        y=[average_booking] * len(daily_booking),
        mode='lines',
        name=f'Average: {average_booking:.2f}',
        line=dict(color='red', width=2, dash='dash'),
    ))

    # Konfigurasi layout chart
    fig_daily.update_layout(
        title="Average Bookings per Day",
        xaxis_title="Date",
        yaxis_title="Number of Bookings",
        legend_title="Metrics",
        template="plotly_white"
    )

    st.plotly_chart(fig_daily)
