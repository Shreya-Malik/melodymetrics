import pandas as pd
import os

# Paths
RAW_PATH = "./data/billboard_raw_500.csv"
CLEAN_PATH = "./data/billboard_cleaned.csv"

# Load data
df = pd.read_csv(RAW_PATH)

print(f"Loaded {len(df)} total records.")

# Drop full duplicates (same song + artist)
initial_shape = df.shape
df_clean = df.drop_duplicates(subset=["Song", "Artist"])
cleaned_shape = df_clean.shape

# Check missing values
missing_song = df_clean['Song'].isna().sum()
missing_artist = df_clean['Artist'].isna().sum()

print(f"\nDuplicates removed: {initial_shape[0] - cleaned_shape[0]}")
print(f"Remaining unique records: {cleaned_shape[0]}")

print("\nMissing values:")
print(f"- Missing 'Song': {missing_song}")
print(f"- Missing 'Artist': {missing_artist}")

# Remove missing song or artist
df_clean = df_clean.dropna(subset=['Song', 'Artist'])

# Final save
os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
df_clean.to_csv(CLEAN_PATH, index=False)

print(f"\nCleaned dataset saved to {CLEAN_PATH}")
