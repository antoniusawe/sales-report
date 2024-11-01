import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

# Sidebar dropdown for location
location = st.sidebar.selectbox("Choose a Location:", ["Bali", "India"])

# Display the main image and title
st.image("https://raw.githubusercontent.com/antoniusawe/sales-report/main/images/house_of_om-removebg-preview.png",  
         use_column_width=True)
st.markdown("<h1 style='text-align: center; font-size: 50px;'>SALES DASHBOARD</h1>", unsafe_allow_html=True)

# Display today's date
today = datetime.today()
st.markdown(f"<h3 style='text-align: center;'>Date: {today.strftime('%d %B %Y')}</h3>", unsafe_allow_html=True)

# Extract month from today's date for comparison
current_month = today.month

# Conditional logic based on location selection
if location == "India":
    # Dropdown for program selection when location is "India"
    program = st.selectbox("Choose a Program:", ["200HR", "300HR"])

    # Load and process data if "200HR" is selected
    if program == "200HR":
        # Load the Excel file from the URL
        url = "https://raw.githubusercontent.com/antoniusawe/sales-report/main/RYP%20data/ryp_student_database_200hr.xlsx"
        
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

            if chart_option == "Total Booking":
                # Process data for Number of Students chart
                batch_counts = data_200hr.groupby(['Batch start date', 'Batch end date'])['Name of student'].count().reset_index()
                
                batch_counts['Batch start date'] = pd.to_datetime(batch_counts['Batch start date'])
                batch_counts['Batch end date'] = pd.to_datetime(batch_counts['Batch end date'])
                batch_counts['Days in Batch'] = (batch_counts['Batch end date'] - batch_counts['Batch start date']).dt.days + 1
                
                batch_counts['Average Bookings per Day'] = batch_counts['Name of student'] / batch_counts['Days in Batch']
                batch_counts = batch_counts.sort_values(by='Batch start date')
                
                batch_counts['Batch'] = batch_counts['Batch start date'].dt.strftime('%B %d, %Y') + " to " + batch_counts['Batch end date'].dt.strftime('%B %d, %Y')
                
                wrapped_labels = [label.replace(" to ", "\nto\n") for label in batch_counts['Batch']]
                student_counts = batch_counts['Name of student'].tolist()
                average_bookings_per_day = batch_counts['Average Bookings per Day'].tolist()

                # Bar chart for Number of Students
                bar_options = {
                "title": {
                    "text": "Total Booking",  # Adding the title for the bar chart
                    "left": "center",          # Center the title
                    "top": "top",              # Position it at the top of the chart
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
                    "text": "Average Booking per Day",  # Adding the title for the line chart
                    "left": "center",           # Center the title
                    "top": "top",               # Position it at the top of the chart
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

            elif chart_option == "Total Payable":
                # Process data for Financial Overview chart
                batch_counts = data_200hr.groupby(['Batch start date', 'Batch end date']).agg(
                    {"Total Payable (in USD or USD equiv)": "sum",
                     "Total paid (as of today)": "sum",
                     "Student still to pay": "sum"}).reset_index()

                batch_counts['Batch start date'] = pd.to_datetime(batch_counts['Batch start date'])
                batch_counts['Batch end date'] = pd.to_datetime(batch_counts['Batch end date'])
                batch_counts = batch_counts.sort_values(by='Batch start date')
                
                batch_counts['Batch'] = batch_counts['Batch start date'].dt.strftime('%B %d, %Y') + " to " + batch_counts['Batch end date'].dt.strftime('%B %d, %Y')
                
                wrapped_labels = [label.replace(" to ", "\nto\n") for label in batch_counts['Batch']]
                total_payable = batch_counts["Total Payable (in USD or USD equiv)"].tolist()
                total_paid = batch_counts["Total paid (as of today)"].tolist()
                student_still_to_pay = batch_counts["Student still to pay"].tolist()

                # Combo chart for Financial Overview
                combo_options = {
                    "title": {
                        "text": "Financial Overview",
                        "left": "center",
                        "top": "top",
                        "textStyle": {"fontSize": 18, "fontWeight": "bold"}
                    },
                    "tooltip": {"trigger": "axis"},
                    "legend": {
                        "data": ["Total Payable", "Total Paid", "Student Still to Pay"],
                        "orient": "horizontal",  # Orientasi horizontal
                        "bottom": "0",           # Posisikan legend di bawah
                        "left": "center"         # Rata tengah
                    },
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
                            "lineStyle": {"type": "dashed", "width": 1},
                            "symbol": "circle",
                            "symbolSize": 8    
                        },
                        {
                            "name": "Total Paid",
                            "data": total_paid,
                            "type": "line",
                            "itemStyle": {"color": "#91CC75"},
                            "lineStyle": {"width": 2},
                            "symbol": "circle",
                            "symbolSize": 8     
                        },
                        {
                            "name": "Student Still to Pay",
                            "data": student_still_to_pay,
                            "type": "line",
                            "lineStyle": {"width": 1, "type": "dotted"},     
                            "itemStyle": {"color": "grey"},
                            "symbol": "circle",
                            "symbolSize": 8     
                        }
                    ]
                }

                # Render the combo chart
                st_echarts(combo_options)

                # Display the grouped summary table below the Financial Overview chart
                # st.write("### Financial Summary by Batch")

                # Display the aggregated data as a table
                financial_summary = batch_counts[['Batch start date', 'Batch end date', 
                                                  'Total Payable (in USD or USD equiv)', 
                                                  'Total paid (as of today)', 
                                                  'Student still to pay']]
                
                # Rename columns for readability
                financial_summary.columns = ["Batch Start Date", "Batch End Date", "Total Payable (USD)", 
                                             "Total Paid (USD)", "Outstanding (USD)"]
                
                financial_summary['Batch Start Date'] = financial_summary['Batch Start Date'].dt.strftime('%B %d, %Y')
                financial_summary['Batch End Date'] = financial_summary['Batch End Date'].dt.strftime('%B %d, %Y')
                
                # Display the table
                st.dataframe(financial_summary)

            # Logika untuk "Data"
            elif chart_option == "Data":
                # Remove the 'S.No.' column from data_200hr before displaying
                data_200hr_display = data_200hr.drop(columns=['S.No.'])

                # Display the modified dataframe as a table
                st.write("Detailed Data View")
                st.dataframe(data_200hr_display) 
            
        except Exception as e:
            st.error("Failed to load data. Please check the URL or your connection.")
            st.write(f"Error: {e}")

    # Load and process data if "200HR" is selected
    elif program == "300HR":
        # Load the Excel file from the URL
        url = "https://raw.githubusercontent.com/antoniusawe/sales-report/main/RYP%20data/ryp_student_database_300hr.xlsx"
        
        try:
            data_300hr = pd.read_excel(url)
            # Calculate Total Booking, Total Payable, and Outstanding
            total_booking_ctr = data_300hr["Name of student"].count()
            total_payable_sum = data_300hr["Total Payable (in USD or USD equiv)"].sum()
            outstanding_sum = data_300hr["Student still to pay"].sum()
            
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

            if chart_option == "Total Booking":
                # Process data for Number of Students chart
                batch_counts = data_300hr.groupby(['Batch start date', 'Batch end date'])['Name of student'].count().reset_index()
                
                batch_counts['Batch start date'] = pd.to_datetime(batch_counts['Batch start date'])
                batch_counts['Batch end date'] = pd.to_datetime(batch_counts['Batch end date'])
                batch_counts['Days in Batch'] = (batch_counts['Batch end date'] - batch_counts['Batch start date']).dt.days + 1
                
                batch_counts['Average Bookings per Day'] = batch_counts['Name of student'] / batch_counts['Days in Batch']
                batch_counts = batch_counts.sort_values(by='Batch start date')
                
                batch_counts['Batch'] = batch_counts['Batch start date'].dt.strftime('%B %d, %Y') + " to " + batch_counts['Batch end date'].dt.strftime('%B %d, %Y')
                
                wrapped_labels = [label.replace(" to ", "\nto\n") for label in batch_counts['Batch']]
                student_counts = batch_counts['Name of student'].tolist()
                average_bookings_per_day = batch_counts['Average Bookings per Day'].tolist()

                # Bar chart for Number of Students
                bar_options = {
                "title": {
                    "text": "Total Booking",  # Adding the title for the bar chart
                    "left": "center",          # Center the title
                    "top": "top",              # Position it at the top of the chart
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
                    "text": "Average Booking per Day",  # Adding the title for the line chart
                    "left": "center",           # Center the title
                    "top": "top",               # Position it at the top of the chart
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

            elif chart_option == "Total Payable":
                # Process data for Financial Overview chart
                batch_counts = data_300hr.groupby(['Batch start date', 'Batch end date']).agg(
                    {"Total Payable (in USD or USD equiv)": "sum",
                     "Total paid (as of today)": "sum",
                     "Student still to pay": "sum"}).reset_index()

                batch_counts['Batch start date'] = pd.to_datetime(batch_counts['Batch start date'])
                batch_counts['Batch end date'] = pd.to_datetime(batch_counts['Batch end date'])
                batch_counts = batch_counts.sort_values(by='Batch start date')
                
                batch_counts['Batch'] = batch_counts['Batch start date'].dt.strftime('%B %d, %Y') + " to " + batch_counts['Batch end date'].dt.strftime('%B %d, %Y')
                
                wrapped_labels = [label.replace(" to ", "\nto\n") for label in batch_counts['Batch']]
                total_payable = batch_counts["Total Payable (in USD or USD equiv)"].tolist()
                total_paid = batch_counts["Total paid (as of today)"].tolist()
                student_still_to_pay = batch_counts["Student still to pay"].tolist()

                # Combo chart for Financial Overview
                combo_options = {
                    "title": {
                        "text": "Financial Overview",
                        "left": "center",
                        "top": "top",
                        "textStyle": {"fontSize": 18, "fontWeight": "bold"}
                    },
                    "tooltip": {"trigger": "axis"},
                    "legend": {
                        "data": ["Total Payable", "Total Paid", "Student Still to Pay"],
                        "orient": "horizontal",  # Orientasi horizontal
                        "bottom": "0",           # Posisikan legend di bawah
                        "left": "center"         # Rata tengah
                    },
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
                            "lineStyle": {"type": "dashed", "width": 1},
                            "symbol": "circle",
                            "symbolSize": 8    
                        },
                        {
                            "name": "Total Paid",
                            "data": total_paid,
                            "type": "line",
                            "itemStyle": {"color": "#91CC75"},
                            "lineStyle": {"width": 2},
                            "symbol": "circle",
                            "symbolSize": 8     
                        },
                        {
                            "name": "Student Still to Pay",
                            "data": student_still_to_pay,
                            "type": "line",
                            "lineStyle": {"width": 1, "type": "dotted"},     
                            "itemStyle": {"color": "grey"},
                            "symbol": "circle",
                            "symbolSize": 8     
                        }
                    ]
                }

                # Render the combo chart
                st_echarts(combo_options)

                # Display the grouped summary table below the Financial Overview chart
                # st.write("### Financial Summary by Batch")

                # Display the aggregated data as a table
                financial_summary = batch_counts[['Batch start date', 'Batch end date', 
                                                  'Total Payable (in USD or USD equiv)', 
                                                  'Total paid (as of today)', 
                                                  'Student still to pay']]
                
                # Rename columns for readability
                financial_summary.columns = ["Batch Start Date", "Batch End Date", "Total Payable (USD)", 
                                             "Total Paid (USD)", "Outstanding (USD)"]
                
                financial_summary['Batch Start Date'] = financial_summary['Batch Start Date'].dt.strftime('%B %d, %Y')
                financial_summary['Batch End Date'] = financial_summary['Batch End Date'].dt.strftime('%B %d, %Y')
                
                # Display the table
                st.dataframe(financial_summary)

            # Logika untuk "Data"
            elif chart_option == "Data":
                # Remove the 'S.No.' column from data_200hr before displaying
                data_200hr_display = data_300hr.drop(columns=['S.No.'])

                # Display the modified dataframe as a table
                st.write("Detailed Data View")
                st.dataframe(data_300hr) 
            
        except Exception as e:
            st.error("Failed to load data. Please check the URL or your connection.")
            st.write(f"Error: {e}")   


else:
    st.write("Data currently unavailable.")
