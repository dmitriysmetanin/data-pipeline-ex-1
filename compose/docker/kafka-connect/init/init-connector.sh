#!/bin/bash

echo "Waiting for Kafka Connect to start..."

# Функция для проверки доступности Kafka Connect
wait_for_connect() {
    echo "Waiting for Kafka Connect REST API (HTTP 200)..."
    while true; do
        code=$(curl -s -o /dev/null -w "%{http_code}" http://kafka-connect:8083/connectors)
        if [ "$code" = "200" ]; then
            echo "Kafka Connect REST API is ready!"
            break
        fi
        echo "Kafka Connect is not ready yet (code: $code). Waiting..."
        sleep 5
    done
}

# Ждем пока Kafka Connect станет доступен
wait_for_connect

echo "Creating PostgreSQL connector..."
response=$(curl -s -X POST -H "Content-Type: application/json" --data '{
  "name": "postgres-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "app-db",
    "database.port": "5432",
    "database.user": "postgres",
    "database.password": "postgres",
    "database.dbname": "bank_oltp2",
    "database.server.name": "bank",
    "topic.prefix": "bank",
    "table.include.list": "public.*",
    "plugin.name": "pgoutput",
    "database.history.kafka.bootstrap.servers": "kafka:9092",
    "database.history.kafka.topic": "schema-changes.bank"
  }
}' http://kafka-connect:8083/connectors)

# Проверяем результат создания коннектора
if echo "$response" | grep -q "error_code"; then
    echo "Error creating connector:"
    echo "$response"
    exit 1
else
    echo "Connector created successfully!"
    echo "Response: $response"
fi

# Проверяем статус коннектора
echo "Checking connector status..."
sleep 5
curl -s http://kafka-connect:8083/connectors/postgres-connector/status | jq '.'

echo "Connector initialization completed" 