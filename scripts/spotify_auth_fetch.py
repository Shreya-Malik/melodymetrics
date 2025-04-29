import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Spotify API Credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Setup Spotify API client
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    ),
    requests_timeout=10
)

def fetch_top_tracks(artist_name, max_tracks=5):
    """Fetch top tracks for a given artist."""
    try:
        result = sp.search(q=f"artist:{artist_name}", type='artist', limit=1)
        if not result['artists']['items']:
            print(f"No artist found for {artist_name}")
            return []

        artist = result['artists']['items'][0]
        artist_id = artist['id']
        artist_followers = artist['followers']['total']
        artist_genres = artist['genres']
        artist_popularity = artist['popularity']

        top_tracks = sp.artist_top_tracks(artist_id)

        tracks_data = []
        for track in top_tracks['tracks'][:max_tracks]:
            track_info = {
                'input_artist': artist_name,
                'track_title': track['name'],
                'album': track['album']['name'],
                'release_date': track['album']['release_date'],
                'track_popularity': track['popularity'],
                'artist_followers': artist_followers,
                'artist_genres': artist_genres,
                'artist_popularity': artist_popularity
            }
            tracks_data.append(track_info)

        return tracks_data

    except Exception as e:
        print(f"Error fetching tracks for {artist_name}: {e}")
        return []

if __name__ == "__main__":
    try:
        # Load artist names from Billboard dataset
        billboard_df = pd.read_csv("./data/billboard_hot_100.csv")

        artists = billboard_df['Artist'].unique()
        print(f"Found {len(artists)} unique artists to fetch from Spotify.")

        all_tracks = []

        for artist in artists:
            print(f"Fetching top tracks for: {artist}")
            artist_tracks = fetch_top_tracks(artist, max_tracks=5)
            all_tracks.extend(artist_tracks)
            time.sleep(0.3)  # Avoid rate limits

        if all_tracks:
            final_df = pd.DataFrame(all_tracks)
            os.makedirs("./data", exist_ok=True)
            final_df.to_csv("./data/spotify_enriched_dataset.csv", index=False)
            print(f"\nSaved {len(final_df)} Spotify enriched tracks to './data/spotify_enriched_dataset.csv'.")
        else:
            print("No tracks fetched from Spotify.")

    except Exception as e:
        print(f"Critical error: {e}")
