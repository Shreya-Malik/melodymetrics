import pandas as pd

DATA_PATH = "./data/final_music_dataset.csv"

try:
    df = pd.read_csv(DATA_PATH)
    print(f"\nLoaded final dataset with {len(df)} records.")

    print("\n--- Missing Values Per Column ---")
    print(df.isnull().sum())

    print("\n--- Summary Statistics ---")
    print(df.describe(include='all'))

    enriched_percent = round((len(df) / 293) * 100, 2)  # 293 = initial cleaned Billboard count
    print(f"\nPercentage of Billboard songs enriched with Spotify data: {enriched_percent}%")

except Exception as e:
    print(f"\nError loading or profiling data: {e}")
