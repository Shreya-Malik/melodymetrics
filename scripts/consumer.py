from kafka import KafkaConsumer
import json
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="melodymetrics_db",
    user="melody_user",
    password="melody_pass"
)
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS song_data (
        song_id INTEGER PRIMARY KEY,
        title TEXT,
        artist TEXT,
        streams INTEGER
    );
""")
conn.commit()

# Set up Kafka Consumer
consumer = KafkaConsumer(
    'melody_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Listening for Kafka messages...")

# Listen and insert data into PostgreSQL
for message in consumer:
    data = message.value
    print(f"🎧 Received from Kafka: {data}")
    try:
        cursor.execute("""
            INSERT INTO song_data (song_id, title, artist, streams)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (song_id) DO NOTHING;
        """, (data["song_id"], data["title"], data["artist"], data["streams"]))
        conn.commit()
        print("✅ Inserted into PostgreSQL")
    except Exception as e:
        print("❌ Error inserting into DB:", e)
        conn.rollback()