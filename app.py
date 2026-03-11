import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from analysis import load_and_clean_data

# Page setup
st.set_page_config(page_title="Spotify Dashboard", layout="wide")

st.title("🎧 Spotify Track Analysis & Recommendation Dashboard")

# Load data
df = load_and_clean_data()

# Sidebar controls
st.sidebar.title("Dashboard Controls")

popularity_range = st.sidebar.slider(
    "Select Popularity Range",
    int(df['track_popularity'].min()),
    int(df['track_popularity'].max()),
    (20,80)
)

page = st.sidebar.radio(
    "Navigate",
    ["Dashboard Overview","Visual Analysis","Top Tracks","Search Track","Recommendation System"]
)

filtered_df = df[
    (df['track_popularity'] >= popularity_range[0]) &
    (df['track_popularity'] <= popularity_range[1])
]

# ---------------- DASHBOARD OVERVIEW ----------------
if page == "Dashboard Overview":

    st.subheader("📊 Key Metrics")

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Tracks", len(df))
    c2.metric("Average Popularity", round(df['track_popularity'].mean(),2))
    c3.metric("Explicit Songs", df['explicit'].sum())

    st.divider()

    st.subheader("Dataset Preview")
    st.dataframe(filtered_df.head(15))

# ---------------- VISUAL ANALYSIS ----------------
elif page == "Visual Analysis":

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Popularity Distribution")

        fig, ax = plt.subplots()
        sns.histplot(filtered_df['track_popularity'], bins=20, ax=ax)
        st.pyplot(fig)

    with col2:
        st.subheader("Explicit vs Non Explicit")

        fig2, ax2 = plt.subplots()
        sns.countplot(x="explicit", data=filtered_df, ax=ax2)
        st.pyplot(fig2)

# ---------------- TOP TRACKS ----------------
elif page == "Top Tracks":

    st.subheader("🔥 Top 10 Popular Tracks")

    top10 = filtered_df.sort_values(
        by="track_popularity",
        ascending=False
    ).head(10)

    st.dataframe(top10[['track_name','track_popularity','explicit']])

# ---------------- SEARCH TRACK ----------------
elif page == "Search Track":

    st.subheader("🔎 Search Track")

    search_song = st.text_input("Type song name")

    if search_song:
        result = df[df['track_name'].str.contains(search_song, case=False)]

        if len(result) > 0:
            st.write("Search Results")
            st.dataframe(result[['track_name','track_popularity','explicit']])
        else:
            st.warning("No track found")

# ---------------- RECOMMENDATION SYSTEM ----------------
elif page == "Recommendation System":

    st.subheader("🎵 Music Recommendation")

    song = st.selectbox(
        "Select a Song",
        df['track_name'].unique()
    )

    popularity = df[df['track_name']==song]['track_popularity'].values[0]

    recommended = df[
        (df['track_popularity'] >= popularity-5) &
        (df['track_popularity'] <= popularity+5)
    ]

    st.write("Songs You Might Like")

    st.dataframe(
        recommended[['track_name','track_popularity','explicit']].head(5)
    )