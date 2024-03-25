import streamlit as st
import pandas as pd
import time
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit_shadcn_ui as ui

st.set_page_config(layout="wide", page_title="NHS GP Reviews")


# Cache the loading of the data to avoid reloading on every interaction
@st.cache_data
def load_data():
    data = pd.read_parquet(
        "streamlit_exp/data/gpreviews_sa.parquet"
    )  # Adjust this to load your data
    return data


df = load_data()


# No need to cache these functions as Streamlit caches based on input
def filter_region(data, region):
    if not region:
        return data, [], [], []
    filtered_data = data[data["Region"].isin(region)]
    icb_unique = filtered_data["ICB"].unique()
    pcn_unique = filtered_data["PCN"].unique()
    practice_name_unique = filtered_data["Practice_Name"].unique()
    return filtered_data, icb_unique, pcn_unique, practice_name_unique


def filter_icb(data, icb):
    if not icb:
        return data, [], []
    filtered_data = data[data["ICB"].isin(icb)]
    pcn_unique = filtered_data["PCN"].unique()
    practice_name_unique = filtered_data["Practice_Name"].unique()
    return filtered_data, pcn_unique, practice_name_unique


def filter_pcn(data, pcn):
    if not pcn:
        return data, []
    filtered_data = data[data["PCN"].isin(pcn)]
    practice_name_unique = filtered_data["Practice_Name"].unique()
    return filtered_data, practice_name_unique


# Streamlit UI
st.title("NHS GP Reviews (22-24)")


# ---- Database Filtering  ----------------------------------------------------------------------------------

# Region filter
selected_region = st.sidebar.multiselect("Region", df["Region"].unique())
filtered_data, icb_unique, pcn_unique, practice_name_unique = filter_region(
    df, selected_region
)

# icb filter - options update based on region selection
selected_icb = st.sidebar.multiselect("ICB", icb_unique)
if selected_icb:
    filtered_data, pcn_unique, practice_name_unique = filter_icb(
        filtered_data, selected_icb
    )

# PCN filter - options update based on icb selection
selected_pcn = st.sidebar.multiselect("PCN", pcn_unique)
if selected_pcn:
    filtered_data, practice_name_unique = filter_pcn(filtered_data, selected_pcn)

# Practice Name filter - options update based on PCN selection
selected_practice_name = st.sidebar.multiselect("Practice Name", practice_name_unique)
if selected_practice_name:
    filtered_data = filtered_data[
        filtered_data["Practice_Name"].isin(selected_practice_name)
    ]


# ---- Total Reviews Metric Card ----------------------------------------------------------------------------------

col1, col2 = st.columns([1, 3])

with col1:
    st.write("")
    ui.metric_card(
        title="Total Reviews",
        content=f"{filtered_data.shape[0]}",
        description="",
        key="card1",
    )
    st.markdown("Sentiment Analysis")
    try:
        # Data for plotting
        labels = "Negative", "Neutral", "Positive"
        sentiment_totals = filtered_data.groupby("sentiment")["sentiment_score"].sum()
        colors = [
            (
                "#7495a8"
                if sentiment == "positive"
                else "#ae4f4d" if sentiment == "negative" else "#eeeadb"
            )
            for sentiment in sentiment_totals.index
        ]
        explode = (0, 0, 0)  # 'explode' the 1st slice (Positive)

        # Plot
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.pie(
            sentiment_totals,
            explode=explode,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=140,
        )
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Draw a circle at the center of pie to make it look like a donut
        centre_circle = plt.Circle((0, 0), 0.50, fc="white")
        fig.gca().add_artist(centre_circle)
        plt.title("Aggregated Sentiment Analysis")
        st.pyplot(fig)
    except:
        ui.badges(
            badge_list=[("Error Loading donut chart.", "secondary")],
            class_name="flex gap-2",
            key="badges1",
        )

with col2:
    try:
        ts = filtered_data.copy()
        ts_df = ts.resample("M", on="time").size()

        fig, ax = plt.subplots(figsize=(18, 2.5))
        sns.lineplot(data=ts_df, ax=ax, color="#d7662a", linewidth=2)
        ax.set_xlabel(
            ""
        )  # Assuming you want no label, if you do, replace "" with your label
        ax.set_ylabel("Review Count")

        # Adding grid, removing spines except left
        ax.yaxis.grid(True, linestyle="--", linewidth=0.5, color="#888888")
        ax.xaxis.grid(True, linestyle="--", linewidth=0.5, color="#888888")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        ax.set_title("Review Count over Time")
    except Exception as e:
        ui.badges(
            badge_list=[(f"Error Loading plot: {str(e)}", "secondary")],
            class_name="flex gap-2",
            key="badges1",
        )
    else:
        st.pyplot(plt)

    st.write("")
    st.write("")

    # Sentiment Analysis Mean over time (Monthly) -------------------------
    filtered_data["time"] = pd.to_datetime(filtered_data["time"])
    filtered_data.set_index("time", inplace=True)

    # Now, group by 'sentiment' and resample by month, then calculate the mean sentiment_score
    monthly_sentiment_means_adjusted = (
        filtered_data.groupby("sentiment")
        .resample("M")["sentiment_score"]
        .mean()
        .unstack(level=0)
    )

    # Fill NaN values, which might be there if there are no records for a given month
    monthly_sentiment_means_adjusted.fillna(0, inplace=True)

    # Melting the DataFrame to long format for easier plotting with seaborn
    data_long_monthly = monthly_sentiment_means_adjusted.reset_index().melt(
        id_vars="time", var_name="Sentiment", value_name="Average Score"
    )

    colors = [
        (
            "#7495a8"
            if sentiment == "positive"
            else "#ae4f4d" if sentiment == "negative" else "#eeeadb"
        )
        for sentiment in sentiment_totals.index
    ]

    # Creating the plot for monthly sentiment scores
    fig, ax = plt.subplots(figsize=(18, 3.5))
    sns.lineplot(
        data=data_long_monthly,
        x="time",
        y="Average Score",
        hue="Sentiment",
        marker="o",
        palette=colors,
        linewidth=2,
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.xaxis.grid(True, linestyle="--", linewidth=0.5, color="#888888")
    ax.yaxis.grid(True, linestyle="--", linewidth=0.5, color="#888888")
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Average Sentiment Score", fontsize=12)
    plt.legend(title="Sentiment")
    plt.tight_layout()
    st.pyplot(plt)


# ---- Total Sentiment Analysis -----------------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
surgery_list = filtered_data["Practice_Name"].unique()
no_of_surgeries = len(surgery_list)
surgery_list.sort()
with col1:
    ui.metric_card(
        title="Mean Rating",
        content=f"{filtered_data['star_rating'].mean()}",
        description="Star Rating 1 - 5",
        key="card3",
    )

with col2:
    ui.metric_card(
        title="Number of Surgeries",
        content=f"{no_of_surgeries}",
        description="In current selection.",
        key="card5",
    )
with col3:
    with st.container(height=120, border=1):
        for surgery in surgery_list:
            st.write(surgery)


# ---- Total Sentiment Analysis -----------------------------------------------------------------------------------

# ---- Total Sentiment Analysis -----------------------------------------------------------------------------------

# ---- Total Sentiment Analysis -----------------------------------------------------------------------------------
