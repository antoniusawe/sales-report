import streamlit as st
import pandas as pd
import pages.ytt as ytt
import pages.ryp as ryp

st.set_page_config(
    page_title="Dashboard House of Om",
    page_icon="https://raw.githubusercontent.com/antoniusawe/sales-report/main/images/house_of_om-removebg-preview.png"
)

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

# Membaca data dari file Excel
try:
    # Path file Excel
    occupancy_file_path = "https://raw.githubusercontent.com/antoniusawe/sales-report/main/data/bali_occupancy.xlsx"
    sales_file_path = "https://raw.githubusercontent.com/antoniusawe/sales-report/main/data/Offline%20Sales%20by%20invoice.xlsx"
    ryp_200hr_file_path = "https://raw.githubusercontent.com/antoniusawe/sales-report/main/data/ryp_student_database_200hr.xlsx"
    ryp_300hr_file_path = "https://raw.githubusercontent.com/antoniusawe/sales-report/main/data/ryp_student_database_300hr.xlsx"

    # Membaca data dari file Sales
    df_sales = pd.read_excel(sales_file_path)

    # Membaca data dari file Occupancy
    df_occupancy = pd.read_excel(occupancy_file_path)
    df_occupancy.columns = df_occupancy.columns.str.strip().str.upper()  # Normalisasi nama kolom Occupancy

    # Membaca data RYP 200HR
    df_ryp_200hr = pd.read_excel(ryp_200hr_file_path)
    df_ryp_200hr.columns = df_ryp_200hr.columns.str.strip().str.upper()  # Normalisasi nama kolom 200HR

    # Membaca data RYP 300HR
    df_ryp_300hr = pd.read_excel(ryp_300hr_file_path)
    df_ryp_300hr.columns = df_ryp_300hr.columns.str.strip().str.upper()  # Normalisasi nama kolom 300HR

    st.success("© 2024 House of Om")
except FileNotFoundError as e:
    if "Offline Sales by invoice" in str(e):
        st.error(f"File Sales tidak ditemukan di lokasi: {sales_file_path}")
        df_sales = None
    if "bali_occupancy" in str(e):
        st.error(f"File Occupancy tidak ditemukan di lokasi: {occupancy_file_path}")
        df_occupancy = None
    if "ryp_student_database_200hr" in str(e):
        st.error(f"File 200HR tidak ditemukan di lokasi: {ryp_200hr_file_path}")
        df_ryp_200hr = None
    if "ryp_student_database_300hr" in str(e):
        st.error(f"File 300HR tidak ditemukan di lokasi: {ryp_300hr_file_path}")
        df_ryp_300hr = None
except Exception as e:
    st.error(f"Terjadi kesalahan saat membaca file: {e}")
    df_sales = None
    df_occupancy = None
    df_ryp_200hr = None
    df_ryp_300hr = None

# Sidebar untuk navigasi antar halaman
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "YTT", "RYP"])

# Menampilkan halaman yang sesuai dengan pilihan user
if page == "Home":
    st.write("Gunakan menu di samping untuk navigasi.")
elif page == "YTT":
    if df_sales is not None and df_occupancy is not None:
        ytt.show(df_sales, df_occupancy)
    else:
        st.warning("Data tidak tersedia. Pastikan file berhasil dimuat.")
elif page == "RYP":
    if df_ryp_200hr is not None and df_ryp_300hr is not None:
        ryp.show_ryp(df_ryp_200hr, df_ryp_300hr)
    else:
        st.warning("Data RYP tidak tersedia. Pastikan file berhasil dimuat.")
