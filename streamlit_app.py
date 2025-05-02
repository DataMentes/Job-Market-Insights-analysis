# ---------------------------
# Import Libraries & Packages
# ---------------------------
from scripts.analysis import *
import sqlite3
import pandas as pd
import streamlit as st


# ---------------------------
# Import Data
# ---------------------------
conn = sqlite3.connect('database.db')
df = pd.read_sql('SELECT * FROM EGYPT', conn)

# ---------------------------
# Egypt Plots
# ---------------------------
plot1 = job_distribution_by_city(df[df['city'] != 'Unknown'], plot_name="job_distribution_by_city_egypt", folder='egypt', top_n=10)

# ---------------------------
# Saudi Plots
# ---------------------------

# ---------------------------
# Sidebar Navigation
# ---------------------------
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select Page", ["Home", "Egypt Market", "Saudi Market", "Comparison"])

# ---------------------------
# Page Content
# ---------------------------
st.title("Job Market Analysis")

if page == "Home":
    st.header("Welcome to the Job Market Analysis App")
    st.write("""
        This app helps you analyze and compare the job markets in Egypt and Saudi Arabia.
        Use the sidebar to navigate between different sections.
    """)

elif page == "Egypt Market":
    st.header("Egypt Job Market")
    st.write("This section will display analysis related to the Egyptian job market.")
    st.pyplot(plot1)

elif page == "Saudi Market":
    st.header("Saudi Arabia Job Market")
    st.write("This section will display analysis related to the Saudi Arabian job market.")
    # st.pyplot(fig)

elif page == "Comparison":
    st.header("Comparison: Egypt vs Saudi Arabia")
    st.write("This section will compare the two job markets side by side.")
    # Placeholder for visual comparison
    # col1, col2 = st.columns(2)

    # with col1:
    #     st.pyplot(...)
    # with col2:
    #     st.pyplot(...)

# ---------------------------
# Footer or Credits
# ---------------------------
st.markdown("---")
st.markdown("Created by DataMentes Team | Job Market Analysis Tool")
