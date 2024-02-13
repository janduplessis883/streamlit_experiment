import streamlit as st
import pandas as pd
from io import StringIO
import time
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit_shadcn_ui as ui
from PIL import Image
from streamlit_dynamic_filters import DynamicFilters
import os
import streamlit_shadcn_ui as ui

st.set_page_config(page_title="Streamlit-exp", layout="wide")


html = """
<style>
.gradient-text {
    background: linear-gradient(45deg, #284d74, #d8ad45, #ae4f4d);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-size: 3em;
    font-weight: bold;
</style>
<div class="gradient-text">GP Surgeries</div>
"""
st.sidebar.markdown("NHS England")
st.sidebar.markdown(html, unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("streamlit_exp/data/full_gpreviews.csv")
    columns_to_display = [
        "ode",
        "Practice_Name",
        "Tel",
        "Web",
        "Email",
        "raw_list",
        "Region",
        "ICB",
        "PCN",
    ]
    df = df[columns_to_display]
    contact_df = df.drop_duplicates()
    return contact_df


data = load_data()


# List the columns you want to show
selected_tab = ui.tabs(
    options=["Contact Details: NHS England GPs", "Surgery Reviews Data"],
    default_value="Contact Details: NHS England GPs",
    key="header",
)

if selected_tab == "Contact Details: NHS England GPs":
    dynamic_filters = DynamicFilters(
        df=data, filters=["Region", "ICB", "PCN", "Practice_Name"]
    )
    dynamic_filters.display_filters(location="sidebar")
    dynamic_filters.display_df()

elif selected_tab == "Surgery Reviews Data":
    st.write("Review Data")
