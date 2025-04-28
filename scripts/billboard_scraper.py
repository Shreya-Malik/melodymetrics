import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_billboard_hot_100():
    url = "https://www.billboard.com/charts/hot-100/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Failed to fetch Billboard data")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    songs = []
    
    entries = soup.find_all('li', class_='o-chart-results-list__item')

    for entry in entries:
        title_tag = entry.find("h3", id="title-of-a-story")
        artist_tag = entry.find("span", class_="c-label")

        if title_tag and artist_tag:
            title = title_tag.text.strip()
            artist = artist_tag.text.strip()

            if title and artist and artist.lower() != 'new':
                songs.append((title, artist))

    return songs

if __name__ == "__main__":
    hot_100 = scrape_billboard_hot_100()

    print("\n🔥 Top 10 Billboard Hot 100 Songs:")
    for i, (title, artist) in enumerate(hot_100[:10], start=1):
        print(f"{i}. {title} — {artist}")

    # Save to CSV
    df = pd.DataFrame(hot_100, columns=["Song", "Artist"])
    df.index += 1
    df.to_csv("../data/billboard_hot_100.csv", index_label="Rank")

    print(f"\n✅ Saved {len(hot_100)} songs to 'data/billboard_hot_100.csv'")
