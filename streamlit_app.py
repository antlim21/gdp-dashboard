import streamlit as st
import pandas as pd
import mysql.connector
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Ride Data Dashboard',
    page_icon=':bike:', 
)

# -----------------------------------------------------------------------------
# Database connection details 
# NOTE: Replace these with your actual credentials or use st.secrets
DB_HOST = "ds4300final.cr02moqaalu6.us-east-2.rds.amazonaws.com"
DB_NAME = "ds4300final"
DB_USER = "admin"
DB_PASSWORD = "L!moAnto2!"

# -----------------------------------------------------------------------------
# Declare a function to get the data from the RDS MySQL database.

@st.cache_data
def get_ride_data():
    """
    Connect to the MySQL database and retrieve average duration and distance
    aggregated by day.
    """
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    query = """
    SELECT 
        DATE(start_time) AS day,
        AVG(duration) AS avg_duration,
        AVG(distance) AS avg_distance
    FROM bike_rides
    GROUP BY DATE(start_time)
    ORDER BY DATE(start_time);
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df

ride_df = get_ride_data()

# -----------------------------------------------------------------------------
# Draw the page

st.title(":bike: Ride Data Dashboard")
st.write("""
This dashboard displays the average ride duration and distance for each day.
""")

# Choose a date range
min_date = ride_df['day'].min()
max_date = ride_df['day'].max()

selected_dates = st.slider(
    "Select the date range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Filter the DataFrame by the selected date range
filtered_df = ride_df[(ride_df['day'] >= selected_dates[0]) & (ride_df['day'] <= selected_dates[1])]

st.subheader("Average Duration and Distance over Time")

# You can show both metrics on the same chart using a wide dataframe format
# For example, you could try:
chart_df = filtered_df.set_index('day')[['avg_duration', 'avg_distance']]

st.line_chart(chart_df)

# If you want to show metrics separately:
st.subheader("Average Duration by Day")
st.line_chart(filtered_df.set_index('day')['avg_duration'])

st.subheader("Average Distance by Day")
st.line_chart(filtered_df.set_index('day')['avg_distance'])

