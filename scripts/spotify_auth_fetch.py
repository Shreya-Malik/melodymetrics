import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set credentials dynamically
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://127.0.0.1:8888/callback')
SLEEP_INTERVAL = float(os.getenv('SLEEP_INTERVAL', 0.3))

# Set up Spotify OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope='user-library-read',
    cache_path=".spotipyoauthcache"
))

def fetch_song_metadata(songs):
    results = []

    for title, artist in songs:
        query = f"track:{title} artist:{artist}"
        search = sp.search(q=query, type='track', limit=1)

        if search['tracks']['items']:
            track = search['tracks']['items'][0]
            track_id = track['id']
            artist_id = track['artists'][0]['id']

            artist_info = sp.artist(artist_id)

            song_data = {
                "input_title": title,
                "input_artist": artist,
                "spotify_title": track['name'],
                "spotify_artist": track['artists'][0]['name'],
                "release_date": track['album']['release_date'],
                "album": track['album']['name'],
                "track_popularity": track['popularity'],
                "artist_genres": artist_info['genres'],
                "artist_followers": artist_info['followers']['total'],
                "artist_popularity": artist_info['popularity']
            }

            print(f"Fetched: {track['name']} by {track['artists'][0]['name']}")
            results.append(song_data)
        else:
            print(f"Not found: {title} by {artist}")

        time.sleep(SLEEP_INTERVAL)

    return results

if __name__ == "__main__":
    sample_songs = [
        ("Shape of You", "Ed Sheeran"),
        ("Flowers", "Miley Cyrus"),
        ("Blinding Lights", "The Weeknd")
    ]

    metadata = fetch_song_metadata(sample_songs)
    for song in metadata:
        print("\nEnriched Song Data:")
        for key, value in song.items():
            print(f"{key}: {value}")
