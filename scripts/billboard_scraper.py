import requests
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Billboard URLs
BILLBOARD_URLS = {
    "Hot 100": "https://www.billboard.com/charts/hot-100/",
    "Global 200": "https://www.billboard.com/charts/billboard-global-200/",
    "Artist 100": "https://www.billboard.com/charts/artist-100/"
}

# Output path
BILLBOARD_CSV_PATH = os.getenv('BILLBOARD_CSV_PATH', './data/billboard_hot_100.csv')

def scrape_billboard_chart(chart_name, url):
    """Fetch song or artist data from a specific Billboard chart."""
    print(f"Scraping {chart_name}...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch {chart_name} ({response.status_code})")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    entries = soup.find_all('li', class_='o-chart-results-list__item')

    songs = []

    for entry in entries:
        title_tag = entry.find("h3", id="title-of-a-story")
        artist_tag = entry.find("span", class_="c-label")

        if title_tag and artist_tag:
            title = title_tag.text.strip()
            artist = artist_tag.text.strip()

            # Skip blank entries or labels like "NEW"
            if title and artist and artist.lower() != 'new':
                songs.append((title, artist))

    print(f"Found {len(songs)} records from {chart_name}.")
    return songs

if __name__ == "__main__":
    all_songs = []

    for chart_name, url in BILLBOARD_URLS.items():
        songs = scrape_billboard_chart(chart_name, url)
        all_songs.extend(songs)

    if all_songs:
        df = pd.DataFrame(all_songs, columns=["Song", "Artist"])
        df.index += 1

        # Ensure output directory exists
        os.makedirs("./data", exist_ok=True)

        df.to_csv(BILLBOARD_CSV_PATH, index_label="Rank")
        print(f"\nSaved {len(df)} total songs to '{BILLBOARD_CSV_PATH}'.")
    else:
        print("No songs found across Billboard charts.")
