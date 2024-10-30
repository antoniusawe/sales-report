import streamlit as st

# st.sidebar.title("Sidebar Title")
location = st.sidebar.selectbox("Choose a Location:", ["Bali", "India"])

st.image("https://raw.githubusercontent.com/antoniusawe/student_database/main/images/house%20of%20om.png",  
         use_column_width=True)
st.markdown("<h1 style='text-align: center; font-size: 50px;'>HOUSE OF OM - DASHBOARD</h1>", unsafe_allow_html=True)

if location == "India":
    program = st.selectbox("Choose a Program:", ["200HR", "300HR"])
else:
    st.write("Select 'India' from the sidebar to view program options.")
    
    if program == "200HR":
        # Load the Excel file from the URL without displaying it in Streamlit
        url = "https://raw.githubusercontent.com/antoniusawe/student_database/main/student_database_200hr.xlsx"
        data_200hr = pd.read_excel(url)

