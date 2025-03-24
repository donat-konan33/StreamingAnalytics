import streamlit as st
import pandas as pd
import plotly.express as px
import time
from lwqueue.clickhouse_queries import get_data
import datetime
st.set_page_config(layout="wide")

# --- UI Streamlit ---
st.title("📊 Messages Analysis from ClickHouse Database ")

# refresh data
container = st.empty()

while True:
    all_messages_df, top_users_df, avg_gap_df = get_data()
    with container.container(border=True):
        st.write("🔹 Refreshing every 10 seconds...")
        st.subheader("🔹 All Messages")
        st.dataframe(all_messages_df)

        top_users_col, mean_time_col = st.columns([2, 3])
        with st.container(border=True):
            with top_users_col:
                st.subheader("🔹 Top 5 Most Active Users")
                st.dataframe(top_users_df)
        with st.container(border=True):
            with mean_time_col:
                st.subheader("🔹 Mean Time Between Messages")
                st.metric(label="📌 Mean time between messages : ", value=f"{avg_gap_df.iloc[0, 0]:.2f} seconds")

        fig_users = px.bar(
            top_users_df, x="username", y="message_count",
            title="Top 5 Active Users",
            color="message_count", text="message_count"
        )
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # generate unique key
        st.plotly_chart(fig_users, use_container_width=True, key=f"chart_{timestamp}")

    time.sleep(10)  # Refresh every 10 secondes
