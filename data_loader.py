import os
import pandas as pd

# -------------------------------
# Load CSV files
# -------------------------------

# You can either use local files:
# data_path = os.path.join(os.path.dirname(__file__), "data")
# csv_files = [os.path.join(data_path, f) for f in os.listdir(data_path) if f.endswith(".csv")]

# Or directly from GitHub (for testing)
csv_urls = [
    "https://raw.githubusercontent.com/EcomCloud/social_media_dashboard/refs/heads/main/data/Facebook-datasets.csv"
    # Add more URLs here for Instagram, Twitter, TikTok if needed
]

df_list = []

for url in csv_urls:
    df = pd.read_csv(url)

    # Handle missing numeric values
    for col in ['num_likes', 'num_replies', 'video_length']:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    # Handle missing text values
    for col in ['comment_text', 'user_url']:
        if col in df.columns:
            df[col] = df[col].fillna('')

    # Parse dates
    if 'date_created' in df.columns:
        df['date_created'] = pd.to_datetime(df['date_created'], errors='coerce')

    # Add platform column based on filename or URL
    platform = 'Unknown'
    if 'facebook' in url.lower():
        platform = 'Facebook'
    elif 'instagram' in url.lower():
        platform = 'Instagram'
    elif 'twitter' in url.lower():
        platform = 'Twitter'
    elif 'tiktok' in url.lower():
        platform = 'TikTok'
    df['platform'] = platform

    df_list.append(df)

# Merge all into one DataFrame
social_df = pd.concat(df_list, ignore_index=True)

# -------------------------------
# Test output
# -------------------------------
if __name__ == "__main__":
    print(social_df.head())
    print(social_df.info())
