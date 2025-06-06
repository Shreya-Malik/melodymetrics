import pandas as pd
import os

INPUT_CSV = "./data/final_music_dataset.csv"
OUTPUT_CSV = "./data/final_music_dataset_cleaned.csv"

# Load the dataset
df = pd.read_csv(INPUT_CSV)
print(f"Initial dataset size: {len(df)}")

# Fill missing artist_genres with 'Unknown'
df['artist_genres'] = df['artist_genres'].fillna('Unknown')

# Optional: remove rows where too many values are missing (not needed now)

# Final check
print("\nRemaining missing values:")
print(df.isnull().sum())

# Save cleaned dataset
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False)
print(f"\nCleaned dataset saved to '{OUTPUT_CSV}' with {len(df)} records.")
