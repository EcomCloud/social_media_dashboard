import os
import pandas as pd

# Path to the 'data' folder
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_csv(filename):
    """Load a CSV safely. If not found, return empty DataFrame."""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            df['platform'] = filename.split('.')[0]  # Add platform column
            # Try to parse date column if exists
            if 'date_created' in df.columns:
                df['date_created'] = pd.to_datetime(df['date_created'], errors='coerce')
            return df
        except Exception as e:
            print(f"⚠️ Error loading {filename}: {e}")
            return pd.DataFrame()
    else:
        print(f"⚠️ File not found: {filename}")
        return pd.DataFrame()

# Load datasets
facebook = load_csv("Facebook.csv")
instagram = load_csv("Instagram.csv")
twitter = load_csv("Twitter.csv")

# Merge into one dataframe
if not facebook.empty or not instagram.empty or not twitter.empty:
    social_df = pd.concat([facebook, instagram, twitter], ignore_index=True)
else:
    social_df = pd.DataFrame()  # if all missing
