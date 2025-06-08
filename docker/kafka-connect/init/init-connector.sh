#!/bin/bash

# Ждем, пока Kafka Connect станет доступен
echo "Waiting for Kafka Connect to start..."
while true; do
    # Проверяем доступность Kafka Connect
    if curl -s http://localhost:8083/connectors > /dev/null; then
        echo "Kafka Connect is ready!"
        break
    fi
    echo "Kafka Connect is not ready yet..."
    sleep 5
done

# Даем Kafka Connect время на полную инициализацию
sleep 10

# Проверяем, существует ли коннектор
if ! curl -s http://localhost:8083/connectors/bank-connector > /dev/null; then
    echo "Creating bank-connector..."
    curl -X POST -H "Content-Type: application/json" --data '{
      "name": "bank-connector",
      "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "database.hostname": "app-db",
        "database.port": "5432",
        "database.user": "debezium",
        "database.password": "dbz",
        "database.dbname": "bank_oltp2",
        "database.server.name": "bank",
        "table.include.list": "public.*",
        "database.history.kafka.bootstrap.servers": "kafka:9092",
        "database.history.kafka.topic": "schema-changes.bank",
        "topic.prefix": "bank-oltp-cdc",
        "plugin.name": "pgoutput"
      }
    }' http://localhost:8083/connectors
    echo "bank-connector created!"
else
    echo "bank-connector already exists"
fi 