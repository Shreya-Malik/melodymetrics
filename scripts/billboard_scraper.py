import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from .env
N_WEEKS = int(os.getenv("BILLBOARD_WEEKS", 15))
SAVE_PATH = os.getenv("BILLBOARD_RAW_PATH", "./data/billboard_raw_500.csv")

def get_recent_sundays(n_weeks):
    """Get list of past N Sundays starting from the most recent."""
    today = datetime.today()
    last_sunday = today - timedelta(days=(today.weekday() + 1) % 7)
    sundays = [(last_sunday - timedelta(weeks=i)).strftime('%Y-%m-%d') for i in range(n_weeks)]
    return sundays

def scrape_billboard_chart(date):
    """Scrape Billboard Hot 100 chart for a given Sunday date."""
    url = f"https://www.billboard.com/charts/hot-100/{date}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data for {date} (Status {response.status_code})")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    entries = soup.find_all('li', class_='o-chart-results-list__item')

    songs = []
    for entry in entries:
        title_tag = entry.find("h3", id="title-of-a-story")
        artist_tag = entry.find("span", class_="c-label")

        if title_tag and artist_tag:
            title = title_tag.text.strip()
            artist = artist_tag.text.strip()
            if title and artist and artist.lower() != "new":
                songs.append((title, artist))

    return songs

if __name__ == "__main__":
    all_songs = []
    sundays = get_recent_sundays(N_WEEKS)

    print(f"Starting Billboard Hot 100 scraping for {N_WEEKS} weeks...\n")

    for date in sundays:
        print(f"Scraping Billboard Hot 100 for week: {date}")
        songs = scrape_billboard_chart(date)
        all_songs.extend(songs)
        time.sleep(1)

    df = pd.DataFrame(all_songs, columns=["Song", "Artist"])
    df.index += 1

    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    df.to_csv(SAVE_PATH, index_label="Rank")

    print(f"\nScraping complete. {len(df)} total records saved to '{SAVE_PATH}'")
