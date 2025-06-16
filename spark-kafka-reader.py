from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, lit, struct
from pyspark.sql.types import StringType, StructType, StructField, LongType, DecimalType, TimestampType
import logging
import threading


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_customers_job(spark):
    try:
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

        # Parse JSON and extract customer_id
        json_schema = StructType([
            StructField("payload", StructType([
                StructField("after", StructType([
                    StructField("customer_id", LongType())
                ]))
            ]))
        ])

        # Convert the value column from binary to string and parse JSON
        parsed_df = df.select(
            from_json(col("value").cast(StringType()), json_schema).alias("data")
        ).select(
            col("data.payload.after.customer_id").alias("customer_id")
        ).withColumn(
            "record_source", lit("bank_oltp2 cdc")
        )

        # Function to write to PostgreSQL
        def write_to_postgres(batch_df, batch_id):
            if batch_df.count() > 0:
                batch_df.write \
                    .format("jdbc") \
                    .option("url", "jdbc:postgresql://db-dwh:5432/bank_dwh") \
                    .option("driver", "org.postgresql.Driver") \
                    .option("dbtable", "hub_customer") \
                    .option("user", "postgres") \
                    .option("password", "postgres") \
                    .mode("append") \
                    .save()

        # Write to PostgreSQL
        logger.info("Starting to write to PostgreSQL...")
        query = (
            parsed_df.writeStream  
            .foreachBatch(write_to_postgres) 
            .outputMode("append")    
            .option("checkpointLocation", "file:///opt/spark/checkpoints/kafka")
            .start()
        )

        logger.info("Stream started successfully")
        
        # Wait for the streaming query to terminate
        query.awaitTermination()

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise 

def run_transactions_job(spark):
    try:
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

if __name__ == "__main__":
    # Create Spark session
    logger.info("Creating Spark session...")
    spark = SparkSession.builder \
        .appName("KafkaReader") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.7.2") \
        .getOrCreate()

    logger.info("Spark session created successfully")

    # Запуск в отдельных потоках
    t1 = threading.Thread(target=run_customers_job, args=(spark,))
    t1.start()
    t1.join()

    t2 = threading.Thread(target=run_transactions_job, args=(spark,))
    t2.start()
    t2.join()