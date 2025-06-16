from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StringType, StructType, StructField, LongType, DecimalType, TimestampType
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Create Spark session
    logger.info("Creating Spark session...")
    spark = SparkSession.builder \
        .appName("KafkaTransactionReader") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()

    logger.info("Spark session created successfully")

    # Define schema for transaction data
    transaction_schema = StructType([
        StructField("payload", StructType([
            StructField("after", StructType([
                StructField("id", LongType()),
                StructField("account_id", LongType()),
                StructField("amount", DecimalType(20, 2)),
                StructField("transaction_type", StringType()),
                StructField("transaction_date", TimestampType()),
                StructField("description", StringType()),
                StructField("another_account", LongType())
            ]))
        ]))
    ])

    # Read from Kafka
    logger.info("Attempting to read from Kafka transactions topic...")
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "dbserver1.public.transactions") \
        .option("startingOffsets", "earliest") \
        .option("failOnDataLoss", "false") \
        .load()

    logger.info("Successfully created Kafka stream for transactions")

    # Parse JSON and extract transaction data
    parsed_df = df.select(
        from_json(col("value").cast(StringType()), transaction_schema).alias("data")
    ).select(
        col("data.payload.after.*")
    )

    # Write to console
    logger.info("Starting console output...")
    query = (
        parsed_df.writeStream
        .format("console")
        .outputMode("append")
        .option("truncate", "false")
        .start()
    )

    logger.info("Stream started successfully")
    
    # Wait for the streaming query to terminate
    query.awaitTermination()

except Exception as e:
    logger.error(f"An error occurred: {str(e)}", exc_info=True)
    raise