import streamlit as st
import pandas as pd
from io import StringIO
import time
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit_shadcn_ui as ui


st.set_page_config(page_title="Streamlit-exp", layout="wide")

html4 = """
<style>
.gradient-text {
    background: linear-gradient(45deg, #284d74, #d8ad45, #b2d9db, #e16d33);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-size: 3em;
    font-weight: bold;
</style>
<div class="gradient-text">Streamlit Exp</div>
"""


# Define current year globally
current_year = datetime.datetime.now().year

# You can use columns to further utilize the wide layout
col1, col2, col3 = st.columns([1, 0.1, 3])

data = None
with col1:
    # Render the HTML in the Streamlit app
    st.markdown(html4, unsafe_allow_html=True)
    # Toggle checkbox
    toggle = st.checkbox("About")

    # Check if the toggle is on or off
    if toggle:
        st.write("Placeholder")
        # st.markdown(html4, unsafe_allow_html=True)
        # # Reading md file from GitHub
        # url = "https://raw.githubusercontent.com/janduplessis883/project-inforcast/master/markdown/quickstart.md"
        # markdown_content = fetch_markdown_content(url)
        # st.markdown(markdown_content, unsafe_allow_html=True)

    # Checkbox to load sample data
    if st.checkbox("Load Sample Data"):
        st.write("Load Sample Data")
        # url = "https://raw.githubusercontent.com/janduplessis883/project-inforcast/master/inforcast/sampledata/sampledata.csv"
        # data = loaddata(url)
        # data = pd.read_csv(url)
        data = "df loaded"
        # data = process_dataframe(data)
        # data = update_location(data)
    else:
        # Only display the file uploader if sample data is not selected
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            data = pd.read_csv(stringio)
            # data = process_dataframe(data)
            # data = update_location(data)

# Rest of the code for processing and plotting
if data is not None:
    with col1:
        st.write("Placeholder")

with col2:
    st.write()

# Check if df_list is available and valid for plotting
with col3:
    if data is not None:
        ui.tabs(
            options=[
                "Dashboard",
                "Feedback Classification",
                "Improvement Suggestions",
                "Sentiment Analysis",
            ],
            default_value="Dashboard",
            key="kanaries",
        )

        choice = ui.select(options=["Apple", "Banana", "Orange"])

        st.markdown(f"Currrent value: {choice}")

        switch_value = ui.switch(
            default_checked=False, label="Explain this page", key="switch1"
        )
        if switch_value == True:
            st.markdown("This is the explination of this page.")

        st.header("Friends & Family Test Analysis Data")
        data = pd.read_csv("data/data.csv")
        bins = st.slider("Select number of bins", min_value=5, max_value=50, value=10)
        fig, ax = plt.subplots(figsize=(16, 3))
        sns.histplot(
            data["subjectivity"], ax=ax, kde=True, color="#d0b05b", bins=bins
        )  # 'kde' for a density plot overlay
        ax.set_title("Subjectivity Histogram")
        ax.set_xlabel("Subjectivity")
        ax.set_ylabel("Frequency")
        ax.yaxis.grid(True, linestyle="--", linewidth=0.5, color="#888888")
        ax.xaxis.grid(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(16, 3))
        sns.histplot(
            data["polarity"], ax=ax, kde=True, color="#3d6e93", bins=bins
        )  # 'kde' for a density plot overlay
        ax.set_title("Polarity Histogram")
        ax.set_xlabel("Polarity")
        ax.set_ylabel("Frequency")
        ax.yaxis.grid(True, linestyle="--", linewidth=0.5, color="#888888")
        ax.xaxis.grid(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        st.pyplot(fig)

        st.write(data)

        # Age Histogram Plot (need to update filtered data for the last year only)
        # age_histplot(filtered_data)

    else:
        st.image(
            "https://github.com/janduplessis883/streamlit_experiment/blob/master/images/clouds.png?raw=true",
            use_column_width=True,
            caption="GitHub: janduplessis883",
        )
