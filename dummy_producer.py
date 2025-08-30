import time
import json
import random
from kafka import KafkaProducer

# Some dummy tweets (positive & negative)
TWEETS = [
    {"username": "alice", "content": "I am so happy today!"},
    {"username": "bob", "content": "Spark streaming is really tricky..."},
    {"username": "charlie", "content": "Feeling great after my workout!"},
    {"username": "dave", "content": "This is so frustrating, nothing works!"},
    {"username": "eve", "content": "Excited about learning Kafka and Spark!"},
    {"username": "frank", "content": "I am very sad today..."},
]

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

if __name__ == "__main__":
    print("🚀 Dummy tweet producer started. Sending data to Kafka...")
    while True:
        tweet = random.choice(TWEETS)
        producer.send("twitter-topic", value=tweet)
        print(f"Sent: {tweet}")
        time.sleep(2)  # send every 2 seconds
