import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
from datetime import datetime

# Sidebar dropdown for location
location = st.sidebar.selectbox("Choose a Location:", ["Bali", "India"])

# Display the main image and title
st.image("https://raw.githubusercontent.com/antoniusawe/sales-report/main/images/house_of_om-removebg-preview.png",  
         use_column_width=True)
st.markdown("<h1 style='text-align: center; font-size: 50px;'>HOUSE OF OM - DASHBOARD</h1>", unsafe_allow_html=True)

# Display today's date
today = datetime.today()
st.markdown(f"<h3 style='text-align: center; font-size: 16px;'>{today.strftime('%d %B %Y')}</h3>", unsafe_allow_html=True)

# Extract month from today's date for comparison
current_month = today.month

if location == "Bali":
    # Sub-dropdown for specific options under "Bali"
    bali_option = st.sidebar.selectbox("Choose a Section:", ["Overview", "Location", "Batch"])
    
    occupancy_url = "https://raw.githubusercontent.com/antoniusawe/sales-report/main/Bali%20data/bali_occupancy.xlsx"
    sales_url = "https://raw.githubusercontent.com/antoniusawe/sales-report/main/Bali%20data/bali_sales.xlsx"
    
    try:
        # Load data for occupancy and sales
        bali_occupancy_data = pd.read_excel(occupancy_url)
        bali_sales_data = pd.read_excel(sales_url)
        
        # Convert 'Batch start date' to datetime if it's not already
        if 'Batch start date' in bali_sales_data.columns:
            bali_sales_data['Batch start date'] = pd.to_datetime(bali_sales_data['Batch start date'], errors='coerce')
        # Convert 'Occupancy' column to numeric if it's not already (remove % and convert to float)
        if 'Occupancy' in bali_occupancy_data.columns:
            bali_occupancy_data['Occupancy'] = bali_occupancy_data['Occupancy'].replace('%', '', regex=True).astype(float)

    except Exception as e:
        st.error("Failed to load data. Please check the URL or your connection.")
        st.write(f"Error: {e}")

    program = st.selectbox("Choose a Program:", ["200HR", "300HR"])

    # Display content based on selected sub-option
    if bali_option == "Overview":
        if program == "200HR":
            # Filter data for 200HR category
            data_200hr_bali = bali_sales_data[bali_sales_data['Category'] == '200HR']
            
            # Find the newest Batch start date for 200HR category
            newest_batch_date = data_200hr_bali['Batch start date'].max()
            
            # Format the newest date to a string for display
            cut_off_date = newest_batch_date.strftime('%B %d, %Y') if pd.notnull(newest_batch_date) else "No date available"
            
            # Calculate Total Booking as count of NAME with BALANCE = 0
            total_booking_ctr = data_200hr_bali[data_200hr_bali["BALANCE"] == 0]["NAME"].count()
            # Calculate Amount as sum of PAID where BALANCE = 0
            total_paid_amount = data_200hr_bali[data_200hr_bali["BALANCE"] == 0]["PAID"].sum()
            # Calculate average Occupancy
            average_occupancy = bali_occupancy_data['Occupancy'].mean()
            
            # Display Cut-off date and Total Booking in a centered format
            st.markdown(f"""
            <div style='text-align: left;'>
                <div style='font-size: 16px; color: #333333;'>Cut-off data: {cut_off_date}</div>
            </div>
            <div style='display: flex; justify-content: center; gap: 50px; padding: 20px;'>
                <div style='text-align: left;'>
                    <div style='font-size: 16px; color: #333333;'>Total Booking</div>
                    <div style='font-size: 48px;'>{total_booking_ctr}</div>
                    <div style='color: #202fb2; font-size: 18px;'>Number of students</div>
                </div>
                <div style='text-align: left;'>
                    <div style='font-size: 16px; color: #333333;'>Amount</div>
                    <div style='font-size: 48px;'>{total_paid_amount:,.0f}</div>
                    <div style='color: #202fb2; font-size: 18px;'>in USD or USD equiv</div>
                </div>
                <div style='text-align: left;'>
                    <div style='font-size: 16px; color: #333333;'>Occupancy</div>
                    <div style='font-size: 48px;'>{average_occupancy:.2f}%</div>
                    <div style='color: #202fb2; font-size: 18px;'>Occupancy Rate</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Create bar chart for Site popularity based on 'Fill'
            site_fill_data = bali_occupancy_data.groupby('Site')['Fill'].sum().reset_index()
            site_fill_data = site_fill_data.sort_values(by='Fill', ascending=False)

            # Create bar chart data for Room popularity based on 'Fill'
            room_fill_data = bali_occupancy_data.groupby('Room')['Fill'].sum().reset_index()
            room_fill_data = room_fill_data.sort_values(by='Fill', ascending=False)

            balance_zero_data = bali_sales_data[bali_sales_data['BALANCE'] == 0]
            month_counts = balance_zero_data.groupby('Month')['NAME'].count().reset_index()
            month_counts = month_counts.sort_values(by='NAME', ascending=False)

            # Identify the highest value for color differentiation
            highest_fill_value_site = site_fill_data['Fill'].max()
            highest_fill_value_room = room_fill_data['Fill'].max()

            # Identifikasi nilai tertinggi untuk chart Month
            highest_value_month = month_counts['NAME'].max()

            # Konfigurasi bar chart untuk Site dengan tooltip
            site_bar_chart_data = {
                "title": {
                    "text": "Top Frequent Sites",
                    "left": "center",
                    "textStyle": {
                        "fontSize": 16,
                        "fontWeight": "bold",
                        "color": "#333333"
                    }
                },
                "tooltip": {
                    "trigger": "item",
                    "formatter": "{b}: {c}"  # Show Site name and Fill value in tooltip
                },
                "xAxis": {
                    "type": "category",
                    "data": site_fill_data['Site'].tolist()
                },
                "yAxis": {
                    "type": "value",
                    "axisLabel": {
                        "fontSize": 6,
                        "margin": 10  # Adjust margin to provide more space for y-axis labels
                    }
                },
                "series": [{
                    "data": [
                        {
                            "value": fill,
                            "itemStyle": {
                                "color": "#FF5733" if fill == highest_fill_value_site else "#5470C6"
                            }
                        }
                        for fill in site_fill_data['Fill']
                    ],
                    "type": "bar",
                    "label": {
                        "show": True,
                        "position": "top",
                        "formatter": "{c}",
                        "fontSize": 9,
                        "color": "#333333"
                    }
                }]
            }

            # Konfigurasi bar chart untuk Room dengan tooltip
            room_bar_chart_data = {
                "title": {
                    "text": "Top Frequent Rooms",
                    "left": "center",
                    "textStyle": {
                        "fontSize": 16,
                        "fontWeight": "bold",
                        "color": "#333333"
                    }
                },
                "tooltip": {
                    "trigger": "item",
                    "formatter": "{b}: {c}"  # Show Room name and Fill value in tooltip
                },
                "xAxis": {
                    "type": "category",
                    "data": room_fill_data['Room'].tolist()
                },
                "yAxis": {
                    "type": "value",
                    "axisLabel": {
                        "fontSize": 6,
                        "margin": 10  # Adjust margin to provide more space for y-axis labels
                    }
                },
                "series": [{
                    "data": [
                        {
                            "value": fill,
                            "itemStyle": {
                                "color": "#FF5733" if fill == highest_fill_value_room else "#5470C6"
                            }
                        }
                        for fill in room_fill_data['Fill']
                    ],
                    "type": "bar",
                    "label": {
                        "show": True,
                        "position": "top",
                        "formatter": "{c}",
                        "fontSize": 9,
                        "color": "#333333"
                    }
                }]
            }

            # Konfigurasi bar chart untuk Month dengan tooltip
            month_bar_chart_data = {
                "title": {
                    "text": "Top Months",
                    "left": "center",
                    "textStyle": {
                        "fontSize": 16,
                        "fontWeight": "bold",
                        "color": "#333333"
                    }
                },
                "tooltip": {
                    "trigger": "item",
                    "formatter": "{b}: {c}"  # Show Month and count of students with Balance = 0
                },
                "xAxis": {
                    "type": "category",
                    "data": month_counts['Month'].tolist()
                },
                "yAxis": {
                    "type": "value",
                    "axisLabel": {
                        "fontSize": 6,
                        "margin": 10  # Adjust margin to provide more space for y-axis labels
                    }
                },
                "series": [{
                    "data": [
                        {
                            "value": count,
                            "itemStyle": {
                                "color": "#FF5733" if count == highest_value_month else "#5470C6"
                            }
                        }
                        for count in month_counts['NAME']
                    ],
                    "type": "bar",
                    "label": {
                        "show": True,
                        "position": "top",
                        "formatter": "{c}",
                        "fontSize": 9,
                        "color": "#333333"
                    }
                }]
            }

            # Menampilkan ketiga grafik berdampingan
            col1, col2, col3 = st.columns(3)

            with col1:
                # Render bar chart Site
                st_echarts(options=site_bar_chart_data, height="300px")

            with col2:
                # Render bar chart Room
                st_echarts(options=room_bar_chart_data, height="300px")

            with col3:
                # Render bar chart Month for fully paid students
                st_echarts(options=month_bar_chart_data, height="300px")

        # Menggunakan `st.button` untuk menambahkan fungsi interaktif
        if st.button("Generate Data", key="generate_button"):
            st.markdown("<h2 style='text-align: center; font-size: 24px; color: #5470C6;'>Bali Occupancy Data</h2>", unsafe_allow_html=True)
            st.dataframe(bali_occupancy_data)

            st.markdown("<h2 style='text-align: center; font-size: 24px; color: #5470C6;'>Bali Sales Data</h2>", unsafe_allow_html=True)
            st.dataframe(bali_sales_data)

    elif bali_option == "Location":
        st.write("Displaying Location section for Bali.")
        # Add specific code or functionalities for the Location section

    elif bali_option == "Batch":
        st.write("Displaying Batch section for Bali.")
        # Add specific code or functionalities for the Batch section

# Conditional logic based on location selection
elif location == "India":
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
