import pandas as pd
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Spotify credentials from .env
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Configurations
BILLBOARD_CSV_PATH = os.getenv('BILLBOARD_CSV_PATH', './data/billboard_hot_100.csv')
FINAL_DATASET_PATH = os.getenv('FINAL_DATASET_PATH', './data/final_music_dataset.csv')
SLEEP_INTERVAL = float(os.getenv('SLEEP_INTERVAL', 0.3))

# Initialize Spotify Client
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    ),
    requests_timeout=10
)

def fetch_spotify_metadata(title, artist):
    try:
        query = f"{title} {artist}"
        results = sp.search(q=query, limit=1, type='track')

        if results and results['tracks']['items']:
            track = results['tracks']['items'][0]
            metadata = {
                'spotify_title': track['name'],
                'spotify_artist': track['artists'][0]['name'],
                'release_date': track['album']['release_date'],
                'album_name': track['album']['name'],
                'track_popularity': track['popularity']
            }
            return metadata
        else:
            print(f"No Spotify results for: {title} by {artist}")
    except Exception as e:
        print(f"Error fetching Spotify metadata for {title} by {artist}: {e}")
    return {}

if __name__ == "__main__":
    try:
        # Load Billboard data
        billboard_df = pd.read_csv(BILLBOARD_CSV_PATH)
        print(f"Loaded Billboard data: {len(billboard_df)} songs")

        enriched_data = []

        for idx, row in billboard_df.iterrows():
            title = row['Song']
            artist = row['Artist']

            print(f"Searching Spotify for: {title} by {artist} (Song {idx + 1})")

            metadata = fetch_spotify_metadata(title, artist)

            if metadata:
                enriched_row = {
                    'billboard_song': title,
                    'billboard_artist': artist,
                    **metadata
                }
                enriched_data.append(enriched_row)
            else:
                print(f"Skipping {title} by {artist}, no Spotify data found.")

            time.sleep(SLEEP_INTERVAL)  # Controlled sleep from config

        if enriched_data:
            final_df = pd.DataFrame(enriched_data)

            # Ensure data folder exists
            os.makedirs(os.path.dirname(FINAL_DATASET_PATH), exist_ok=True)

            final_df.to_csv(FINAL_DATASET_PATH, index=False)
            print(f"\nSaved final merged dataset to '{FINAL_DATASET_PATH}'")
        else:
            print("No enriched data to save.")

    except Exception as e:
        print(f"Critical error in integration script: {e}")
