import streamlit as st
import pandas as pd
from io import StringIO
import time
import datetime
import matplotlib.pyplot as plt

from main import *
from apptext import *

st.set_page_config(page_title="INForcast", layout="wide")


def loaddata(url):
    df = pd.read_csv(url)
    return df


# Define current year globally
current_year = datetime.datetime.now().year

# You can use columns to further utilize the wide layout
col1, col2, col3 = st.columns([1, 0.1, 3])

data = None
with col1:
    # Render the HTML in the Streamlit app
    st.image(
        "https://github.com/janduplessis883/project-inforcast/blob/master/images/inforcast-log2.png?raw=true"
    )
    # Toggle checkbox
    toggle = st.checkbox("Quick Start")

    # Check if the toggle is on or off
    if toggle:
        st.markdown(html4, unsafe_allow_html=True)
        # Reading md file from GitHub
        url = "https://raw.githubusercontent.com/janduplessis883/project-inforcast/master/markdown/quickstart.md"
        markdown_content = fetch_markdown_content(url)
        st.markdown(markdown_content, unsafe_allow_html=True)

    # Checkbox to load sample data
    if st.checkbox("Load Sample Data"):
        url = "https://raw.githubusercontent.com/janduplessis883/project-inforcast/master/inforcast/sampledata/sampledata.csv"
        data = loaddata(url)
        data = pd.read_csv(url)
        data = process_dataframe(data)
        data = update_location(data)
    else:
        # Only display the file uploader if sample data is not selected
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            data = pd.read_csv(stringio)
            data = process_dataframe(data)
            data = update_location(data)

# Rest of the code for processing and plotting
if data is not None:
    with col1:
        # Assuming 'location' is the column name containing the IDs
        location_counts = data["location"].value_counts()
        most_frequent_location = location_counts.idxmax()

        # Create a selectbox with the most frequent location as the default
        selected_location = st.selectbox(
            "Select a location:",
            options=location_counts.index,
            index=location_counts.index.get_loc(most_frequent_location),
        )

        # Filter the DataFrame based on the selected location ID
        filtered_data = data[data["location"] == selected_location]

        df_list = age_groups(filtered_data, display_years=24)
        counts = count_last_year(filtered_data)
        previous_count = count_previous_year(filtered_data)

with col2:
    st.write()

# Check if df_list is available and valid for plotting
with col3:
    if data is not None and "df_list" in locals():
        st.markdown(html2, unsafe_allow_html=True)
        plot_age_groups(df_list, df_list[-1]["count"].max())

        st.markdown(html3, unsafe_allow_html=True)
        st.markdown(
            "Below **Total Influenza Vaccine** given this year. The figure below in green is your total for the previous flu season."
        )

        this_year = age_groups(filtered_data, display_years=2)
        plot_age_groups(this_year, df_list[-1]["count"].max())

        # 3 columns for TOTALS for the year
        col1, col2, col3 = st.columns(3)

        col1.metric(
            label="Children (< 18 yrs)",
            value=str(counts[0]),
            delta=str(previous_count[0]),
        )
        col2.metric(
            label="18 - 64 yrs", value=str(counts[1]), delta=str(previous_count[1])
        )
        col3.metric(
            label="Over 65 yrs", value=str(counts[2]), delta=str(previous_count[2])
        )

        # Age Histogram Plot (need to update filtered data for the last year only)
        age_histplot(filtered_data)

    else:
        st.image(
            "https://github.com/janduplessis883/project-inforcast/blob/master/images/inforcast-2.png?raw=true",
            use_column_width=True,
            caption="GitHub: janduplessis883",
        )
