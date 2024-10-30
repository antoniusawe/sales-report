import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

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
            # Calculate Total Booking and Total Payable
            total_booking_ctr = data_200hr["Name of student"].count()
            total_payable_sum = data_200hr["Total Payable (in USD or USD equiv)"].sum()
            outstanding_sum = data_200hr["Student still to pay"].sum()

            outstanding_percentage = (outstanding_sum / total_payable_sum * 100) if total_payable_sum else 0

            # Display Total Booking and Total Payable in a centered format
            st.markdown(f"""
            <div style='display: flex; justify-content: center; gap: 50px; padding: 20px;'>
                <div style='text-align: left;'>
                    <div style='font-size: 14px; color: #333333;'>Total Booking</div>
                    <div style='font-size: 48px; '>{total_booking_ctr}</div>
                    <div style='color: #202fb2; font-size: 16px; '>Number of Students</div>
                </div>
                <div style='text-align: left;'>
                    <div style='font-size: 14px; color: #333333;'>Total Payable</div>
                    <div style='font-size: 48px; '>{total_payable_sum:,.0f}</div>
                    <div style='color: #202fb2; font-size: 16px; '>in USD or USD equiv</div>
                </div>
                <div style='text-align: left;'>
                    <div style='font-size: 14px; color: #333333;'>Outstanding</div>
                    <div style='font-size: 48px;'>{outstanding_sum:,.0f}</div>
                    <div style='color: #202fb2; font-size: 16px;'>{outstanding_percentage:.2f}% of Total Payable</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Group data by batch start and end dates and count the number of students
            batch_counts = data_200hr.groupby(['Batch start date', 'Batch end date'])['Name of student'].count().reset_index()
            batch_counts['Batch'] = batch_counts['Batch start date'].astype(str) + " to " + batch_counts['Batch end date'].astype(str)
            
            # Create wrapped labels
            wrapped_labels = [label.replace(" to ", "\nto\n").replace(" ", "\n", 1) for label in batch_counts['Batch']]
            student_counts = batch_counts['Name of student'].tolist()

            # Echarts options for Bar Chart with wrapped labels
            options = {
                "tooltip": {"trigger": "axis"},
                "xAxis": {
                    "type": "category",
                    "data": wrapped_labels,
                    "axisLabel": {"interval": 0}  # Keep wrapped labels without rotation
                },
                "yAxis": {"type": "value"},
                "series": [
                    {
                        "data": student_counts,
                        "type": "bar",
                        "name": "Student Count",
                        "itemStyle": {"color": "#5470C6"}
                    }
                ]
            }

            # Render the bar chart
            st_echarts(options)

        except Exception as e:
            st.error("Failed to load data. Please check the URL or your connection.")
            st.write(f"Error: {e}")

else:
    st.write("Select 'India' from the sidebar to view program options.")
