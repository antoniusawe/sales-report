import streamlit as st
import pandas as pd
import plotly.express as px

def show_payable(ryp_data, program_choice):
    # st.header(f"Payable Information for {program_choice}")

    # # Debugging: Tampilkan kolom yang tersedia
    # st.write("Available Columns in Dataset:")
    # st.write(ryp_data.columns)

    # Validasi kolom data yang diperlukan
    required_columns = ['Batch start date', 'Batch end date', 'Total Payable (in USD or USD equiv)', 'Total paid (as of today)']
    if not all(col in ryp_data.columns for col in required_columns):
        st.error("Required columns are missing in the data.")
        return

    # Menghitung total payable dan paid per batch
    batch_data = ryp_data.groupby(['Batch start date', 'Batch end date']).agg(
        Total_Payable=('Total Payable (in USD or USD equiv)', 'sum'),
        Total_Paid=('Total paid (as of today)', 'sum')
    ).reset_index()

    # # Debugging: Tampilkan data setelah pengelompokan
    # st.write("Batch Data After Grouping:")
    # st.write(batch_data)

    # Cek jika data kosong
    if batch_data.empty:
        st.warning("No data available for the selected program or filters.")
        return

    # Konversi tanggal batch ke datetime
    batch_data['Batch start date'] = pd.to_datetime(batch_data['Batch start date'])
    batch_data['Batch end date'] = pd.to_datetime(batch_data['Batch end date'])

    # Sorting berdasarkan Batch Start Date
    batch_data = batch_data.sort_values(by='Batch start date').reset_index(drop=True)

    # Membuat label batch dengan format vertikal
    batch_data['Batch'] = batch_data['Batch start date'].dt.strftime('%d %b %Y') + "<br>to<br>" + batch_data['Batch end date'].dt.strftime('%d %b %Y')

    # # Menampilkan tabel data untuk verifikasi
    # st.dataframe(batch_data[['Batch start date', 'Batch end date', 'Total_Payable', 'Total_Paid']])

    # Membuat Line Chart Combo
    fig_combo = px.line(
        batch_data,
        x='Batch',
        y=['Total_Payable', 'Total_Paid'],
        title="Payable and Paid Over Batches",
        labels={
            'value': 'Amount (USD)',
            'Batch': 'Batch',
            'variable': 'Metric'
        },
        markers=True
    )

    # Menambahkan teks di atas titik data untuk keterbacaan
    for trace in fig_combo.data:
        trace.update(text=trace.y, textposition="top center")

    # Menampilkan grafik
    st.plotly_chart(fig_combo, use_container_width=True)
