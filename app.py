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
            # Calculate Total Booking, Total Payable, and Outstanding
            total_booking_ctr = data_200hr["Name of student"].count()
            total_payable_sum = data_200hr["Total Payable (in USD or USD equiv)"].sum()
            outstanding_sum = data_200hr["Student still to pay"].sum()
            
            # Calculate the percentage of Outstanding from Total Payable
            outstanding_percentage = (outstanding_sum / total_payable_sum * 100) if total_payable_sum else 0

            # Display Total Booking, Total Payable, and Outstanding in a centered format
            st.markdown(f"""
            <div style='display: flex; justify-content: center; gap: 50px; padding: 20px;'>
                <div style='text-align: left;'>
                    <div style='font-size: 16px; color: #333333;'>Total Booking</div>
                    <div style='font-size: 48px;'>{total_booking_ctr}</div>
                    <div style='color: #202fb2; font-size: 18px;'>Number of Students</div>
                </div>
                <div style='text-align: left;'>
                    <div style='font-size: 16px; color: #333333;'>Total Payable</div>
                    <div style='font-size: 48px;'>{total_payable_sum:,.0f}</div>
                    <div style='color: #202fb2; font-size: 18px;'>in USD or USD equiv</div>
                </div>
                <div style='text-align: left;'>
                    <div style='font-size: 16px; color: #333333;'>Outstanding</div>
                    <div style='font-size: 48px;'>{outstanding_sum:,.0f}</div>
                    <div style='color: #202fb2; font-size: 18px;'>{outstanding_percentage:.2f}% of Total Payable</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Dropdown for chart data selection
            chart_option = st.selectbox("Choose Data to Display:", ["Total Booking", "Total Payable", "Data"])

            # Only show the Number of Students chart if "Total Booking" is selected
            if chart_option == "Total Booking":
                # Group data by batch start and end dates and count the number of students
                batch_counts = data_200hr.groupby(['Batch start date', 'Batch end date'])['Name of student'].count().reset_index()
                
                # Calculate the number of days in each batch
                batch_counts['Batch start date'] = pd.to_datetime(batch_counts['Batch start date'])
                batch_counts['Batch end date'] = pd.to_datetime(batch_counts['Batch end date'])
                batch_counts['Days in Batch'] = (batch_counts['Batch end date'] - batch_counts['Batch start date']).dt.days + 1
                
                # Calculate average bookings per day per batch
                batch_counts['Average Bookings per Day'] = batch_counts['Name of student'] / batch_counts['Days in Batch']
                
                # Sort data by Batch start date to ensure chronological order
                batch_counts = batch_counts.sort_values(by='Batch start date')
                
                # Convert dates back to string format for display purposes
                batch_counts['Batch'] = batch_counts['Batch start date'].dt.strftime('%B %d, %Y') + " to " + batch_counts['Batch end date'].dt.strftime('%B %d, %Y')
                
                # Create wrapped labels
                wrapped_labels = [label.replace(" to ", "\nto\n") for label in batch_counts['Batch']]
                student_counts = batch_counts['Name of student'].tolist()
                average_bookings_per_day = batch_counts['Average Bookings per Day'].tolist()

                # Bar chart for Number of Students
                bar_options = {
                    "title": {
                        "text": "Number of Students",
                        "left": "center",
                        "top": "top",
                        "textStyle": {"fontSize": 18, "fontWeight": "bold"}
                    },
                    "tooltip": {"trigger": "axis"},
                    "xAxis": {
                        "type": "category",
                        "data": wrapped_labels,
                        "axisLabel": {
                            "interval": 0,
                            "fontSize": 7,
                            "rotate": 0,
                            "lineHeight": 12,
                            "fontWeight": "bold"
                        }
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
                st_echarts(bar_options)

                # Line chart for Average Bookings per Day
                line_options = {
                    "title": {
                        "text": "Average Bookings per Day",
                        "left": "center",
                        "top": "top",
                        "textStyle": {"fontSize": 18, "fontWeight": "bold"}
                    },
                    "tooltip": {"trigger": "axis"},
                    "xAxis": {
                        "type": "category",
                        "data": wrapped_labels,
                        "axisLabel": {
                            "interval": 0,
                            "fontSize": 7,
                            "rotate": 0,
                            "lineHeight": 12,
                            "fontWeight": "bold"
                        }
                    },
                    "yAxis": {"type": "value"},
                    "series": [
                        {
                            "data": average_bookings_per_day,
                            "type": "line",
                            "name": "Average Bookings per Day",
                            "itemStyle": {"color": "#EE6666"},
                            "lineStyle": {"width": 2}
                        }
                    ]
                }

                # Render the line chart below the bar chart
                st_echarts(line_options)

            # Chart for Total Payable, Total Paid, and Student Still to Pay
            elif chart_option == "Total Payable":
                # Group data by batch start and end dates and calculate the sums
                batch_totals = data_200hr.groupby(['Batch start date', 'Batch end date']).agg({
                    'Total Payable (in USD or USD equiv)': 'sum',
                    'Total paid (as of today)': 'sum',
                    'Student still to pay': 'sum'
                }).reset_index()

                # Sort data by Batch start date
                batch_totals['Batch start date'] = pd.to_datetime(batch_totals['Batch start date'])
                batch_totals['Batch end date'] = pd.to_datetime(batch_totals['Batch end date'])
                batch_totals = batch_totals.sort_values(by='Batch start date')
                
                # Convert dates back to string format for display purposes
                batch_totals['Batch'] = batch_totals['Batch start date'].dt.strftime('%B %d, %Y') + " to " + batch_totals['Batch end date'].dt.strftime('%B %d, %Y')

                # Create wrapped labels
                wrapped_labels = [label.replace(" to ", "\nto\n") for label in batch_totals['Batch']]
                total_payable = batch_totals['Total Payable (in USD or USD equiv)'].tolist()
                total_paid = batch_totals['Total paid (as of today)'].tolist()
                student_still_to_pay = batch_totals['Student still to pay'].tolist()

                # Combo chart for Total Payable, Total Paid, and Student Still to Pay
                combo_options = {
                    "title": {
                        "text": "Financial Overview per Batch",
                        "left": "center",
                        "top": "top",
                        "bottom": "0%",
                        "textStyle": {"fontSize": 18, "fontWeight": "bold"}
                    },
                    "tooltip": {"trigger": "axis"},
                    "legend": {"data": ["Total Payable", "Total Paid", "Student Still to Pay"]},
                    "xAxis": {
                        "type": "category",
                        "data": wrapped_labels,
                        "axisLabel": {
                            "interval": 0,
                            "fontSize": 7,
                            "rotate": 0,
                            "lineHeight": 12,
                            "fontWeight": "bold"
                        }
                    },
                    "yAxis": {"type": "value"},
                    "series": [
                        {
                            "name": "Total Payable",
                            "data": total_payable,
                            "type": "line",
                            "itemStyle": {"color": "#5470C6"},
                            "lineStyle": {"width": 2},
                            "symbol": "circle"
                        },
                        {
                            "name": "Total Paid",
                            "data": total_paid,
                            "type": "line",
                            "itemStyle": {"color": "#91CC75"},
                            "lineStyle": {"width": 2, "type": "dashed"},
                            "symbol": "triangle"
                        },
                        {
                            "name": "Student Still to Pay",
                            "data": student_still_to_pay,
                            "type": "line",
                            "itemStyle": {"color": "#EE6666"},
                            "lineStyle": {"width": 2},
                            "symbol": "diamond"
                        }
                    ]
                }

                # Render the combo chart
                st_echarts(combo_options)

        except Exception as e:
            st.error("Failed to load data. Please check the URL or your connection.")
            st.write(f"Error: {e}")

else:
    st.write("Select 'India' from the sidebar to view program options.")
