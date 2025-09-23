import os
import pandas as pd

# Define the data folder path
data_path = os.path.join(os.path.dirname(__file__), "data")

# Recursively list all CSV files in subfolders
csv_files = []
for root, dirs, files in os.walk(data_path):
    for f in files:
        if f.endswith(".csv"):
            csv_files.append(os.path.join(root, f))

# Platform name mapping
platform_map = {
    "facebook": "Facebook",
    "instagram": "Instagram",
    "twitter": "Twitter",
    "tiktok": "TikTok"
}

df_list = []

for file_path in csv_files:
    df = pd.read_csv(file_path)

    # Infer platform from filename or folder
    name = os.path.basename(file_path).split('.')[0].lower()
    df['platform'] = platform_map.get(name, name)

    # Parse dates
    if 'date_created' in df.columns:
        df['date_created'] = pd.to_datetime(
            df['date_created'],
            format='%Y-%m-%dT%H:%M:%S.%fZ',
            errors='coerce'
        )

    df_list.append(df)

# Merge all into one DataFrame
social_df = pd.concat(df_list, ignore_index=True)

if __name__ == "__main__":
    print(social_df.head())
    print(social_df.info())
