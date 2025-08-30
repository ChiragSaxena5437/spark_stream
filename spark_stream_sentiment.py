from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StringType
from textblob import TextBlob
import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

spark = SparkSession.builder \
    .appName("SentimentStream") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

schema = StructType() \
    .add("username", StringType()) \
    .add("content", StringType())

raw_stream = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

raw_data = raw_stream.select(from_json(col("value"), schema).alias("data")).select("data.*")

def get_sentiment(text):
    if text is None or text.strip() == "":
        return "Neutral"
    analysis = TextBlob(text).sentiment.polarity
    if analysis > 0:
        return "Positive"
    elif analysis < 0:
        return "Negative"
    else:
        return "Neutral"

sentiment_udf = udf(get_sentiment, StringType())
with_sentiment = raw_data.withColumn("sentiment", sentiment_udf(col("content")))

query_console = with_sentiment.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

query_parquet = with_sentiment.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "./stream_output/parquet") \
    .option("checkpointLocation", "./stream_output/checkpoint") \
    .start()

spark.streams.awaitAnyTermination()
