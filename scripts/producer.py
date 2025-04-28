from kafka import KafkaProducer
import json
import time

# Connect to Kafka broker running in Docker
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sample streaming data (Spotify-style mock)
sample_data = [
    {"song_id": 1, "title": "Eclipse", "artist": "Nova", "streams": 12000},
    {"song_id": 2, "title": "Aurora", "artist": "Skye", "streams": 8500},
    {"song_id": 3, "title": "Midnight Sun", "artist": "Lumen", "streams": 14300}
]

# Send messages every 2 seconds
for song in sample_data:
    producer.send('melody_topic', value=song)
    print(f"Sent to Kafka: {song}")
    time.sleep(2)

producer.flush()
producer.close()