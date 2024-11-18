import streamlit as st
st.set_page_config(page_title="Dashboard House of Om", page_icon="🏠")

import pandas as pd
import pages.page1 as page1  # Import halaman pertama yang akan kita buat
import pages.page2 as page2  # Import halaman pertama yang akan kita buat

# Menyembunyikan navigasi default di sidebar dengan CSS
hide_default_sidebar_nav = """
    <style>
    [data-testid="stSidebarNav"] ul {
        display: none;
    }
    </style>
"""
st.markdown(hide_default_sidebar_nav, unsafe_allow_html=True)

# Display the main image and title
st.image("https://raw.githubusercontent.com/antoniusawe/sales-report/main/images/house_of_om-removebg-preview.png",  
         use_column_width=True)
st.markdown(
    """
    <div style='text-align: center;'>
        <h1 style='font-size: 50px; margin-bottom: 0;'>HOUSE OF OM</h1>
        <h2 style='font-size: 30px; margin-top: 0; color: grey;'>SALES & OCCUPANCY DASHBOARD</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Judul aplikasi
# st.title("Sales Dashboard & Occupancy")

# Membaca data dari file Excel
try:
    occupancy_data = pd.read_excel("https://raw.githubusercontent.com/antoniusawe/sales-report/main/data/bali_occupancy.xlsx")
    sales_data = pd.read_excel("https://raw.githubusercontent.com/antoniusawe/sales-report/main/data/bali_sales.xlsx")
    ryp_200hr_data = pd.read_excel("https://raw.githubusercontent.com/antoniusawe/sales-report/main/data/ryp_student_database_200hr.xlsx")
    ryp_300hr_data = pd.read_excel("https://raw.githubusercontent.com/antoniusawe/sales-report/main/data/ryp_student_database_300hr.xlsx")
    st.success("© 2024 House of Om")
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")

# Sidebar untuk navigasi antar halaman
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Homepage", "📊 Bali", "📈 RYP"])

# Menampilkan halaman yang sesuai dengan pilihan user
if page == "🏠 Homepage":
    st.write("Selamat datang di dashboard occupancy dan sales data. Gunakan menu di samping untuk navigasi.")
elif page == "📊 Bali":
    page1.show(occupancy_data, sales_data)
elif page == "📈 RYP":
    page2.show(ryp_200hr_data, ryp_300hr_data)
