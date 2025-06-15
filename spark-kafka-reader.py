from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StringType
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Create Spark session
    logger.info("Creating Spark session...")
    spark = SparkSession.builder \
        .appName("KafkaReader") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()

    logger.info("Spark session created successfully")

    # Read from Kafka
    logger.info("Attempting to read from Kafka...")
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "dbserver1.public.customers") \
        .option("startingOffsets", "earliest") \
        .option("failOnDataLoss", "false") \
        .load()

    logger.info("Successfully created Kafka stream")

    # Convert the value column from binary to string
    df = df.select(col("value").cast(StringType()))

    # Write to console
    logger.info("Starting to write to console...")
    query = df.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .start()

    logger.info("Stream started successfully")
    
    # Wait for the streaming query to terminate
    query.awaitTermination()

except Exception as e:
    print(e)
    logger.error(f"An error occurred: {str(e)}", exc_info=True)
    raise 