import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import social_df  # Your merged DataFrame from pandas.py

# -------------------------------
# Streamlit Page Configuration
# -------------------------------
st.set_page_config(page_title="Social Media Dashboard", layout="wide")
st.title("📊 Social Media Dashboard")
st.markdown("Insights across Facebook, Instagram, Twitter, and TikTok")

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("Filters")
platforms = st.sidebar.multiselect(
    "Select Platform(s):",
    options=social_df['platform'].unique(),
    default=social_df['platform'].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range:",
    [social_df['date_created'].min().date(), social_df['date_created'].max().date()]
)

post_types = st.sidebar.multiselect(
    "Select Post Type(s):",
    options=social_df['subtype'].unique(),
    default=social_df['subtype'].unique()
)

# Filter data
filtered_df = social_df[
    (social_df['platform'].isin(platforms)) &
    (social_df['subtype'].isin(post_types)) &
    (social_df['date_created'].dt.date.between(date_range[0], date_range[1]))
]

# -------------------------------
# Top KPIs
# -------------------------------
st.subheader("📌 Key Metrics")
total_posts = filtered_df['post_id'].nunique()
total_likes = filtered_df['num_likes'].sum()
total_comments = filtered_df['comment_id'].nunique()
filtered_df['engagement'] = filtered_df['num_likes'] + filtered_df['num_replies']
avg_engagement_per_post = filtered_df.groupby('post_id')['engagement'].sum().mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Posts", total_posts)
col2.metric("Total Likes", total_likes)
col3.metric("Total Comments", total_comments)
col4.metric("Avg Engagement per Post", f"{avg_engagement_per_post:.2f}")

# -------------------------------
# Line Chart: Posts Over Time
# -------------------------------
st.subheader("📈 Posts Over Time")
posts_over_time = filtered_df.groupby(['platform', pd.Grouper(key='date_created', freq='D')])\
                      ['post_id'].count().reset_index(name='num_posts')
fig_posts = px.line(posts_over_time, x='date_created', y='num_posts', color='platform',
                    title="Daily Posts per Platform")
st.plotly_chart(fig_posts, use_container_width=True)

# -------------------------------
# Line Chart: Likes Over Time
# -------------------------------
st.subheader("❤️ Likes Over Time")
likes_over_time = filtered_df.groupby(['platform', pd.Grouper(key='date_created', freq='D')])\
                      ['num_likes'].sum().reset_index()
fig_likes = px.line(likes_over_time, x='date_created', y='num_likes', color='platform',
                    title="Daily Likes per Platform")
st.plotly_chart(fig_likes, use_container_width=True)

# -------------------------------
# Top 10 Posts by Engagement
# -------------------------------
st.subheader("🏆 Top 10 Posts by Engagement")
top_posts = filtered_df.groupby(['post_id', 'platform', 'post_url'])['engagement'].sum()\
            .sort_values(ascending=False).head(10).reset_index()
st.table(top_posts)

# -------------------------------
# Bar Chart: Engagement by Post Type
# -------------------------------
st.subheader("📊 Engagement by Post Type")
engagement_by_type = filtered_df.groupby('subtype')['engagement'].sum().reset_index()
fig_bar = px.bar(engagement_by_type, x='subtype', y='engagement', text='engagement',
                 title="Total Engagement per Post Type")
st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------------
# Optional: Word Cloud or Sentiment Analysis
# -------------------------------
# You can extend this later with word clouds from comment_text or sentiment analysis

st.markdown("Developed with ❤️ using Python, Pandas, Plotly, and Streamlit")
