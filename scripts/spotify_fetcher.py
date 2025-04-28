import requests
import base64

# 🔑 Set your Spotify credentials here
CLIENT_ID = 'bb50ce3a40264186b606249c4caac421'
CLIENT_SECRET = '3f342271aca34ebf94b39a59856362b9'

# Encode credentials
credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# Step 1: Get access token using Client Credentials flow
auth_url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "client_credentials"
}
response = requests.post(auth_url, headers=headers, data=data)
token_info = response.json()

access_token = token_info.get("access_token")

if not access_token:
    print("❌ Failed to get access token:", token_info)
    exit()

print("✅ Access token acquired.")

# Step 2: Search for a track
search_url = "https://api.spotify.com/v1/search"
query = "Midnight Sun"
params = {
    "q": query,
    "type": "track",
    "limit": 1
}
search_headers = {
    "Authorization": f"Bearer {access_token}"
}
search_response = requests.get(search_url, headers=search_headers, params=params)
track_data = search_response.json()

if not track_data['tracks']['items']:
    print("❌ No track found.")
    exit()

track = track_data['tracks']['items'][0]
track_id = track['id']
print(f"🎵 Found track: {track['name']} by {track['artists'][0]['name']}")

# Step 3: Get audio features
features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
features_response = requests.get(features_url, headers=search_headers)
features = features_response.json()
print("🔍 Raw Audio Features Response:")
print(features)