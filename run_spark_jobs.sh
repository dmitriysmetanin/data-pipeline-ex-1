#!/bin/bash
# run_spark_jobs.sh

# Запуск первого задания
spark-submit \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
    --conf spark.driver.extraClassPath=/opt/bitnami/spark/jars/* \
    --conf spark.executor.extraClassPath=/opt/bitnami/spark/jars/* \
    --conf spark.python.use.daemon=false \
    --conf spark.python.worker.reuse=false \
    spark-kafka-reader.py &

# Запуск второго задания
spark-submit \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
    --conf spark.driver.extraClassPath=/opt/bitnami/spark/jars/* \
    --conf spark.executor.extraClassPath=/opt/bitnami/spark/jars/* \
    --conf spark.python.use.daemon=false \
    --conf spark.python.worker.reuse=false \
    spark-kafka-transactions.py &

# Ожидание завершения всех фоновых процессов
wait