import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Credentials from .env
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# Set up Spotify client
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
        # First attempt: structured search
        query = f'track:"{title}" artist:"{artist}"'
        search = sp.search(q=query, type='track', limit=1)

        if search['tracks']['items']:
            track = search['tracks']['items'][0]
        else:
            # Retry: loose search with just title if no result
            query_retry = f'{title}'
            search = sp.search(q=query_retry, type='track', limit=1)
            if search['tracks']['items']:
                track = search['tracks']['items'][0]
            else:
                print(f"Could not find metadata for {title} by {artist}")
                continue  # Skip this song if still no match

        try:
            track_id = track['id']
            artist_id = track['artists'][0]['id']
            artist_info = sp.artist(artist_id)

            song_data = {
                "input_title": title,
                "input_artist": artist,
                "spotify_title": track['name'],
                "spotify_artist": track['artists'][0]['name'],
                "release_date": track['album']['release_date'],
                "album_name": track['album']['name'],
                "track_popularity": track['popularity'],
                "artist_genres": artist_info.get('genres', []),
                "artist_followers": artist_info.get('followers', {}).get('total', 0),
                "artist_popularity": artist_info.get('popularity', 0)
            }
            results.append(song_data)

        except Exception as e:
            print(f"Error processing {title} by {artist}: {e}")
            continue

        time.sleep(0.4)  # Sleep slightly longer on API

    return results

if __name__ == "__main__":
    sample_songs = [
        ("Shape of You", "Ed Sheeran"),
        ("Flowers", "Miley Cyrus"),
        ("Blinding Lights", "The Weeknd")
    ]

    metadata = fetch_song_metadata(sample_songs)
    for song in metadata:
        print("\nSong Metadata:")
        for key, value in song.items():
            print(f"{key}: {value}")
