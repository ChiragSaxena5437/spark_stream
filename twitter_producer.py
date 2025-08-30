import os
import json
import tweepy
from kafka import KafkaProducer

BEARER_TOKEN=""
producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

client = tweepy.StreamingClient(BEARER_TOKEN)

class TweetStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        data = {
            "username": "unknown",  # free tier doesn’t return username directly
            "content": tweet.text
        }
        producer.send("tweets", data)
        print(f"Sent: {data}")

stream = TweetStream(BEARER_TOKEN)
stream.add_rules(tweepy.StreamRule("happy OR sad OR spark"))
stream.filter(tweet_fields=["created_at", "lang"])
