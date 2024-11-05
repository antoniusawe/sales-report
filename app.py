if location_analysis_option == "Occupancy Rate":
            st.write(f"Displaying Occupancy Rate for {today.strftime('%B')} in Bali.")

            # Filter the occupancy data for the current month and year
            bali_occupancy_data['Date'] = pd.to_datetime(bali_occupancy_data['Year'].astype(str) + '-' + bali_occupancy_data['Month'], format='%Y-%B')
            
            # Filter data for the last three months, including the current month
            current_date = datetime(today.year, current_month, 1)
            three_months_ago = current_date - pd.DateOffset(months=2)  # Getting data from three months ago
            last_three_months_data = bali_occupancy_data[
                (bali_occupancy_data['Date'] >= three_months_ago) &
                (bali_occupancy_data['Date'] <= current_date)
            ]

            # Reformat Month back to string (e.g., "November")
            last_three_months_data['Month'] = last_three_months_data['Date'].dt.strftime('%B')
            
            # Convert Occupancy to numeric and calculate the average per Site and Month
            last_three_months_data['Occupancy'] = pd.to_numeric(last_three_months_data['Occupancy'], errors='coerce')
            
            # Group by Year, Month, and Site to aggregate data
            aggregated_data = last_three_months_data.groupby(['Year', 'Month', 'Site']).agg({
                'Fill': 'sum',
                'Available': 'sum',
                'Occupancy': 'mean'
            }).reset_index()
            
            # Rename columns as per requirement
            aggregated_data = aggregated_data.rename(columns={
                'Available': 'Empty Spots',
                'Occupancy': 'Occupancy (%)'
            })
            
            # Convert Occupancy to percentage format for display, but keep raw data for calculations
            aggregated_data['Occupancy (%)'] = aggregated_data['Occupancy (%)'] * 100

            # Display Occupancy Rate data for the last 3 months
            st.write("### Occupancy Rate Comparison Over the Last 3 Months")
            st.dataframe(aggregated_data[['Year', 'Month', 'Site', 'Fill', 'Empty Spots', 'Occupancy (%)']])

            # Prepare data for area chart to visualize growth over the last three months
            # Pivot data to make each Site a separate line on the area chart
            area_chart_data = aggregated_data.pivot(index=['Year', 'Month'], columns='Site', values='Occupancy (%)').fillna(0)

            # Convert the MultiIndex to a string for Month-Year format
            area_chart_data.index = area_chart_data.index.map(lambda x: f"{x[1]} {x[0]}")  # e.g., "November 2024"

            # Prepare data for ECharts
            area_chart_options = {
                "title": {"text": "Occupancy Rate Growth Over the Last 3 Months", "left": "center"},
                "tooltip": {"trigger": "axis"},
                "legend": {"data": area_chart_data.columns.tolist()},
                "xAxis": {
                    "type": "category",
                    "data": area_chart_data.index.tolist(),
                },
                "yAxis": {"type": "value", "name": "Occupancy (%)"},
                "series": [
                    {
                        "name": site,
                        "type": "line",
                        "stack": "Total",
                        "areaStyle": {},
                        "data": area_chart_data[site].tolist()
                    } for site in area_chart_data.columns
                ]
            }

            # Render the area chart
            st_echarts(options=area_chart_options, height="400px")
