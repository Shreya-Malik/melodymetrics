import pandas as pd
import os

# File paths from environment or defaults
BILLBOARD_CSV_PATH = os.getenv('BILLBOARD_CSV_PATH', './data/billboard_hot_100.csv')
SPOTIFY_CSV_PATH = os.getenv('SPOTIFY_CSV_PATH', './data/spotify_enriched_dataset.csv')
FINAL_DATASET_PATH = os.getenv('FINAL_DATASET_PATH', './data/final_music_dataset.csv')

def integrate_datasets():
    try:
        # Load Billboard and Spotify datasets
        billboard_df = pd.read_csv(BILLBOARD_CSV_PATH)
        spotify_df = pd.read_csv(SPOTIFY_CSV_PATH)

        print(f"Loaded {len(billboard_df)} Billboard records.")
        print(f"Loaded {len(spotify_df)} Spotify records.")

        # Merge both datasets
        combined_df = pd.concat([billboard_df, spotify_df], ignore_index=True)

        # Drop any duplicate rows
        combined_df.drop_duplicates(inplace=True)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(FINAL_DATASET_PATH), exist_ok=True)

        # Save the merged dataset
        combined_df.to_csv(FINAL_DATASET_PATH, index=False)

        print(f"Integration completed. Final dataset saved at '{FINAL_DATASET_PATH}' with {len(combined_df)} records.")

    except Exception as e:
        print(f"Error during integration: {e}")

if __name__ == "__main__":
    integrate_datasets()
