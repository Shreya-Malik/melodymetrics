import requests
import json
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read configs from .env
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
BILLBOARD_CSV_PATH = os.getenv('BILLBOARD_CSV_PATH', './data/billboard_hot_100.csv')

def search_youtube_video(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1,
        "key": YOUTUBE_API_KEY
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
        "key": YOUTUBE_API_KEY
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
    # Example song title to search
    song_title = "Shape of You Ed Sheeran"

    print(f"Searching YouTube for: {song_title}")
    video_id = search_youtube_video(song_title)

    if video_id:
        print(f"Found video ID: {video_id}")
        comments = fetch_comments(video_id)

        if comments:
            # Make sure data folder exists
            os.makedirs(os.path.dirname(BILLBOARD_CSV_PATH), exist_ok=True)

            # Save comments to CSV
            df = pd.DataFrame(comments, columns=["Comment"])
            df.to_csv("./data/youtube_comments_sample.csv", index=False)
            print("Saved comments to './data/youtube_comments_sample.csv'")
        else:
            print("No comments found.")
    else:
        print("No video found.")
