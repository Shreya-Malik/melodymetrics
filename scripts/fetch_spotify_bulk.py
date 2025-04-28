import requests
import base64
import time

# Your credentials
CLIENT_ID = 'bb50ce3a40264186b606249c4caac421'
CLIENT_SECRET = '3f342271aca34ebf94b39a59856362b9'

# Auth token generator
def get_token():
    auth_url = "https://accounts.spotify.com/api/token"
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    res = requests.post(auth_url, headers=headers, data=data)
    return res.json().get("access_token")

# Search + fetch audio features
def fetch_spotify_data(songs):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    results = []

    for title, artist in songs:
        query = f"{title} {artist}"
        search_url = "https://api.spotify.com/v1/search"
        params = {
            "q": query,
            "type": "track",
            "limit": 1
        }

        search_res = requests.get(search_url, headers=headers, params=params)
        items = search_res.json().get('tracks', {}).get('items', [])

        if not items:
            print(f"❌ Not found: {query}")
            continue

        track = items[0]
        track_id = track['id']
        features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        feat_res = requests.get(features_url, headers=headers)
        features = feat_res.json()

        if 'danceability' in features:
            results.append({
                "title": title,
                "artist": artist,
                "spotify_title": track['name'],
                "spotify_artist": track['artists'][0]['name'],
                "popularity": track['popularity'],
                "duration_ms": track['duration_ms'],
                "danceability": features['danceability'],
                "energy": features['energy'],
                "tempo": features['tempo'],
                "valence": features['valence'],
                "loudness": features['loudness']
            })
        else:
            print(f"⚠️ No features for {query}")
        time.sleep(0.5)  # prevent rate limits

    return results
if __name__ == "__main__":
    test_songs = [
        ("Blinding Lights", "The Weeknd"),
        ("Levitating", "Dua Lipa"),
        ("Shape of You", "Ed Sheeran")
    ]

    data = fetch_spotify_data(test_songs)
    for song in data:
        print("🎶", song)

