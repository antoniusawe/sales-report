import streamlit as st
import pandas as pd
import plotly.express as px

def show_booking(ryp_data, program_choice):
    # Batch-wise booking information
    # st.subheader("Batch-Wise Booking")
    if 'Batch start date' in ryp_data.columns:
        # Menghitung jumlah siswa per kombinasi Batch Start Date dan Batch End Date
        batch_data = ryp_data.groupby(['Batch start date', 'Batch end date']).size().reset_index(name='Number of Students')

        # Konversi kolom Batch Start Date dan Batch End Date ke datetime
        batch_data['Batch start date'] = pd.to_datetime(batch_data['Batch start date'])
        batch_data['Batch end date'] = pd.to_datetime(batch_data['Batch end date'])

        # Sorting berdasarkan Batch Start Date
        batch_data = batch_data.sort_values(by='Batch start date').reset_index(drop=True)

        # Membuat label batch dengan format vertikal
        batch_data['Batch'] = batch_data['Batch start date'].dt.strftime('%d %b %Y') + "<br>to<br>" + batch_data['Batch end date'].dt.strftime('%d %b %Y')

        # Menampilkan data batch dalam tabel
        # st.dataframe(batch_data[['Batch start date', 'Batch end date', 'Number of Students']])

        # Grafik distribusi booking per batch
        fig_batch = px.bar(
            batch_data,
            x=batch_data['Batch'],  # Menggunakan label batch yang sudah terurut
            y=batch_data['Number of Students'],
            title="Booking Distribution",
            labels={'x': 'Batch', 'y': 'Number of Students'},
            text=batch_data['Number of Students']
        )

        # Menampilkan jumlah siswa di luar batang
        fig_batch.update_traces(textposition='outside')

        # Mengatur ulang label sumbu-X dengan format vertikal
        fig_batch.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(len(batch_data))),  # Indeks sumbu-X sesuai urutan
                ticktext=batch_data['Batch']  # Label dengan <br> untuk memisah baris
            ),
            xaxis_tickangle=0,  # Jangan diputar
            xaxis_title="Batch",
            yaxis_title="Number of Students"
        )

        # Tampilkan grafik
        st.plotly_chart(fig_batch, use_container_width=True)
    else:
        st.warning("Batch start date column is missing in the data.")

    # Total booking berdasarkan sumber booking
    # st.subheader("Booking Source Distribution")
    booking_source_data = ryp_data['Booking source'].value_counts().reset_index()
    booking_source_data.columns = ['Booking Source', 'Number of Students']
    # st.dataframe(booking_source_data)

    # Grafik distribusi sumber booking (Plotly)
    fig_booking_source = px.bar(
        booking_source_data,
        x='Booking Source',
        y='Number of Students',
        title="Student Distribution by Booking Source",
        labels={'Number of Students': 'Count'},
        text='Number of Students'
    )
    fig_booking_source.update_traces(textposition='outside')
    st.plotly_chart(fig_booking_source, use_container_width=True)
