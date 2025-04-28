import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database credentials from .env
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Final dataset path from .env
FINAL_DATASET_PATH = os.getenv('FINAL_DATASET_PATH', './data/final_music_dataset.csv')

# Create the database engine
engine = create_engine(f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')

try:
    # Load the final dataset
    df = pd.read_csv(FINAL_DATASET_PATH)

    # Upload to PostgreSQL
    df.to_sql('final_music_data', engine, if_exists='replace', index=False)

    print("Final enriched dataset uploaded successfully to PostgreSQL.")
except Exception as e:
    print(f"Error uploading dataset to PostgreSQL: {e}")
