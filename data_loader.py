import os
import pandas as pd

# Path to the 'data' folder
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_csv(filename):
    """Load a CSV safely, return empty DataFrame if not found."""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        print(f"⚠️ File not found: {filename}")
        return pd.DataFrame()  # empty if missing

# Load each dataset
facebook = load_csv("Facebook.csv")
instagram = load_csv("Instagram.csv")
twitter = load_csv("Twitter.csv")

# Merge into one dataframe
if not facebook.empty or not instagram.empty or not twitter.empty:
    social_df = pd.concat([facebook, instagram, twitter], ignore_index=True)
else:
    social_df = pd.DataFrame()  # all missing
