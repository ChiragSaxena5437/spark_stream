from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf, to_timestamp, window, date_format
from pyspark.sql.types import StructType, StringType
from textblob import TextBlob

# Sentiment function
def get_sentiment(text):
    try:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0:
            return (polarity, "positive")
        elif polarity < 0:
            return (polarity, "negative")
        else:
            return (polarity, "neutral")
    except:
        return (0.0, "neutral")

spark = SparkSession.builder \
    .appName("TwitterSentimentStreaming") \
    .getOrCreate()

schema = StructType() \
    .add("username", StringType()) \
    .add("content", StringType()) \
    .add("timestamp", StringType())

sentiment_udf = udf(get_sentiment, "struct<sentiment:double,sentiment_label:string>")

df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "tweets")
    .load()
)

json_df = df.select(from_json(col("value").cast("string"), schema).alias("data"))
flat_df = json_df.select(
    col("data.username"),
    col("data.content"),
    to_timestamp("data.timestamp").alias("timestamp")
)

with_sentiment = flat_df.withColumn("sentiment_struct", sentiment_udf(col("content")))
final_df = with_sentiment.select(
    "timestamp",
    "username",
    "content",
    col("sentiment_struct.sentiment").alias("sentiment"),
    col("sentiment_struct.sentiment_label").alias("sentiment_label"),
    date_format("timestamp", "yyyy-MM-dd HH:mm").alias("minute")
)

query = (
    final_df.writeStream
    .format("parquet")
    .option("path", "./stream_output/parquet")
    .option("checkpointLocation", "./stream_output/checkpoint")
    .outputMode("append")
    .start()
)

query.awaitTermination()
