import pandas as pd
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API Credentials
SPOTIFY_CLIENT_ID = 'bb50ce3a40264186b606249c4caac421'
SPOTIFY_CLIENT_SECRET = '3f342271aca34ebf94b39a59856362b9'

# Initialize Spotify API Client
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
            print(f"⚠️ No Spotify results for: {title} by {artist}")
    except Exception as e:
        print(f"❌ Error fetching Spotify metadata for {title} by {artist}: {e}")
    return {}

if __name__ == "__main__":
    try:
        billboard_df = pd.read_csv("../data/billboard_hot_100.csv")
        print(f"✅ Loaded Billboard data: {len(billboard_df)} songs")

        enriched_data = []

        for idx, row in billboard_df.iterrows():
            title = row['Song']
            artist = row['Artist']

            print(f"🔎 Searching Spotify for: {title} by {artist} (Song {idx+1})")

            metadata = fetch_spotify_metadata(title, artist)

            if metadata:
                enriched_row = {
                    'billboard_song': title,
                    'billboard_artist': artist,
                    **metadata
                }
                enriched_data.append(enriched_row)
            else:
                print(f"⚠️ Skipping {title} by {artist}, no Spotify data found.")

            time.sleep(0.3)  # Avoid API rate limits

        if enriched_data:
            final_df = pd.DataFrame(enriched_data)

            # ✅ Save final merged dataset to CSV
            final_df.to_csv("../data/final_music_dataset.csv", index=False)
            print("\n✅ Saved final merged dataset to 'data/final_music_dataset.csv'")
        else:
            print("⚠️ No data to save!")

    except Exception as e:
        print(f"❌ Critical error in integration script: {e}")

    
