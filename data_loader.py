import pandas as pd
import glob
import os

data_folder = "data"

facebook = pd.read_csv(os.path.join(data, "Facebook.csv"))
twitter = pd.read_csv(os.path.join(data, "Twitter.csv"))
instagram = pd.read_csv(os.path.join(data, "Instagram.csv"))
tiktok = pd.read_csv(os.path.join(data, "Tiktok.csv"))

# List all CSV files for social media platforms
csv_files = ["Facebook.csv", "Instagram.csv", "Twitter.csv", "Tiktok.csv"]

# Initialize empty list to store individual DataFrames
df_list = []

for file in csv_files:
    file_path = os.path.join(folder_path, file)
    
    # Load CSV
    df = pd.read_csv(file_path)
    
    # Add a 'platform' column based on filename
    df['platform'] = file.split('.')[0]  # e.g., 'Facebook', 'Instagram'
    
    # Convert 'date_created' to datetime
    df['date_created'] = pd.to_datetime(df['date_created'], errors='coerce')
    
    # Append to list
    df_list.append(df)

# Merge all dataframes into a single DataFrame
social_df = pd.concat(df_list, ignore_index=True)

# Optional: check the merged dataframe
print(social_df.head())
print(social_df.info())
