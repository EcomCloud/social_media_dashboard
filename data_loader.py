import os
import pandas as pd

# Define the data folder path
data_path = os.path.join(os.path.dirname(__file__), "data")

# List all CSV files inside data folder
csv_files = [f for f in os.listdir(data_path) if f.endswith(".csv")]

# Initialize empty list to store individual DataFrames
df_list = []

for file in csv_files:
    file_path = os.path.join(data_path, file)
    
    # Load CSV
    df = pd.read_csv(file_path)
    
    # Add a 'platform' column based on filename
    df['platform'] = file.split('.')[0]  # e.g., 'Facebook', 'Instagram'
    
    # Convert 'date_created' to datetime if the column exists
    if 'date_created' in df.columns:
        df['date_created'] = pd.to_datetime(df['date_created'], errors='coerce')
    
    # Append to list
    df_list.append(df)

# Merge all dataframes into a single DataFrame
social_df = pd.concat(df_list, ignore_index=True)

# Optional: check the merged dataframe
if __name__ == "__main__":
    print(social_df.head())
    print(social_df.info())
