import streamlit as st
import pandas as pd
import plotly.express as px

def show_batch(filtered_sales_data, program_choice, selected_year, selected_month):
    st.header("Batch-specific Sales Data Analysis")

    # Menampilkan informasi program, tahun, dan bulan yang dipilih
    if program_choice:
        st.write(f"**Program:** {program_choice}")
    if selected_year != "All":
        st.write(f"**Year:** {selected_year}")
    if selected_month != "All":
        st.write(f"**Month:** {selected_month}")

    # Dropdown untuk memilih Site, termasuk opsi "All"
    site_options = ["All"] + filtered_sales_data['Site'].dropna().unique().tolist()
    selected_site = st.selectbox("Select Site", site_options)

    # Filter berdasarkan Site yang dipilih, kecuali jika "All" dipilih
    if selected_site != "All":
        filtered_sales_data = filtered_sales_data[filtered_sales_data['Site'] == selected_site]

    # Menangani data kosong
    if filtered_sales_data.empty:
        st.warning("Data tidak ditemukan untuk site yang dipilih.")
        return

    # Pastikan kolom 'PAID STATUS' ada, jika tidak tambahkan dengan nilai default 'NOT PAID'
    if 'PAID STATUS' not in filtered_sales_data.columns:
        filtered_sales_data['PAID STATUS'] = 'NOT PAID'
    else:
        filtered_sales_data['PAID STATUS'] = filtered_sales_data['PAID STATUS'].fillna('NOT PAID')

    # Isi nilai kosong pada kolom 'Group' dengan nilai dari kolom 'Site'
    if 'Group' in filtered_sales_data.columns and 'Site' in filtered_sales_data.columns:
        filtered_sales_data['Group'] = filtered_sales_data['Group'].fillna(filtered_sales_data['Site'])

    # Mengelompokkan data berdasarkan 'Batch start date', 'Batch end date', dan 'Group'
    if {'Batch start date', 'Batch end date', 'Group', 'PAID STATUS'}.issubset(filtered_sales_data.columns):
        # Hitung jumlah setiap status pembayaran
        batch_sales_summary = filtered_sales_data.groupby(
            ['Batch start date', 'Batch end date', 'Group', 'PAID STATUS']
        ).size().reset_index(name='Count')

        # Pivot data untuk membuat kolom per status pembayaran
        batch_sales_summary = batch_sales_summary.pivot_table(
            index=['Batch start date', 'Batch end date', 'Group'],
            columns='PAID STATUS',
            values='Count',
            fill_value=0
        ).reset_index()

        # Pastikan semua status pembayaran ada dalam dataframe
        for status in ['FULLY PAID', 'DEPOSIT', 'NOT PAID']:
            if status not in batch_sales_summary.columns:
                batch_sales_summary[status] = 0

        # Konversi 'Batch start date' menjadi datetime untuk pengurutan
        batch_sales_summary['Batch Start Date Temp'] = pd.to_datetime(batch_sales_summary['Batch start date'], format='%d %b %Y', errors='coerce')

        # Hapus baris dengan tanggal yang tidak valid
        batch_sales_summary = batch_sales_summary.dropna(subset=['Batch Start Date Temp'])

        # Urutkan berdasarkan 'Batch Start Date Temp'
        batch_sales_summary = batch_sales_summary.sort_values(by='Batch Start Date Temp')

        # Hapus kolom sementara 'Batch Start Date Temp' setelah pengurutan
        batch_sales_summary = batch_sales_summary.drop(columns=['Batch Start Date Temp'])

        # Tampilkan data sales per batch dalam tabel
        st.subheader("Sales Data per Batch by Payment Status")
        st.dataframe(batch_sales_summary)

        # Menampilkan stacked bar chart untuk distribusi status pembayaran
        st.subheader("Payment Status Distribution by Batch Start Date")
        
        # Mengubah data ke format long untuk stacked bar chart
        batch_sales_summary_long = batch_sales_summary.melt(
            id_vars=['Batch start date'], 
            value_vars=['FULLY PAID', 'DEPOSIT', 'NOT PAID'], 
            var_name='Payment Status', 
            value_name='Count'
        )

        # Membuat stacked bar chart menggunakan Plotly
        fig = px.bar(
            batch_sales_summary_long, 
            x='Batch start date', 
            y='Count', 
            color='Payment Status', 
            title="Payment Status Distribution by Batch Start Date (Stacked)",
            labels={'Batch start date': 'Batch Start Date', 'Count': 'Number of Students'},
            barmode='stack'
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Data tidak memiliki kolom yang diperlukan untuk analisis batch.")
