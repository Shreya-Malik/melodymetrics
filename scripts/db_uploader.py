import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Paths and DB credentials from .env
CSV_PATH = os.getenv('FINAL_CLEANED_DATA_PATH', './data/final_music_dataset_cleaned.csv')

DB_USER = os.getenv('POSTGRES_USER', 'melody_user')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'melody_pass')
DB_NAME = os.getenv('POSTGRES_DB', 'melodymetrics_db')
DB_HOST = os.getenv('POSTGRES_HOST', 'melody_postgres')  # docker service name
DB_PORT = os.getenv('POSTGRES_PORT', '5432')

# Read the dataset
df = pd.read_csv(CSV_PATH)
print(f"Loaded dataset with {len(df)} records.")

# Upload to PostgreSQL
try:
    engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    df.to_sql('music_data', engine, if_exists='replace', index=False)
    print("Dataset uploaded successfully to table 'music_data'.")
except Exception as e:
    print("Error uploading to database:", e)
