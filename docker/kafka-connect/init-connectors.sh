#!/bin/bash

# Wait for Kafka Connect to be ready
echo "Waiting for Kafka Connect to be ready..."
while [ "$(curl -s -o /dev/null -w ''%{http_code}'' localhost:8083/connectors)" != "200" ]; do
    echo "Kafka Connect is not ready yet..."
    sleep 5
done

# Wait for plugins to be loaded
echo "Waiting for plugins to be loaded..."
while ! curl -s localhost:8083/connector-plugins | grep -q "io.debezium.connector.postgresql.PostgresConnector"; do
    echo "Plugins are not loaded yet..."
    sleep 5
done

# Create connectors
echo "Creating connectors..."
for connector in /kafka/connect/connectors/*.json; do
    if [ -f "$connector" ]; then
        echo "Creating connector from $connector"
        curl -X POST -H "Content-Type: application/json" --data @"$connector" http://localhost:8083/connectors
        echo ""
    fi
done

echo "Connector initialization completed!" 