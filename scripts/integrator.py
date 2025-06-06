import pandas as pd
import time
import os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from dotenv import load_dotenv

load_dotenv()

# Load configuration
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
CLEAN_INPUT_PATH = os.getenv("BILLBOARD_CLEAN_PATH", "./data/billboard_cleaned.csv")
FINAL_OUTPUT_PATH = os.getenv("FINAL_DATASET_PATH", "./data/final_music_dataset.csv")
SLEEP_TIME = float(os.getenv("SLEEP_INTERVAL", 0.3))

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

def fetch_spotify_metadata(title, artist):
    try:
        query = f"track:{title} artist:{artist}"
        results = sp.search(q=query, type='track', limit=1)
        if results and results['tracks']['items']:
            track = results['tracks']['items'][0]
            artist_id = track['artists'][0]['id']
            artist_data = sp.artist(artist_id)

            return {
                "spotify_title": track["name"],
                "spotify_artist": track["artists"][0]["name"],
                "release_date": track["album"]["release_date"],
                "album": track["album"]["name"],
                "track_popularity": track["popularity"],
                "artist_genres": ", ".join(artist_data["genres"]),
                "artist_followers": artist_data["followers"]["total"],
                "artist_popularity": artist_data["popularity"]
            }
    except Exception as e:
        print(f"Error fetching {title} by {artist}: {e}")
    return None

if __name__ == "__main__":
    billboard_df = pd.read_csv(CLEAN_INPUT_PATH)
    print(f"\nLoaded cleaned Billboard data: {len(billboard_df)} songs")

    enriched = []
    errors = 0

    for idx, row in billboard_df.iterrows():
        title = row["Song"]
        artist = row["Artist"]
        print(f"Fetching metadata for {title} by {artist}...")

        metadata = fetch_spotify_metadata(title, artist)

        if metadata:
            enriched.append({
                "billboard_song": title,
                "billboard_artist": artist,
                **metadata
            })
        else:
            errors += 1

        time.sleep(SLEEP_TIME)

    print(f"\nSuccessfully enriched {len(enriched)} songs out of {len(billboard_df)}")
    print(f"Failed to enrich: {errors} songs ({round(errors / len(billboard_df) * 100, 2)}%)")

    # Save enriched dataset
    os.makedirs(os.path.dirname(FINAL_OUTPUT_PATH), exist_ok=True)
    pd.DataFrame(enriched).to_csv(FINAL_OUTPUT_PATH, index=False)
    print(f"\nFinal dataset saved to {FINAL_OUTPUT_PATH}")
