import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def show_booking(filtered_df_sales, filtered_df_leads):
    st.header("Overview by Booking")
    # Add a small note below the header
    st.caption("This overview uses the **DATE OF PAYMENT** as the primary reference for the analysis.")

    # Mengurutkan data berdasarkan 'NAME' dan 'DATE OF PAYMENT' (oldest first)
    filtered_df_sales = filtered_df_sales.sort_values(by=['NAME', 'DATE OF PAYMENT'])

    # Hapus duplikat berdasarkan 'NAME', hanya ambil yang paling awal
    unique_bookings = filtered_df_sales.drop_duplicates(subset='NAME', keep='first')

    # Konversi kolom 'PRODUCT PRICE' ke tipe numerik
    unique_bookings['PRODUCT PRICE'] = pd.to_numeric(unique_bookings['PRODUCT PRICE'], errors='coerce')

    # Tambahkan kolom nomor bulan untuk pengurutan
    unique_bookings['MONTH_NUM'] = pd.to_datetime(unique_bookings['MONTH'], format='%B', errors='coerce').dt.month

    # Urutkan data berdasarkan YEAR dan MONTH_NUM
    unique_bookings = unique_bookings.sort_values(by=['YEAR', 'MONTH_NUM'])

    # Hitung total amount dari 'PRODUCT PRICE'
    total_amount = unique_bookings['PRODUCT PRICE'].sum()

    # Menghitung unique leads
    unique_leads = filtered_df_leads.loc[filtered_df_leads['PIPELINE_NAME'] != 'Clients'].drop_duplicates(subset='ID', keep='first')

    # Hitung Booking Rate
    total_bookings = unique_bookings['NAME'].nunique()
    total_leads = unique_leads['ID'].nunique()
    booking_rate = total_bookings / total_leads if total_leads > 0 else 0  # Menghindari pembagian dengan 0

    # Tampilkan Total Booking, Total Amount, dan Occupancy berdampingan
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; text-align: center; padding: 20px;">
            <div style="flex: 1; padding: 0 20px;">
                <h2 style="font-size: 20px; color: #333333;">Total Leads</h2>
                <h1 style="font-size: 46px; color: #333333; margin: 0;">{unique_leads['ID'].nunique()}</h1>
                <p style="font-size: 18px; color: #1f77b4;">Number of Leads</p>
            </div>
            <div style="flex: 1; padding: 0 20px;">
                <h2 style="font-size: 20px; color: #333333;">Total Booking</h2>
                <h1 style="font-size: 46px; color: #333333; margin: 0;">{unique_bookings['NAME'].nunique()}</h1>
                <p style="font-size: 18px; color: #1f77b4;">Number of students</p>
            </div>
            <div style="flex: 1; padding: 0 20px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <h2 style="font-size: 20px; color: #333333;">Booking Rate</h2>
                <h1 style="font-size: 46px; color: #333333; margin: 0;">{booking_rate:.2%}</h1>  <!-- Format as percentage -->
                <p style="font-size: 18px; color: #1f77b4;">Booking to Leads Ratio</p>
            </div>
        </div>

        <!-- Menambahkan Flexbox baru untuk Total Amount di baris bawah -->
        <div style="display: flex; justify-content: center; text-align: center; padding: 20px; margin-top: 20px;">
            <div style="flex: 1; padding: 0 20px;">
                <h2 style="font-size: 24px; color: #333333;">Total Amount</h2>
                <h1 style="font-size: 50px; color: #333333; margin: 0;">${total_amount:,.0f}</h1>
                <p style="font-size: 18px; color: #1f77b4;">in USD or USD equiv</p>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # **Chart 1: Total Amount per Month**
    # Pastikan 'PRODUCT PRICE' adalah numerik
    unique_bookings['PRODUCT PRICE'] = pd.to_numeric(unique_bookings['PRODUCT PRICE'], errors='coerce')

    # Agregasi data untuk menghitung total_amount per MONTH
    monthly_data = unique_bookings.groupby('MONTH').agg(
        total_amount=('PRODUCT PRICE', 'sum'),  # Total amount
        unique_bookings=('NAME', 'nunique')  # Jumlah unique bookings
    ).reset_index()

    # Pastikan urutan bulan benar dengan mengonversi ke datetime, lalu kembali ke string
    monthly_data['MONTH'] = pd.to_datetime(monthly_data['MONTH'], format='%B', errors='coerce')
    monthly_data = monthly_data.sort_values(by='MONTH')
    monthly_data['MONTH'] = monthly_data['MONTH'].dt.strftime('%B')

    # Membuat grafik interaktif menggunakan Plotly Express
    fig_month = px.bar(
        monthly_data,
        x='MONTH',
        y='total_amount',  # Menggunakan total amount sebagai y-axis
        title="Total Amount per Month",
        labels={'total_amount': 'Total Amount (USD)', 'MONTH': 'Month'},
        text='total_amount'  # Menampilkan total amount di dalam bar
    )
    fig_month.update_traces(
        texttemplate='%{text:.2s}',  # Format angka dengan singkatan (mis. 1k, 1M)
        textposition='inside'  # Posisi label di dalam batang
    )
    fig_month.update_layout(
        xaxis=dict(title="Month"),
        yaxis=dict(title="Total Amount (USD)"),
        uniformtext_minsize=10,  # Ukuran teks minimal
        uniformtext_mode='show'  # Selalu tampilkan teks
    )

    # Tampilkan grafik di Streamlit
    st.plotly_chart(fig_month, use_container_width=True)

    # **Interaktif Chart: Unique Bookings per Month with Weeks**
    # Agregasi data untuk menghitung jumlah unik NAME per WEEK dan MONTH
    # Urutkan data berdasarkan urutan kalender
    weekly_data = unique_bookings.groupby(['MONTH', 'WEEK'])[['NAME']].agg(
        unique_bookings=('NAME', 'nunique')
    ).reset_index()

    # Pastikan urutan bulan benar dengan mengonversi ke datetime, lalu kembali ke string
    weekly_data['MONTH'] = pd.to_datetime(weekly_data['MONTH'], format='%B', errors='coerce')
    weekly_data = weekly_data.sort_values(by=['MONTH', 'WEEK'])
    weekly_data['MONTH'] = weekly_data['MONTH'].dt.strftime('%B')

    # Membuat grouped bar chart dengan gradasi manual
    fig = px.bar(
        weekly_data,
        x='MONTH',
        y='unique_bookings',  # Gunakan 'unique_bookings' sebagai y-axis
        color='WEEK',
        title="Bookings per Weeks",
        labels={'unique_bookings': 'Number of Bookings', 'WEEK': 'Week', 'MONTH': 'Month'},
        # text='unique_bookings',  # Menampilkan angka di atas bar
        barmode='group'  # Membuat grouped bar chart
    )
    fig.update_layout(
        xaxis=dict(title="Month"),
        yaxis=dict(title="Number of Bookings"),
        legend=dict(title="Week")
    )

    # Tampilkan grafik di Streamlit
    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        weekly_data,
        x='MONTH',
        y='unique_bookings',
        color='WEEK',
        title="Bookings per Weeks",
        labels={'unique_bookings': 'Number of Bookings', 'WEEK': 'Week', 'MONTH': 'Month'},
        text='unique_bookings',  # Menampilkan angka di atas bar
        barmode='group'
    )
    
    # Update posisi teks
    fig.update_traces(
        texttemplate='%{text}',  # Format teks (bisa ubah sesuai kebutuhan)
        textposition='outside'   # Posisi teks (e.g., 'outside', 'inside')
    )
    
    # Update layout
    fig.update_layout(
        xaxis=dict(title="Month"),
        yaxis=dict(title="Number of Bookings"),
        legend=dict(title="Week")
    )

    # **Chart 2: Line Chart - Average Bookings per Day**
    # Agregasi data per hari
    daily_data = unique_bookings.groupby('DATE OF PAYMENT').agg(
        daily_bookings=('NAME', 'nunique')  # Jumlah unique bookings per hari
    ).reset_index()

    # from plotly.subplots import make_subplots
    # import plotly.graph_objects as go
    
    # # Membuat layout dengan 2 baris (1 untuk chart, 1 untuk tabel)
    # fig = make_subplots(
    #     rows=2, cols=1,
    #     shared_xaxes=True,  # Share x-axis antara chart dan tabel
    #     row_heights=[0.8, 0.2],  # Tinggi masing-masing row
    #     vertical_spacing=0.05
    # )
    
    # # Tambahkan bar chart (row 1)
    # fig.add_trace(
    #     go.Bar(
    #         x=weekly_data['MONTH'],
    #         y=weekly_data['unique_bookings'],
    #         marker_color=weekly_data['WEEK'],  # Warna berdasarkan minggu
    #         name='Bookings per Weeks',
    #         text=weekly_data['unique_bookings'],  # Tampilkan teks
    #         textposition='outside'
    #     ),
    #     row=1, col=1
    # )
    
    # # Tambahkan tabel (row 2)
    # fig.add_trace(
    #     go.Table(
    #         header=dict(
    #             values=["Month", "Week", "Unique Bookings"],
    #             fill_color='lightgrey',
    #             align='center'
    #         ),
    #         cells=dict(
    #             values=[
    #                 weekly_data['MONTH'],  # Kolom bulan
    #                 weekly_data['WEEK'],  # Kolom minggu
    #                 weekly_data['unique_bookings']  # Kolom bookings
    #             ],
    #             align='center'
    #         )
    #     ),
    #     row=2, col=1
    # )
    
    # # Update layout
    # fig.update_layout(
    #     height=800,  # Tinggi grafik
    #     title_text="Bookings per Weeks with Data Table"
    # )
    
    # # Tampilkan di Streamlit
    # st.plotly_chart(fig, use_container_width=True)

    # Hitung rata-rata booking harian
    avg_daily_bookings = daily_data['daily_bookings'].mean()

    # Buat line chart
    fig_daily = px.line(
        daily_data,
        x='DATE OF PAYMENT',
        y='daily_bookings',
        title="Average Bookings per Day",
        labels={'DATE OF PAYMENT': 'Date', 'daily_bookings': 'Number of Bookings'},
        markers=True
    )
    fig_daily.add_annotation(
        x=daily_data['DATE OF PAYMENT'].iloc[-1],
        y=avg_daily_bookings,
        text=f"Avg: {avg_daily_bookings:.2f}",
        showarrow=False,
        font=dict(size=12, color="red")
    )
    fig_daily.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Bookings",
        shapes=[
            # Tambahkan garis horizontal rata-rata
            dict(
                type="line",
                x0=daily_data['DATE OF PAYMENT'].min(),
                x1=daily_data['DATE OF PAYMENT'].max(),
                y0=avg_daily_bookings,
                y1=avg_daily_bookings,
                line=dict(color="Red", width=2, dash="dot"),
            )
        ]
    )

    st.plotly_chart(fig_daily, use_container_width=True)
