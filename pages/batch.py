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

    # Pastikan kolom 'PAID STATUS' ada, jika tidak tambahkan dengan nilai default 'NOT PAID'
    if 'PAID STATUS' not in filtered_sales_data.columns:
        filtered_sales_data['PAID STATUS'] = 'NOT PAID'
    else:
        filtered_sales_data['PAID STATUS'] = filtered_sales_data['PAID STATUS'].fillna('NOT PAID')

    # Mengelompokkan data berdasarkan 'Batch start date', 'Batch end date', dan 'Group'
    if {'Batch start date', 'Batch end date', 'Group', 'PAID STATUS'}.issubset(filtered_sales_data.columns):
        batch_sales_summary = filtered_sales_data.groupby(
            ['Batch start date', 'Batch end date', 'Group']
        ).agg(
            FULLY_PAID=('PAID STATUS', lambda x: (x == 'FULLY PAID').sum()),
            DEPOSIT=('PAID STATUS', lambda x: (x == 'DEPOSIT').sum()),
            NOT_PAID=('PAID STATUS', lambda x: (x == 'NOT PAID').sum())
        ).reset_index()

        # Konversi 'Batch start date' menjadi datetime untuk pengurutan
        batch_sales_summary['Batch Start Date Temp'] = pd.to_datetime(batch_sales_summary['Batch start date'], format='%d %b %Y')
        
        # Urutkan berdasarkan 'Batch Start Date Temp' yang sudah diubah ke datetime
        batch_sales_summary = batch_sales_summary.sort_values(by='Batch Start Date Temp')
        
        # Hapus kolom sementara 'Batch Start Date Temp' setelah pengurutan
        batch_sales_summary = batch_sales_summary.drop(columns=['Batch Start Date Temp'])

        # Ubah nama kolom untuk meningkatkan keterbacaan
        batch_sales_summary = batch_sales_summary.rename(columns={
            'Batch start date': 'Batch Start Date',
            'Batch end date': 'Batch End Date',
            'Group': 'Group',
            'FULLY_PAID': 'Fully Paid',
            'DEPOSIT': 'Deposit',
            'NOT_PAID': 'Not Paid'
        })

        # Tampilkan data sales per batch dalam tabel
        st.subheader("Sales Data per Batch by Payment Status")
        st.dataframe(batch_sales_summary)

        # Menampilkan stacked bar chart untuk distribusi status pembayaran
        st.subheader("Payment Status Distribution by Batch Start Date")
        
        # Mengubah data ke format long untuk stacked bar chart
        batch_sales_summary_long = batch_sales_summary.melt(
            id_vars=['Batch Start Date'], 
            value_vars=['Fully Paid', 'Deposit', 'Not Paid'], 
            var_name='Payment Status', 
            value_name='Count'
        )

        # Membuat stacked bar chart menggunakan Plotly
        fig = px.bar(
            batch_sales_summary_long, 
            x='Batch Start Date', 
            y='Count', 
            color='Payment Status', 
            title="Payment Status Distribution by Batch Start Date (Stacked)",
            labels={'Batch Start Date': 'Batch Start Date', 'Count': 'Number of Students'},
            barmode='stack'
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Data tidak memiliki kolom yang diperlukan untuk analisis batch.")
