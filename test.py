import os
import glob
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from streamlit_autorefresh import st_autorefresh


PARQUET_DIR = "./stream_output/parquet"

st.set_page_config(page_title="Twitter Sentiment (Offline Viewer)", layout="wide")
st.title("📊 Twitter Hashtag Sentiment (Loaded from Files)")

st_autorefresh(interval=10 * 1000, key="refresh")


@st.cache_data(ttl=10)
def load_data():
    """Load all parquet files available in PARQUET_DIR"""
    if not os.path.exists(PARQUET_DIR):
        return pd.DataFrame()

    files = glob.glob(os.path.join(PARQUET_DIR, "*.parquet"))
    if not files:
        return pd.DataFrame()

    try:
        df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
        return df
    except Exception as e:
        st.error(f"Error reading parquet files: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("⚡ No data found in parquet files. Add some files to ./stream_output/parquet")
    st.stop()

if "sentiment_label" not in df.columns and "sentiment" in df.columns:
    df["sentiment_label"] = df["sentiment"]

if "timestamp" not in df.columns:
    df["timestamp"] = pd.Timestamp.now()

if "minute" not in df.columns:
    df["minute"] = pd.to_datetime(df["timestamp"]).dt.floor("T")

if "username" not in df.columns:
    df["username"] = "Unknown"
df["username"] = df["username"].fillna("Unknown")

sentiments = ["All"] + sorted(df["sentiment_label"].dropna().unique().tolist())
users = ["All"] + sorted(df["username"].dropna().unique().tolist())

col1, col2 = st.columns(2)
with col1:
    sentiment_filter = st.selectbox("Filter by Sentiment", sentiments)
with col2:
    user_filter = st.selectbox("Filter by Username", users)

filtered_df = df.copy()
if sentiment_filter != "All":
    filtered_df = filtered_df[filtered_df["sentiment_label"] == sentiment_filter]
if user_filter != "All":
    filtered_df = filtered_df[filtered_df["username"] == user_filter]

total = len(filtered_df)
by_label = filtered_df["sentiment_label"].value_counts()

st.subheader(f"Total Tweets: {total}")
col1, col2 = st.columns([1, 2])

with col1:
    if not by_label.empty:
        fig, ax = plt.subplots()
        ax.pie(by_label, labels=by_label.index, autopct='%1.1f%%', startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

with col2:
    if not by_label.empty:
        st.bar_chart(by_label)

st.subheader("🌟 Trending Words")
text = " ".join(filtered_df["content"].dropna().astype(str))
if text.strip():
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
else:
    st.write("Not enough text for wordcloud.")

if "minute" in filtered_df.columns:
    st.subheader("⏱️ Sentiment Over Time")
    ts = (
        filtered_df.groupby(["minute", "sentiment_label"])
        .size()
        .reset_index(name="count")
    )
    if not ts.empty:
        st.line_chart(
            ts.pivot(index="minute", columns="sentiment_label", values="count").fillna(0)
        )

st.subheader("📡 Latest Tweets from Files")
cols = ["timestamp", "username", "content", "sentiment", "sentiment_label"]
for col in cols:
    if col not in filtered_df.columns:
        filtered_df[col] = None

show = filtered_df[cols].sort_values("timestamp", ascending=False).head(20)
st.dataframe(show, use_container_width=True, hide_index=True)
