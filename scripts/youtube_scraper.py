import requests
import json
import pandas as pd

API_KEY = 'AIzaSyCy2jNp-Jyk9SMsFGEQHEBvbZ-kKTCgi0k'

def search_youtube_video(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()
        if results["items"]:
            video_id = results["items"][0]["id"]["videoId"]
            return video_id
    return None

def fetch_comments(video_id, max_comments=20):
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": max_comments,
        "textFormat": "plainText",
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    comments = []
    if response.status_code == 200:
        data = response.json()
        for item in data['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
    return comments

if __name__ == "__main__":
    song_title = "Shape of You Ed Sheeran"

    print(f"🔎 Searching YouTube for: {song_title}")
    video_id = search_youtube_video(song_title)

    if video_id:
        print(f"✅ Found video ID: {video_id}")
        comments = fetch_comments(video_id)

        print(f"\n💬 Top Comments:")
        for comment in comments:
            print(f"- {comment}")

        # Save comments
        df = pd.DataFrame(comments, columns=["Comment"])
        df.to_csv("../data/youtube_comments_sample.csv", index=False)
        print("\n✅ Saved comments to 'data/youtube_comments_sample.csv'")
    else:
        print("❌ No video found.")
