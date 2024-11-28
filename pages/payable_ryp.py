import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def show_payable(data, program_choice):
    """
    Menampilkan data payable berdasarkan pilihan program dengan visualisasi line chart.
    :param data: DataFrame yang telah difilter untuk Payable.
    :param program_choice: Pilihan program dari pengguna (All, 200HR, 300HR).
    """

    # Header untuk bagian Payable
    st.subheader(f"Payable Details ({program_choice})")
    st.caption("Details about total payable amounts over time.")

    # Validasi data kosong
    if data.empty:
        st.warning("No payable data available for the selected program.")
        return

    # Proses kolom tanggal booking
    if 'DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT' in data.columns:
        data['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT'] = pd.to_datetime(
            data['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT'], errors='coerce'
        )

        # Filter data dengan tanggal booking valid
        valid_data = data[data['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT'].notnull()]

        # Tambahkan kolom bulan untuk visualisasi
        valid_data['BOOKING MONTH'] = valid_data['DATE ON WHICH CUSTOMER MADE THE BOOKING DEPOSIT'].dt.to_period('M').astype(str)

        # Agregasi total payable per bulan
        payable_distribution = valid_data.groupby('BOOKING MONTH')['TOTAL PAYABLE (IN USD OR USD EQUIV)'].sum().reset_index()
        payable_distribution.rename(columns={'TOTAL PAYABLE (IN USD OR USD EQUIV)': 'TOTAL PAYABLE'}, inplace=True)

        # Agregasi total paid per bulan
        paid_distribution = valid_data.groupby('BOOKING MONTH')['TOTAL PAID (AS OF TODAY)'].sum().reset_index()
        paid_distribution.rename(columns={'TOTAL PAID (AS OF TODAY)': 'TOTAL PAID'}, inplace=True)

        # Sorting bulan agar terurut
        payable_distribution['BOOKING MONTH'] = pd.to_datetime(payable_distribution['BOOKING MONTH'], format='%Y-%m')
        payable_distribution.sort_values(by='BOOKING MONTH', inplace=True)
        payable_distribution['BOOKING MONTH'] = payable_distribution['BOOKING MONTH'].dt.strftime('%b %Y')

        paid_distribution['BOOKING MONTH'] = pd.to_datetime(paid_distribution['BOOKING MONTH'], format='%Y-%m')
        paid_distribution.sort_values(by='BOOKING MONTH', inplace=True)
        paid_distribution['BOOKING MONTH'] = paid_distribution['BOOKING MONTH'].dt.strftime('%b %Y')

        # Visualisasi dengan line chart menggunakan Plotly
        # st.markdown("### Total Payable and Total Paid Over Time")
        fig = go.Figure()

        # Tambahkan garis untuk Total Payable
        fig.add_trace(go.Scatter(
            x=payable_distribution['BOOKING MONTH'],
            y=payable_distribution['TOTAL PAYABLE'],
            mode='lines+markers',
            name='Total Payable',
            line=dict(color='blue', width=2),
        ))

        # Tambahkan garis putus-putus untuk Total Paid
        fig.add_trace(go.Scatter(
            x=paid_distribution['BOOKING MONTH'],
            y=paid_distribution['TOTAL PAID'],
            mode='lines+markers',
            name='Total Paid',
            line=dict(color='green', width=2, dash='dash'),
        ))

        # Konfigurasi layout chart
        fig.update_layout(
            title="Total Payable vs Total Paid Distribution",
            xaxis_title="Month",
            yaxis_title="Amount (USD)",
            legend_title="Metrics",
            template="plotly_white"
        )

        st.plotly_chart(fig)
    else:
        st.warning("Booking deposit date information is not available.")

    # # Tambahkan tabel data payable untuk referensi
    # st.markdown("### Payable Data Table")
    # st.dataframe(data)
