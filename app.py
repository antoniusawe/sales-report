import streamlit as st
import pandas as pd

# Sidebar dropdown for location
location = st.sidebar.selectbox("Choose a Location:", ["Bali", "India"])

# Display the main image and title
st.image("https://raw.githubusercontent.com/antoniusawe/student_database/main/images/house%20of%20om.png",  
         use_column_width=True)
st.markdown("<h1 style='text-align: center; font-size: 50px;'>HOUSE OF OM - DASHBOARD</h1>", unsafe_allow_html=True)

# Conditional logic based on location selection
if location == "India":
    # Dropdown for program selection when location is "India"
    program = st.selectbox("Choose a Program:", ["200HR", "300HR"])

    # Load and process data if "200HR" is selected
    if program == "200HR":
        # Load the Excel file from the URL
        url = "https://raw.githubusercontent.com/antoniusawe/student_database/main/student_database_200hr.xlsx"
        
        try:
            data_200hr = pd.read_excel(url)
            # Calculate Total Booking by counting non-null entries in "Name of student"
            total_booking_ctr = data_200hr["Name of student"].count()

            st.markdown(f"""
            <div style='display: flex; flex-direction: column; align-items: flex-start; padding-left: 10px;'>
                <div style='font-size: 18px; color: #333333;'>Total Booking</div>
                <div style='font-size: 48px; '>{total_booking_ctr}</div>
                <div style='color: #202fb2; font-size: 22px; '>Number of students</div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error("Failed to load data. Please check the URL or your connection.")
            st.write(f"Error: {e}")

else:
    st.write("Select 'India' from the sidebar to view program options.")
