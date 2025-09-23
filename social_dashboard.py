import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import social_df  # Your merged DataFrame from data_loader.py

# -------------------------------
# Streamlit Page Configuration
# -------------------------------
st.set_page_config(page_title="Social Media Dashboard", layout="wide")
st.title("📊 Social Media Dashboard")
st.markdown("Insights across Facebook, Instagram, Twitter, and TikTok")
import streamlit as st
from data_loader import social_df

# Page setup
st.set_page_config(page_title="📊 Social Media Dashboard", layout="wide")

st.title("📊 Social Media Dashboard")

# Check if data loaded
if social_df.empty:
    st.warning("⚠️ No data loaded. Please check your CSV files inside the `data/` folder.")
else:
    st.success(f"✅ Data loaded successfully with {len(social_df)} records.")

    # Date filter (only if 'date_created' exists)
    if 'date_created' in social_df.columns:
        min_date = social_df['date_created'].min()
        max_date = social_df['date_created'].max()

        if pd.notna(min_date) and pd.notna(max_date):
            date_range = st.sidebar.date_input(
                "📅 Select Date Range:",
                [min_date.date(), max_date.date()]
            )

            if len(date_range) == 2:
                start_date, end_date = date_range
                mask = (social_df['date_created'] >= pd.to_datetime(start_date)) & \
                       (social_df['date_created'] <= pd.to_datetime(end_date))
                filtered_df = social_df.loc[mask]
            else:
                filtered_df = social_df
        else:
            filtered_df = social_df
    else:
        filtered_df = social_df

    # Data preview
    st.subheader("📋 Data Preview")
    st.dataframe(filtered_df.head(20))  # Show first 20 rows

    # Quick stats
    st.subheader("📈 Quick Stats")
    st.write(filtered_df.describe(include="all"))

    # Platform counts
    if 'platform' in filtered_df.columns:
        st.subheader("📊 Records by Platform")
        st.bar_chart(filtered_df['platform'].value_counts())


# -------------------------------
# Preprocess Data
# -------------------------------
if "date_created" in social_df.columns:
    social_df["date_created"] = pd.to_datetime(social_df["date_created"], errors="coerce")
    social_df = social_df.dropna(subset=["date_created"])  # remove rows without valid dates

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("Filters")

# Platform filter
platforms = st.sidebar.multiselect(
    "Select Platform(s):",
    options=social_df["platform"].unique(),
    default=social_df["platform"].unique()
)

# Date filter (safe handling of NaT / empty dataframe)
if not social_df.empty:
    start_date = social_df["date_created"].min().date()
    end_date = social_df["date_created"].max().date()
else:
    start_date = end_date = pd.Timestamp.today().date()

date_range = st.sidebar.date_input(
    "Select Date Range:",
    [start_date, end_date]
)

# Post type filter
post_types = st.sidebar.multiselect(
    "Select Post Type(s):",
    options=social_df["subtype"].unique(),
    default=social_df["subtype"].unique()
)

# Apply filters
filtered_df = social_df[
    (social_df["platform"].isin(platforms)) &
    (social_df["subtype"].isin(post_types)) &
    (social_df["date_created"].dt.date.between(date_range[0], date_range[1]))
].copy()

# -------------------------------
# Top KPIs
# -------------------------------
st.subheader("📌 Key Metrics")

total_posts = filtered_df["post_id"].nunique()
total_likes = filtered_df["num_likes"].sum()
total_comments = filtered_df["comment_id"].nunique()

filtered_df["engagement"] = filtered_df["num_likes"] + filtered_df["num_replies"]
avg_engagement_per_post = (
    filtered_df.groupby("post_id")["engagement"].sum().mean()
    if not filtered_df.empty else 0
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Posts", total_posts)
col2.metric("Total Likes", total_likes)
col3.metric("Total Comments", total_comments)
col4.metric("Avg Engagement per Post", f"{avg_engagement_per_post:.2f}")

# -------------------------------
# Line Chart: Posts Over Time
# -------------------------------
st.subheader("📈 Posts Over Time")
if not filtered_df.empty:
    posts_over_time = (
        filtered_df.groupby(["platform", pd.Grouper(key="date_created", freq="D")])["post_id"]
        .count()
        .reset_index(name="num_posts")
    )
    fig_posts = px.line(posts_over_time, x="date_created", y="num_posts", color="platform",
                        title="Daily Posts per Platform")
    st.plotly_chart(fig_posts, use_container_width=True)
else:
    st.info("No data available for selected filters.")

# -------------------------------
# Line Chart: Likes Over Time
# -------------------------------
st.subheader("❤️ Likes Over Time")
if not filtered_df.empty:
    likes_over_time = (
        filtered_df.groupby(["platform", pd.Grouper(key="date_created", freq="D")])["num_likes"]
        .sum()
        .reset_index()
    )
    fig_likes = px.line(likes_over_time, x="date_created", y="num_likes", color="platform",
                        title="Daily Likes per Platform")
    st.plotly_chart(fig_likes, use_container_width=True)
else:
    st.info("No data available for selected filters.")

# -------------------------------
# Top 10 Posts by Engagement
# -------------------------------
st.subheader("🏆 Top 10 Posts by Engagement")
if not filtered_df.empty:
    top_posts = (
        filtered_df.groupby(["post_id", "platform", "post_url"])["engagement"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    st.table(top_posts)
else:
    st.info("No posts to display for selected filters.")

# -------------------------------
# Bar Chart: Engagement by Post Type
# -------------------------------
st.subheader("📊 Engagement by Post Type")
if not filtered_df.empty:
    engagement_by_type = filtered_df.groupby("subtype")["engagement"].sum().reset_index()
    fig_bar = px.bar(
        engagement_by_type, x="subtype", y="engagement", text="engagement",
        title="Total Engagement per Post Type"
    )
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("No engagement data for selected filters.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("Developed with ❤️ using Python, Pandas, Plotly, and Streamlit")
